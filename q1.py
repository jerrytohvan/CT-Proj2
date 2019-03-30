# Team ID: G4T12
import  itertools
import numpy as np


def store_in_dict(locations):
    dd = {}
    for loc in locations:
        lst = loc.split(",")
        if lst[0] not in dd :
            dd[lst[0]] = {lst[1]: lst[2]}
        else:
            start = lst[0]
            dest = lst[1]
            val = int(lst[2])
            dd[start][dest] = val
    return dd


def firstGreedyShortestPath(dict_loc, start_location, all_cities, k):
    #all_cities: ['RUS', 'CAN', 'SIN', 'KOR', 'CHN', 'MEX', 'AUS', 'GMY', 'FRN', 'SPN']
    #k: length of orders 
    selected_order_ids = []

    curr = start_location
    while len(selected_order_ids) != k:
        #least dist 
        mini = 99999999
        low_k = ''
        index=0
        for j in range(0, len(all_cities)):
            city = all_cities[j]
            if j not in selected_order_ids and curr != all_cities[j] and mini > dict_loc[curr][city]:
                mini = dict_loc[curr][city]
                low_k = city
                index = j
        selected_order_ids.append(index)
        curr = low_k
    return tuple(selected_order_ids)

def returnOrders(list_orders, orders):
    return [orders[i] for i in list_orders]


def schedule1(locations, start_location, number_of_trucks, orders):
    # TODO: replace the code in this function with your algorithm
    # orders: Order ID, Weight, Delivery location
    # This simple model solution does not make use of locations
    # However, to optimize your longest traveling time, you should use the information in locations.
    #OUTPUT: 
    # [[(1, 100, 'RUS'), (5, 200, 'CHN'), (9, 180, 'FRN')],
    # [(2, 150, 'CAN'), (6, 250, 'MEX'), (10, 230, 'SPN')],
    # [(3, 250, 'SIN'), (7, 350, 'AUS')],
    # [(4, 300, 'KOR'), (8, 270, 'GMY')]]
    max_list = []
    for i in range(number_of_trucks):
        max_list.append([])

    dict_loc= store_in_dict(locations)
  
    
    no_ordes = len(orders)
    copy_orders = orders

    no_per_trucks = len(orders) // number_of_trucks +1
    max_list_index = 0
    while number_of_trucks > 0: 
        #base case
        all_cities =  ([i[2] for i in orders])
        if number_of_trucks == 1:
            shortest_path = firstGreedyShortestPath(dict_loc,start_location, all_cities,len(orders))
            max_list[max_list_index] = returnOrders(shortest_path, orders)
            number_of_trucks = 0
        else:
            shortest_path = firstGreedyShortestPath(dict_loc,start_location, all_cities,len(orders))
            max_list[max_list_index] = returnOrders(shortest_path[1:no_per_trucks], orders)

            #remove orders 
            for i in shortest_path[1:no_per_trucks]:
                orders[i] = ()
            orders= [t for t in orders if t != ()]

            max_list_index += 1
            number_of_trucks -= 1

    return max_list
