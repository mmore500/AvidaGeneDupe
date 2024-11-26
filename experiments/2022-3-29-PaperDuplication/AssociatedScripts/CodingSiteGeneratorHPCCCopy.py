'''
CodingSiteGeneratorHPCCCopy.py
Author: Cameron Haynes
Initial Date: May or June 2022

For any given Avida run, Analyze mode can be used to find the most dominant organism at a given timepoint.
This script takes in information about this dominant organism, including its genome, and outputs a row in
a Pandas dataframe for each task with a list of coding sites, viability sites, and other statistics.
===========================================================================================================

This script begins by collecting the paths to all of the directories where data will be found, and then it
proceeds to iterate through those directories and apply the same analysis to each in turn.




'''


import os
import csv
import numpy as np
import pandas as pd
import sys
import uuid

desiredUpdateToAnalyze = sys.argv[1]

runDirectories = []
Treatments = []
treatmentParameters = {"Baseline-Treatment":[0.0025, 0.0, 0.0, 0.05, 0.05, 0.0, 0],
"Slip-NOP":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 1],
"Slip-duplicate":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0],
"Slip-scatter":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 5],
"Slip-scramble":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 3],
"Slip-random":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 2],
"High-Mutation":[0.0025,0.0075,0.0075,0.05,0.05,0.0,0]}
stream = os.popen('pwd')
pwd = stream.read().rstrip()
experimentDir = pwd
dataDir = pwd
experimentName = pwd.split('/')[-1]


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

'''To collect all the paths, it begins at the directory associated with the Avida experiment run. Then, it
gathers all of the subdirectories and considers if they are valid treatments, according to the list provided.
For each valid treatment, it adds the replicate subdirectories contained in the treatment directory to a list.
This list is what is iterated over for analysis.

Once all the run directories have been collated, the 
'''

for subdir in os.listdir(dataDir):
    if subdir not in ['Baseline-Treatment', 'Slip-duplicate']:
        continue
    treatment = Treatment(os.path.join(dataDir,subdir))
    Treatments.append(treatment)

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
    os.system('cp {}/default-heads.org .'.format(configDir))
    os.system('cp {}/environment.cfg .'.format(configDir))
    os.system('cp {}/events.cfg .'.format(configDir))
    os.system('cp {}/instset-heads___sensors_NONE.cfg .'.format(configDir))
    os.system(f"./avida -set ANALYZE_FILE informationAnalyzer.cfg -a > analyze.log")
    os.system('rm avida')
    os.system('rm avida.cfg')
    os.system('rm default-heads.org')
    os.system('rm environment.cfg')
    os.system('rm events.cfg')
    os.system('rm instset-heads___sensors_NONE.cfg')


def getTasks(organismString):
    analyzeOutputs = organismString.split()
    
    tasks = list(analyzeOutputs[0])
    for k,task in enumerate(tasks):
        tasks[k] = int(task)

    return np.array(tasks)

def getTaskCodingSitesOverRun(knockoutDataFile):
    #replicateData = os.path.join(runDir,f"Timepoint_{desiredUpdateToAnalyze}/data/detail_Org0FitnessDifferences.dat")
    datFileContents = getOrganisms(knockoutDataFile)
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
        
        viabilityKnockout = bool(int(getViability(knockoutOrg)))
        viabilityOriginal = bool(int(getViability(analyzedOrganism)))

        #If the viability of the knockout is different than the original, then it is true that the knockout
        #is a viability site
        viabilitySite = not viabilityKnockout == viabilityOriginal

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

def writeTaskCodingSitesInPandasDataFrame(treatment, lineageGenerationIndex, runDir, taskCodingSites, viabilitySites, numUniqueCodingSites):
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
        treatment.treatmentDataframe.loc[rowName] = [runName, lineageGenerationIndex, taskNames[k], desiredUpdateToAnalyze, treatment.treatmentName, taskCodingSites[k], len(taskCodingSites[k]), numUniqueCodingSites, viabilitySites, len(viabilitySites), genomeLength, fracCodingSites, fracViabilitySites, viabilityToCodingRatio, getGenome(runDir)]

def getAndWriteTaskCodingSites(treatment, runDir):
    lineageDetailFiles = [fileName for fileName in os.listdir(runDir) if "FitnessDifferences.dat" in fileName]
    for k in range(len(lineageDetailFiles)):
        orgKnockoutDataFile = lineageDetailFiles[k]
        taskCodingSites, viabilitySites, numUniqueCodingSites = getTaskCodingSitesOverRun(orgKnockoutDataFile)
        writeTaskCodingSitesInPandasDataFrame(treatment, k, runDir, taskCodingSites, viabilitySites, numUniqueCodingSites)

def writeExperimentTaskCodingSites(treatmentArray):
    for treatment in treatmentArray:
        treatmentName = treatment.treatmentName
        print(treatmentName)
        
        for runDir in treatment.runDirectories:
            createDatAnalyzeCfg(runDir)
            executeInfoAnalysis(runDir)
            
        treatmentData = []
        for runDir in treatment.runDirectories:
            getAndWriteTaskCodingSites(treatment, runDir)
            os.chdir(runDir)
            os.system(f"rm -r Timepoint_{desiredUpdateToAnalyze}")

linDatFile = ".dat"

writeExperimentTaskCodingSites(Treatments)

counter = 0

for treatment in Treatments:
    print(treatment.treatmentDataframe)
    treatment.treatmentDataframe["Run UUID"] = uuid.uuid4()
    treatment.treatmentDataframe.to_csv(f"{experimentDir}/{experimentName}-{treatment.treatmentName}-TaskCodingSitesWithViabilitySitesAtUpdate{desiredUpdateToAnalyze}.csv")
    counter += 1



