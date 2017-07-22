# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 12:54:22 2017

@author: Khalid
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 18:02:50 2017

@author: Khalid
"""
from multiprocessing import Process,Queue
import math
import numpy as np
import time
import multiprocessing

Training_data = []
Testing_data = []

matrix_dimensions_row = None
matrix_dimensions_column = 10

num_of_processes = 0

###### Take input from user and initialize the values ######
def Take_input():
    global matrix_dimensions_row
    global matrix_dimensions_column
    global num_of_processes
    
    matrix_dimensions_row = int(input("Enter the number of rows N : "))
    matrix_dimensions_column = int(input("Enter the number of column M : "))
    num_of_processes = int(input("Enter the number of processes to run : "))
    print("Generating a 1xM Vector for Testing data")

###### Generate the matrix and fill it with random values ######
def Generate_matrix():
    global random_point
    global Training_data
    global Testing_data
    global matrix_dimensions_row
    global matrix_dimensions_column
    
    Training_data = np.random.random((matrix_dimensions_row,matrix_dimensions_column))
    Testing_data = np.random.random((matrix_dimensions_column))
    
    Training_data = Training_data * 10          # numbers lie between range 0-9
    Training_data = Training_data.astype(int)
    
    Testing_data = Testing_data * 10            # numbers lie between range 0-9
    Testing_data = Testing_data.astype(int)     
     
def Calculate_kNN_Parallel(start_index,terminating_index,Training_data_chunk,Testing_data,result_Queue):
    
    least_distance = 0

    for i in range(0,len(Training_data_chunk)):
        temp = 0
        sqrt_result = 1
        TrainingData_temp = 0
        TestingData_temp = 0
        
        for j in range(len(Testing_data)):  # Calculate the dot product
            temp += (Training_data_chunk[i][j] * Testing_data[j])
            TrainingData_temp += math.pow(Training_data_chunk[i][j],2)
            TestingData_temp += math.pow(Testing_data[j],2)
        
        a = math.sqrt(TrainingData_temp)
           
        b = math.sqrt(TestingData_temp)
       
        sqrt_result = a * b
       
        cos_theta = temp / sqrt_result
        
        if cos_theta > least_distance:
            least_distance = cos_theta
            class_index = i
    
    result = [cos_theta,class_index]
            
    result_Queue.put(result)

def Multiprocess_function(result_Queue):    
    global num_of_processes
    global matrix_dimensions_row
    global Training_data
    global Testing_data
    
    multiprocess_handle = []
            
    for j in range(0,num_of_processes):
        start_index = int((matrix_dimensions_row/num_of_processes) * j)
        end_index = int((matrix_dimensions_row/num_of_processes) * (j+1))
        t = Process(target = Calculate_kNN_Parallel, args=(start_index,end_index,Training_data[start_index:end_index],Testing_data,result_Queue))
        
        multiprocess_handle.append(t)
        
        t.start()
        
        
    for k in range(0,num_of_processes):
        multiprocess_handle[k].join()


if __name__=="__main__":
    
    Take_input()
    Generate_matrix()
    print("\nCalculating . . .\n")
    
    Final_minimum_distance_and_index = multiprocessing.Queue()      # Queue used to share data for multiprocessing in Python
    
    before = time.time()
        
    Multiprocess_function(Final_minimum_distance_and_index)
        
    after = time.time()
        
    final_cosine_similarity = 0     # Resulting/Final Cosine Similarity
    final_index = 0                 # Index of the nearest point
        
    for i in range(num_of_processes):                               # Loop thorugh no. of processes
        min_and_index = (Final_minimum_distance_and_index.get())    # Get each value from the Queue 
        if min_and_index[0] > final_cosine_similarity:              # and check which is smallest
            final_cosine_similarity = min_and_index[0]              # First index is the cosine similarity
            final_index = (i+1) * min_and_index[1]                  # Second index is the nearest neighbour index
                
                
    print("The maximum cosine similarity is : " + str(final_cosine_similarity))
    print("The nearest neighbour is with index : " + str(final_index))
    print("And the time taken is : " + str(after-before) + " seconds")