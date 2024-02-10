import rezensionen
def calc_dif(data_dict, solution=rezensionen.example_sort):
    wrong=0
    total=0
    for key1 in data_dict:
        nested_dict=data_dict[key1]
        for key2 in nested_dict:
            if nested_dict[key2] != {}:
                for key3 in nested_dict[key2]:
                    if solution[key3] != (key1, key2):
                        print(f"{key3}, {key1}, {key2}")
                        wrong+=1
                    total+=1
    return wrong/total