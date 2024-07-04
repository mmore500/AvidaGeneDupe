'''
CodingSiteGeneratorHPCCCopy.py
Author: Cameron Haynes
Initial Date: May or June 2022

For any given Avida run, Analyze mode can be used to find the most dominant organism at a given timepoint.
This script takes in information about this dominant organism, including its genome, and outputs a row in
a Pandas dataframe for each task with a list of coding sites, viability sites, and other statistics.

Usage Example: python3 CodingSiteGeneratorHPCCCopy.py ${UPDATE_TO_ANALYZE}

Output: For each experimental treatment, a CSV file containing the rows of the aforementioned Pandas dataframe
===========================================================================================================

Overall Algorithm
1. Define variables and the different parameters for each treatment
2. Collect the paths to all of the directories where data will be found
3. The coding sites, and associated data for each of the dominant organisms
are generated and written in a Pandas dataframe for each treatment
4. The resultant Pandas dataframe, one for each treatment, is written to a CSV file

'''

import os
import csv
import numpy as np
import pandas as pd
import sys
import uuid

from CodingSiteGeneratorHPCCCopyFunctions import writeExperimentTaskCodingSites
import CodingSiteGeneratorHPCCCopyFunctions


'''
1. Define variables and the different parameters for each treatment
    a. Use the sys packages argv object to retrieve the examined update from the command line use of this script
    b. Initialize containers for storing the paths to where data is being held
    c. Provide the parameter values for the Avida runs of each treatment
    d. Get the name of the directory where this script is being executed to make correct absolute paths
    e. Define a Treatment class to encapsulate the paths for different treatment's raw data and the treatment's output dataframe
'''

'''
a. Use the sys package's argv object to retrieve the examined update from the command line use of this script
'''
CodingSiteGeneratorHPCCCopyFunctions.desiredUpdateToAnalyze = sys.argv[1]

'''
b. Initialize containers for storing the experimental treatments
'''
Treatments = []

'''
c. Provide the parameter values for the Avida runs of each treatment
'''
treatmentParameters = {"Baseline-Treatment":[0.0025, 0.0, 0.0, 0.05, 0.05, 0.0, 0],
"Slip-NOP":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 1],
"Slip-duplicate":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0],
"Slip-scatter":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 5],
"Slip-scramble":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 3],
"Slip-random":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 2],
"High-Mutation":[0.0025,0.0075,0.0075,0.05,0.05,0.0,0]}

'''
d. Get the name of the directory where this script is being executed to make correct absolute paths
'''
stream = os.popen('pwd')
pwd = stream.read().rstrip()
experimentDir = pwd
dataDir = pwd
experimentName = pwd.split('/')[-1]

'''
e. Define a Treatment class to encapsulate the paths for different treatment's raw data and the treatment's output dataframe
'''
class Treatment():
    def __init__(self,treatmentPath):
        self.treatmentDir = treatmentPath
        self.runDirectories = []
        self.treatmentName = self.treatmentDir.split('/')[-1]
        self.treatmentDataframe = pd.DataFrame(columns = ["Run ID",
                                                          "Lineage Generation Index",
                                                          "Task", 
                                                          "Update Analyzed",
                                                          "Treatment",
                                                          "Task Coding Sites", 
                                                          "Number of Task Coding Sites", 
                                                          "Number of Unique Coding Sites", 
                                                          "Viability Sites", 
                                                          "Number of Viability Sites", 
                                                          "Genome Length", 
                                                          "Fraction Task Coding Sites", 
                                                          "Fraction Viability Sites", 
                                                          "Ratio of Viability Sites to Coding Sites", 
                                                          "Genome"])

'''
2. Collect the paths to all of the directories where data will be found
    a. Gather all of the subdirectories and add them to the list for iteration if they are valid treatments,
      according to the list provided.
    b. For each valid treatment, add the replicate subdirectories contained in the treatment directory to the treatment's list.
'''

for subdir in os.listdir(dataDir):
    '''
    a. Gather all of the subdirectories and add them to the list for iteration if they are valid treatments,
    according to the list provided.
    '''
    if subdir not in ['Baseline-Treatment', 'Slip-scramble']:
        continue
    treatment = Treatment(os.path.join(dataDir,subdir))
    Treatments.append(treatment)

    '''
    b. For each valid treatment, add the replicate subdirectories contained in the treatment directory to the treatment's list.
    '''
    for run_dir in os.listdir(treatment.treatmentDir):
        if not 'run_' in run_dir:
            continue
        treatment.runDirectories.append(os.path.join(treatment.treatmentDir,run_dir))

'''
3. The coding sites, and associated data for each of the dominant organisms
are generated and written in a Pandas dataframe for each treatment
'''
writeExperimentTaskCodingSites(Treatments)

'''
4. The resultant Pandas dataframe, one for each treatment, is written to a CSV file
'''
for treatment in Treatments:
    print(treatment.treatmentDataframe)
    treatment.treatmentDataframe["Run UUID"] = uuid.uuid4()
    treatment.treatmentDataframe.to_csv(f"{experimentDir}/{experimentName}-{treatment.treatmentName}-TaskCodingSitesWithViabilitySitesAtUpdate{desiredUpdateToAnalyze}.csv")
    counter += 1



