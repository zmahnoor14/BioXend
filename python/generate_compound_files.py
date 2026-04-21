#!/usr/bin/env python3
"""
Process a CSV of SMILES → lookup ChEMBL metadata → create submission-ready compound files.
Author = Mahnoor Zulfiqar, James Blackshaw
Input CSV must contain:
SMILES,Names,Study_ID
"""

from rdkit import Chem
import argparse
import pandas as pd
from rdkit.Chem import PandasTools
import os
from rdkit import RDConfig
import itertools
import requests

def extract_smiles(mol_record):
    """Extract canonical SMILES from ChEMBL JSON."""
    mol_structures = mol_record.get('molecule_structures', {})
    return mol_structures.get('canonical_smiles', None)

def query_chembl(smiles_list, batch_size = 100):
    """Query ChEMBL for many canonical SMILES at once."""
    url_stem = "https://www.ebi.ac.uk"
    cols = ",".join(["molecule_chembl_id", "pref_name", "molecule_structures"])
    all_results = []
    # Split SMILES into batches:
    for i in range(0, len(smiles_list), batch_size):
        batch = smiles_list[i:i + batch_size]
        smiles_str = ",".join(batch)

        url_string = (
            f"{url_stem}/chembl/api/data/molecule?"
            f"molecule_structures__canonical_smiles__in={smiles_str}&"
            f"only={cols}&format=json&limit=1000"
        )

        print(f"[INFO] Querying ChEMBL batch {i//batch_size+1} / "
        f"{(len(smiles_list)-1)//batch_size+1}")
        url = requests.get( url_string ).json()
        #This is a list of molecules found in ChEMBL for that list
        results = url['molecules']

        while url["page_meta"]["next"]:
            url = requests.get(url_stem + url["page_meta"]["next"]).json()
            requests.extend(url["molecules"])
        all_results.extend(results)
    
    df = pd.DataFrame(all_results)
    df["canonical_smiles"] = df.apply(extract_smiles, axis = 1)
    return df

def generate_compound_files(input_csv, prefix, ridx):
    df = pd.read_csv(input_csv, sep = ",")
    # ChEMBL lookup
    smiles_list = df["SMILES"].tolist()
    chembl_df = query_chembl(smiles_list)
    smiles_not_chembl = chembl_df[chembl_df["molecule_chembl_id"].isna()]["canonical_smiles"]
    if len(smiles_not_chembl) == 0:
        print("all SMILES pass ChEMBL check")
    elif len(smiles_not_chembl) > 0:
        print("SMILES NOT in ChEMBL!")
        print(smiles_not_chembl)

    df['ROMol'] = df['SMILES'].apply(lambda x: Chem.MolFromSmiles(x))
    ridx = ", ".join(itertools.repeat(ridx, len(df))).split(', ')
    data_list = list(range(1,len(df)+1))
    num_to_use = len(str(len(df))) + 1
    CIDX = [prefix + str(item).zfill(num_to_use) for item in data_list]
    df["CIDX"] = CIDX
    df["RIDX"] = ridx
    df["COMPOUND_NAME"] = df["Names"]
    if "Study_ID" not in df.columns:
        df["COMPOUND_KEY"] = df["Names"]
    PandasTools.WriteSDF(df, "COMPOUND_CTAB.sdf", properties=['CIDX'])

    frame_record = df[["CIDX", "RIDX", "COMPOUND_NAME", "COMPOUND_KEY"]]
    frame_record.to_csv("COMPOUND_RECORD.tsv", sep ="\t", index=False)

    print("[SUCCESS] COMPOUND_CTAB.sdf and COMPOUND_RECORD.tsv Files written")

    return frame_record, chembl_df



# --------------------------
# Argument parser
# --------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate ChEMBL submission compound files")
    
    parser.add_argument("--input_csv", required=True, help="Input compound csv")
    parser.add_argument("--prefix", required=True, help="Prefix for CIDX IDs")
    parser.add_argument("--ridx", required=True, help="RIDX study identifier")

args = parser.parse_args()
generate_compound_files(
    args.input_csv,
    args.prefix,
    args.ridx
)
