"""
Tests for bin/reference.py

# Run all tests (basic output):
# conda run -n rdkit_env pytest tests/test_reference.py -v

# See the actual error message values when a test fails (-s shows print output, --tb=short shows a compact traceback):
# conda run -n rdkit_env pytest tests/test_reference.py -v --tb=short

# Run only the validate tests to focus on error messages:
# conda run -n rdkit_env pytest tests/test_reference.py::TestValidate -v

# Run a single specific test:
# conda run -n rdkit_env pytest tests/test_reference.py::TestValidate::test_missing_both_doi_and_pubmed_exact_message -v

# See what error messages validate() actually produces right now (useful for debugging):

# conda run -n rdkit_env python -c "
# import sys; sys.path.insert(0, 'bin')
# from reference import validate
# import pandas as pd

# df = pd.DataFrame([{
#     'Reference_identifier': '',
#     'DOI': '', 'PUBMED_ID': '',
#     'DATA_LICENCE': 'CC0', 'CONTACT': 'a@b.com',
#     'YEAR': '2024', 'REF_TYPE': 'Thesis',
#     'TITLE': 'T', 'ABSTRACT': 'A', 'AUTHORS': 'X'
# }])
# for e in validate(df):
#     print(e)
# "
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))
from reference import (
    CHEMBL_COLS,
    MANDATORY_FIELDS,
    build_readme_toml,
    build_reference_tsv,
    read_reference_sheet,
    validate,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_row(**kwargs) -> dict:
    """Minimal valid reference row; override fields via kwargs."""
    base = {
        "Reference_identifier": "TestRef_2024",
        "PUBMED_ID": "12345678",
        "DATA_LICENCE": "CC0",
        "CONTACT": "test@example.com",
        "JOURNAL_NAME": "Nature",
        "YEAR": "2024",
        "VOLUME": "10",
        "ISSUE": "2",
        "FIRST_PAGE": "100",
        "LAST_PAGE": "110",
        "REF_TYPE": "Publication",
        "TITLE": "A test study",
        "DOI": "10.1000/test",
        "PATENT_ID": "",
        "ABSTRACT": "We studied biotransformation.",
        "AUTHORS": "Doe, Jane; Smith, John",
    }
    base.update(kwargs)
    return base


def _df(*rows) -> pd.DataFrame:
    return pd.DataFrame(list(rows))


# ---------------------------------------------------------------------------
# validate()
# ---------------------------------------------------------------------------

class TestValidate:
    """
    Each test pins the exact error message text produced by validate().
    This catches silent regressions where the message wording drifts but
    a substring check still passes.
    """

    def test_valid_row_no_errors(self):
        df = _df(_make_row())
        assert validate(df) == []

    def test_missing_reference_identifier_exact_message(self):
        df = _df(_make_row(Reference_identifier=""))
        errors = validate(df)
        assert "Row 1: 'Reference_identifier' (RIDX) is empty." in errors

    def test_none_reference_identifier_exact_message(self):
        # None should be treated the same as an empty string
        df = _df(_make_row(Reference_identifier=None))
        errors = validate(df)
        assert "Row 1: 'Reference_identifier' (RIDX) is empty." in errors

    def test_missing_both_doi_and_pubmed_exact_message(self):
        df = _df(_make_row(DOI="", PUBMED_ID=""))
        errors = validate(df)
        assert "Row 1: at least one of DOI or PUBMED_ID is required." in errors

    def test_doi_only_no_identifier_error(self):
        # DOI present, no PUBMED_ID — should not raise the doi/pubmed error
        df = _df(_make_row(PUBMED_ID="", REF_TYPE="Dataset"))
        errors = validate(df)
        assert not any("DOI or PUBMED_ID" in e for e in errors)

    def test_pubmed_only_no_identifier_error(self):
        # PUBMED_ID present, no DOI — should not raise the doi/pubmed error
        df = _df(_make_row(DOI=""))
        errors = validate(df)
        assert not any("DOI or PUBMED_ID" in e for e in errors)

    @pytest.mark.parametrize("field", MANDATORY_FIELDS)
    def test_each_mandatory_field_exact_message(self, field):
        df = _df(_make_row(**{field: ""}))
        errors = validate(df)
        assert f"Row 1: mandatory field '{field}' is empty." in errors

    def test_publication_missing_pubmed_exact_message(self):
        df = _df(_make_row(REF_TYPE="Publication", PUBMED_ID=""))
        errors = validate(df)
        assert "Row 1: conditional mandatory field 'PUBMED_ID' is empty." in errors

    def test_non_publication_pubmed_not_required(self):
        df = _df(_make_row(REF_TYPE="Dataset", PUBMED_ID=""))
        errors = validate(df)
        assert not any("conditional mandatory" in e for e in errors)

    def test_invalid_ref_type_exact_message(self):
        # The allowed set's repr has no guaranteed order, so we match the
        # fixed parts of the message and confirm all allowed values appear.
        df = _df(_make_row(REF_TYPE="Thesis"))
        errors = validate(df)
        match = next((e for e in errors if "REF_TYPE 'Thesis' not in" in e), None)
        assert match is not None, f"Expected REF_TYPE error not found in: {errors}"
        assert match.startswith("Row 1:")
        for allowed_val in ("Publication", "Patent", "Dataset", "Book"):
            assert allowed_val in match

    @pytest.mark.parametrize("ref_type", ["Publication", "Patent", "Dataset", "Book"])
    def test_all_allowed_ref_types_produce_no_ref_type_error(self, ref_type):
        row = _make_row(REF_TYPE=ref_type)
        if ref_type != "Publication":
            row["PUBMED_ID"] = ""
        df = _df(row)
        errors = validate(df)
        assert not any("not in" in e for e in errors)

    def test_multiple_rows_error_labels_are_correct(self):
        # Row 1 is missing RIDX; Row 2 is missing both DOI and PUBMED_ID.
        # Errors must be attributed to the right row number.
        row1 = _make_row(Reference_identifier="")
        row2 = _make_row(Reference_identifier="Valid_2024", DOI="", PUBMED_ID="")
        df = _df(row1, row2)
        errors = validate(df)
        assert "Row 1: 'Reference_identifier' (RIDX) is empty." in errors
        assert "Row 2: at least one of DOI or PUBMED_ID is required." in errors
        # Cross-check: row1 error should NOT appear under Row 2 label
        assert "Row 2: 'Reference_identifier' (RIDX) is empty." not in errors

    def test_empty_dataframe_returns_no_errors(self):
        df = pd.DataFrame(columns=list(_make_row().keys()))
        assert validate(df) == []


# ---------------------------------------------------------------------------
# build_reference_tsv()
# ---------------------------------------------------------------------------

class TestBuildReferenceTsv:

    def test_output_has_all_chembl_cols(self):
        df = _df(_make_row())
        result = build_reference_tsv(df)
        assert list(result.columns) == CHEMBL_COLS

    def test_ridx_comes_from_reference_identifier(self):
        df = _df(_make_row(Reference_identifier="MyStudy_2024"))
        result = build_reference_tsv(df)
        assert result["RIDX"].iloc[0] == "MyStudy_2024"

    def test_doi_value_preserved(self):
        df = _df(_make_row(DOI="10.1000/xyz"))
        result = build_reference_tsv(df)
        assert result["DOI"].iloc[0] == "10.1000/xyz"

    def test_nan_values_become_empty_string(self):
        df = _df(_make_row(VOLUME=np.nan, ISSUE=float("nan")))
        result = build_reference_tsv(df)
        assert result["VOLUME"].iloc[0] == ""
        assert result["ISSUE"].iloc[0] == ""

    def test_whitespace_stripped_from_values(self):
        df = _df(_make_row(TITLE="  Spaced Title  "))
        result = build_reference_tsv(df)
        assert result["TITLE"].iloc[0] == "Spaced Title"

    def test_multiple_rows_preserved(self):
        df = _df(_make_row(Reference_identifier="Ref1"), _make_row(Reference_identifier="Ref2"))
        result = build_reference_tsv(df)
        assert len(result) == 2
        assert list(result["RIDX"]) == ["Ref1", "Ref2"]

    def test_none_ridx_becomes_empty_string(self):
        df = _df(_make_row(Reference_identifier=None))
        result = build_reference_tsv(df)
        assert result["RIDX"].iloc[0] == ""

    def test_row_order_matches_chembl_cols(self):
        df = _df(_make_row())
        result = build_reference_tsv(df)
        assert list(result.columns) == CHEMBL_COLS


# ---------------------------------------------------------------------------
# build_readme_toml()
# ---------------------------------------------------------------------------

class TestBuildReadmeToml:

    def _toml_row(self, **kwargs):
        base = {
            "Reference_identifier": "Ref1",
            "Chembl_version": "34",
            "Names": "Mahnoor Zulfiqar, Jane Doe",
            "Institutions": "EMBL, HZI",
            "Links": "https://example.com",
            "TITLE": "A biotransformation study",
            "Description": "Gut microbiome study",
            "Recent_changes": "Initial submission",
            "Goal_of_submission": "ChEMBL deposition",
            "Compounds": "50",
            "Assays": "10",
            "Endpoints": "IC50, Ki",
            "Multiplexed": "false",
        }
        base.update(kwargs)
        return base

    def test_single_row_top_level_sections(self):
        df = _df(self._toml_row())
        result = build_readme_toml(df)
        assert set(result.keys()) == {"Deposition", "Dataset", "Summary_stats"}

    def test_deposition_title_from_title_col(self):
        df = _df(self._toml_row(TITLE="My Study"))
        result = build_readme_toml(df)
        assert result["Deposition"]["Title"] == "My Study"

    def test_int_fields_coerced(self):
        df = _df(self._toml_row(Chembl_version="34", Compounds="50", Assays="10"))
        result = build_readme_toml(df)
        assert result["Deposition"]["Chembl_version"] == 34
        assert result["Summary_stats"]["Compounds"] == 50
        assert result["Summary_stats"]["Assays"] == 10

    def test_bool_field_false(self):
        df = _df(self._toml_row(Multiplexed="false"))
        result = build_readme_toml(df)
        assert result["Summary_stats"]["Multiplexed"] is False

    def test_bool_field_true(self):
        df = _df(self._toml_row(Multiplexed="true"))
        result = build_readme_toml(df)
        assert result["Summary_stats"]["Multiplexed"] is True

    def test_list_field_comma_separated(self):
        df = _df(self._toml_row(Names="Alice, Bob, Carol"))
        result = build_readme_toml(df)
        assert result["Deposition"]["Names"] == ["Alice", "Bob", "Carol"]

    def test_list_field_newline_separated(self):
        df = _df(self._toml_row(Endpoints="IC50\nKi\nEC50"))
        result = build_readme_toml(df)
        assert result["Summary_stats"]["Endpoints"] == ["IC50", "Ki", "EC50"]

    def test_multiple_rows_produces_lists_per_section(self):
        df = _df(self._toml_row(TITLE="Study A"), self._toml_row(TITLE="Study B"))
        result = build_readme_toml(df)
        assert isinstance(result["Deposition"], list)
        assert len(result["Deposition"]) == 2
        assert isinstance(result["Dataset"], list)
        assert isinstance(result["Summary_stats"], list)

    def test_int_coercion_failure_returns_raw_string(self):
        df = _df(self._toml_row(Compounds="N/A"))
        result = build_readme_toml(df)
        assert result["Summary_stats"]["Compounds"] == "N/A"

    def test_nan_int_field_returns_empty_string(self):
        df = _df(self._toml_row(Compounds=np.nan))
        result = build_readme_toml(df)
        assert result["Summary_stats"]["Compounds"] == ""

    def test_empty_list_field_returns_empty_list(self):
        df = _df(self._toml_row(Endpoints=""))
        result = build_readme_toml(df)
        assert result["Summary_stats"]["Endpoints"] == []


# ---------------------------------------------------------------------------
# read_reference_sheet()
# ---------------------------------------------------------------------------

class TestReadReferenceSheet:
    """
    Mocks pd.read_excel so no ODS file is required.
    Tests the cleaning and slicing logic inside read_reference_sheet.
    """

    def _make_raw_ods(self, data_row: dict) -> pd.DataFrame:
        """
        Simulate the raw ODS layout:
          row 0 — ignored
          row 1 — column names  (_ROW_COLNAMES)
          row 2 — ignored
          row 3 — ignored
          row 4 — first data row  (_ROW_DATA_START)
        """
        col_names = list(data_row.keys())
        n_cols = len(col_names)
        filler = [None] * n_cols
        rows = [
            filler,          # row 0
            col_names,       # row 1 → used as headers
            filler,          # row 2
            filler,          # row 3
            list(data_row.values()),  # row 4 → first data row
        ]
        return pd.DataFrame(rows)

    def _call(self, data_row: dict) -> pd.DataFrame:
        raw = self._make_raw_ods(data_row)
        with patch("reference.pd.read_excel", return_value=raw):
            return read_reference_sheet(Path("dummy.ods"))

    def test_returns_dataframe(self):
        result = self._call(_make_row())
        assert isinstance(result, pd.DataFrame)

    def test_column_names_from_row1(self):
        result = self._call(_make_row())
        assert "Reference_identifier" in result.columns
        assert "DOI" in result.columns

    def test_data_starts_at_row4(self):
        result = self._call(_make_row(DOI="10.1000/abc"))
        assert result["DOI"].iloc[0] == "10.1000/abc"

    def test_nan_string_replaced_with_empty(self):
        result = self._call(_make_row(DOI="nan"))
        assert result["DOI"].iloc[0] == ""

    def test_whitespace_stripped(self):
        result = self._call(_make_row(TITLE="  My Title  "))
        assert result["TITLE"].iloc[0] == "My Title"

    def test_all_nan_rows_dropped(self):
        col_names = list(_make_row().keys())
        n_cols = len(col_names)
        filler = [None] * n_cols
        data_row = list(_make_row().values())
        rows = [
            filler,
            col_names,
            filler,
            filler,
            data_row,
            filler,  # extra all-NaN row that should be dropped
        ]
        raw = pd.DataFrame(rows)
        with patch("reference.pd.read_excel", return_value=raw):
            result = read_reference_sheet(Path("dummy.ods"))
        assert len(result) == 1


