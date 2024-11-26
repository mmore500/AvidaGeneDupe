import os
import csv
import numpy as np

dataDir = '/Users/cameronhaynes/Documents/VSCodeGitProjects/AvidaGeneDupe/experiments/2022-2-4-PaperDuplicationWMod/testResults'
runDirectories = []
Treatments = []
treatmentParameters = {"Baseline-Treatment":[0.0025, 0.0, 0.0, 0.05, 0.05, 0.0, 0],
"Slip-NOP":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 1]}

class Treatment():
    def __init__(self,treatmentPath):
        self.treatmentDir = treatmentPath
        self.runDirectories = []
        self.treatmentName = self.treatmentDir.split('/')[-1]

for subdir in os.listdir(dataDir):
    if '.' in subdir:
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
        formatLineTerms = (datFileLines[1].split())[1:]
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
    return (genomeString[:instructionIndex] + genomeString[instructionIndex + 1:])

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
    dest.write('DETAIL detail_Org{}FitnessDifferences.dat task_list gest_time comp_merit merit fitness efficiency length\n\n'.format(orgCount))

def knockoutDatFile(datFile,dest):
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

def createDatAnalyzeCfg(datFile):
        f = open('informationAnalyzer.cfg','w')
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
    configDir = "/Users/cameronhaynes/Documents/VSCodeGitProjects/AvidaGeneDupe/experiments/2022-2-4-PaperDuplicationWMod/testResults/hpcc/config"
    os.system("cp /Users/cameronhaynes/Documents/VSCodeGitProjects/AvidaGeneDupe/avida/cbuild/work/avida {}".format(runDir))
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

def getInformation(replicateData):
    datFileContents = getOrganisms(replicateData)
    (organisms,analyzedOrganism) = (datFileContents[:-1],datFileContents[-1])

    #Next step: add Avida Parameters and Replicate ID

    organismsMetrics = getMetrics(analyzedOrganism)
    information = np.zeros(organismsMetrics.size)
    for org in organisms:
        #Note that the absolute value is only being taken of the difference, so it should be proper
        information = information + np.abs(organismsMetrics + (-1*getMetrics(org)))
    
    return information

def getCodingSites(replicateData):
    datFileContents = getOrganisms(replicateData)
    (organisms,analyzedOrganism) = (datFileContents[:-1],datFileContents[-1])

    #Next step: add Avida Parameters and Replicate ID

    organismsMetrics = getMetrics(analyzedOrganism)
    codingSites = np.zeros(organismsMetrics.size)
    for org in organisms:
        #Note that the absolute value is only being taken of the difference, so it should be proper
        comparedMetrics = getMetrics(org)
        codingSitesPresent = [1 if (organismsMetrics[k] - comparedMetrics[k]) != 0 else 0 for k in range(0,organismsMetrics.size)]
        codingSites = codingSites + np.array(codingSitesPresent)
    
    return codingSites

def getLength(replicateData):
    datFileContents = getOrganisms(replicateData)
    analyzedOrganism = datFileContents[-1]
    
    length = int(analyzedOrganism.split()[-1])
    return length

def informAndMakeTidy(treatmentArray, useCodingSites = True):
    with open('FinalDominantInfo.csv', mode='w') as tidyDat:

        data_writer = csv.writer(tidyDat, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['Treatment',"COPY_MUT_PROB","COPY_INS_PROB","COPY_DEL_PROB","DIVIDE_INS_PROB","DIVIDE_DEL_PROB","DIVIDE_SLIP_PROB","SLIP_FILL_MODE",'Replicate #','Information Type','Information Concentration'])

        for treatment in treatmentArray:
            treatmentName = treatment.treatmentName
            
            for runDir in treatment.runDirectories:
                dataDir = os.path.join(runDir,"data")
                infoFile = os.path.join(dataDir,"detail_MostNumerous.dat")
                os.chdir(dataDir)
                createDatAnalyzeCfg(infoFile)
                executeInfoAnalysis(runDir)
                
            
            treatmentData = []
            for runDir in treatment.runDirectories:
                treatmentData.append(os.path.join(runDir,"data/detail_Org0FitnessDifferences.dat"))

            for replicateData in treatmentData:
                information = getCodingSites(replicateData) if useCodingSites else getInformation(replicateData)
                length = getLength(replicateData)
                runName = None
                for folderName in replicateData.split('/'):
                    if 'run_' not in folderName:
                        continue
                    else:
                        runName = folderName
                runParts = runName.split('_')
                runNum = runParts[-1]
                infoTypes = getDatFileHeaders(replicateData)
                for k,type in enumerate(infoTypes):
                    data_writer.writerow([treatmentName,*treatmentParameters[treatmentName],runNum,type,information[k],information[k]/length]])
                

linDatFile = ".dat"

informAndMakeTidy(Treatments)




