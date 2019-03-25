# do NOT submit this file
import numpy as np

# for scoring Q1. score = furthest distance taken by all trucks (smaller is better)
# if verbose is True, this function prints out the distance travelled by each truck
def get_score_q1(locations_file, start, orders, result, verbose = False):
  locmap = read_map(locations_file)

  #Compute shortest distance between START and any delivery location, between any 2 delivery location
  fulldest = {}
  compact = [start]

  for order in orders:
      compact.append(order[2])
      
  for node in compact:
      distance = dijkstra(node, locmap)
      fulldest[node] = {}
      for tem in compact:
          fulldest[node][tem] = distance[tem][1]
  max_travel_time = 0

  for i in range(len(result)):
      path = result[i]
      travel_time = 0
      src = start
      for k in range(len(path)):
          dst = path[k][2]
          travel_time += fulldest[src][dst]
          src = dst
      travel_time += fulldest[src][start]
      
      if verbose:
        print("travel time for truck " + str(i+1) + ": " + str(travel_time))
      
      if travel_time > max_travel_time:
          max_travel_time = travel_time
  return str(max_travel_time)

  
# for scoring Q2. score = total distance taken by all trucks (smaller is better)
# if verbose is True, this function prints out the distance travelled by each truck
def get_score_q2(locations_file, start, orders, result, verbose = False):
  locmap = read_map(locations_file)

  #Compute shortest distance between START and any delivery location, between any 2 delivery location
  fulldest = {}
  compact = [start]

  for order in orders:
      compact.append(order[2])
  for node in compact:
      distance = dijkstra(node, locmap)
      fulldest[node] = {}
      for tem in compact:
          fulldest[node][tem] = distance[tem][1]
  total_travel_distance = 0

  for i in range(len(result)):
      path = result[i]
      travel_distance = 0
      src = start
      for k in range(len(path)):
          dst = path[k][2]
          travel_distance += fulldest[src][dst]
          src = dst
      travel_distance += fulldest[src][start]
      
      if verbose:
        print("distance for truck " + str(i+1) + " : " + str(travel_distance))
      
      total_travel_distance += travel_distance
  
  return str(total_travel_distance)

# Returns a list read from filename (e.g. location_1.csv) 
# every element in the list is a line from the CSV file. The first line (header line) is ignored. 
# for example, if "location_1.csv" is passed in as filename, this function returns: ["USA,CAN,731", "USA,BHM,1623", "USA,CUB,1813"...]
def read_location(filename):
    my_list = []
    
    with open(filename) as datafile:
        datafile.readline()    # remove the first element (which is the header)
        for line in datafile:
            my_list.append(line.strip())
    
    return my_list
   
# check the validity of results returned by schedule1() in q1.py
# returns "" if OK. returns a string (error message) if not OK.
def check_validity_q1(orders, results, num_truck):
    if len(results) != num_truck:
        return "Error: the number of schedules in results does not match the number of trucks"
        
    tem = []
    
    for order in orders:
        tem.append(order[2]) #delivery location 
        
    for path in results:
        for node in path:
            if not node[2] in tem:
                return "Error: There is a delivery location (" + str(node) + ") in results that is not in orders"
            tem.remove(node[2]) # delivery location 
            
    if len(tem) > 0: # not all destinations in orders have been found in results
        return "Error: Not all orders were fulfilled. These delivery locations have not been visited: " + str(tem)
        
    return "" # all OK 

# check the validity of results returned by schedule2() in q2.py
# returns "" if OK. returns a string (error message) if not OK. 
def check_validity_q2(capacities, orders, results):
    if len(capacities) != len(results):
        return "Error: the number of schedules in results does not match the number of trucks in capacities"

    tem = []
    
    for order in orders:
        tem.append(order[2]) # delivery location 
        
    for i in range(len(results)):
        path = results[i] # path is a schedule 
        weight = 0
        for node in path:
            weight += node[1] # weight of that order 
            if not node[2] in tem:
                return "Error: There is a delivery location (" + str(node) + ") in results that is not in orders"
            tem.remove(node[2]) # delivery location 
        if weight > capacities[i]:
            err_msg = "Error: Truck " + str(i + 1) + " is overloaded! Its capacity is only " + str(capacities[i]) + ", but it is carrying orders weighing " + str(weight)
            return err_msg # error 
            
    if len(tem) > 0:
        return "Error: Not all orders were fulfilled. These delivery locations have not been visited: " + str(tem)
        
    return "" # all OK 

# dijkstra's algorithm     
def dijkstra(start, graph):
    distance = {}
    visited = {}
    #Initialize
    for loc in graph:
        distance[loc] = [loc, np.iinfo(np.int64).max]
        visited[loc] = 0
    queue = [start]
    distance[start][0] = start
    distance[start][1] = 0
    while len(queue) > 0:
        node = queue.pop(0)
        for neighbour, dist in graph[node].items(): # changed by mok
            if dist >= 0:
                if distance[neighbour][1] > dist + distance[node][1]:
                    distance[neighbour][0] = node
                    distance[neighbour][1] = dist + distance[node][1]
                if visited[neighbour] == 0:
                    queue.append(neighbour)
        visited[node] = 1
    return distance
    
# Returns a dictionary read from filename (e.g. location_1.csv) 
# Key: origin location. value: dictionary of destination/distance. 
# for example: {'USA': {'USA': 0, 'CAN': 731, 'BHM': 1623...}, ...}
#   The distance from USA to CAN is 731. the distance from USA to BHM is 1623 etc...
def read_map(filename):
    locmap = {}
    with open(filename) as datafile:
        datafile.readline()
        for line in datafile:
            attrs = line.rstrip().split(',')
            if(attrs[0] not in locmap):
                locmap[attrs[0]] = {attrs[0]:0, attrs[1]:int(attrs[2])}
            else:
                locmap[attrs[0]][attrs[1]]=int(attrs[2])
    return locmap

# Returns a list of orders read from filename (e.g. order_1.csv).
# Format of order CSV file: order ID, weight, deliver location (destination). 
# Each row in the CSV file is represented as a tuple in the returned list. 
# example of returned list (read from order_1.csv): [(1, 100, 'RUS'), (2, 150, 'CAN'), (3, 250, 'SIN'), (4, 300, 'KOR'), (5, 200, 'CHN'), (6, 250, 'MEX'), (7, 350, 'AUS'), (8, 270, 'GMY'), (9, 180, 'FRN'), (10, 230, 'SPN')]
def read_order(filename): #Order No.,Weight,To
    orders = []
    with open(filename) as test:
        test.readline()
        for line in test:
            attrs = line.rstrip().split(',')
            orders.append((int(attrs[0]),int(attrs[1]),attrs[2]))
    return orders

# Returns a list of load capacities of trucks read from filename (e.g. load_1.csv).
# Format of order CSV file: truck ID, load (weight). Assumption is that ID will always be 1, 2, 3...
# example of returned list (read from load_1.csv): [100, 1000, 2000]
def read_load(filename): #Truck ID,Load
    loads = []
    with open(filename) as test:
        test.readline()
        for line in test:
            attrs = line.rstrip().split(',')
            loads.append(int(attrs[1]))
    return loads
