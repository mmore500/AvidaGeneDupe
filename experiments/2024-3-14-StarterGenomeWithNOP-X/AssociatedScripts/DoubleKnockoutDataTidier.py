import os
import csv
import numpy as np


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

for subdir in os.listdir(dataDir):
    if '.' in subdir:
        continue
    elif 'Test-Job' in subdir:
        continue
    elif 'Slip-NOP' in subdir:
        continue
    elif 'Slip-random' in subdir:
        continue
    elif 'Slip-scatter' in subdir:
        continue
    elif 'High-Mutation' in subdir:
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


def getMetrics(organismString):
    presentTasks = 0
    analyzeOutputs = organismString.split()
    
    tasks = analyzeOutputs[0]
    for task in tasks:
        if int(task) != 0:
            presentTasks +=1

    #Thus, having counted the number of tasks presently indicated by the task list, we can now just concatenate the rest of the metrics
    metrics = [float(output) for output in analyzeOutputs[1:-1]]
    metrics = [float(presentTasks)] + metrics

    return np.array(metrics)

def getTasks(organismString):
    analyzeOutputs = organismString.split()
    
    tasks = list(analyzeOutputs[0])
    for k,task in enumerate(tasks):
        tasks[k] = int(task)

    return np.array(tasks)

def isSiteRedundant(nonCodingSiteData):
    siteDatFileContents = getOrganisms(nonCodingSiteData)
    (organisms,analyzedOrganism) = (siteDatFileContents[:-1],siteDatFileContents[-1])

    #Next step: add Avida Parameters and Replicate ID

    organismsTasks = getTasks(analyzedOrganism)
    taskCounts = np.zeros(organismsTasks.size)
    for org in organisms:
        #Note that the absolute value is only being taken of the difference, so it should be proper
        taskCounts = taskCounts + np.abs(organismsTasks + (-1*getTasks(org)))
    
    if(np.sum(taskCounts) > 0):
        return True
    else:
        return False

def retrieveCodingSites(runDir):
    f = open(os.path.join(runDir,'data/codingSites.txt'),'r')
    codingSites = f.readlines()[0].split(',')
    codingSites.pop()

    for k, site in enumerate(codingSites):
        codingSites[k] = int(site)
    codingSites = np.array(codingSites)
    f.close()
    return codingSites

def filterNonCodingSites(codingSites, runDir):
    genomeLength = getLength(runDir)

    possibleIndices = np.arange(genomeLength)
    nonCodingIndices = [idx for idx in possibleIndices if idx not in codingSites]
    return nonCodingIndices

def getLength(runDir):
    replicateData = os.path.join(runDir, 'data/detail_MostNumerous.dat')
    datFileContents = getOrganisms(replicateData)
    analyzedOrganism = datFileContents[-1]
    
    #-2 is used here because the length is being pulled from the MostNumerous.dat file in which the length is second-to-last
    length = int(analyzedOrganism.split()[-2])
    return length

def informAndMakeTidy(treatmentArray, useCodingSites = True):
    with open('DoubleKnockoutData.csv', mode='w') as tidyDat:

        data_writer = csv.writer(tidyDat, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['Treatment',"COPY_MUT_PROB","COPY_INS_PROB","COPY_DEL_PROB","DIVIDE_INS_PROB","DIVIDE_DEL_PROB","DIVIDE_SLIP_PROB","SLIP_FILL_MODE",'Replicate #','Length', 'Number of Coding Sites', 'Fraction of Redundant Non-Coding Sites'])

        for treatment in treatmentArray:
            treatmentName = treatment.treatmentName
            print(treatmentName)
                
            for runDir in treatment.runDirectories:
                #Get contents of run directory
                runDirContents = os.listdir(runDir)
                #Filter out the dat files from the double knockout generator
                nonCodingSiteDatList = [file for file in runDirContents if "detail_Org" in file]
                #Get back redundancy result
                redundantSites = 0
                for siteFile in nonCodingSiteDatList:
                    if(isSiteRedundant(siteFile)):
                        redundantSites+=1
                
                #Normalize number of redundant non-coding sites by total number of non-coding sites
                codingSites = retrieveCodingSites(runDir)
                nonCodingSites = filterNonCodingSites(codingSites,runDir)
                nonCodingRedundantFrac = redundantSites/len(nonCodingSites)
                
                length = getLength(runDir)

                runName = None
                for folderName in runDir.split('/'):
                    if 'run_' not in folderName:
                        continue
                    else:
                        runName = folderName
                runParts = runName.split('_')
                runNum = runParts[-1]
                params = treatmentParameters[treatmentName]
                data_writer.writerow([treatmentName,params[0],params[1],params[2],params[3],params[4],params[5],params[6],runNum,length, len(codingSites), nonCodingRedundantFrac])
                

linDatFile = ".dat"

informAndMakeTidy(Treatments)




