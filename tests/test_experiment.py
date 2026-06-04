"""
Tests for bin/experiment.py

# ---------------------------------------------------------------------------
# How to run
# ---------------------------------------------------------------------------

Run all tests (basic output):
conda run -n rdkit_env pytest tests/test_experiment.py -v

See the actual error message values when a test fails:
conda run -n rdkit_env pytest tests/test_experiment.py -v --tb=short

Run only the validate tests to focus on error messages:
conda run -n rdkit_env pytest tests/test_experiment.py::TestValidate -v

Run a single specific test:
conda run -n rdkit_env pytest tests/test_experiment.py::TestBuildAssayParam::test_temperature_coerced_to_integer -v

See what error messages validate() actually produces right now (useful for debugging):

conda run -n rdkit_env python -c "
import sys; sys.path.insert(0, 'bin')
from experiment import build_assay_param, validate
import pandas as pd

exp_df = pd.DataFrame([{
    'identifier': 'assay1',
    'Incubation temperature in celsius': '37',
    'Oxygen conditions': 'anaerobic',
    'Time-course information (i.e., number of timepoints)': '0,6,24',
    'Time_unit': 'h',
    'DOSE': '',
    'DOSE_unit': '',
    'Biomass/inoculum density at the start': '',
    'Biomass/inoculum density at the end': '',
    'Pre-culture preparation and conditions': '',
    'Sample preparation': '',
    'Media composition': '',
    'Shaking speed': '',
    'Negative controls': '',
    'Antibiotic pre-treatment': '',
    'Sample storage': '',
}])
param_df = build_assay_param(exp_df, aidx_list=['assay1'])
for e in validate(param_df, expected_aidx=['assay1']):
    print(e)
print(param_df.to_string())
"
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))
from experiment import (
    ASSAY_PARAM_COLS,
    MANDATORY_PARAM_FIELDS,
    VALID_PARAM_TYPES,
    _apply_aidx_mapping,
    _build_aidx_map,
    _clean,
    _extract_aidx_from_experiment,
    _extract_aidx_from_mapping,
    _get_experiment_for_assay,
    _make_row,
    build_assay_param,
    validate,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_exp_row(**kwargs) -> dict:
    """Minimal Experiment sheet row with all columns present; override via kwargs."""
    base = {
        "identifier":                                           "assay1",
        "Pre-culture preparation and conditions":               "",
        "Sample preparation":                                   "",
        "Incubation temperature in celsius":                    "37",
        "Time-course information (i.e., number of timepoints)": "0,6,24",
        "Time_unit":                                            "h",
        "Oxygen conditions":                                    "anaerobic",
        "Media composition":                                    "",
        "Shaking speed":                                        "",
        "Negative controls":                                    "",
        "Antibiotic pre-treatment":                             "",
        "Sample storage":                                       "",
        "Biomass/inoculum density at the start":                "",
        "Biomass/inoculum density at the end":                  "",
        "DOSE":                                                 "",
        "DOSE_unit":                                            "",
    }
    base.update(kwargs)
    return base


def _param_row(**kwargs) -> dict:
    """Minimal valid ASSAY_PARAM record row; override via kwargs."""
    base = {
        "AIDX":       "Zimmermann_Ecoli_Biotransformation",
        "TYPE":       "CONDITION",
        "RELATION":   "",
        "VALUE":      "",
        "UNITS":      "",
        "TEXT_VALUE": "anaerobic",
        "COMMENTS":   "",
    }
    base.update(kwargs)
    return base


def _df(*rows) -> pd.DataFrame:
    return pd.DataFrame(list(rows))


AIDX_MAP = {"assay1": "Zimmermann_Ecoli_Biotransformation",
             "assay2": "Zimmermann_Bacteroides_Biotransformation"}


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
        assert _clean("  anaerobic  ") == "anaerobic"

    def test_non_nan_number_converted_to_string(self):
        assert _clean(37) == "37"

    def test_empty_string_stays_empty(self):
        assert _clean("") == ""


# ---------------------------------------------------------------------------
# _make_row()
# ---------------------------------------------------------------------------

class TestMakeParamRow:

    def test_required_fields_set(self):
        row = _make_row("assay1", "CONDITION")
        assert row["AIDX"] == "assay1"
        assert row["TYPE"] == "CONDITION"

    def test_defaults_are_empty_strings(self):
        row = _make_row("assay1", "CONDITION")
        for field in ("RELATION", "VALUE", "UNITS", "TEXT_VALUE", "COMMENTS"):
            assert row[field] == ""

    def test_all_fields_passable(self):
        row = _make_row("A1", "TEMPERATURE", relation="=", value="37",
                        units="celsius", text_value="", comments="note")
        assert row["VALUE"] == "37"
        assert row["UNITS"] == "celsius"
        assert row["COMMENTS"] == "note"

    def test_keys_match_assay_param_cols(self):
        row = _make_row("A1", "CONDITION")
        assert set(row.keys()) == set(ASSAY_PARAM_COLS)


# ---------------------------------------------------------------------------
# _get_experiment_for_assay()
# ---------------------------------------------------------------------------

class TestGetExperimentForAssay:

    def test_identifier_all_matches_any_aidx(self):
        exp_df = _df(_make_exp_row(identifier="all"))
        assert _get_experiment_for_assay(exp_df, "anything") is not None

    def test_identifier_all_case_insensitive(self):
        exp_df = _df(_make_exp_row(identifier="ALL"))
        assert _get_experiment_for_assay(exp_df, "x") is not None

    def test_identifier_most_matches_any_aidx(self):
        exp_df = _df(_make_exp_row(identifier="most"))
        assert _get_experiment_for_assay(exp_df, "assay1") is not None

    def test_identifier_most_case_insensitive(self):
        exp_df = _df(_make_exp_row(identifier="MOST"))
        assert _get_experiment_for_assay(exp_df, "assay1") is not None

    def test_specific_aidx_matches(self):
        exp_df = _df(_make_exp_row(identifier="assay1"))
        assert _get_experiment_for_assay(exp_df, "assay1") is not None

    def test_specific_aidx_does_not_match_other(self):
        exp_df = _df(_make_exp_row(identifier="assay1"))
        assert _get_experiment_for_assay(exp_df, "assay2") is None

    def test_comma_separated_list_matches_member(self):
        exp_df = _df(_make_exp_row(identifier="assay1, assay2, assay3"))
        assert _get_experiment_for_assay(exp_df, "assay2") is not None

    def test_comma_separated_list_non_member_returns_none(self):
        exp_df = _df(_make_exp_row(identifier="assay1,assay2"))
        assert _get_experiment_for_assay(exp_df, "assay3") is None

    def test_empty_identifier_skipped(self):
        exp_df = _df(_make_exp_row(identifier=""))
        assert _get_experiment_for_assay(exp_df, "assay1") is None

    def test_empty_dataframe_returns_none(self):
        exp_df = pd.DataFrame(columns=list(_make_exp_row().keys()))
        assert _get_experiment_for_assay(exp_df, "assay1") is None


# ---------------------------------------------------------------------------
# _extract_aidx_from_experiment()
# ---------------------------------------------------------------------------

class TestExtractAidxFromExperiment:

    def test_specific_identifier_included(self):
        exp_df = _df(_make_exp_row(identifier="assay1"))
        assert _extract_aidx_from_experiment(exp_df) == ["assay1"]

    def test_all_rows_skipped(self):
        exp_df = _df(_make_exp_row(identifier="all"))
        assert _extract_aidx_from_experiment(exp_df) == []

    def test_most_rows_skipped(self):
        exp_df = _df(_make_exp_row(identifier="most"))
        assert _extract_aidx_from_experiment(exp_df) == []

    def test_comma_separated_expanded(self):
        exp_df = _df(_make_exp_row(identifier="assay1, assay2"))
        result = _extract_aidx_from_experiment(exp_df)
        assert result == ["assay1", "assay2"]

    def test_duplicates_removed(self):
        exp_df = _df(
            _make_exp_row(identifier="assay1"),
            _make_exp_row(identifier="assay1"),
        )
        assert _extract_aidx_from_experiment(exp_df) == ["assay1"]

    def test_order_preserved(self):
        exp_df = _df(
            _make_exp_row(identifier="assay2"),
            _make_exp_row(identifier="assay1"),
        )
        assert _extract_aidx_from_experiment(exp_df) == ["assay2", "assay1"]

    def test_empty_rows_skipped(self):
        exp_df = _df(_make_exp_row(identifier=""))
        assert _extract_aidx_from_experiment(exp_df) == []

    def test_mixed_all_and_specific(self):
        exp_df = _df(
            _make_exp_row(identifier="all"),
            _make_exp_row(identifier="assay1"),
        )
        assert _extract_aidx_from_experiment(exp_df) == ["assay1"]


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
        tsv.write_text("assay_identifier\tAIDX\nassay1\tA1\n\tA2\nassay3\t\n")
        result = _build_aidx_map(tsv)
        assert result == {"assay1": "A1"}

    def test_multiple_entries_all_loaded(self, tmp_path):
        tsv = tmp_path / "ASSAY_MAPPING.tsv"
        tsv.write_text("assay_identifier\tAIDX\nassay1\tA1\nassay2\tA2\n")
        result = _build_aidx_map(tsv)
        assert len(result) == 2


# ---------------------------------------------------------------------------
# _extract_aidx_from_mapping()
# ---------------------------------------------------------------------------

class TestExtractAidxFromMapping:

    def test_none_path_returns_empty_list(self):
        assert _extract_aidx_from_mapping(None) == []

    def test_nonexistent_path_returns_empty_list(self):
        assert _extract_aidx_from_mapping(Path("/no/such/file.tsv")) == []

    def test_valid_tsv_returns_ordered_keys(self, tmp_path):
        tsv = tmp_path / "ASSAY_MAPPING.tsv"
        tsv.write_text("assay_identifier\tAIDX\nassay1\tA1\nassay2\tA2\n")
        result = _extract_aidx_from_mapping(tsv)
        assert result == ["assay1", "assay2"]

    def test_duplicates_removed_order_preserved(self, tmp_path):
        tsv = tmp_path / "ASSAY_MAPPING.tsv"
        tsv.write_text("assay_identifier\tAIDX\nassay1\tA1\nassay1\tA1\n")
        result = _extract_aidx_from_mapping(tsv)
        assert result == ["assay1"]

    def test_empty_keys_skipped(self, tmp_path):
        tsv = tmp_path / "ASSAY_MAPPING.tsv"
        tsv.write_text("assay_identifier\tAIDX\nassay1\tA1\n\tA2\n")
        result = _extract_aidx_from_mapping(tsv)
        assert result == ["assay1"]


# ---------------------------------------------------------------------------
# _apply_aidx_mapping()
# ---------------------------------------------------------------------------

class TestApplyAidxMapping:

    def test_empty_map_returns_unchanged(self):
        df = _df(_param_row(AIDX="assay1"))
        result = _apply_aidx_mapping(df, {})
        assert result["AIDX"].iloc[0] == "assay1"

    def test_empty_dataframe_returned_unchanged(self):
        df = pd.DataFrame(columns=ASSAY_PARAM_COLS)
        result = _apply_aidx_mapping(df, AIDX_MAP)
        assert result.empty

    def test_known_key_replaced_with_generated_aidx(self):
        df = _df(_param_row(AIDX="assay1"))
        result = _apply_aidx_mapping(df, AIDX_MAP)
        assert result["AIDX"].iloc[0] == "Zimmermann_Ecoli_Biotransformation"

    def test_unknown_key_kept_as_is_with_warning(self, capsys):
        df = _df(_param_row(AIDX="unknown_assay"))
        result = _apply_aidx_mapping(df, AIDX_MAP)
        assert result["AIDX"].iloc[0] == "unknown_assay"
        assert "No AIDX mapping for 'unknown_assay'" in capsys.readouterr().err

    def test_mixed_known_and_unknown_rows(self):
        df = _df(_param_row(AIDX="assay1"), _param_row(AIDX="assay2"))
        result = _apply_aidx_mapping(df, AIDX_MAP)
        assert result["AIDX"].iloc[0] == "Zimmermann_Ecoli_Biotransformation"
        assert result["AIDX"].iloc[1] == "Zimmermann_Bacteroides_Biotransformation"

    def test_original_dataframe_not_mutated(self):
        df = _df(_param_row(AIDX="assay1"))
        _apply_aidx_mapping(df, AIDX_MAP)
        assert df["AIDX"].iloc[0] == "assay1"


# ---------------------------------------------------------------------------
# build_assay_param()
# ---------------------------------------------------------------------------

class TestBuildAssayParam:

    def test_output_has_assay_param_cols(self):
        exp_df = _df(_make_exp_row())
        result = build_assay_param(exp_df, ["assay1"])
        assert list(result.columns) == ASSAY_PARAM_COLS

    def test_temperature_emitted_as_numeric(self):
        exp_df = _df(_make_exp_row(
            **{"Incubation temperature in celsius": "37"}
        ))
        result = build_assay_param(exp_df, ["assay1"])
        temp_rows = result[result["TYPE"] == "TEMPERATURE"]
        assert len(temp_rows) == 1
        assert temp_rows["VALUE"].iloc[0] == "37"
        assert temp_rows["RELATION"].iloc[0] == "="
        assert temp_rows["UNITS"].iloc[0] == "celsius"

    def test_temperature_float_coerced_to_integer(self):
        exp_df = _df(_make_exp_row(
            **{"Incubation temperature in celsius": "37.0"}
        ))
        result = build_assay_param(exp_df, ["assay1"])
        temp_rows = result[result["TYPE"] == "TEMPERATURE"]
        assert temp_rows["VALUE"].iloc[0] == "37"

    def test_timepoint_combines_values_and_unit(self):
        exp_df = _df(_make_exp_row(
            **{
                "Time-course information (i.e., number of timepoints)": "0,6,24",
                "Time_unit": "h",
            }
        ))
        result = build_assay_param(exp_df, ["assay1"])
        tp_rows = result[result["TYPE"] == "TIMEPOINT"]
        assert len(tp_rows) == 1
        assert tp_rows["TEXT_VALUE"].iloc[0] == "0,6,24 h"

    def test_timepoint_without_unit(self):
        exp_df = _df(_make_exp_row(
            **{
                "Time-course information (i.e., number of timepoints)": "0,6,24",
                "Time_unit": "",
            }
        ))
        result = build_assay_param(exp_df, ["assay1"])
        tp_rows = result[result["TYPE"] == "TIMEPOINT"]
        assert tp_rows["TEXT_VALUE"].iloc[0] == "0,6,24"

    def test_oxygen_condition_emitted_as_text(self):
        exp_df = _df(_make_exp_row(**{"Oxygen conditions": "anaerobic"}))
        result = build_assay_param(exp_df, ["assay1"])
        cond_rows = result[result["TYPE"] == "CONDITION"]
        assert len(cond_rows) == 1
        assert cond_rows["TEXT_VALUE"].iloc[0] == "anaerobic"

    def test_biomass_start_only(self):
        exp_df = _df(_make_exp_row(
            **{"Biomass/inoculum density at the start": "1e8 CFU/mL"}
        ))
        result = build_assay_param(exp_df, ["assay1"])
        bio_rows = result[result["TYPE"] == "BIOMASS"]
        assert len(bio_rows) == 1
        assert bio_rows["TEXT_VALUE"].iloc[0] == "1e8 CFU/mL"
        assert bio_rows["COMMENTS"].iloc[0] == ""

    def test_biomass_end_only(self):
        exp_df = _df(_make_exp_row(
            **{"Biomass/inoculum density at the end": "2e8 CFU/mL"}
        ))
        result = build_assay_param(exp_df, ["assay1"])
        bio_rows = result[result["TYPE"] == "BIOMASS"]
        assert len(bio_rows) == 1
        assert bio_rows["COMMENTS"].iloc[0] == "End: 2e8 CFU/mL"

    def test_biomass_start_and_end(self):
        exp_df = _df(_make_exp_row(
            **{
                "Biomass/inoculum density at the start": "1e8 CFU/mL",
                "Biomass/inoculum density at the end":   "2e8 CFU/mL",
            }
        ))
        result = build_assay_param(exp_df, ["assay1"])
        bio_rows = result[result["TYPE"] == "BIOMASS"]
        assert bio_rows["TEXT_VALUE"].iloc[0] == "1e8 CFU/mL"
        assert bio_rows["COMMENTS"].iloc[0] == "End: 2e8 CFU/mL"

    def test_biomass_not_emitted_when_both_empty(self):
        exp_df = _df(_make_exp_row(
            **{
                "Biomass/inoculum density at the start": "",
                "Biomass/inoculum density at the end":   "",
            }
        ))
        result = build_assay_param(exp_df, ["assay1"])
        assert "BIOMASS" not in result["TYPE"].values

    def test_dose_emitted_with_relation_and_units(self):
        exp_df = _df(_make_exp_row(DOSE="100", DOSE_unit="µM"))
        result = build_assay_param(exp_df, ["assay1"])
        dose_rows = result[result["TYPE"] == "DOSE"]
        assert len(dose_rows) == 1
        assert dose_rows["VALUE"].iloc[0] == "100"
        assert dose_rows["RELATION"].iloc[0] == "="
        assert dose_rows["UNITS"].iloc[0] == "µM"

    def test_dose_not_emitted_when_empty(self):
        exp_df = _df(_make_exp_row(DOSE="", DOSE_unit=""))
        result = build_assay_param(exp_df, ["assay1"])
        assert "DOSE" not in result["TYPE"].values

    def test_empty_text_fields_not_emitted(self):
        exp_df = _df(_make_exp_row(**{"Sample preparation": ""}))
        result = build_assay_param(exp_df, ["assay1"])
        assert "SAMPLE PREPARATION" not in result["TYPE"].values

    def test_all_identifier_applies_to_all_aidxs(self):
        exp_df = _df(_make_exp_row(identifier="all", **{"Oxygen conditions": "aerobic"}))
        result = build_assay_param(exp_df, ["assay1", "assay2"])
        cond_rows = result[result["TYPE"] == "CONDITION"]
        assert set(cond_rows["AIDX"]) == {"assay1", "assay2"}

    def test_aidx_not_in_experiment_skipped_with_warning(self, capsys):
        exp_df = _df(_make_exp_row(identifier="assay1"))
        result = build_assay_param(exp_df, ["assay1", "missing_assay"])
        assert "missing_assay" not in result["AIDX"].values
        assert "No Experiment row found for AIDX 'missing_assay'" in capsys.readouterr().err

    def test_multiple_aidxs_all_get_rows(self):
        exp_df = _df(_make_exp_row(identifier="all", **{"Oxygen conditions": "anaerobic"}))
        result = build_assay_param(exp_df, ["assay1", "assay2"])
        assert set(result["AIDX"]) == {"assay1", "assay2"}

    def test_empty_aidx_list_returns_empty_dataframe(self):
        exp_df = _df(_make_exp_row())
        result = build_assay_param(exp_df, [])
        assert list(result.columns) == ASSAY_PARAM_COLS
        assert len(result) == 0


# ---------------------------------------------------------------------------
# validate()
# ---------------------------------------------------------------------------

class TestValidate:
    """Each test pins the exact error message text produced by validate()."""

    def _label(self, row: dict) -> str:
        return f"Row 1 (AIDX={row['AIDX']}, TYPE={row['TYPE']})"

    def test_valid_record_no_errors(self):
        df = _df(_param_row())
        assert validate(df, []) == []

    @pytest.mark.parametrize("field", MANDATORY_PARAM_FIELDS)
    def test_each_mandatory_field_exact_message(self, field):
        row = _param_row(**{field: ""})
        df = _df(row)
        errors = validate(df, [])
        aidx = row["AIDX"]
        type_ = row["TYPE"]
        label = f"Row 1 (AIDX={aidx}, TYPE={type_})"
        assert any(
            e.startswith(label) and f"mandatory field '{field}' is empty." in e
            for e in errors
        ), f"Expected mandatory-field error for '{field}' not found in: {errors}"

    def test_invalid_type_message(self):
        row = _param_row(TYPE="INVALID_TYPE")
        df = _df(row)
        errors = validate(df, [])
        label = self._label(row)
        assert any(
            e.startswith(label) and "TYPE 'INVALID_TYPE' not in" in e
            for e in errors
        )

    @pytest.mark.parametrize("valid_type", list(VALID_PARAM_TYPES))
    def test_all_valid_types_produce_no_type_error(self, valid_type):
        row = _param_row(TYPE=valid_type)
        if valid_type in ("TEMPERATURE", "DOSE"):
            row.update({"VALUE": "37", "RELATION": "=", "UNITS": "celsius", "TEXT_VALUE": ""})
        df = _df(row)
        errors = validate(df, [])
        assert not any("not in" in e and "TYPE" in e for e in errors)

    def test_value_without_relation_exact_message(self):
        row = _param_row(TYPE="TEMPERATURE", VALUE="37", RELATION="", UNITS="celsius", TEXT_VALUE="")
        df = _df(row)
        errors = validate(df, [])
        label = self._label(row)
        assert f"{label}: RELATION is required when VALUE is set." in errors

    def test_relation_without_value_exact_message(self):
        row = _param_row(RELATION="=", VALUE="", TEXT_VALUE="some text")
        df = _df(row)
        errors = validate(df, [])
        label = self._label(row)
        assert f"{label}: VALUE is required when RELATION is set." in errors

    def test_temperature_value_without_units_exact_message(self):
        row = _param_row(TYPE="TEMPERATURE", VALUE="37", RELATION="=", UNITS="", TEXT_VALUE="")
        df = _df(row)
        errors = validate(df, [])
        label = self._label(row)
        assert f"{label}: UNITS is required when VALUE is set for TYPE 'TEMPERATURE'." in errors

    def test_dose_value_without_units_exact_message(self):
        row = _param_row(TYPE="DOSE", VALUE="100", RELATION="=", UNITS="", TEXT_VALUE="")
        df = _df(row)
        errors = validate(df, [])
        label = self._label(row)
        assert f"{label}: UNITS is required when VALUE is set for TYPE 'DOSE'." in errors

    def test_non_numeric_type_value_without_units_no_error(self):
        # CONDITION, MEDIA, etc. don't require UNITS even when VALUE is set
        row = _param_row(TYPE="CONDITION", VALUE="x", RELATION="=", UNITS="", TEXT_VALUE="")
        df = _df(row)
        errors = validate(df, [])
        assert not any("UNITS is required" in e for e in errors)

    def test_both_value_and_text_value_empty_exact_message(self):
        row = _param_row(VALUE="", TEXT_VALUE="")
        df = _df(row)
        errors = validate(df, [])
        label = self._label(row)
        assert (
            f"{label}: both VALUE and TEXT_VALUE are empty — "
            "at least one must be non-empty."
        ) in errors

    def test_expected_aidx_missing_from_output_exact_message(self):
        df = _df(_param_row(AIDX="assay1"))
        errors = validate(df, expected_aidx=["assay1", "assay2"])
        assert (
            "AIDX 'assay2': no parameter rows were generated "
            "(check the Experiment sheet identifier column)."
        ) in errors

    def test_expected_aidx_present_no_missing_error(self):
        df = _df(_param_row(AIDX="assay1"))
        errors = validate(df, expected_aidx=["assay1"])
        assert not any("no parameter rows were generated" in e for e in errors)

    def test_empty_expected_aidx_no_missing_error(self):
        df = _df(_param_row())
        assert validate(df, expected_aidx=[]) == []

    def test_multiple_rows_errors_attributed_correctly(self):
        row1 = _param_row(AIDX="A1", TYPE="CONDITION", AIDX_label="A1")
        row2 = _param_row(AIDX="A2", TYPE="TEMPERATURE",
                          VALUE="37", RELATION="=", UNITS="", TEXT_VALUE="")
        row1["AIDX"] = "A1"
        row2["AIDX"] = "A2"
        df = _df(row1, row2)
        errors = validate(df, expected_aidx=[])
        assert "Row 2 (AIDX=A2, TYPE=TEMPERATURE): UNITS is required when VALUE is set for TYPE 'TEMPERATURE'." in errors
        assert "Row 1 (AIDX=A1, TYPE=CONDITION): UNITS is required" not in errors

    def test_empty_dataframe_with_expected_aidx_reports_missing(self):
        df = pd.DataFrame(columns=ASSAY_PARAM_COLS)
        errors = validate(df, expected_aidx=["assay1"])
        assert any("assay1" in e and "no parameter rows" in e for e in errors)

    def test_empty_dataframe_no_expected_aidx_no_errors(self):
        df = pd.DataFrame(columns=ASSAY_PARAM_COLS)
        assert validate(df, expected_aidx=[]) == []
