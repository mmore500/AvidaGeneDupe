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
        datDir = os.path.join(runDir,"data")
        datFile = os.path.join(datDir,"detail_MostNumerous.dat")
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
    configDir = os.path.join("~/AvidaGeneDupe/experiments/","{}/hpcc/config".format(experimentName))
    os.system("cp ~/AvidaGeneDupe/avida/cbuild/work/avida {}".format(runDir))
    os.chdir(runDir)
    os.system('cp {}/avida.cfg .'.format(configDir)) 
    os.system('cp {}/default-heads.org .'.format(configDir))
    os.system('cp {}/environment.cfg .'.format(configDir))
    os.system('cp {}/events.cfg .'.format(configDir))
    os.system('cp {}/instset-heads___sensors_NONE.cfg .'.format(configDir))
    os.system("./avida -set ANALYZE_FILE data/informationAnalyzer.cfg -a > analyze.log")
    os.system('rm avida')
    os.system('rm avida.cfg')
    os.system('rm default-heads.org')
    os.system('rm environment.cfg')
    os.system('rm events.cfg')
    os.system('rm instset-heads___sensors_NONE.cfg')

def getLength(replicateData):
    datFileContents = getOrganisms(replicateData)
    analyzedOrganism = datFileContents[-1]
    
    length = int(analyzedOrganism.split()[-1])
    return length

def getTasks(organismString):
    analyzeOutputs = organismString.split()

    tasks = list(analyzeOutputs[0])
    for k,task in enumerate(tasks):
        tasks[k] = int(task)

    return np.array(tasks)

def getTaskCodingSitesOverRun(replicateData):
    datFileContents = getOrganisms(replicateData)
    (organisms,analyzedOrganism) = (datFileContents[:-1],datFileContents[-1])

    #Next step: add Avida Parameters and Replicate ID

    organismsTasks = getTasks(analyzedOrganism)

    genomeLength = getLength(replicateData)

    codingSites = np.zeros((genomeLength,len(organismsTasks)))
    for idx, org in enumerate(organisms):
        #Note that the absolute value is only being taken of the difference, so it should be proper
        
        comparison = np.abs(organismsTasks - getTasks(org))
        codingSites[idx,:] = comparison

    return codingSites

def writeTaskCodingSites(runDir,codingSites):
    writeDirectory = os.path.join(runDir,"data/codingSites.txt")
    with open(writeDirectory,'w') as f:
        lengthOfGenome = codingSites.shape[0]
        codingSitesToWrite = []
        
        for j in range(codingSites.shape[1]):
            possibleSites = np.arange(lengthOfGenome)
            sitesOfCoding = np.where(codingSites[:,j] > 0)
            codingSitesToWrite.append(possibleSites[sitesOfCoding])

        for k, blank in enumerate(codingSitesToWrite):
            for site in codingSitesToWrite[k]:
                f.write('{},'.format(site))
            f.write('\n')

def writeExperimentTaskCodingSites(treatmentArray):
    for treatment in treatmentArray:
        treatmentName = treatment.treatmentName
        print(treatmentName)
        
        for runDir in treatment.runDirectories:
            createDatAnalyzeCfg(runDir)
            executeInfoAnalysis(runDir)
            
        treatmentData = []
        for runDir in treatment.runDirectories:
            replicateData = os.path.join(runDir,"data/detail_Org0FitnessDifferences.dat")
            taskCodingSites = getTaskCodingSitesOverRun(replicateData)
            writeTaskCodingSites(runDir,taskCodingSites)

linDatFile = ".dat"

writeExperimentTaskCodingSites(Treatments)




