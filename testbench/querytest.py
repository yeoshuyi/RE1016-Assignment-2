"""
testbench code for query
"""


import re
import itertools


db = {
        'Ananda Kitchen': {"Ali's Kitchen": 'Malay, Spicy'}, 
        'Fine Food @ the South Spine': {"Encik's Kitchen": 'Malay, Spicy, Halal', 'Noodles & Soups': 'Chinese, Western, Soups'}, 
        'Food Court 1': {'Ayam Penyat': 'Malay, Spicy, Halal', 'Kee Chicken Rice': 'Chinese, Chicken, Rice'}, 
        'Food Court 11': {'88 Cai Fan': 'Chinese, Mixed Rice', 'Kimkimbap': 'Korean, Spicy', 'TAF Prata House': 'Indian, Spicy, Halal'}, 
        'Food Court 13': {'13 Ramen Shop': 'Japanese, Halal', 'ABC Western': 'Western, Fries, Burgers, Halal'}, 
        'Food Court 14': {'Burger House': 'Western, Fries, Burgers, Halal', 'Willy Waffles': 'Western, Waffles'}, 
        'Food Court 16': {'16 Kitchen': 'Chinese, Western, Indian, Malay', 'Chicken Rice @ 16': 'Chinese, Chicken, Rice'}, 
        'Food Court 2': {'Tonkatsu House': 'Japanese, Spicy', 'Viet Delights': 'Vietnamese, Spicy'}, 
        'Food Court 9': {'Bangkok Delights': 'Thai, Spicy', "Muthu's Curry House": 'Indian, Spicy, Halal'}, 
        'Foodgle Food Court': {"Hot Mama's Mala Hotpot": 'Chinese, Spicy', 'Koreantown': 'Korean, Spicy'}, 
        'North Hill Food Court': {'Hilly Western': 'Western, Fries, Burgers, Halal', 'Shan Shan Chinese': 'Chinese, Mixed Rice'}, 
        'North Spine': {'CFK': 'Western, Fries, Burgers, Chicken, Halal', "McRonald's": 'Western, Fries, Burgers, Halal'}, 
        'North Spine Food Court': {'Hearty n Healthy': 'Chinese, Western, Salads', "Lee's Kitchen": 'Chinese, Spicy', 'Spicy Mala Hotpot': 'Chinese, Spicy'}, 
        'Pioneer Food Court': {'Ah Wong Desserts': 'Chinese, Western, Desserts', 'Xian Delicacies': 'Chinese, Spicy'}, 
        'Quad Cafe': {'Sichuan Delights': 'Chinese, Spicy', 'Yong Tau Foo': 'Chinese, Halal'}
}

query = [['Spicy'], ['Malay']] #(SPICY & MALAY & HALAL) + (CHINESE & HALAL)

def query_to_dict(db, query):
    results = {}

    for i in range(len(query)):
        temp = []
        for fc, stalls in db.items():
            #print(stalls.items())
            for stall, keyword in stalls.items():
                #print(keyword)
                stall_keyword = keyword.split(', ')
                #print(stall_keyword)
                if all(key in stall_keyword for key in query[i]):
                    #results.update({stall:i})
                    temp.append(tuple([stall,fc]))
        results.update({i:temp})
    #print(results)
    return results

# def find_combinations(results):
#     condition_sets = {i: set(stall) for i, stall in results.items()}
#     index = condition_sets.keys()
    
#     for i in range(1, len(index) + 1):
#         for combo in itertools.combinations(index, i):
#             intersect_sets = [condition_sets[i] for temp in combo]
#             intersect_stalls = set.intersection(*intersect_sets)
#             print(intersect_stalls)

# find_combinations(query_to_dict(db,query))    


def display_dict(results):
    for i in sorted(results.keys()):
        stalls = [f"{stall} ({court})" for stall, court in results[i]]
        stalls_list = "\n".join(stalls)

        print(f"{i} condition: \n{stalls_list}\n\n")

#display_dict(query_to_dict(db,query))