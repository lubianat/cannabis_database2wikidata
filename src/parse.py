import xmltodict
import re
from pathlib import Path
import tqdm
import json

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data").resolve()
RESULTS = HERE.parent.joinpath("results").resolve()


cdb_compounds = DATA.joinpath("compounds.xml").read_text()

cdb_compounds_list = cdb_compounds.split('<?xml version="1.0" encoding="UTF-8"?>')


cdb_compounds_dict = {}
for entry in tqdm.tqdm(cdb_compounds_list):
    if entry == "":
        continue
    cdb_dict = xmltodict.parse(entry)

    inchikey = cdb_dict["compound"]["inchikey"]
    cdb_id = cdb_dict["compound"]["accession"]
    cdb_compounds_dict[inchikey] = cdb_id

RESULTS.joinpath("compound_dict.json").write_text(
    json.dumps(cdb_compounds_dict, indent=4, sort_keys=True)
)
a = 1
