# Team ID: G4T12

import  itertools
 
def store_in_dict(locations):
    dd = {}
    for loc in locations:
        lst = loc.split(",")
        if lst[0] not in dd :
            dd[lst[0]] = {lst[1]: lst[2]}
        else:
            start = lst[0]
            dest = lst[1]
            val = lst[2]
            dd[start][dest] = val
    return dd


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
    orders_left = orders

    max_list = []
    for i in range(number_of_trucks):
        max_list.append([])

    # print("Start :" + start_location)


    #approx equal dist per no trucks:
    k = len(orders) // number_of_trucks
    dict_locations = store_in_dict(locations)

    all_orders_index = ([i for i in range(0,len(orders))])
    all_cities =  ([i[2] for i in orders])
    
    #all combinations on equal weight
    permuts_orders_index = list(itertools.combinations(all_orders_index,k))

    #calculate all possible travel cost:
    all_travel_cost = []
    for possible_order in permuts_orders_index:
        start_cost = int(dict_locations[start_location][orders[possible_order[0]][2]])
        end_cost = int(dict_locations[orders[possible_order[-1]][2]][start_location])
        middle_cost = 0
        for i in range(0, len(possible_order)-1):
            middle_cost+= int(dict_locations[orders[possible_order[i]][2]][orders[possible_order[i+1]][2]])
        all_travel_cost.append(start_cost+middle_cost+end_cost)
   
    #add index before sorting to the smallest correspoding to `all_travel_cost` & `permuts_orders_index`

    all_travel_cost_index = []
    for i in range(0, len(all_travel_cost)):
        all_travel_cost_index.append([i,all_travel_cost[i]])
    all_travel_cost_index.sort(key=lambda x: x[1])
    #getting corresponding index
    # print(all_travel_cost_index)

    # ======== START =============
    i = 0
    truck_no = 0
    remove_copy_order_index = []
    while(number_of_trucks>0 and i<len(all_travel_cost_index)):
        combi_cities = [orders[j][2] for j in permuts_orders_index[all_travel_cost_index[i][0]]]
        filter_for = ''.join(combi_cities)
        if filter_for in ''.join(all_cities):

            # print("MATCH")
            # print(combi_cities)
            # print(all_cities)
            #base case add the of coutries rest in 
            if(truck_no==len(max_list)-1):
            #might recalculate to get less travel cost
                # print("Cities left: ")
                # print(all_cities)
                for j in remove_copy_order_index:
                    orders_left[j] = ()
                # print("order left: ")
                orders_left = [t for t in orders_left if t != ()]
                # print(orders_left)

                all_orders_left_index = ([i for i in range(0,len(orders_left))])
                permuts_orders_left_index = list(itertools.permutations(all_orders_left_index,len(orders_left)))
                #calculate all possible travel cost:
                all_travel_cost_left = []
                for possible_order in permuts_orders_left_index:
                    start_cost = int(dict_locations[start_location][orders_left[possible_order[0]][2]])
                    end_cost = int(dict_locations[orders_left[possible_order[-1]][2]][start_location])
                    middle_cost = 0
                    for j in range(0, len(possible_order)-1):
                        middle_cost+= int(dict_locations[orders_left[possible_order[j]][2]][orders_left[possible_order[j+1]][2]])
                    all_travel_cost_left.append(start_cost+middle_cost+end_cost)
                
                all_travel_cost_left_index = []
                for j in range(0, len(all_travel_cost_left)):
                    all_travel_cost_left_index.append([j,all_travel_cost_left[j]])
              
                all_travel_cost_left_index.sort(key=lambda x: x[1])


                #get first index (cheapest travel cost)
                for j in permuts_orders_left_index[all_travel_cost_left_index[0][0]]:
                    max_list[truck_no].append(orders_left[j])
                number_of_trucks = 0
            else:
                #add to trucks

                for j in permuts_orders_index[all_travel_cost_index[i][0]]:
                    if len(max_list[truck_no])<k-1:
                        max_list[truck_no].append(orders[j])
                    else:
                        truck_no+=1
                        max_list[truck_no].append(orders[j])
                        number_of_trucks -= 1
                    remove_copy_order_index.append(j)
            for city in combi_cities:
                try:
                    if city in all_cities:
                        all_cities.remove(city)
                except:
                    pass
        i+=1


    return max_list


