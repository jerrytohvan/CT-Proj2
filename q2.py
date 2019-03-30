# Team ID: G4T12
import itertools,operator

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


def firstGreedyShortestPath(dict_loc, start_location, all_orders, k):
    #all_cities: ['RUS', 'CAN', 'SIN', 'KOR', 'CHN', 'MEX', 'AUS', 'GMY', 'FRN', 'SPN']
    #k: length of orders 
    selected_order_ids = []

    curr = start_location
    while len(selected_order_ids) != k:
        #least dist 
        mini = 99999999
        low_k = ''
        index=0
        for j in  range (0, len(all_orders)):
            city = all_orders[j][2]
            if j not in selected_order_ids and curr != city and mini > int(dict_loc[curr][city]):
                mini = int(dict_loc[curr][city])
                low_k = city
                index = j
        selected_order_ids.append(index)
        curr=low_k
    return tuple(selected_order_ids)

def returnOrders(list_orders, orders):
    return [orders[i] for i in list_orders]

def findNextCityWithLeastDiff(dict_loc, start_location, orders, cap):
    cap_diff_list = []
    index=0   
    curr = start_location
    for j in  range (0, len(orders)):
        city = orders[j][2]
        if curr != city:
            order_weight = int(orders[j][1])
            diff = cap - order_weight
            dist = int(dict_loc[curr][city])
            if(diff >=0):
                cap_diff_list.append([j,dist,diff])
    if len(cap_diff_list) == 0:
        return -1
    cap_diff_list = sorted(cap_diff_list,key=lambda x:  (x[1], x[2]))   
    return cap_diff_list[0][0]


def schedule2(locations, start_location, capacities, orders):
    #stores orders before finding shortest path
    max_list = []
    #stores weight left for each truck in a 2D
    total_weight_list = []
    #stores the last location as starting point to look for other short distance to the next city
    start_location_list = []
    #stores the orders after finding shortest path )(THIS IS FINAL RESULT)
    temp_max_list = []

    #initialise arrays with existing values before processing
    for i in range(0,len(capacities)):
        max_list.append([])
        temp_max_list.append([])
        total_weight_list.append([int(capacities[i])])
        start_location_list.append([start_location])

    #transform locations_1 to dictionary form
    dict_loc= store_in_dict(locations)

    #loops not sure how many times but until all orders are inserted
    while len(orders)!=0: 
        #loops each truck: This ensure fair distribution for every loop. At every loop algo will find the shortest distance to the next city
        for i in range (0,len(capacities)):
            #ignore if current cap left over for the truck is 0. It keeps looping if 0 is not reach but no order can fill the gap.
            if total_weight_list[i][0]>0:
                #find index of the next city which has the last distance from where the truck is at currently and that it meets the cap
                index = findNextCityWithLeastDiff(dict_loc, start_location_list[i][0],orders,total_weight_list[i][0])
                #if the index exists, means that it has meet the current capacity availability
                if index != -1:
                    #add order to the current max_list
                    max_list[i].append(orders[index])
                    #reduce current cap by the weight of the order for next round
                    total_weight_list[i][0] -= orders[index][1]
                    #change last location of the truck
                    start_location_list[i][0] = orders[index][2]
                    #remove order so that i wont be taken into account for the next round
                    orders.pop(index)

    #optimise differences here =================
    #Jerry: I think what you can do is to run simulation of which order in 2 array cant be swapped that will result to lesser distance, you can use write a algo similar to firstGreedyShortestPath to find the lesser path. 
    #If the total route distance is lesser than the current minimum, swap. Loop this process for n number of simulation as an input. That should work efficiently :) based on statistic this will result to better distance as the n simulation grows
    
    #===== EXAMPLE ====
    # n_simul = 5000
    # for rounds in n_simul:
    #     for trucks in max_list:
    #         for truct in trucks:
                #can it maybe do a random pick to swap 2 cities on 2 routes by picking 2 random trucks and 2 orders
                #if can compute all distance is it lesser than the initial route order?
                #if yes change max_list to current orders


    #end of optimations ====================

    #find shortest path for all orders in the max_list
    index = 0
    for each_orders in max_list:
        all_cities =  ([i[2] for i in each_orders])
        #find shortest path from current order : returns indexes
        shortest_path = firstGreedyShortestPath(dict_loc,start_location, each_orders,len(all_cities))
        #get all orders with current order
        temp_max_list[index] = returnOrders(shortest_path, each_orders)
        index +=1
    return temp_max_list

  
