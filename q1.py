# Team ID: G4T12
import utilities as util
import numpy as np
from collections import defaultdict
 

def convertArrayToDictionary(locations):
    dictionary = {}
    for array in locations:
        elements = array.split(',')
        key1 = elements[0]
        key2 = elements[1]
        val = elements[2]
        if key1 not in dictionary:
            dictionary[key1] = {}
   
        dictionary[key1][key2] = (val)
    return dictionary


def schedule1(locations, start_location, number_of_trucks, orders):   
    # TODO: replace the code in this function with your algorithm
  
    #orders: Order ID, Weight, Delivery location
    
    #This simple model solution does not make use of locations
    #However, to optimize your longest traveling time, you should use the information in locations. 


    #sample `locations`:  ['WSM,SOL,1581', 'WSM,FJI,823']
    locations = convertArrayToDictionary(locations)
    # print(locations["WSM"]["SOL"])

    max_list = []
    
    for i in range(number_of_trucks):
        max_list.append([])
        
    for i in range(len(orders)):
        max_list[i%number_of_trucks].append(orders[i])
        
    return max_list