import json

from pathlib import Path

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data").resolve()
RESULTS = HERE.parent.joinpath("results").resolve()


cdb_compounds = json.loads(RESULTS.joinpath("compound_dict.json").read_text())
wikidata_compounds = json.loads(
    RESULTS.joinpath("inchikey_to_wikidata.json").read_text()
)


qs = ""
for inchikey, qid in wikidata_compounds.items():
    cdb_number = cdb_compounds[inchikey].replace("CDB", "")
    qs += f'{qid}|P11160|"{cdb_number}"|S248|Q114598186' + "\n"

RESULTS.joinpath("quickstatements.txt").write_text(qs)
