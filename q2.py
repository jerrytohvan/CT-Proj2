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


def firstGreedyShortestPath(dict_loc, start_location, all_cities, k):
    #all_cities: ['RUS', 'CAN', 'SIN', 'KOR', 'CHN', 'MEX', 'AUS', 'GMY', 'FRN', 'SPN']
    #k: length of orders 
    selected_order_ids = []
    curr = start_location
    cost = 0
    while len(selected_order_ids) != k:
        #least dist 
        mini = 99999999
        low_k = ''
        index=0
        for j in  range (0, len(all_cities)):
            city = all_cities[j]
            if j not in selected_order_ids and curr != all_cities[j] and mini > dict_loc[curr][city]:
                mini = dict_loc[curr][city]
                low_k = city
                index = j
                cost += mini
        selected_order_ids.append(index)
        curr=low_k


    return [cost, tuple(selected_order_ids)]

def returnOrders(list_orders, orders):
    return [orders[i] for i in list_orders]

def findCombinationsWithCap(orders,limit):
    return ""

def findShortestPath(list_combinations, dict_loc, start_location,cap):
    cost_paths = []
    weight_paths = []
    for path in list_combinations:
        all_cities =  ([i[2] for i in path])
        ids = firstGreedyShortestPath(dict_loc,start_location,all_cities, len(path))
        orders = returnOrders(ids[1],path)
        # weight - cap absolute difference
        weight_path = cap - sum([i[1] for i in orders])
        if(weight_path >=0):
            cost_paths.append([ids[0], orders,weight_path])

    cost_paths = sorted(cost_paths,key=lambda x:  (x[2], x[0]))
    return cost_paths[0][1]

def schedule2(locations, start_location, capacities, orders):
    # TODO: replace the code in this function with your algorithm
    # orders: Order ID, Weight, Delivery location
    # This simple model solution does not make use of locations
    # However, to optimize your longest traveling time, you should use the information in locations.
   
#[[(2, 150, 'CAN'), (5, 200, 'CHN'), (1, 100, 'RUS'), (9, 180, 'FRN')], [(2, 150, 'CAN'), (1, 100, 'RUS')], [(1, 100, 'RUS')], [(2, 150, 'CAN'), (1, 100, 'RUS'), (9, 180, 'FRN')], [(2, 150, 'CAN'), (10, 230, 'SPN'), (5, 200, 'CHN'), (1, 100, 'RUS'), (9, 180, 'FRN')]]
    max_list = []
    for i in range(len(capacities)):
        max_list.append([])

    dict_loc= store_in_dict(locations)
    
    orders.sort(key=lambda x: x[1])
    orders_id = ([i[0] for i in orders]) 
    orders_weight = ([i[1] for i in orders]) 
    max_list_index = 0

    n_simulation = 10

    for cap in capacities:
        #get all possible combinations with total sum, returns index
        cap_orders = []
        for i in range(len(orders), 0, -1):
            for seq in itertools.combinations(orders_id, i):
                total = [orders_weight[j] for j in range(0,len(seq))]
                if sum(total) <= cap:
                    obj_orders = [orders[j] for j in range(0,len(seq))]
                    obj_orders = set(obj_orders)
                    cap_orders.append(list(obj_orders))

        # cap_orders = returnOrders(cap_orders_id, orders)
        cap_orders= [list(t) for t in set(tuple(element) for element in cap_orders)]
        shortest_path = findShortestPath(cap_orders, dict_loc, start_location,cap)
        # print(shortest_path[1])
        #insert to truck
        max_list[max_list_index] = shortest_path
        
        # remove cities from orders

        for i in shortest_path:
            for j in orders:
                if i == j:
                    orders.remove(j)
 
        max_list_index+=1
    return max_list

  
