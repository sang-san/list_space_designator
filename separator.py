from typing import List, Tuple
from datetime import datetime
from itertools import takewhile


class List_Separator_Middleware:
    def __init__(self, print_runtime: bool = True, print_lenghts: bool = False):
        self.print_runtime = print_runtime
        self.print_lenghts = print_lenghts

    def filter_for_lowest_value_keys(self, dct: dict):
        if dct:
            filter_value = dct[min(dct, key=dct.get)]
            for key in dct: 
                if dct[key] == filter_value:
                    yield key

    def separate_list_into_spaces(
        self,
        data_values: List[str],
        spaces: List[Tuple[str, int]]
    ):
        start = datetime.now()

        total_spaces = sum([tup[1] for tup in spaces])
        num_data_values = len(data_values)

        if total_spaces < num_data_values:
            print(f"not enough strings to contain them all at once total data_values: {num_data_values} total pricelist spaces: {total_spaces}")

            i, list_name_data_value_lists = 0, {tup[0]:[] for tup in spaces}
            for list_name, space in spaces:
                end = i + space
                list_name_data_value_lists[list_name].append(data_values[i:end])
                i += space

            return list_name_data_value_lists
        
        list_name_data_value_lists = {tup[0]:[] for tup in spaces}
        data_value_spots_granted = {data_value: 0 for data_value in data_values}
        for list_name, space in spaces:
            set_space = space
            local_data_value_spots_granted = data_value_spots_granted.copy()
            

            while space > 0 and len(data_values) != len(list_name_data_value_lists[list_name]): # safety margin 
                newly_added_data_values = []
                
                for data_value in takewhile(
                    lambda x: space > 0,
                    self.filter_for_lowest_value_keys(local_data_value_spots_granted)
                ):
                    data_value_spots_granted[data_value] += 1
                    space -= 1

                    list_name_data_value_lists[list_name].append(data_value)
                    newly_added_data_values.append(data_value)

                for data_value in newly_added_data_values: local_data_value_spots_granted.pop(data_value, None)

            if self.print_lenghts: print(f"list for {list_name} had {len(list_name_data_value_lists[list_name])} data_values assigned, having a set max space of {set_space}")

        if self.print_runtime: print(f"Runtime: {datetime.now()-start}")
        return list_name_data_value_lists
