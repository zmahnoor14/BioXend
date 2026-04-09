

import pandas as pd
import pubchempy as pcp
import numpy as np
def isNaN(string):
    return string != string
import os
import glob
import re
import csv 
import time
import json
import sys

#RDKit is a python cheminformatics toolkit
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem import rdFMCS
from rdkit.Chem import PandasTools
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import SDWriter

def smiles2sdf(compound_df = "COMPOUND_RECORD.tsv", output_file = "output_example.sdf"):
    df = pd.read_csv(compound_df, sep = "\t")
    data = df[['CIDX', 'COMPOUND_NAME', "SMILES"]]
    data['ROMol'] = data['SMILES'].apply(lambda x: Chem.MolFromSmiles(x))
    # Write the DataFrame to an SDF file with the SMILES column named 'ROMol'
    PandasTools.WriteSDF(data, output_file, properties=list(data.columns))
    PandasTools.WriteSDF(data, output_file, properties=['CIDX'])
smiles2sdf(compound_df = "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/Immunosuppressants/COMPOUND_RECORD_withSMILES.tsv", output_file = "/g/zimmermann/Members/zulfiqar/ZM000_PistoiaPrj/Immunosuppressants/output_example.sdf")

