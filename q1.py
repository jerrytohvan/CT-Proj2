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

    #stores all order ids with the shortest path
    selected_order_ids = []

    #initialise current location of truck
    curr = start_location

    #loop will run as long as it has meet the length of the inserted orders
    while len(selected_order_ids) != k:
        #least dist first initialised to 9999999999 so that the first order will be set as the minimum distance
        mini = 99999999
        low_k = ''
        index=0
        #run each cities of orders
        for j in  range (0, len(all_cities)):
            city = all_cities[j]
            #when current order is not in the selected path, current order city is not equal to current city (next city cant be curr city), and the distance cost is lesser than the current initialised minimum city
            if j not in selected_order_ids and curr != city and mini > int(dict_loc[curr][city]):
                #set new minimum distance of current order
                mini = int(dict_loc[curr][city])
                #set new city to current order
                low_k = city
                #set index of the minimum distance to current order's index
                index = j
        #when all orders were checked, add minimum distance order to the current path
        selected_order_ids.append(index)
        #initialise the new truck location for next round
        curr=low_k
    return tuple(selected_order_ids)

def returnOrders(list_orders, orders):
    #retuns order of inserted index
    return [orders[i] for i in list_orders]


def schedule1(locations, start_location, number_of_trucks, orders):
    # TODO: replace the code in this function with your algorithm
    # orders: Order ID, Weight, Delivery location
    # This simple model solution does not make use of locations
    # However, to optimize your longest traveling time, you should use the information in locations.

    #initialise trucks list
    max_list = []
    for i in range(number_of_trucks):
        max_list.append([])

    #convert current locations to dictionary format, for easy retrieval
    dict_loc= store_in_dict(locations)
    
    #ensures equal distribution of orders so that no of orders per trucks are balanced (most probably will result to minimum travel distance)
    no_per_trucks = len(orders) // number_of_trucks +1
    max_list_index = 0

    #loops all until all trucks are filled with orders
    while number_of_trucks > 0: 
        #get all city in orders
        all_cities =  ([i[2] for i in orders])
        #base case: when there is 1 trucks left insert all leftovers orders to the last truck
        if number_of_trucks == 1:
            shortest_path = firstGreedyShortestPath(dict_loc,start_location, all_cities,len(orders))
            max_list[max_list_index] = returnOrders(shortest_path, orders)
            number_of_trucks = 0
        else:
            #for each truck we find the shortest path of all available cities, returns index
            shortest_path = firstGreedyShortestPath(dict_loc,start_location, all_cities,len(orders))
            #but here we take the shortest path order indexes up to the no_per_trucks
            max_list[max_list_index] = returnOrders(shortest_path[1:no_per_trucks], orders)

            #remove orders that is inserted to current truck
            for i in shortest_path[1:no_per_trucks]:
                orders[i] = ()
            orders= [t for t in orders if t != ()]

            #intialise indec for the next truck
            max_list_index += 1
            #1 truck has been filled with the orders
            number_of_trucks -= 1

    return max_list
