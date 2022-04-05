import os
import csv
import sys

dataDir = './'
runDirectories = []
Treatments = []
treatmentParameters = {"Baseline-Treatment":[0.0025, 0.0, 0.0, 0.05, 0.05, 0.0, 0],
"Slip-NOP":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 1],
"Slip-duplicate":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0],
"Slip-scatter":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 5],
"Slip-scramble":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 3],
"Slip-random":[0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 2],
"High-Mutation":[0.0025,0.0075,0.0075,0.05,0.05,0.0,0]}

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


#List slicing goes up to but does not include the last element!!
def countTasks(organismString):
    presentTasks = 0

    analyzeOutputs = organismString.split()
    if(len(analyzeOutputs) == 16):
        tasks = analyzeOutputs[2:11]
    elif(len(analyzeOutputs) == 17):
        tasks = analyzeOutputs[3:12]
    else:
        print("Improper Data String Length")
        sys.exit(0)

    for task in tasks:
        if int(task) != 0:
            presentTasks +=1
    return presentTasks

def getOrganismID(organismString):
    analyzeOutputs = organismString.split()
    ID = analyzeOutputs[0]
    return ID

def getUpdateBorn(organismString):
    analyzeOutputs = organismString.split()
    updateBorn = analyzeOutputs[1]
    return updateBorn

def makeTidy(treatmentArray):
    with open('FinalDominantTaskCounts.csv', mode='w') as tidyDat:

        data_writer = csv.writer(tidyDat, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['Treatment',"COPY_MUT_PROB","COPY_INS_PROB","COPY_DEL_PROB","DIVIDE_INS_PROB","DIVIDE_DEL_PROB","DIVIDE_SLIP_PROB","SLIP_FILL_MODE",'Replicate #','Organism ID','Update Born','Task Count'])

        for treatment in treatmentArray:
            treatmentName = treatment.treatmentName
            
            treatmentData = []
            for runDir in treatment.runDirectories:
                treatmentData.append(os.path.join(runDir,"data/detail_MostNumerous.dat"))

            for replicateData in treatmentData:
                organisms = getOrganisms(replicateData)


                #Next step: add Avida Parameters and Replicate ID

                for organism in organisms:
                    ID = getOrganismID(organism)
                    updateBorn = getUpdateBorn(organism)
                    numTasks = countTasks(organism)
                    runName = None
                    for folderName in replicateData.split('/'):
                        if 'run_' not in folderName:
                            continue
                        else:
                            runName = folderName
                    runParts = runName.split('_')
                    runNum = runParts[-1]
                    params = treatmentParameters[treatmentName]
                    data_writer.writerow([treatmentName,params[0],params[1],params[2],params[3],params[4],params[5],params[6],runNum,ID,updateBorn,numTasks])

linDatFile = ".dat"

makeTidy(Treatments)




