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
desiredUpdateToAnalyze = sys.argv[1]

'''
b. Initialize containers for storing the paths to where data is being held
'''
#NOTE: I think this runDirectories can be deleted because the paths to run directories are already
#being stored in the appropriate list in each treatment instance
runDirectories = []
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

#Use r"Path" to avoid any problems from special characters
def getOrganisms(filePath):
    with open(filePath,'r') as datFile:
        lines = datFile.readlines()
        initalOrgPos = 0
        for k,line in enumerate(lines):
            if (line[0] != '') & (line[0] != '#') & (line[0] != '\n'):
                initialOrgPos = k
                break
            else:
                continue

        organisms = []
        for i in range(initialOrgPos,len(lines)):
            if(lines[i] != ''):
                organisms.append(lines[i])
            else:
                continue

        if(len(organisms) > 0):
            return organisms
        else:
            print("Error: please check code")

def getDatFileHeaders(datFile):
    with open(datFile,'r') as dataF:
        datFileLines = dataF.readlines()
        formatLineTerms = (datFileLines[1].split())[1:-1]
        for k,term in enumerate(formatLineTerms):
            if term == 'task_list':
                formatLineTerms[k] = 'Task Count'
        return formatLineTerms


def getOrganismID(organismString):
    analyzeOutputs = organismString.split()
    ID = analyzeOutputs[0]
    return ID

def getUpdateBorn(organismString):
    analyzeOutputs = organismString.split()
    updateBorn = analyzeOutputs[1]
    return updateBorn

def getLength(runDir):
    replicateData = os.path.join(runDir, f'Timepoint_{desiredUpdateToAnalyze}/data/detail_MostNumerousAt{desiredUpdateToAnalyze}.dat')
    datFileContents = getOrganisms(replicateData)
    analyzedOrganism = datFileContents[-1]
    
    #-2 is used here because the length is being pulled from the MostNumerous.dat file in which the length is second-to-last
    length = int(analyzedOrganism.split()[-2])
    return length

def getViability(organism):
    #-2 is used here because the viability is being pulled from the knockout analysis file in which the viability is second-to-last
    viability = int(organism.split()[-2])
    return viability

def getGenome(runDir):
    replicateData = os.path.join(runDir, f'Timepoint_{desiredUpdateToAnalyze}/data/detail_MostNumerousAt{desiredUpdateToAnalyze}.dat')
    datFileContents = getOrganisms(replicateData)
    analyzedOrganism = datFileContents[-1]
    
    #-2 is used here because the length is being pulled from the MostNumerous.dat file in which the length is second-to-last
    genome = analyzedOrganism.split()[-1]
    return genome
    
def knockItOut(genomeString,instructionIndex):
    knuckOutGenome = list(genomeString)
    knuckOutGenome[instructionIndex] = 'A'
    return "".join(knuckOutGenome)

def knockoutDatGenome(dest,genome,orgCount):
    knuckOutGenomes = []
    for instructionIndex,inst in enumerate(genome):
        knuckOutGenome = knockItOut(genome,instructionIndex)
        knuckOutGenomes.append('LOAD_SEQUENCE ' + knuckOutGenome + '\n')
    writeFile = dest
    knuckOutGenomes.append('LOAD_SEQUENCE ' + genome + '\n')
    dest.write('SET_BATCH {} \n\n'.format(orgCount))
    dest.writelines(knuckOutGenomes)
    dest.write('RECALC\n\n')
    dest.write('DETAIL detail_Org{}FitnessDifferences.dat task_list gest_time comp_merit merit fitness efficiency viable length\n\n'.format(orgCount))

def knockoutDatFile(datFile,dest):
    #os.system('pwd')
    with open(datFile,'r') as X:
        lines = X.readlines()
        orgCount = 0
        for k,line in enumerate(lines):
            if('#' in line):
                continue
            if(len(line) <= 1):
                continue
            orgData = line.split()
            genome = orgData[-1]
            knockoutDatGenome(dest,genome,orgCount)
            orgCount+=1

def createDatAnalyzeCfg(runDir):
        datDir = os.path.join(runDir,f"Timepoint_{desiredUpdateToAnalyze}")

        datFile = os.path.join(datDir,f"data/detail_MostNumerousAt{desiredUpdateToAnalyze}.dat")
            
        configFile = os.path.join(datDir,'informationAnalyzer.cfg')
        f = open(configFile,'w')
        preamble = ['################################################################################################\n',
                    '# This file is used to setup avida when it is in analysis-only mode, which can be triggered by\n'
                    '# running "avida -a".\n',
                    '#\n', 
                    '# Please see the documentation in documentation/analyze.html for information on how to use\n',
                    '# analyze mode.\n',
                    '################################################################################################\n',
                    '\n',
                    '\n']
        f.writelines(preamble)
        
        knockoutDatFile(datFile,f)

def executeInfoAnalysis(runDir):
    #To accommodate the appropriate gcc compiler not being automatically loaded
    os.system('module load gcc/11.2.0')

    timepointRunDir = os.path.join(runDir, f"Timepoint_{desiredUpdateToAnalyze}")

    configDir = os.path.join("~/Documents/AvidaGeneDupe/experiments/","{}/hpcc/config".format(experimentName))
    os.system("cp ~/Documents/AvidaGeneDupe/avida/cbuild/work/avida {}".format(timepointRunDir))
    os.chdir(timepointRunDir)
    os.system('cp {}/avida.cfg .'.format(configDir)) 
    os.system('cp {}/default-headsWithNOP-X.org .'.format(configDir))
    os.system('cp {}/environment.cfg .'.format(configDir))
    os.system('cp {}/events.cfg .'.format(configDir))
    os.system('cp {}/instset-heads___sensors_NONE.cfg .'.format(configDir))
    os.system(f"./avida -set ANALYZE_FILE informationAnalyzer.cfg -a > analyze.log")
    os.system('rm avida')
    os.system('rm avida.cfg')
    os.system('rm default-headsWithNOP-X.org')
    os.system('rm environment.cfg')
    os.system('rm events.cfg')
    os.system('rm instset-heads___sensors_NONE.cfg')


def getTasks(organismString):
    analyzeOutputs = organismString.split()
    
    tasks = list(analyzeOutputs[0])
    for k,task in enumerate(tasks):
        tasks[k] = int(task)

    return np.array(tasks)

def getTaskCodingSitesOverRun(runDir):
    replicateData = os.path.join(runDir,f"Timepoint_{desiredUpdateToAnalyze}/data/detail_Org0FitnessDifferences.dat")
    datFileContents = getOrganisms(replicateData)
    (knockoutOrganisms,analyzedOrganism) = (datFileContents[:-1],datFileContents[-1])

    #Next step: add Avida Parameters and Replicate ID

    organismsTasks = getTasks(analyzedOrganism)
    
    #codingSites is now a numpy array of boolean values; each row, col corresponds to task, genome site
    #and gives 1 if coding site, 0 if not
    codingSites = [[] for k in range(len(organismsTasks))]

    numCodingSites = 0

    viabilitySites = set()

    for site, knockoutOrg in enumerate(knockoutOrganisms):
        knockoutOrganismTasks = getTasks(knockoutOrg)
        
        viabilitySite = bool(int(getViability(knockoutOrg)))

        if viabilitySite:
            viabilitySites.add(site)
        else:
            codingSite = False
            for j in range(len(organismsTasks)):
                if organismsTasks[j] != knockoutOrganismTasks[j]:
                    codingSite = True
                    codingSites[j].append(site)
            
            if codingSite:
                numCodingSites = numCodingSites + 1

    viabilitySites = sorted(list(viabilitySites))

    return codingSites, viabilitySites, numCodingSites

def writeTaskCodingSitesInPandasDataFrame(treatment, runDir, taskCodingSites, viabilitySites, numUniqueCodingSites):
    runDirElements = runDir.split('/')
    runName = runDirElements[-1]

    taskNames = ["NOT",
                 "NAND",
                 "AND",
                 "ORNOT",
                 "OR",
                 "ANDNOT",
                 "NOR",
                 "XOR",
                 "EQUALS"]

    genomeLength = getLength(runDir)

    fracCodingSites = numUniqueCodingSites / genomeLength
    fracViabilitySites = len(viabilitySites) / genomeLength

    try:
        viabilityToCodingRatio = fracViabilitySites / fracCodingSites
    except(ZeroDivisionError):
        viabilityToCodingRatio = 0

    for k in range(9):
        rowName = f"{runName}," + f"{taskNames[k]}"
        treatment.treatmentDataframe.loc[rowName] = [runName, taskNames[k], desiredUpdateToAnalyze, treatment.treatmentName, taskCodingSites[k], len(taskCodingSites[k]), numUniqueCodingSites, viabilitySites, len(viabilitySites), genomeLength, fracCodingSites, fracViabilitySites, viabilityToCodingRatio, getGenome(runDir)]

def writeTaskCodingSites(runDir,codingSites):
    writeDirectory = os.path.join(runDir,f"Timepoint_{desiredUpdateToAnalyze}/data/codingSites.txt")
    with open(writeDirectory,'w') as f:
        for site in codingSites:
            f.write('{},'.format(site))

'''
writeExperimentTaskCodingSites():
Input: The list of valid treatments to be iterated over

Algorithm
For each run directory (the overarching container for the raw data of a given replicate) in each treatment

a. Create an Analyze mode analyze.cfg named "informationAnalyzer.cfg" through generating knockout genomes

b. Use informationAnalyzer.cfg to run Analyze mode on the knockout genomes to generate data on the effect of
each knockout

c. Parse the Analyze mode output to get the dominant organism's coding and viability sites

d. Write the coding and viability sites along with other relevant metrics to a Pandas dataframe,
 one row for each task in the environment

e. Remove the subdirectory for the update to analyze, so that space is freed in scratch
'''
def writeExperimentTaskCodingSites(treatmentArray):
    for treatment in treatmentArray:
        treatmentName = treatment.treatmentName
        print(treatmentName)

        '''
        For each run directory (the overarching container for the raw data of a given replicate) in each treatment
        '''
        for runDir in treatment.runDirectories:
            #runDirElements = runDir.split('/')
            #runName = runDirElements[-1]
            #print(f"{runName} elements = {os.listdir(runDir)}")

            '''
            a. Create an Analyze mode analyze.cfg named "informationAnalyzer.cfg" through generating knockout genomes
            '''
            createDatAnalyzeCfg(runDir)

            '''
            b. Use informationAnalyzer.cfg to run Analyze mode on the knockout genomes to generate data on the effect of 
            each knockout
            '''
            executeInfoAnalysis(runDir)

        #NOTE: treatmentData is also something from a past iteration that can be erased    
        treatmentData = []
        for runDir in treatment.runDirectories:
            '''
            c. Parse the Analyze mode output to get the dominant organism's coding and viability sites
            '''
            taskCodingSites, viabilitySites, numUniqueCodingSites = getTaskCodingSitesOverRun(runDir)

            '''
            d. Write the coding and viability sites along with other relevant metrics to a Pandas dataframe,
             one row for each task in the environment
            '''
            writeTaskCodingSitesInPandasDataFrame(treatment, runDir, taskCodingSites, viabilitySites, numUniqueCodingSites)

            '''
            e. Remove the subdirectory for the update to analyze, so that space is freed in scratch
            '''
            os.chdir(runDir)
            os.system(f"rm -r Timepoint_{desiredUpdateToAnalyze}")

#NOTE: linDatFile is also not used anywhere else
linDatFile = ".dat"

'''
3. The coding sites, and associated data for each of the dominant organisms
are generated and written in a Pandas dataframe for each treatment
'''
writeExperimentTaskCodingSites(Treatments)

#NOTE: Delete this variable, because it is a debugging artifact
counter = 0

'''
4. The resultant Pandas dataframe, one for each treatment, is written to a CSV file
'''
for treatment in Treatments:
    print(treatment.treatmentDataframe)
    treatment.treatmentDataframe["Run UUID"] = uuid.uuid4()
    treatment.treatmentDataframe.to_csv(f"{experimentDir}/{experimentName}-{treatment.treatmentName}-TaskCodingSitesWithViabilitySitesAtUpdate{desiredUpdateToAnalyze}.csv")
    counter += 1



