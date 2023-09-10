from typing import List, Tuple
from datetime import datetime
from itertools import takewhile


class Pricelist_Separator_Middleware:
    def __init__(self, print_runtime: bool = True):
        self.print_runtime = print_runtime

    def filter_for_lowest_value_keys(self, dct: dict):
        if dct:
            filter_value = dct[min(dct, key=dct.get)]
            for key in dct: 
                if dct[key] == filter_value:
                    yield key

    def separate_list_into_spaces(
        self,
        skus: List[str],
        pricelist_spaces: List[Tuple[str, int]]
    ):
        start = datetime.now()

        total_pricelist_spaces = sum([tup[1] for tup in pricelist_spaces])
        num_skus = len(skus)

        if total_pricelist_spaces < num_skus:
            print(f"not enough strings to contain them all at once total skus: {num_skus} total pricelist spaces: {total_pricelist_spaces}")

            i, steamid_sku_lists = 0, {tup[0]:[] for tup in pricelist_spaces}
            for steamid, pricelist_space in pricelist_spaces:
                steamid_sku_lists[steamid].append(skus[i:pricelist_space])
                i += pricelist_space

            return steamid_sku_lists
        
        steamid_sku_lists = {tup[0]:[] for tup in pricelist_spaces}
        sku_spots_granted = {sku: 0 for sku in skus}
        for steamid, pricelist_space in pricelist_spaces:
            set_pricelist_space = pricelist_space
            local_sku_spots_granted = sku_spots_granted.copy()
            

            while pricelist_space > 0 and len(skus) != len(steamid_sku_lists[steamid]): # safety margin 
                newly_added_skus = []
                
                for sku in takewhile(
                    lambda x: pricelist_space > 0,
                    self.filter_for_lowest_value_keys(local_sku_spots_granted)
                ):
                    sku_spots_granted[sku] += 1
                    pricelist_space -= 1

                    steamid_sku_lists[steamid].append(sku)
                    newly_added_skus.append(sku)

                for sku in newly_added_skus: local_sku_spots_granted.pop(sku, None)


            print(f"pricelist for {steamid} had {len(steamid_sku_lists[steamid])} skus assigned, having a set max space of {set_pricelist_space}")

        if self.print_runtime: print(f"Runtime: {datetime.now()-start}")
        return steamid_sku_lists