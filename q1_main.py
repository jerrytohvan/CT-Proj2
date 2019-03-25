# do NOT submit this file
import numpy as np
import copy
import utilities as util
import q1

# change these values to vary the test case
START = "GUA"  # ensure that the START location is not found in ORDER_FILE          
NUM_TRUCKS = 3
LOCATIONS_FILE = "data\locations_1.csv" 
ORDER_FILE = "data\order_1.csv"

orders = util.read_order(ORDER_FILE)
orders_copy = copy.deepcopy(orders)
#print("Orders :" + str(orders))
locations = util.read_location(LOCATIONS_FILE)

# call your function
result = q1.schedule1(locations, START, NUM_TRUCKS, orders_copy)

# print your results 
print("START : " + START + ", NUM_TRUCKS : " + str(NUM_TRUCKS))
print("Your algorithm returned the following schedules:")
for schedule in result:
    print(schedule)
print()

# check if result returned by schedule1() is valid 
err_msg = util.check_validity_q1(orders, result, NUM_TRUCKS)
if err_msg != "":
    print("Result is not valid")
    print(err_msg) 
else: 
    score = util.get_score_q1(LOCATIONS_FILE, START, orders, result, True)
    print("Max travel time (lower is better): " + score)
