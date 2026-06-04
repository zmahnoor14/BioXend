"""
Tests for bin/biotransformation.py

# ---------------------------------------------------------------------------
# How to run
# ---------------------------------------------------------------------------

Run all tests (basic output):
conda run -n rdkit_env pytest tests/test_biotransformation.py -v

See the actual error message values when a test fails:
conda run -n rdkit_env pytest tests/test_biotransformation.py -v --tb=short

Run only the validate tests to focus on error messages:
conda run -n rdkit_env pytest tests/test_biotransformation.py::TestValidate -v

Run a single specific test:
conda run -n rdkit_env pytest tests/test_biotransformation.py::TestBuildActivityComment::test_mz_and_rt_combined -v

See what error messages validate() actually produces right now (useful for debugging):

conda run -n rdkit_env python -c "
import sys; sys.path.insert(0, 'bin')
from biotransformation import build_activity_tsv, validate
import pandas as pd

df = pd.DataFrame([{
    'Common_Name': 'Ethanol',
    'Chemical_identifier': '',
    'ASSAY_Identifier': 'assay1',
    'Activity_type': '',
    'TEXT_VALUE': '',
    'RELATION': '??',
    'VALUE': '50',
    'UPPER_VALUE': '',
    'UNITS': '',
    'ACTION_TYPE': 'INVALID',
    'ACTIVITY_COMMENT': '',
    'Reaction_type': '',
    'Metabolite_mz': '',
    'Metabolite_rt': '',
    'Metabolite_annotation': '',
    'Metabolite_annotation_level': '',
}])
cidx_map = {'ethanol': 'HMDM01'}
aidx_map = {'assay1': 'Zimmermann_Ecoli_Biotransformation'}
activity_df = build_activity_tsv(df, ridx='TestRef', cidx_map=cidx_map, aidx_map=aidx_map)
for e in validate(activity_df):
    print(e)
"
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))
from biotransformation import (
    CHEMBL_COLS,
    MANDATORY_FIELDS,
    VALID_ACTION_TYPES,
    VALID_RELATIONS,
    _build_activity_comment,
    _build_aidx_map,
    _build_cidx_map,
    _clean,
    _coerce_numeric,
    _resolve_aidx,
    _resolve_cidx,
    build_activity_tsv,
    validate,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_row(**kwargs) -> dict:
    """Minimal valid Biotransformation sheet row; override fields via kwargs."""
    base = {
        "Common_Name":                "Ethanol",
        "Chemical_identifier":        "",
        "ASSAY_Identifier":           "assay1",
        "Activity_type":              "",
        "TEXT_VALUE":                 "Active",
        "RELATION":                   "",
        "VALUE":                      "",
        "UPPER_VALUE":                "",
        "UNITS":                      "",
        "ACTION_TYPE":                "SUBSTRATE",
        "ACTIVITY_COMMENT":           "Detected in gut",
        "Reaction_type":              "",
        "Metabolite_mz":              "",
        "Metabolite_rt":              "",
        "Metabolite_annotation":      "",
        "Metabolite_annotation_level": "",
    }
    base.update(kwargs)
    return base


def _record_row(**kwargs) -> dict:
    """Minimal valid ACTIVITY.tsv record row (output of build_activity_tsv)."""
    base = {
        "CIDX":             "HMDM01",
        "RIDX":             "TestRef",
        "CRIDX":            "TestRef",
        "AIDX":             "Zimmermann_Ecoli_Biotransformation",
        "TYPE":             "Biotransformation",
        "TEXT_VALUE":       "Active",
        "RELATION":         "",
        "VALUE":            "",
        "UPPER_VALUE":      "",
        "UNITS":            "",
        "ACTIVITY_COMMENT": "Detected in gut",
        "ACTION_TYPE":      "SUBSTRATE",
    }
    base.update(kwargs)
    return base


def _df(*rows) -> pd.DataFrame:
    return pd.DataFrame(list(rows))


CIDX_MAP = {"ethanol": "HMDM01", "aspirin": "HMDM02"}
AIDX_MAP = {"assay1": "Zimmermann_Ecoli_Biotransformation"}


# ---------------------------------------------------------------------------
# _clean()
# ---------------------------------------------------------------------------

class TestClean:
    """
    Note: biotransformation._clean converts non-str non-NaN values to str(v),
    unlike microbes._clean which returns v unchanged.
    """

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
        assert _clean("  Ethanol  ") == "Ethanol"

    def test_non_nan_number_converted_to_string(self):
        assert _clean(42) == "42"

    def test_empty_string_stays_empty(self):
        assert _clean("") == ""


# ---------------------------------------------------------------------------
# _coerce_numeric()
# ---------------------------------------------------------------------------

class TestCoerceNumeric:

    def test_empty_string_returns_empty(self):
        assert _coerce_numeric("") == ""

    def test_none_returns_empty(self):
        assert _coerce_numeric(None) == ""

    def test_integer_valued_float_returns_int_string(self):
        assert _coerce_numeric("85.0") == "85"
        assert _coerce_numeric(85.0) == "85"

    def test_non_integer_float_returned_as_is(self):
        assert _coerce_numeric("85.5") == "85.5"

    def test_zero_float_returns_zero_string(self):
        assert _coerce_numeric("0.0") == "0"

    def test_non_numeric_string_returned_stripped(self):
        assert _coerce_numeric("  N/A  ") == "N/A"

    def test_plain_integer_string(self):
        assert _coerce_numeric("50") == "50"


# ---------------------------------------------------------------------------
# _build_cidx_map()
# ---------------------------------------------------------------------------

class TestBuildCidxMap:

    def test_none_path_returns_empty_dict(self):
        assert _build_cidx_map(None) == {}

    def test_nonexistent_path_returns_empty_dict(self):
        assert _build_cidx_map(Path("/no/such/file.tsv")) == {}

    def test_valid_tsv_builds_lowercase_map(self, tmp_path):
        tsv = tmp_path / "COMPOUND_MAPPING.tsv"
        tsv.write_text("Common_Name\tCIDX\nEthanol\tHMDM01\nAspirin\tHMDM02\n")
        result = _build_cidx_map(tsv)
        assert result == {"ethanol": "HMDM01", "aspirin": "HMDM02"}

    def test_keys_are_lowercased(self, tmp_path):
        tsv = tmp_path / "COMPOUND_MAPPING.tsv"
        tsv.write_text("Common_Name\tCIDX\nEthanol\tHMDM01\n")
        result = _build_cidx_map(tsv)
        assert "ethanol" in result
        assert "Ethanol" not in result

    def test_rows_with_empty_name_or_cidx_skipped(self, tmp_path):
        tsv = tmp_path / "COMPOUND_MAPPING.tsv"
        tsv.write_text("Common_Name\tCIDX\n\tHMDM01\nEthanol\t\nAspirin\tHMDM02\n")
        result = _build_cidx_map(tsv)
        assert result == {"aspirin": "HMDM02"}

    def test_multiple_compounds_all_loaded(self, tmp_path):
        tsv = tmp_path / "COMPOUND_MAPPING.tsv"
        tsv.write_text("Common_Name\tCIDX\nA\tC01\nB\tC02\nC\tC03\n")
        result = _build_cidx_map(tsv)
        assert len(result) == 3


# ---------------------------------------------------------------------------
# _build_aidx_map()
# ---------------------------------------------------------------------------

class TestBuildAidxMap:

    def test_none_path_returns_empty_dict(self):
        assert _build_aidx_map(None) == {}

    def test_nonexistent_path_returns_empty_dict(self):
        assert _build_aidx_map(Path("/no/such/file.tsv")) == {}

    def test_valid_tsv_builds_map(self, tmp_path):
        tsv = tmp_path / "ASSAY_MAPPING.tsv"
        tsv.write_text("assay_identifier\tAIDX\nassay1\tZimmermann_Ecoli_Biotransformation\n")
        result = _build_aidx_map(tsv)
        assert result == {"assay1": "Zimmermann_Ecoli_Biotransformation"}

    def test_rows_with_empty_values_skipped(self, tmp_path):
        tsv = tmp_path / "ASSAY_MAPPING.tsv"
        tsv.write_text("assay_identifier\tAIDX\nassay1\tAIDX_1\n\tAIDX_2\nassay3\t\n")
        result = _build_aidx_map(tsv)
        assert result == {"assay1": "AIDX_1"}

    def test_multiple_assays_all_loaded(self, tmp_path):
        tsv = tmp_path / "ASSAY_MAPPING.tsv"
        tsv.write_text("assay_identifier\tAIDX\na1\tA1\na2\tA2\n")
        result = _build_aidx_map(tsv)
        assert len(result) == 2


# ---------------------------------------------------------------------------
# _resolve_cidx()
# ---------------------------------------------------------------------------

class TestResolveCidx:

    def test_common_name_resolved_from_map(self):
        row = pd.Series(_make_row(Common_Name="Ethanol"))
        assert _resolve_cidx(row, CIDX_MAP) == "HMDM01"

    def test_common_name_lookup_is_case_insensitive(self):
        row = pd.Series(_make_row(Common_Name="ETHANOL"))
        assert _resolve_cidx(row, CIDX_MAP) == "HMDM01"

    def test_falls_back_to_chemical_identifier(self):
        row = pd.Series(_make_row(Common_Name="Unknown", Chemical_identifier="CIDX9999"))
        assert _resolve_cidx(row, CIDX_MAP) == "CIDX9999"

    def test_chemical_identifier_used_when_no_map(self):
        row = pd.Series(_make_row(Common_Name="", Chemical_identifier="CIDX0001"))
        assert _resolve_cidx(row, {}) == "CIDX0001"

    def test_neither_found_returns_empty(self):
        row = pd.Series(_make_row(Common_Name="Unknown", Chemical_identifier=""))
        assert _resolve_cidx(row, CIDX_MAP) == ""

    def test_empty_common_name_uses_chemical_identifier(self):
        row = pd.Series(_make_row(Common_Name="", Chemical_identifier="HMDM03"))
        assert _resolve_cidx(row, CIDX_MAP) == "HMDM03"

    def test_map_entry_preferred_over_chemical_identifier(self):
        row = pd.Series(_make_row(Common_Name="Ethanol", Chemical_identifier="DIRECT"))
        assert _resolve_cidx(row, CIDX_MAP) == "HMDM01"


# ---------------------------------------------------------------------------
# _resolve_aidx()
# ---------------------------------------------------------------------------

class TestResolveAidx:

    def test_assay_identifier_resolved_from_map(self):
        row = pd.Series(_make_row(ASSAY_Identifier="assay1"))
        assert _resolve_aidx(row, AIDX_MAP) == "Zimmermann_Ecoli_Biotransformation"

    def test_assay_identifier_used_as_is_when_not_in_map(self, capsys):
        row = pd.Series(_make_row(ASSAY_Identifier="unknown_assay"))
        result = _resolve_aidx(row, AIDX_MAP)
        assert result == "unknown_assay"
        assert "No AIDX mapping found" in capsys.readouterr().err

    def test_assay_identifier_used_as_is_when_map_empty(self):
        row = pd.Series(_make_row(ASSAY_Identifier="full_aidx_value"))
        assert _resolve_aidx(row, {}) == "full_aidx_value"

    def test_empty_assay_identifier_returns_empty(self):
        row = pd.Series(_make_row(ASSAY_Identifier=""))
        assert _resolve_aidx(row, AIDX_MAP) == ""

    def test_column_key_is_case_insensitive(self):
        # Column may appear as 'assay_identifier' (lowercase) or 'ASSAY_Identifier'
        row = pd.Series({"assay_identifier": "assay1"})
        assert _resolve_aidx(row, AIDX_MAP) == "Zimmermann_Ecoli_Biotransformation"


# ---------------------------------------------------------------------------
# _build_activity_comment()
# ---------------------------------------------------------------------------

class TestBuildActivityComment:

    def _row(self, **kwargs) -> pd.Series:
        base = {
            "ACTIVITY_COMMENT":          "",
            "Reaction_type":             "",
            "Metabolite_mz":             "",
            "Metabolite_rt":             "",
            "Metabolite_annotation":     "",
            "Metabolite_annotation_level": "",
        }
        base.update(kwargs)
        return pd.Series(base)

    def test_only_base_comment(self):
        result = _build_activity_comment(self._row(ACTIVITY_COMMENT="Detected"))
        assert result == "Detected"

    def test_all_empty_returns_empty_string(self):
        assert _build_activity_comment(self._row()) == ""

    def test_reaction_type_sentence(self):
        result = _build_activity_comment(self._row(Reaction_type="hydroxylation"))
        assert "The reaction is hydroxylation" in result

    def test_mz_and_rt_combined(self):
        result = _build_activity_comment(self._row(Metabolite_mz="180.06", Metabolite_rt="3.5"))
        assert "The Metabolite m/z is 180.06 with retention time 3.5." in result

    def test_mz_only(self):
        result = _build_activity_comment(self._row(Metabolite_mz="180.06"))
        assert "The Metabolite m/z is 180.06" in result
        assert "retention time" not in result

    def test_rt_only(self):
        result = _build_activity_comment(self._row(Metabolite_rt="3.5"))
        assert "with retention time 3.5." in result
        assert "m/z" not in result

    def test_annotation_with_level(self):
        result = _build_activity_comment(
            self._row(Metabolite_annotation="4-OH-testosterone", Metabolite_annotation_level="2")
        )
        assert "The annotated metabolite is 4-OH-testosterone with annotation level of 2" in result

    def test_annotation_without_level(self):
        result = _build_activity_comment(
            self._row(Metabolite_annotation="4-OH-testosterone")
        )
        assert "The annotated metabolite is 4-OH-testosterone" in result
        assert "level" not in result

    def test_all_fields_joined_by_semicolons(self):
        result = _build_activity_comment(self._row(
            ACTIVITY_COMMENT="Base",
            Reaction_type="reduction",
            Metabolite_mz="200.1",
            Metabolite_rt="5.0",
            Metabolite_annotation="Metabolite-A",
            Metabolite_annotation_level="1",
        ))
        parts = result.split("; ")
        assert len(parts) == 4
        assert parts[0] == "Base"

    def test_base_plus_reaction_only(self):
        result = _build_activity_comment(self._row(
            ACTIVITY_COMMENT="Observed", Reaction_type="oxidation"
        ))
        assert result == "Observed; The reaction is oxidation"


# ---------------------------------------------------------------------------
# build_activity_tsv()
# ---------------------------------------------------------------------------

class TestBuildActivityTsv:

    def test_output_has_all_chembl_cols(self):
        df = _df(_make_row())
        result = build_activity_tsv(df, ridx="TestRef", cidx_map=CIDX_MAP, aidx_map=AIDX_MAP)
        assert list(result.columns) == CHEMBL_COLS

    def test_ridx_and_cridx_set_to_ridx_arg(self):
        df = _df(_make_row())
        result = build_activity_tsv(df, ridx="MyStudy", cidx_map=CIDX_MAP, aidx_map=AIDX_MAP)
        assert result["RIDX"].iloc[0] == "MyStudy"
        assert result["CRIDX"].iloc[0] == "MyStudy"

    def test_type_always_biotransformation(self):
        df = _df(_make_row())
        result = build_activity_tsv(df, ridx="R", cidx_map=CIDX_MAP, aidx_map=AIDX_MAP)
        assert result["TYPE"].iloc[0] == "Biotransformation"

    def test_cidx_resolved_from_map(self):
        df = _df(_make_row(Common_Name="Ethanol"))
        result = build_activity_tsv(df, ridx="R", cidx_map=CIDX_MAP, aidx_map=AIDX_MAP)
        assert result["CIDX"].iloc[0] == "HMDM01"

    def test_aidx_resolved_from_map(self):
        df = _df(_make_row(ASSAY_Identifier="assay1"))
        result = build_activity_tsv(df, ridx="R", cidx_map=CIDX_MAP, aidx_map=AIDX_MAP)
        assert result["AIDX"].iloc[0] == "Zimmermann_Ecoli_Biotransformation"

    def test_text_value_used_when_value_empty(self):
        df = _df(_make_row(TEXT_VALUE="Active", VALUE=""))
        result = build_activity_tsv(df, ridx="R", cidx_map=CIDX_MAP, aidx_map=AIDX_MAP)
        assert result["TEXT_VALUE"].iloc[0] == "Active"
        assert result["VALUE"].iloc[0] == ""

    def test_value_set_clears_text_value(self):
        # When VALUE is present, TEXT_VALUE is left empty (both cannot coexist)
        df = _df(_make_row(TEXT_VALUE="Active", VALUE="50.0"))
        result = build_activity_tsv(df, ridx="R", cidx_map=CIDX_MAP, aidx_map=AIDX_MAP)
        assert result["VALUE"].iloc[0] == "50"
        assert result["TEXT_VALUE"].iloc[0] == ""

    def test_value_integer_float_coerced(self):
        df = _df(_make_row(VALUE="85.0"))
        result = build_activity_tsv(df, ridx="R", cidx_map=CIDX_MAP, aidx_map=AIDX_MAP)
        assert result["VALUE"].iloc[0] == "85"

    def test_activity_comment_built_from_extension_fields(self):
        df = _df(_make_row(
            ACTIVITY_COMMENT="",
            Reaction_type="hydroxylation",
            Metabolite_mz="180.06",
        ))
        result = build_activity_tsv(df, ridx="R", cidx_map=CIDX_MAP, aidx_map=AIDX_MAP)
        comment = result["ACTIVITY_COMMENT"].iloc[0]
        assert "hydroxylation" in comment
        assert "180.06" in comment

    def test_multiple_rows_all_written(self):
        df = _df(_make_row(Common_Name="Ethanol"), _make_row(Common_Name="Aspirin"))
        result = build_activity_tsv(df, ridx="R", cidx_map=CIDX_MAP, aidx_map=AIDX_MAP)
        assert len(result) == 2

    def test_empty_dataframe_returns_empty_with_cols(self):
        df = pd.DataFrame(columns=list(_make_row().keys()))
        result = build_activity_tsv(df, ridx="R", cidx_map=CIDX_MAP, aidx_map=AIDX_MAP)
        assert list(result.columns) == CHEMBL_COLS
        assert len(result) == 0


# ---------------------------------------------------------------------------
# validate()
# ---------------------------------------------------------------------------

class TestValidate:
    """Each test pins the exact error message text produced by validate()."""

    def _label(self, row: dict) -> str:
        return f"Row 1 (CIDX={row['CIDX']}, AIDX={row['AIDX']})"

    def test_valid_record_no_errors(self):
        df = _df(_record_row())
        assert validate(df) == []

    @pytest.mark.parametrize("field", MANDATORY_FIELDS)
    def test_each_mandatory_field_exact_message(self, field):
        row = _record_row(**{field: ""})
        df = _df(row)
        errors = validate(df)
        # validate() uses row.get(key, '?') — '?' only fires when key is absent;
        # when the key exists but is empty the label shows the empty string.
        cidx = row["CIDX"]   # "" when field=="CIDX", else "HMDM01"
        aidx = row["AIDX"]   # "" when field=="AIDX", else full AIDX
        label = f"Row 1 (CIDX={cidx}, AIDX={aidx})"
        assert any(
            e.startswith(label) and f"mandatory field '{field}' is empty." in e
            for e in errors
        ), f"Expected mandatory-field error for '{field}' not found in: {errors}"

    def test_both_text_value_and_value_empty_exact_message(self):
        row = _record_row(TEXT_VALUE="", VALUE="")
        df = _df(row)
        errors = validate(df)
        label = self._label(row)
        assert (
            f"{label}: both TEXT_VALUE and VALUE are empty — "
            "at least one must be provided."
        ) in errors

    def test_text_value_present_no_text_value_error(self):
        df = _df(_record_row(TEXT_VALUE="Active", VALUE=""))
        errors = validate(df)
        assert not any("TEXT_VALUE and VALUE are empty" in e for e in errors)

    def test_value_present_no_text_value_error(self):
        df = _df(_record_row(TEXT_VALUE="", VALUE="50", RELATION="=", UNITS="%"))
        errors = validate(df)
        assert not any("TEXT_VALUE and VALUE are empty" in e for e in errors)

    def test_value_set_requires_relation_exact_message(self):
        row = _record_row(VALUE="50", RELATION="", UNITS="%")
        df = _df(row)
        errors = validate(df)
        label = self._label(row)
        assert f"{label}: RELATION is required when VALUE is set." in errors

    def test_value_set_requires_units_exact_message(self):
        row = _record_row(VALUE="50", RELATION="=", UNITS="")
        df = _df(row)
        errors = validate(df)
        label = self._label(row)
        assert f"{label}: UNITS is required when VALUE is set." in errors

    def test_value_with_relation_and_units_no_error(self):
        df = _df(_record_row(TEXT_VALUE="", VALUE="50", RELATION="=", UNITS="%"))
        errors = validate(df)
        assert not any("RELATION" in e or "UNITS" in e for e in errors)

    def test_invalid_relation_exact_message(self):
        row = _record_row(RELATION="??")
        df = _df(row)
        errors = validate(df)
        label = self._label(row)
        assert any(
            e.startswith(label) and "RELATION '??' not in" in e
            for e in errors
        )

    @pytest.mark.parametrize("rel", list(VALID_RELATIONS))
    def test_all_valid_relations_produce_no_relation_error(self, rel):
        df = _df(_record_row(RELATION=rel))
        errors = validate(df)
        assert not any("not in" in e and "RELATION" in e for e in errors)

    def test_invalid_action_type_message_contains_value(self):
        row = _record_row(ACTION_TYPE="INVALID_TYPE")
        df = _df(row)
        errors = validate(df)
        label = self._label(row)
        assert any(
            e.startswith(label) and "ACTION_TYPE 'INVALID_TYPE' not in" in e
            for e in errors
        )

    @pytest.mark.parametrize("action_type", ["SUBSTRATE", "INHIBITOR", "ACTIVATOR"])
    def test_valid_action_types_produce_no_action_type_error(self, action_type):
        df = _df(_record_row(ACTION_TYPE=action_type))
        errors = validate(df)
        assert not any("ACTION_TYPE" in e and "not in" in e for e in errors)

    def test_empty_action_type_no_action_type_error(self):
        df = _df(_record_row(ACTION_TYPE=""))
        errors = validate(df)
        assert not any("ACTION_TYPE" in e for e in errors)

    def test_multiple_rows_errors_attributed_correctly(self):
        row1 = _record_row(CIDX="C1", AIDX="A1", TYPE="")
        row2 = _record_row(CIDX="C2", AIDX="A2", TEXT_VALUE="", VALUE="")
        df = _df(row1, row2)
        errors = validate(df)
        assert "Row 1 (CIDX=C1, AIDX=A1): mandatory field 'TYPE' is empty." in errors
        assert (
            "Row 2 (CIDX=C2, AIDX=A2): both TEXT_VALUE and VALUE are empty — "
            "at least one must be provided."
        ) in errors
        # Cross-check: row1 error not attributed to row2
        assert "Row 2 (CIDX=C2, AIDX=A2): mandatory field 'TYPE' is empty." not in errors

    def test_empty_dataframe_no_errors(self):
        df = pd.DataFrame(columns=list(_record_row().keys()))
        assert validate(df) == []
