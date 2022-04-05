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
def getTimeCourse(filePath):
    with open(filePath,'r') as datFile:
        timeCourse = dict()

        lines = datFile.readlines()
        for k,line in enumerate(lines):
            if('#' in line):
                continue
            if(len(line) <= 1):
                continue
            presentTasks = 0
            analyzeOutputs = line.split()
            for k in range(1,len(analyzeOutputs)):
                if float(analyzeOutputs[k]) > 0.25*3600:
                    presentTasks +=1
            timeCourse[analyzeOutputs[0]] = presentTasks

        if(len(timeCourse) > 0):
            return timeCourse
        else:
            print("Error in getting Timecourse: please check code")



def makeTidy(treatmentArray):
    with open('TaskCountTimeCourse.csv', mode='w') as tidyDat:

        data_writer = csv.writer(tidyDat, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['Treatment',"COPY_MUT_PROB","COPY_INS_PROB","COPY_DEL_PROB","DIVIDE_INS_PROB","DIVIDE_DEL_PROB","DIVIDE_SLIP_PROB","SLIP_FILL_MODE",'Replicate #','Time','Tasks Present'])

        for treatment in treatmentArray:
            treatmentName = treatment.treatmentName
            
            treatmentData = []
            for runDir in treatment.runDirectories:
                treatmentData.append(os.path.join(runDir,"data/tasks.dat"))

            for replicateData in treatmentData:
                timeCourse = getTimeCourse(replicateData)


                #Next step: add Avida Parameters and Replicate ID

                for time in timeCourse.keys():
                    numTasks = timeCourse[time]
                    runName = None
                    for folderName in replicateData.split('/'):
                        if 'run_' not in folderName:
                            continue
                        else:
                            runName = folderName
                    runParts = runName.split('_')
                    runNum = runParts[-1]
                    params = treatmentParameters[treatmentName]
                    data_writer.writerow([treatmentName,params[0],params[1],params[2],params[3],params[4],params[5],params[6],runNum,time,numTasks])

linDatFile = ".dat"

makeTidy(Treatments)




