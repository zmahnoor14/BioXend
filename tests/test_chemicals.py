"""
Tests for bin/chemicals.py

# ---------------------------------------------------------------------------
# How to run
# ---------------------------------------------------------------------------

Run all tests (basic output):
conda run -n rdkit_env pytest tests/test_chemicals.py -v

See the actual error message values when a test fails:
conda run -n rdkit_env pytest tests/test_chemicals.py -v --tb=short

Run only the validate tests to focus on error messages:
conda run -n rdkit_env pytest tests/test_chemicals.py::TestValidate -v

Run a single specific test:
conda run -n rdkit_env pytest tests/test_chemicals.py::TestValidate::test_missing_compound_name_exact_message -v

See what error messages validate() actually produces right now (useful for debugging):

conda run -n rdkit_env python -c "
import sys; sys.path.insert(0, 'bin')
from chemicals import build_compound_records, validate
import pandas as pd

df = pd.DataFrame([{
    'Chemical_identifier': '',
    'SMILES': 'CCO',
    'Common_Name': '',
    'Local_Synonym': '',
    'Vendor': '',
    'database_ID': '',
}])
records = build_compound_records(df, ridx='TestRef', prefix='HMDM')
for e in validate(records):
    print(e)
"
"""

import sys
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from rdkit import Chem

sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))
from chemicals import (
    CHEMBL_COLS,
    MANDATORY_FIELDS,
    _make_cidx,
    build_compound_records,
    read_chemicals_sheet,
    validate,
    write_compound_ctab_sdf,
)

# ---------------------------------------------------------------------------
# Real SMILES used across tests
# ---------------------------------------------------------------------------
ETHANOL   = "CCO"
ASPIRIN   = "CC(=O)Oc1ccccc1C(=O)O"
CAFFEINE  = "Cn1c(=O)c2c(ncn2C)n(c1=O)C"
INVALID   = "not_a_smiles"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_row(**kwargs) -> dict:
    """Minimal valid chemicals row; override fields via kwargs."""
    base = {
        "Chemical_identifier": "",
        "SMILES":              ETHANOL,
        "Common_Name":         "Ethanol",
        "Local_Synonym":       "EtOH",
        "Vendor":              "Sigma",
        "database_ID":         "DB00898",
    }
    base.update(kwargs)
    return base


def _df(*rows) -> pd.DataFrame:
    return pd.DataFrame(list(rows))


# ---------------------------------------------------------------------------
# _make_cidx()
# ---------------------------------------------------------------------------

class TestMakeCidx:
    """
    CIDX zero-padding scales with dataset size so that all identifiers
    share the same width (len(str(total)) + 1).
    """

    def test_single_digit_total_width_2(self):
        # total=9 → width=2 → PREFIX01..PREFIX09
        assert _make_cidx(1, 9, "HMDM") == "HMDM01"
        assert _make_cidx(9, 9, "HMDM") == "HMDM09"

    def test_two_digit_total_width_3(self):
        # total=10 → width=3 → PREFIX001..PREFIX010
        assert _make_cidx(1,  10, "HMDM") == "HMDM001"
        assert _make_cidx(10, 10, "HMDM") == "HMDM010"

    def test_three_digit_total_width_4(self):
        assert _make_cidx(1,   100, "HMDM") == "HMDM0001"
        assert _make_cidx(100, 100, "HMDM") == "HMDM0100"

    def test_four_digit_total_width_5(self):
        assert _make_cidx(1,    1000, "HMDM") == "HMDM00001"
        assert _make_cidx(1000, 1000, "HMDM") == "HMDM01000"

    def test_custom_prefix(self):
        assert _make_cidx(1, 9, "ZM") == "ZM01"
        assert _make_cidx(1, 9, "CIDX") == "CIDX01"

    def test_sequential_cidxs_are_unique(self):
        cidxs = [_make_cidx(n, 5, "P") for n in range(1, 6)]
        assert len(set(cidxs)) == 5


# ---------------------------------------------------------------------------
# build_compound_records()
# ---------------------------------------------------------------------------

class TestBuildCompoundRecords:

    def test_valid_smiles_produces_one_record(self):
        df = _df(_make_row(SMILES=ETHANOL))
        result = build_compound_records(df, ridx="TestRef", prefix="HMDM")
        assert len(result) == 1

    def test_invalid_smiles_row_is_skipped(self, capsys):
        df = _df(_make_row(SMILES=INVALID))
        result = build_compound_records(df, ridx="TestRef", prefix="HMDM")
        assert len(result) == 0
        captured = capsys.readouterr()
        assert "invalid or missing SMILES" in captured.err

    def test_empty_smiles_row_is_skipped(self, capsys):
        df = _df(_make_row(SMILES=""))
        result = build_compound_records(df, ridx="TestRef", prefix="HMDM")
        assert len(result) == 0
        assert "invalid or missing SMILES" in capsys.readouterr().err

    def test_mixed_valid_invalid_only_valid_kept(self):
        df = _df(
            _make_row(SMILES=ETHANOL,  Common_Name="Ethanol"),
            _make_row(SMILES=INVALID,  Common_Name="Bad"),
            _make_row(SMILES=ASPIRIN,  Common_Name="Aspirin"),
        )
        result = build_compound_records(df, ridx="TestRef", prefix="HMDM")
        assert len(result) == 2
        assert list(result["COMPOUND_NAME"]) == ["Ethanol", "Aspirin"]

    def test_ridx_set_on_all_rows(self):
        df = _df(_make_row(SMILES=ETHANOL), _make_row(SMILES=ASPIRIN))
        result = build_compound_records(df, ridx="MyStudy", prefix="HMDM")
        assert all(result["RIDX"] == "MyStudy")

    def test_provided_chemical_identifier_used_as_cidx(self):
        df = _df(_make_row(Chemical_identifier="CIDX9999"))
        result = build_compound_records(df, ridx="R", prefix="HMDM")
        assert result["CIDX"].iloc[0] == "CIDX9999"

    def test_auto_generated_cidx_when_identifier_missing(self):
        df = _df(_make_row(Chemical_identifier=""))
        result = build_compound_records(df, ridx="R", prefix="HMDM")
        assert result["CIDX"].iloc[0] == "HMDM01"

    def test_auto_cidx_sequential_across_rows(self):
        df = _df(
            _make_row(Chemical_identifier="", SMILES=ETHANOL),
            _make_row(Chemical_identifier="", SMILES=ASPIRIN),
            _make_row(Chemical_identifier="", SMILES=CAFFEINE),
        )
        result = build_compound_records(df, ridx="R", prefix="P")
        assert list(result["CIDX"]) == ["P01", "P02", "P03"]

    def test_compound_name_from_common_name(self):
        df = _df(_make_row(Common_Name="Aspirin", SMILES=ASPIRIN))
        result = build_compound_records(df, ridx="R", prefix="HMDM")
        assert result["COMPOUND_NAME"].iloc[0] == "Aspirin"

    def test_compound_key_from_local_synonym(self):
        df = _df(_make_row(Local_Synonym="ASA", Common_Name="Aspirin", SMILES=ASPIRIN))
        result = build_compound_records(df, ridx="R", prefix="HMDM")
        assert result["COMPOUND_KEY"].iloc[0] == "ASA"

    def test_compound_key_falls_back_to_common_name(self):
        df = _df(_make_row(Local_Synonym="", Common_Name="Ethanol", SMILES=ETHANOL))
        result = build_compound_records(df, ridx="R", prefix="HMDM")
        assert result["COMPOUND_KEY"].iloc[0] == "Ethanol"

    def test_compound_source_vendor_preferred(self):
        df = _df(_make_row(Vendor="Sigma", database_ID="DB001"))
        result = build_compound_records(df, ridx="R", prefix="HMDM")
        assert result["COMPOUND_SOURCE"].iloc[0] == "Sigma"

    def test_compound_source_falls_back_to_database_id(self):
        df = _df(_make_row(Vendor="", database_ID="DB001"))
        result = build_compound_records(df, ridx="R", prefix="HMDM")
        assert result["COMPOUND_SOURCE"].iloc[0] == "DB001"

    def test_compound_source_empty_when_both_missing(self):
        df = _df(_make_row(Vendor="", database_ID=""))
        result = build_compound_records(df, ridx="R", prefix="HMDM")
        assert result["COMPOUND_SOURCE"].iloc[0] == ""

    def test_private_smiles_and_mol_columns_present(self):
        df = _df(_make_row(SMILES=ETHANOL))
        result = build_compound_records(df, ridx="R", prefix="HMDM")
        assert "_smiles" in result.columns
        assert "_mol" in result.columns
        assert result["_smiles"].iloc[0] == ETHANOL
        assert result["_mol"].iloc[0] is not None

    def test_all_invalid_smiles_returns_empty_dataframe(self):
        df = _df(_make_row(SMILES=INVALID), _make_row(SMILES="???"))
        result = build_compound_records(df, ridx="R", prefix="HMDM")
        assert result.empty


# ---------------------------------------------------------------------------
# validate()
# ---------------------------------------------------------------------------

class TestValidate:
    """
    validate() operates on the *output* of build_compound_records,
    so CIDX and RIDX are already set; only the mandatory-field check matters.
    """

    def _record_row(self, **kwargs) -> dict:
        base = {
            "CIDX":            "HMDM01",
            "RIDX":            "TestRef",
            "COMPOUND_KEY":    "EtOH",
            "COMPOUND_NAME":   "Ethanol",
            "COMPOUND_SOURCE": "Sigma",
            "_smiles":         ETHANOL,
            "_mol":            Chem.MolFromSmiles(ETHANOL),
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
        cidx = row["CIDX"] if field != "CIDX" else ""
        expected_label = f"Row 1 (CIDX={cidx})"
        assert any(
            e.startswith(expected_label) and f"mandatory field '{field}' is empty." in e
            for e in errors
        ), f"Expected error for field '{field}' not found in: {errors}"

    def test_missing_cidx_label_shows_empty_cidx(self):
        df = _df(self._record_row(CIDX=""))
        errors = validate(df)
        assert "Row 1 (CIDX=): mandatory field 'CIDX' is empty." in errors

    def test_missing_compound_name_exact_message(self):
        df = _df(self._record_row(COMPOUND_NAME=""))
        errors = validate(df)
        assert "Row 1 (CIDX=HMDM01): mandatory field 'COMPOUND_NAME' is empty." in errors

    def test_multiple_rows_errors_attributed_correctly(self):
        row1 = self._record_row(CIDX="HMDM01", COMPOUND_NAME="")
        row2 = self._record_row(CIDX="HMDM02", COMPOUND_KEY="")
        df = _df(row1, row2)
        errors = validate(df)
        assert "Row 1 (CIDX=HMDM01): mandatory field 'COMPOUND_NAME' is empty." in errors
        assert "Row 2 (CIDX=HMDM02): mandatory field 'COMPOUND_KEY' is empty." in errors
        assert "Row 2 (CIDX=HMDM02): mandatory field 'COMPOUND_NAME' is empty." not in errors

    def test_empty_dataframe_no_errors(self):
        df = pd.DataFrame(columns=list(self._record_row().keys()))
        assert validate(df) == []


# ---------------------------------------------------------------------------
# write_compound_ctab_sdf()
# ---------------------------------------------------------------------------

class TestWriteCompoundCtabSdf:

    def _build_records(self, smiles_list: list[tuple[str, str, str]]) -> pd.DataFrame:
        """Build a minimal record_df from (cidx, name, smiles) tuples."""
        rows = []
        for cidx, name, smi in smiles_list:
            mol = Chem.MolFromSmiles(smi)
            rows.append({"CIDX": cidx, "COMPOUND_NAME": name, "_mol": mol})
        return pd.DataFrame(rows)

    def test_sdf_file_is_created(self, tmp_path):
        records = self._build_records([("HMDM01", "Ethanol", ETHANOL)])
        out = tmp_path / "COMPOUND_CTAB.sdf"
        write_compound_ctab_sdf(records, out)
        assert out.exists()

    def test_sdf_contains_correct_molecule_count(self, tmp_path):
        records = self._build_records([
            ("HMDM01", "Ethanol", ETHANOL),
            ("HMDM02", "Aspirin", ASPIRIN),
        ])
        out = tmp_path / "COMPOUND_CTAB.sdf"
        write_compound_ctab_sdf(records, out)
        suppl = list(Chem.SDMolSupplier(str(out)))
        assert len(suppl) == 2

    def test_cidx_property_written_to_sdf(self, tmp_path):
        records = self._build_records([("HMDM01", "Ethanol", ETHANOL)])
        out = tmp_path / "COMPOUND_CTAB.sdf"
        write_compound_ctab_sdf(records, out)
        mol = next(Chem.SDMolSupplier(str(out)))
        assert mol.GetProp("CIDX") == "HMDM01"

    def test_molecule_name_written_to_sdf(self, tmp_path):
        records = self._build_records([("HMDM01", "Ethanol", ETHANOL)])
        out = tmp_path / "COMPOUND_CTAB.sdf"
        write_compound_ctab_sdf(records, out)
        mol = next(Chem.SDMolSupplier(str(out)))
        assert mol.GetProp("_Name") == "Ethanol"

    def test_output_dir_created_if_missing(self, tmp_path):
        records = self._build_records([("HMDM01", "Ethanol", ETHANOL)])
        nested = tmp_path / "new_dir" / "COMPOUND_CTAB.sdf"
        write_compound_ctab_sdf(records, nested)
        assert nested.exists()

    def test_molecules_have_2d_coordinates(self, tmp_path):
        records = self._build_records([("HMDM01", "Ethanol", ETHANOL)])
        out = tmp_path / "COMPOUND_CTAB.sdf"
        write_compound_ctab_sdf(records, out)
        mol = next(Chem.SDMolSupplier(str(out), removeHs=False))
        assert mol.GetNumConformers() > 0

    def test_cidx_per_molecule_correct_when_multiple(self, tmp_path):
        records = self._build_records([
            ("HMDM01", "Ethanol", ETHANOL),
            ("HMDM02", "Aspirin", ASPIRIN),
            ("HMDM03", "Caffeine", CAFFEINE),
        ])
        out = tmp_path / "COMPOUND_CTAB.sdf"
        write_compound_ctab_sdf(records, out)
        mols = list(Chem.SDMolSupplier(str(out)))
        cidxs = [m.GetProp("CIDX") for m in mols]
        assert cidxs == ["HMDM01", "HMDM02", "HMDM03"]


# ---------------------------------------------------------------------------
# read_chemicals_sheet()  — mock-based, no ODS file required
# ---------------------------------------------------------------------------

class TestReadChemicalsSheet:

    def _make_raw_ods(self, data_row: dict) -> pd.DataFrame:
        col_names = list(data_row.keys())
        n_cols = len(col_names)
        filler = [None] * n_cols
        rows = [
            filler,
            col_names,        # row 1 → column headers
            filler,
            filler,
            list(data_row.values()),  # row 4 → first data row
        ]
        return pd.DataFrame(rows)

    def _call(self, data_row: dict) -> pd.DataFrame:
        raw = self._make_raw_ods(data_row)
        with patch("chemicals.pd.read_excel", return_value=raw):
            return read_chemicals_sheet(Path("dummy.ods"))

    def test_returns_dataframe(self):
        result = self._call(_make_row())
        assert isinstance(result, pd.DataFrame)

    def test_column_names_from_row1(self):
        result = self._call(_make_row())
        assert "SMILES" in result.columns
        assert "Common_Name" in result.columns

    def test_data_starts_at_row4(self):
        result = self._call(_make_row(SMILES=ETHANOL))
        assert result["SMILES"].iloc[0] == ETHANOL

    def test_nan_string_replaced_with_empty(self):
        result = self._call(_make_row(Vendor="nan"))
        assert result["Vendor"].iloc[0] == ""

    def test_whitespace_stripped(self):
        result = self._call(_make_row(Common_Name="  Ethanol  "))
        assert result["Common_Name"].iloc[0] == "Ethanol"

    def test_all_nan_rows_dropped(self):
        col_names = list(_make_row().keys())
        n_cols = len(col_names)
        filler = [None] * n_cols
        rows = [
            filler,
            col_names,
            filler,
            filler,
            list(_make_row().values()),
            filler,   # trailing all-NaN row — must be dropped
        ]
        raw = pd.DataFrame(rows)
        with patch("chemicals.pd.read_excel", return_value=raw):
            result = read_chemicals_sheet(Path("dummy.ods"))
        assert len(result) == 1
