"""
Tests for bin/microbes.py

# ---------------------------------------------------------------------------
# How to run
# ---------------------------------------------------------------------------

Run all tests (basic output):
conda run -n rdkit_env pytest tests/test_microbes.py -v

See the actual error message values when a test fails:
conda run -n rdkit_env pytest tests/test_microbes.py -v --tb=short

Run only the validate tests to focus on error messages:
conda run -n rdkit_env pytest tests/test_microbes.py::TestValidate -v

Run a single specific test:
conda run -n rdkit_env pytest tests/test_microbes.py::TestBuildDescription::test_single_bacteria_with_strain -v

Run live API integration tests (requires internet):
conda run -n rdkit_env pytest tests/test_microbes.py -m integration -v

Skip integration tests (default for CI / offline):
conda run -n rdkit_env pytest tests/test_microbes.py -m "not integration" -v

See what error messages validate() actually produces right now (useful for debugging):

conda run -n rdkit_env python -c "
import sys; sys.path.insert(0, 'bin')
from microbes import build_assay_tsv, validate
import pandas as pd

df = pd.DataFrame([{
    'assay_identifier': 'assay1',
    'ASSAY_ORGANISM': 'Escherichia coli',
    'ASSAY_STRAIN': 'K12',
    'ASSAY_TAX_ID': '',
    'ASSAY_TYPE': 'B',
    'ASSAY_SOURCE': '',
    'ASSAY_TISSUE': '',
    'ASSAY_CELL_TYPE': '',
    'ASSAY_SUBCELLULAR_FRACTION': '',
    'ASSAY_GROUP': '',
    'TARGET_TYPE': '',
    'TARGET_NAME': '',
    'TARGET_ACCESSION': 'P',
    'TARGET_ORGANISM': '',
    'TARGET_TAX_ID': '',
    'ENAorSRA_project_Accession_number': '',
    'ENAorSRA_sample_Accession_number': '',
}])
exp_df = pd.DataFrame()
assay_df, _ = build_assay_tsv(df, ridx='TestRef', exp_df=exp_df,
                               xenobiotic_class='drug', taxid_lookup=False)
for e in validate(assay_df):
    print(e)
"
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))
from microbes import (
    CHEMBL_COLS,
    MANDATORY_FIELDS,
    VALID_ASSAY_TYPES,
    VALID_TARGET_TYPES,
    _UNIPROT_ACCESSION_RE,
    _build_description,
    _clean,
    _get_experiment_for_assay,
    _looks_like_accession,
    _make_aidx,
    _ncbi_taxid,
    _parse_timecourse,
    _slugify,
    _straininfo_by_accession,
    _uniprot_lookup,
    build_assay_tsv,
    lookup_taxid,
    validate,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_microbe_row(**kwargs) -> dict:
    """Minimal valid Microbes sheet row; override fields via kwargs."""
    base = {
        "assay_identifier":                   "assay1",
        "ASSAY_ORGANISM":                     "Escherichia coli",
        "ASSAY_STRAIN":                       "K12",
        "ASSAY_TAX_ID":                       "83333",
        "ASSAY_TYPE":                         "B",
        "ASSAY_SOURCE":                       "Zimmermann",
        "ASSAY_TISSUE":                       "",
        "ASSAY_CELL_TYPE":                    "",
        "ASSAY_SUBCELLULAR_FRACTION":         "",
        "ASSAY_GROUP":                        "",
        "TARGET_TYPE":                        "",
        "TARGET_NAME":                        "",
        "TARGET_ACCESSION":                   "",
        "TARGET_ORGANISM":                    "",
        "TARGET_TAX_ID":                      "",
        "ENAorSRA_project_Accession_number":  "",
        "ENAorSRA_sample_Accession_number":   "",
        "Gene_name":                          "",
    }
    base.update(kwargs)
    return base


def _make_exp_row(**kwargs) -> dict:
    base = {
        "identifier":                                       "all",
        "Instrument_4_measurement":                         "LC-MS",
        "Time-course information (i.e., number of timepoints)": "0,6,24",
        "Time_unit":                                        "h",
        "Oxygen conditions":                                "anaerobic",
    }
    base.update(kwargs)
    return base


def _df(*rows) -> pd.DataFrame:
    return pd.DataFrame(list(rows))


def _build(microbe_kwargs=None, exp_kwargs=None, ridx="TestRef",
           xenobiotic_class="drug") -> tuple:
    """Build assay_df + aidx_map with taxid_lookup disabled."""
    mrow = _make_microbe_row(**(microbe_kwargs or {}))
    erow = _make_exp_row(**(exp_kwargs or {}))
    microbes_df = _df(mrow)
    exp_df = _df(erow)
    return build_assay_tsv(
        microbes_df, ridx=ridx, exp_df=exp_df,
        xenobiotic_class=xenobiotic_class, taxid_lookup=False,
    )


# ---------------------------------------------------------------------------
# _clean()
# ---------------------------------------------------------------------------

class TestClean:

    def test_nan_float_becomes_empty(self):
        import numpy as np
        assert _clean(float("nan")) == ""

    def test_nan_string_becomes_empty(self):
        assert _clean("nan") == ""

    def test_none_string_becomes_empty(self):
        assert _clean("None") == ""

    def test_nan_uppercase_string_becomes_empty(self):
        assert _clean("NaN") == ""

    def test_normal_string_stripped(self):
        assert _clean("  Escherichia coli  ") == "Escherichia coli"

    def test_non_nan_number_returned_as_is(self):
        assert _clean(42) == 42

    def test_empty_string_stays_empty(self):
        assert _clean("") == ""


# ---------------------------------------------------------------------------
# _looks_like_accession()
# ---------------------------------------------------------------------------

class TestLooksLikeAccession:

    @pytest.mark.parametrize("accession", [
        "DSM 2840", "ATCC 11775", "NCTC 10537", "LMG 2093", "DSMZ1234",
    ])
    def test_culture_collection_numbers_recognised(self, accession):
        assert _looks_like_accession(accession) is True

    @pytest.mark.parametrize("text", [
        "Escherichia coli", "gut metagenome", "", "K12", "DSM",
    ])
    def test_organism_names_not_recognised(self, text):
        assert _looks_like_accession(text) is False


# ---------------------------------------------------------------------------
# _parse_timecourse()
# ---------------------------------------------------------------------------

class TestParseTimecourse:

    def test_empty_string_returns_empty_triple(self):
        assert _parse_timecourse("") == ("", "", "")

    def test_single_value(self):
        assert _parse_timecourse("24") == ("1", "24", "24")

    def test_multiple_values_count_min_max(self):
        n, lo, hi = _parse_timecourse("0,6,12,24")
        assert n == "4"
        assert lo == "0"
        assert hi == "24"

    def test_float_values_with_integer_representation(self):
        n, lo, hi = _parse_timecourse("0.0,6.0,24.0")
        assert lo == "0"
        assert hi == "24"

    def test_whitespace_around_values_ignored(self):
        n, lo, hi = _parse_timecourse(" 0 , 3 , 6 ")
        assert n == "3"

    def test_non_numeric_tokens_returns_count_and_endpoints(self):
        n, lo, hi = _parse_timecourse("early,mid,late")
        assert n == "3"
        assert lo == "early"
        assert hi == "late"

    def test_timecourse_from_docstring_example(self):
        n, lo, hi = _parse_timecourse("0,3,6,9,12,24")
        assert n == "6"
        assert lo == "0"
        assert hi == "24"


# ---------------------------------------------------------------------------
# _slugify()
# ---------------------------------------------------------------------------

class TestSlugify:

    def test_spaces_become_underscores(self):
        assert _slugify("gut metagenome") == "gut_metagenome"

    def test_hyphens_become_underscores(self):
        assert _slugify("E-coli") == "E_coli"

    def test_special_chars_removed(self):
        assert _slugify("E.coli (K12)") == "Ecoli_K12"

    def test_leading_trailing_whitespace_stripped(self):
        assert _slugify("  Salmonella  ") == "Salmonella"

    def test_multiple_spaces_become_single_underscore(self):
        assert _slugify("gut  metagenome") == "gut_metagenome"

    def test_empty_string(self):
        assert _slugify("") == ""


# ---------------------------------------------------------------------------
# _make_aidx()
# ---------------------------------------------------------------------------

class TestMakeAidx:

    def test_no_source_no_strain(self):
        assert _make_aidx("Escherichia_coli", "", "", "", "") == \
               "Escherichia_coli_Biotransformation"

    def test_with_source_prepended(self):
        result = _make_aidx("Escherichia_coli", "", "Zimmermann", "", "")
        assert result.startswith("Zimmermann_")
        assert "Biotransformation" in result

    def test_with_strain_appended(self):
        result = _make_aidx("Salmonella_typhimurium", "LT2", "", "", "")
        assert "LT2" in result
        assert result.endswith("Biotransformation")

    def test_community_organism_appends_community_not_strain(self):
        result = _make_aidx("gut metagenome", "DSM 1234", "Zimmermann", "", "")
        assert "community" in result
        assert "DSM" not in result

    def test_target_name_appended_without_accession(self):
        result = _make_aidx("E_coli", "", "", "DNAK", "")
        assert result.endswith("DNAK")

    def test_target_accession_preferred_over_name(self):
        result = _make_aidx("E_coli", "", "", "DNAK", "P0A6Y8")
        assert result.endswith("P0A6Y8")
        assert "DNAK" not in result

    def test_full_example_from_docstring(self):
        result = _make_aidx(
            "Salmonella typhimurium", "LT2", "Zimmermann", "", ""
        )
        assert "Zimmermann" in result
        assert "Salmonella_typhimurium" in result
        assert "LT2" in result
        assert "Biotransformation" in result

    def test_duplicate_base_not_generated_here(self):
        # _make_aidx itself always returns the base — deduplication is in build_assay_tsv
        r1 = _make_aidx("E_coli", "", "", "", "")
        r2 = _make_aidx("E_coli", "", "", "", "")
        assert r1 == r2


# ---------------------------------------------------------------------------
# _get_experiment_for_assay()
# ---------------------------------------------------------------------------

class TestGetExperimentForAssay:

    def test_identifier_all_matches_any_aidx(self):
        exp_df = _df(_make_exp_row(identifier="all"))
        result = _get_experiment_for_assay(exp_df, "any_aidx")
        assert result is not None

    def test_identifier_all_case_insensitive(self):
        exp_df = _df(_make_exp_row(identifier="ALL"))
        assert _get_experiment_for_assay(exp_df, "x") is not None

    def test_specific_aidx_matches(self):
        exp_df = _df(_make_exp_row(identifier="assay1"))
        assert _get_experiment_for_assay(exp_df, "assay1") is not None

    def test_comma_separated_list_matches_member(self):
        exp_df = _df(_make_exp_row(identifier="assay1, assay2, assay3"))
        assert _get_experiment_for_assay(exp_df, "assay2") is not None

    def test_aidx_not_in_list_returns_none(self):
        exp_df = _df(_make_exp_row(identifier="assay1,assay2"))
        assert _get_experiment_for_assay(exp_df, "assay3") is None

    def test_empty_identifier_skipped(self):
        exp_df = _df(_make_exp_row(identifier=""))
        assert _get_experiment_for_assay(exp_df, "assay1") is None

    def test_empty_dataframe_returns_none(self):
        exp_df = pd.DataFrame(columns=list(_make_exp_row().keys()))
        assert _get_experiment_for_assay(exp_df, "assay1") is None


# ---------------------------------------------------------------------------
# _build_description()
# ---------------------------------------------------------------------------

class TestBuildDescription:

    def _series(self, **kwargs) -> pd.Series:
        return pd.Series(_make_microbe_row(**kwargs))

    def _exp(self, **kwargs) -> pd.Series:
        return pd.Series(_make_exp_row(**kwargs))

    def test_single_bacteria_no_experiment(self):
        desc = _build_description(self._series(), None, "drug")
        assert "Escherichia coli" in desc
        assert "biotransformation" in desc
        # No measurement sentence when exp_row is None
        assert "measured" not in desc

    def test_single_bacteria_with_strain(self):
        desc = _build_description(self._series(ASSAY_STRAIN="K12"), None, "drug")
        assert "strain K12" in desc

    def test_single_bacteria_no_strain(self):
        desc = _build_description(self._series(ASSAY_STRAIN=""), None, "drug")
        assert "strain" not in desc

    def test_community_template_used_for_metagenome(self):
        desc = _build_description(
            self._series(ASSAY_ORGANISM="gut metagenome", ASSAY_STRAIN="DSM 1"),
            None, "drug",
        )
        assert "community" in desc
        assert "strain" not in desc

    def test_community_includes_ena_project_accession(self):
        desc = _build_description(
            self._series(
                ASSAY_ORGANISM="gut metagenome",
                ENAorSRA_project_Accession_number="PRJNA123",
            ),
            None, "drug",
        )
        assert "PRJNA123" in desc
        assert "study accession number" in desc

    def test_community_includes_ena_sample_accession(self):
        desc = _build_description(
            self._series(
                ASSAY_ORGANISM="gut metagenome",
                ENAorSRA_sample_Accession_number="SAMN001",
            ),
            None, "drug",
        )
        assert "SAMN001" in desc
        assert "sample accession number" in desc

    def test_measurement_sentence_with_full_experiment(self):
        desc = _build_description(self._series(), self._exp(), "drug")
        assert "LC-MS" in desc
        assert "3 time points" in desc
        assert "0 to 24" in desc
        assert "h" in desc
        assert "anaerobic" in desc

    def test_instrument_in_measurement_sentence(self):
        desc = _build_description(
            self._series(), self._exp(Instrument_4_measurement="HPLC"), "drug"
        )
        assert "HPLC" in desc

    def test_xenobiotic_class_used_in_description(self):
        desc = _build_description(self._series(), None, "pesticide")
        assert "pesticide" in desc

    def test_empty_xenobiotic_class_defaults_to_xenobiotic_compound(self):
        desc = _build_description(self._series(), None, "")
        assert "xenobiotic compound" in desc

    def test_no_measurement_sentence_when_exp_all_empty(self):
        exp = self._exp(
            **{
                "Instrument_4_measurement": "",
                "Time-course information (i.e., number of timepoints)": "",
                "Time_unit": "",
                "Oxygen conditions": "",
            }
        )
        desc = _build_description(self._series(), exp, "drug")
        assert "measured" not in desc


# ---------------------------------------------------------------------------
# build_assay_tsv()
# ---------------------------------------------------------------------------

class TestBuildAssayTsv:

    def test_returns_dataframe_and_aidx_map(self):
        assay_df, aidx_map = _build()
        assert isinstance(assay_df, pd.DataFrame)
        assert isinstance(aidx_map, dict)

    def test_output_has_all_chembl_cols(self):
        assay_df, _ = _build()
        assert list(assay_df.columns) == CHEMBL_COLS

    def test_ridx_set_on_all_rows(self):
        microbes_df = _df(_make_microbe_row(), _make_microbe_row(ASSAY_ORGANISM="Bacteroides"))
        assay_df, _ = build_assay_tsv(
            microbes_df, ridx="MyStudy", exp_df=pd.DataFrame(),
            xenobiotic_class="drug", taxid_lookup=False,
        )
        assert all(assay_df["RIDX"] == "MyStudy")

    def test_user_key_maps_to_generated_aidx(self):
        assay_df, aidx_map = _build(microbe_kwargs={"assay_identifier": "exp_a"})
        assert "exp_a" in aidx_map
        assert aidx_map["exp_a"] == assay_df["AIDX"].iloc[0]

    def test_blank_user_key_gets_fallback_key(self):
        assay_df, aidx_map = _build(microbe_kwargs={"assay_identifier": ""})
        assert "assay1" in aidx_map

    def test_duplicate_organism_strain_gets_suffix(self):
        row = _make_microbe_row(assay_identifier="a1")
        row2 = dict(row, assay_identifier="a2")
        microbes_df = _df(row, row2)
        assay_df, _ = build_assay_tsv(
            microbes_df, ridx="R", exp_df=pd.DataFrame(),
            xenobiotic_class="drug", taxid_lookup=False,
        )
        aidxs = list(assay_df["AIDX"])
        assert aidxs[0] != aidxs[1]
        assert aidxs[1].endswith("_2")

    def test_assay_type_normalised_to_first_char(self):
        assay_df, _ = _build(microbe_kwargs={"ASSAY_TYPE": "binding"})
        assert assay_df["ASSAY_TYPE"].iloc[0] == "B"

    def test_target_type_lowercase_stored_as_uppercase(self):
        assay_df, _ = _build(microbe_kwargs={"TARGET_TYPE": "protein"})
        assert assay_df["TARGET_TYPE"].iloc[0] == "PROTEIN"

    def test_target_type_mixed_case_stored_as_uppercase(self):
        assay_df, _ = _build(microbe_kwargs={"TARGET_TYPE": "Single Protein"})
        assert assay_df["TARGET_TYPE"].iloc[0] == "SINGLE PROTEIN"

    def test_assay_tax_id_integer_coercion(self):
        assay_df, _ = _build(microbe_kwargs={"ASSAY_TAX_ID": "83333.0"})
        assert assay_df["ASSAY_TAX_ID"].iloc[0] == "83333"

    def test_empty_exp_df_produces_description_without_measurement(self):
        microbes_df = _df(_make_microbe_row())
        assay_df, _ = build_assay_tsv(
            microbes_df, ridx="R", exp_df=pd.DataFrame(),
            xenobiotic_class="drug", taxid_lookup=False,
        )
        desc = assay_df["ASSAY_DESCRIPTION"].iloc[0]
        assert "biotransformation" in desc
        assert "measured" not in desc

    def test_taxid_lookup_false_makes_no_network_calls(self):
        with patch("microbes.lookup_taxid") as mock_lookup, \
             patch("microbes._uniprot_lookup") as mock_uniprot:
            _build(microbe_kwargs={"ASSAY_TAX_ID": ""})
            mock_lookup.assert_not_called()
            mock_uniprot.assert_not_called()

    def test_experiment_row_joined_by_user_key(self):
        microbes_df = _df(_make_microbe_row(assay_identifier="myassay"))
        exp_df = _df(_make_exp_row(
            identifier="myassay",
            Instrument_4_measurement="HPLC",
        ))
        assay_df, _ = build_assay_tsv(
            microbes_df, ridx="R", exp_df=exp_df,
            xenobiotic_class="drug", taxid_lookup=False,
        )
        assert "HPLC" in assay_df["ASSAY_DESCRIPTION"].iloc[0]


# ---------------------------------------------------------------------------
# _UNIPROT_ACCESSION_RE
# ---------------------------------------------------------------------------

class TestUniprotAccessionRegex:
    """Unit tests for the _UNIPROT_ACCESSION_RE pattern in isolation."""

    @pytest.mark.parametrize("acc", [
        # Old format (SwissProt): [OPQ][0-9][A-Z0-9]{3}[0-9]
        "P0A6Y8",   # canonical DnaK E. coli entry
        "Q9Y253",   # starts with Q
        "O15350",   # starts with O
        "P12345",   # all-digit suffix — still valid old format
        # New format 6-char (TrEMBL): [A-NR-Z][0-9][A-Z][A-Z0-9]{2}[0-9]
        "A2BC19",
        "B7ZW16",
        "C5IYJ3",
        # New format 10-char (TrEMBL): same prefix + repeat of [A-Z][A-Z0-9]{2}[0-9]
        "A0A023GPI8",
        "A0A009IHW8",
    ])
    def test_valid_accessions_match(self, acc):
        assert _UNIPROT_ACCESSION_RE.match(acc), (
            f"'{acc}' should match the UniProt accession regex but did not."
        )

    @pytest.mark.parametrize("acc", [
        "P",            # too short
        "P0A6Y",        # 5 chars — one short
        "P0A6Y88",      # 7 chars — one too long for old format
        "p0a6y8",       # lowercase
        "1P0A6Y",       # starts with digit
        "NOTANID",      # plain letters, wrong structure
        "P0A6Y-8",      # hyphen not in alphabet
        "",             # empty string
        "P0A6Y8 ",      # trailing space
        " P0A6Y8",      # leading space
    ])
    def test_invalid_accessions_do_not_match(self, acc):
        assert not _UNIPROT_ACCESSION_RE.match(acc), (
            f"'{acc}' should NOT match the UniProt accession regex but did."
        )


# ---------------------------------------------------------------------------
# validate()
# ---------------------------------------------------------------------------

class TestValidate:
    """
    validate() operates on the output of build_assay_tsv.
    Tests pin the exact error message text.
    """

    def _record_row(self, **kwargs) -> dict:
        base = {
            "AIDX":                       "Zimmermann_Escherichia_coli_K12_Biotransformation",
            "RIDX":                       "TestRef",
            "ASSAY_DESCRIPTION":          "The drug is tested on Escherichia coli strain K12 for biotransformation.",
            "ASSAY_TYPE":                 "B",
            "ASSAY_GROUP":                "",
            "ASSAY_ORGANISM":             "Escherichia coli",
            "ASSAY_STRAIN":               "K12",
            "ASSAY_TAX_ID":              "83333",
            "ASSAY_SOURCE":               "Zimmermann",
            "ASSAY_TISSUE":               "",
            "ASSAY_CELL_TYPE":            "",
            "ASSAY_SUBCELLULAR_FRACTION": "",
            "TARGET_TYPE":                "",
            "TARGET_NAME":                "",
            "TARGET_ACCESSION":           "",
            "TARGET_ORGANISM":            "",
            "TARGET_TAX_ID":              "",
        }
        base.update(kwargs)
        return base

    def test_valid_record_no_errors(self):
        df = _df(self._record_row())
        assert validate(df) == []

    @pytest.mark.parametrize("field", MANDATORY_FIELDS)
    def test_each_mandatory_field_exact_message(self, field):
        row = self._record_row(**{field: ""})
        df = _df(row)
        errors = validate(df)
        aidx = row["AIDX"] if field != "AIDX" else ""
        label = f"Row 1 (AIDX={aidx})"
        assert any(
            e.startswith(label) and f"mandatory field '{field}' is empty." in e
            for e in errors
        ), f"Expected mandatory-field error for '{field}' not found in: {errors}"

    def test_invalid_assay_type_exact_message(self):
        df = _df(self._record_row(ASSAY_TYPE="X"))
        errors = validate(df)
        aidx = self._record_row()["AIDX"]
        assert any(
            f"Row 1 (AIDX={aidx})" in e and "ASSAY_TYPE 'X' not in" in e
            for e in errors
        )

    @pytest.mark.parametrize("valid_type", list(VALID_ASSAY_TYPES))
    def test_all_valid_assay_types_pass(self, valid_type):
        df = _df(self._record_row(ASSAY_TYPE=valid_type))
        errors = validate(df)
        assert not any("ASSAY_TYPE" in e for e in errors)

    # --- TARGET_TYPE ---

    def test_invalid_target_type_exact_message(self):
        df = _df(self._record_row(TARGET_TYPE="BLOB"))
        errors = validate(df)
        aidx = self._record_row()["AIDX"]
        assert any(
            f"Row 1 (AIDX={aidx})" in e and "TARGET_TYPE 'BLOB' not in" in e
            for e in errors
        )

    def test_invalid_target_type_lowercase_normalised_before_check(self):
        """validate() uppercases TARGET_TYPE before checking — 'protein' should behave like 'PROTEIN'."""
        df = _df(self._record_row(TARGET_TYPE="protein"))
        errors = validate(df)
        assert not any("TARGET_TYPE" in e for e in errors)

    @pytest.mark.parametrize("valid_type", [
        "PROTEIN", "SINGLE PROTEIN", "PROTEIN COMPLEX", "ORGANISM",
        "NUCLEIC-ACID", "NO TARGET", "CELL-LINE", "SMALL MOLECULE",
    ])
    def test_representative_valid_target_types_pass(self, valid_type):
        df = _df(self._record_row(TARGET_TYPE=valid_type))
        errors = validate(df)
        assert not any("TARGET_TYPE" in e for e in errors), (
            f"Unexpected TARGET_TYPE error for valid value '{valid_type}': {errors}"
        )

    @pytest.mark.parametrize("valid_type", list(VALID_TARGET_TYPES))
    def test_all_valid_target_types_pass(self, valid_type):
        df = _df(self._record_row(TARGET_TYPE=valid_type))
        errors = validate(df)
        assert not any("TARGET_TYPE" in e for e in errors), (
            f"Unexpected TARGET_TYPE error for valid value '{valid_type}': {errors}"
        )

    def test_empty_target_type_no_error(self):
        """TARGET_TYPE is optional — empty value must not trigger a controlled-vocab error."""
        df = _df(self._record_row(TARGET_TYPE=""))
        errors = validate(df)
        assert not any("TARGET_TYPE" in e for e in errors)

    def test_chimeric_protein_and_lipid_are_separate_entries(self):
        """Guard against the missing-comma bug that concatenated 'CHIMERIC PROTEIN' + 'LIPID'."""
        assert "CHIMERIC PROTEIN" in VALID_TARGET_TYPES, (
            "'CHIMERIC PROTEIN' missing — check for missing comma in VALID_TARGET_TYPES"
        )
        assert "LIPID" in VALID_TARGET_TYPES, (
            "'LIPID' missing — check for missing comma in VALID_TARGET_TYPES"
        )
        assert "CHIMERIC PROTEINLIPID" not in VALID_TARGET_TYPES, (
            "String concatenation bug: 'CHIMERIC PROTEIN' and 'LIPID' were merged"
        )

    def test_target_organism_without_tax_id_exact_message(self):
        df = _df(self._record_row(TARGET_ORGANISM="Homo sapiens", TARGET_TAX_ID=""))
        errors = validate(df)
        aidx = self._record_row()["AIDX"]
        assert f"Row 1 (AIDX={aidx}): TARGET_TAX_ID is required when TARGET_ORGANISM is filled." in errors

    def test_target_organism_with_tax_id_no_error(self):
        df = _df(self._record_row(TARGET_ORGANISM="Homo sapiens", TARGET_TAX_ID="9606"))
        errors = validate(df)
        assert not any("TARGET_TAX_ID" in e for e in errors)

    def test_target_name_without_accession_exact_message(self):
        df = _df(self._record_row(TARGET_NAME="DNAK", TARGET_ACCESSION=""))
        errors = validate(df)
        aidx = self._record_row()["AIDX"]
        assert f"Row 1 (AIDX={aidx}): TARGET_ACCESSION (UniProt ID) is recommended when TARGET_NAME is provided." in errors

    def test_target_name_with_accession_no_error(self):
        df = _df(self._record_row(TARGET_NAME="DNAK", TARGET_ACCESSION="P0A6Y8"))
        errors = validate(df)
        assert not any("TARGET_ACCESSION" in e for e in errors)

    # --- TARGET_ACCESSION format validation ---

    @pytest.mark.parametrize("bad_acc", [
        "P",            # too short (1 char)
        "P0A6Y",        # 5 chars — one short of old format
        "P0A6Y88",      # 7 chars — one too long for old format
        "p0a6y8",       # lowercase — UniProt accessions are uppercase only
        "1P0A6Y",       # starts with a digit, not a letter
        "NOTANID",      # plain word, wrong format
        "P0A6Y-8",      # hyphen not allowed
    ])
    def test_invalid_accession_format_exact_message(self, bad_acc):
        df = _df(self._record_row(TARGET_ACCESSION=bad_acc))
        errors = validate(df)
        aidx = self._record_row()["AIDX"]
        expected = (
            f"Row 1 (AIDX={aidx}): TARGET_ACCESSION '{bad_acc}' is not a valid UniProt "
            f"accession format (expected e.g. 'P0A6Y8' or 'A0A023GPI8')."
        )
        assert expected in errors, (
            f"Expected format-error for '{bad_acc}' not found.\nGot: {errors}"
        )

    @pytest.mark.parametrize("good_acc", [
        "P0A6Y8",       # old format — SwissProt (starts with P)
        "Q9Y253",       # old format — SwissProt (starts with Q)
        "O15350",       # old format — SwissProt (starts with O)
        "A2BC19",       # new format — TrEMBL, 6-char variant
        "A0A023GPI8",   # new format — TrEMBL, 10-char variant
        "B7ZW16",       # new format — TrEMBL, 6-char variant
    ])
    def test_valid_accession_format_no_error(self, good_acc):
        df = _df(self._record_row(TARGET_ACCESSION=good_acc))
        errors = validate(df)
        format_errors = [e for e in errors if "not a valid UniProt accession format" in e]
        assert not format_errors, (
            f"Unexpected format-error for valid accession '{good_acc}': {format_errors}"
        )

    def test_empty_accession_does_not_trigger_format_error(self):
        """Empty TARGET_ACCESSION must not produce a format error (only a presence warning)."""
        df = _df(self._record_row(TARGET_ACCESSION=""))
        errors = validate(df)
        assert not any("not a valid UniProt accession format" in e for e in errors)

    def test_multiple_rows_errors_attributed_correctly(self):
        row1 = self._record_row(AIDX="A1", ASSAY_DESCRIPTION="")
        row2 = self._record_row(AIDX="A2", ASSAY_TAX_ID="")
        df = _df(row1, row2)
        errors = validate(df)
        assert "Row 1 (AIDX=A1): mandatory field 'ASSAY_DESCRIPTION' is empty." in errors
        assert "Row 2 (AIDX=A2): mandatory field 'ASSAY_TAX_ID' is empty." in errors
        assert "Row 2 (AIDX=A2): mandatory field 'ASSAY_DESCRIPTION' is empty." not in errors

    def test_empty_dataframe_no_errors(self):
        df = pd.DataFrame(columns=list(self._record_row().keys()))
        assert validate(df) == []


# ---------------------------------------------------------------------------
# lookup_taxid() — mock-based
# ---------------------------------------------------------------------------

class TestLookupTaxid:

    def setup_method(self):
        import microbes
        microbes._taxid_cache.clear()

    def test_empty_organism_returns_empty(self):
        assert lookup_taxid("") == ""

    def test_accession_strain_calls_straininfo_first(self):
        with patch("microbes._straininfo_by_accession", return_value="1234") as mock_si, \
             patch("microbes._ncbi_taxid", return_value="") as mock_ncbi:
            result = lookup_taxid("Escherichia coli", "DSM 498")
            mock_si.assert_called_once_with("DSM 498")
            mock_ncbi.assert_not_called()
            assert result == "1234"

    def test_non_accession_strain_calls_ncbi(self):
        with patch("microbes._straininfo_by_accession") as mock_si, \
             patch("microbes._ncbi_taxid", return_value="562") as mock_ncbi:
            result = lookup_taxid("Escherichia coli", "K12")
            mock_si.assert_not_called()
            mock_ncbi.assert_called_once_with("Escherichia coli")
            assert result == "562"

    def test_straininfo_miss_falls_back_to_ncbi(self):
        with patch("microbes._straininfo_by_accession", return_value=""), \
             patch("microbes._ncbi_taxid", return_value="562") as mock_ncbi:
            result = lookup_taxid("Escherichia coli", "DSM 498")
            mock_ncbi.assert_called_once()
            assert result == "562"

    def test_result_cached_second_call_makes_no_request(self):
        with patch("microbes._ncbi_taxid", return_value="562") as mock_ncbi:
            lookup_taxid("Escherichia coli", "K12")
            lookup_taxid("Escherichia coli", "K12")
            assert mock_ncbi.call_count == 1


# ---------------------------------------------------------------------------
# _uniprot_lookup() — mock-based
# ---------------------------------------------------------------------------

class TestUniprotLookup:

    def setup_method(self):
        import microbes
        microbes._uniprot_cache.clear()

    def _mock_response(self, status_code=200, json_data=None):
        mock = MagicMock()
        mock.status_code = status_code
        mock.json.return_value = json_data or {}
        mock.raise_for_status = MagicMock()
        return mock

    def test_empty_accession_returns_empty_dict(self):
        result = _uniprot_lookup("")
        assert result == {"name": "", "organism": "", "taxid": ""}

    def test_404_returns_empty_dict(self):
        with patch("microbes.requests.get",
                   return_value=self._mock_response(status_code=404)):
            result = _uniprot_lookup("INVALID")
        assert result == {"name": "", "organism": "", "taxid": ""}

    def test_successful_response_parsed_correctly(self):
        payload = {
            "proteinDescription": {
                "recommendedName": {"fullName": {"value": "Heat shock protein 70"}}
            },
            "organism": {"scientificName": "Escherichia coli", "taxonId": 83333},
        }
        with patch("microbes.requests.get",
                   return_value=self._mock_response(json_data=payload)):
            result = _uniprot_lookup("P0A6Y8")
        assert result["name"] == "Heat shock protein 70"
        assert result["organism"] == "Escherichia coli"
        assert result["taxid"] == "83333"

    def test_falls_back_to_entry_id_when_no_recommended_name(self):
        payload = {
            "uniProtkbId": "DNAK_ECOLI",
            "organism": {"scientificName": "Escherichia coli", "taxonId": 83333},
        }
        with patch("microbes.requests.get",
                   return_value=self._mock_response(json_data=payload)):
            result = _uniprot_lookup("P0A6Y8")
        assert result["name"] == "DNAK_ECOLI"

    def test_network_error_returns_empty_dict(self):
        import requests as req
        with patch("microbes.requests.get",
                   side_effect=req.exceptions.RequestException("timeout")):
            result = _uniprot_lookup("P0A6Y8")
        assert result == {"name": "", "organism": "", "taxid": ""}

    def test_result_cached_second_call_makes_no_request(self):
        payload = {
            "proteinDescription": {"recommendedName": {"fullName": {"value": "X"}}},
            "organism": {"scientificName": "Y", "taxonId": 1},
        }
        with patch("microbes.requests.get",
                   return_value=self._mock_response(json_data=payload)) as mock_get:
            _uniprot_lookup("P0A6Y8")
            _uniprot_lookup("P0A6Y8")
            assert mock_get.call_count == 1


# ---------------------------------------------------------------------------
# Live API integration tests
# ---------------------------------------------------------------------------
# These tests make real HTTP requests to three external services:
#   UniProt REST API   — https://rest.uniprot.org/uniprotkb
#   StrainInfo API     — https://api.straininfo.dsmz.de
#   NCBI e-utilities   — https://eutils.ncbi.nlm.nih.gov
#
# Run them with:
#   conda run -n rdkit_env pytest tests/test_microbes.py -m integration -v
#
# Skip them (e.g. in CI without network):
#   conda run -n rdkit_env pytest tests/test_microbes.py -m "not integration" -v
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestUniprotLookupLive:
    """
    Live integration tests for _uniprot_lookup().

    Reference entry used: P0A6Y8 — DnaK (DNAK_ECOLI), E. coli K-12.
    This is one of the most annotated entries in UniProt and its accession,
    recommended name, organism, and TaxID are stable across releases.
    """

    def setup_method(self):
        import microbes
        microbes._uniprot_cache.clear()

    # --- Success: canonical well-annotated entry P0A6Y8 ---

    def test_known_accession_name_is_non_empty(self):
        result = _uniprot_lookup("P0A6Y8")
        assert result["name"], (
            "UniProt P0A6Y8 (DnaK / DNAK_ECOLI) should return a non-empty protein name. "
            f"Got: {result!r}. Confirm https://rest.uniprot.org/uniprotkb/P0A6Y8.json is reachable."
        )

    def test_known_accession_organism_is_ecoli(self):
        result = _uniprot_lookup("P0A6Y8")
        assert "coli" in result["organism"].lower(), (
            "UniProt P0A6Y8 organism should contain 'coli' (protein belongs to E. coli K-12). "
            f"Got organism: {result['organism']!r}"
        )

    def test_known_accession_taxid_is_numeric(self):
        result = _uniprot_lookup("P0A6Y8")
        assert result["taxid"].isdigit(), (
            f"UniProt P0A6Y8 TaxID should be a numeric string. Got: {result['taxid']!r}"
        )

    def test_known_accession_taxid_is_ecoli_k12(self):
        result = _uniprot_lookup("P0A6Y8")
        # 83333 = E. coli K-12; 511145 = K-12 substr. MG1655 — both are acceptable
        assert result["taxid"] in {"83333", "511145"}, (
            f"UniProt P0A6Y8 TaxID should be 83333 (E. coli K-12) or 511145 (MG1655). "
            f"Got: {result['taxid']!r}"
        )

    def test_known_accession_all_three_fields_resolved(self):
        """Confirm the three fields that microbes.py auto-fills from TARGET_ACCESSION."""
        result = _uniprot_lookup("P0A6Y8")
        for field in ("name", "organism", "taxid"):
            assert result[field], (
                f"UniProt P0A6Y8: field '{field}' is unexpectedly empty. "
                f"Full result: {result!r}"
            )

    def test_successful_result_is_cached(self):
        """A second call must not make a new HTTP request (served from in-memory cache)."""
        _uniprot_lookup("P0A6Y8")  # populate cache via real network call
        with patch("microbes.requests.get") as mock_get:
            _uniprot_lookup("P0A6Y8")
            mock_get.assert_not_called()

    # --- Failure: non-existent or invalid accessions ---

    def test_garbage_accession_returns_empty_dict(self):
        """
        A clearly invalid string (not a real accession) must not raise and
        must return all-empty dict — either via a 404 or a RequestException.
        """
        result = _uniprot_lookup("NOTANACCESSION_XYZ")
        assert result == {"name": "", "organism": "", "taxid": ""}, (
            f"Expected all-empty dict for garbage accession 'NOTANACCESSION_XYZ', got: {result!r}"
        )


@pytest.mark.integration
class TestStrainInfoAPILive:
    """
    Live integration tests for _straininfo_by_accession().

    Reference strain: DSM 498 — E. coli K-12, deposited in DSMZ.
    Culture collection accession DSM 498 maps to NCBI Taxonomy via StrainInfo's
    deposit endpoint, which is the core use case of this API in microbes.py.
    """

    # --- Success ---

    def test_dsm_498_returns_non_empty_taxid(self):
        result = _straininfo_by_accession("DSM 498")
        assert result, (
            "Expected a non-empty TaxID for DSM 498 (E. coli K-12 from DSMZ). "
            f"Got: {result!r}. Confirm https://api.straininfo.dsmz.de is reachable."
        )

    def test_dsm_498_taxid_is_numeric(self):
        result = _straininfo_by_accession("DSM 498")
        assert result.isdigit(), (
            f"TaxID for DSM 498 must be a numeric string (NCBI TaxID format). "
            f"Got: {result!r}"
        )

    def test_dsm_498_taxid_is_ecoli_clade(self):
        """DSM 498 is E. coli K-12; TaxID must be in the E. coli taxonomy subtree."""
        result = _straininfo_by_accession("DSM 498")
        ecoli_taxids = {"562", "83333", "511145"}
        assert result in ecoli_taxids, (
            f"TaxID for DSM 498 (E. coli K-12) should be one of {ecoli_taxids} "
            f"(562=species, 83333=K-12 strain, 511145=MG1655 substrain). Got: {result!r}"
        )

    # --- Failure ---

    def test_unknown_accession_returns_empty_string(self):
        """
        An accession with no StrainInfo deposit record should return ''.
        The API returns 404 → the function catches it and returns ''.
        """
        result = _straininfo_by_accession("ZZZZZ 99999")
        assert result == "", (
            f"Expected '' for unknown accession 'ZZZZZ 99999' but got: {result!r}"
        )

    def test_malformed_input_returns_empty_string(self):
        """
        A string that is not a culture collection accession must not raise
        and must return '' (the API will 404 or return an empty list).
        """
        result = _straininfo_by_accession("not_a_real_accession###")
        assert result == "", (
            f"Expected '' for malformed input 'not_a_real_accession###' but got: {result!r}"
        )


@pytest.mark.integration
class TestNCBITaxonomyAPILive:
    """
    Live integration tests for _ncbi_taxid().

    Uses the NCBI Taxonomy e-utilities esearch endpoint.
    TaxIDs for well-established type species are stable across NCBI releases.
    """

    # --- Success ---

    def test_escherichia_coli_returns_562(self):
        result = _ncbi_taxid("Escherichia coli")
        assert result == "562", (
            f"Expected TaxID '562' for 'Escherichia coli' but got: {result!r}. "
            "Confirm https://eutils.ncbi.nlm.nih.gov is reachable."
        )

    def test_homo_sapiens_returns_9606(self):
        result = _ncbi_taxid("Homo sapiens")
        assert result == "9606", (
            f"Expected TaxID '9606' for 'Homo sapiens' but got: {result!r}"
        )

    def test_bacteroides_thetaiotaomicron_returns_818(self):
        """A core gut microbiome species commonly used in BioXend / MIX-MB studies."""
        result = _ncbi_taxid("Bacteroides thetaiotaomicron")
        assert result == "818", (
            f"Expected TaxID '818' for 'Bacteroides thetaiotaomicron' but got: {result!r}"
        )

    # --- Failure ---

    def test_unknown_organism_returns_empty_string(self):
        """
        A nonsense organism name returns no hits from NCBI esearch.
        _ncbi_taxid must return '' (not raise).
        """
        result = _ncbi_taxid("Xyzzy frobnicator 99999ZZZZ")
        assert result == "", (
            f"Expected '' for unknown organism 'Xyzzy frobnicator 99999ZZZZ' but got: {result!r}"
        )

    def test_partial_name_still_returns_string(self):
        """
        Even a partial or ambiguous name must not raise — result may be a TaxID
        or empty, but must always be a string.
        """
        result = _ncbi_taxid("Bacteroides")
        assert isinstance(result, str), (
            f"_ncbi_taxid must always return a string. Got: {type(result)} — {result!r}"
        )
