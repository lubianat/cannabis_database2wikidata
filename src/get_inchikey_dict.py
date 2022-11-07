import json
from pathlib import Path
from itertools import islice
import tqdm
from wdcuration import query_wikidata
import time

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data").resolve()
RESULTS = HERE.parent.joinpath("results").resolve()


def main():
    cdb_compounds_dict = json.loads(RESULTS.joinpath("compound_dict.json").read_text())

    inchikeys_to_lookup = [a for a in cdb_compounds_dict]

    print(inchikeys_to_lookup)
    wd_results = lookup_multiple_ids(inchikeys_to_lookup, "P235")
    inchikey2wikidata = {}
    for wd_result in wd_results:
        inchikey2wikidata[wd_result["id"]] = wd_result["qid"]
    RESULTS.joinpath("inchikey_to_wikidata.json").write_text(
        json.dumps(inchikey2wikidata, indent=4, sort_keys=True)
    )


def chunk(arr_range, arr_size):
    arr_range = iter(arr_range)
    return iter(lambda: tuple(islice(arr_range, arr_size)), ())


def lookup_multiple_ids(list_of_ids, wikidata_property):

    if len(list_of_ids) > 200:
        list_of_smaller_lists_of_ids = chunk(list_of_ids, 200)
        result_dict_list = []
        for small_list in tqdm.tqdm(list_of_smaller_lists_of_ids):
            current_list_of_dicts = lookup_multiple_ids(small_list, wikidata_property)
            result_dict_list.extend(current_list_of_dicts)
            time.sleep(0.3)

        return result_dict_list

    formatted_ids = '""'.join(list_of_ids)
    query = (
        """
  SELECT  
  (REPLACE(STR(?item), ".*Q", "Q") AS ?qid) 
  ?id 
  WHERE { """
        f'VALUES ?id {{ "{formatted_ids}" }} . '
        f"?item wdt:{wikidata_property} ?id . "
        """
  }
  """
    )
    return query_wikidata(query)


if __name__ == "__main__":
    main()
