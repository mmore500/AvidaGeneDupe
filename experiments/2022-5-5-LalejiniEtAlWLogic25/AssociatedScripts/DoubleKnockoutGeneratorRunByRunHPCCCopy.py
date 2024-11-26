import os
import csv
import numpy as np


stream = os.popen('pwd')
pwd = stream.read().rstrip()
runDir = pwd

experimentName = pwd.split('/')[-3]

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

def knockItOut(genomeString,instructionIndex):
    knuckOutGenome = list(genomeString)
    knuckOutGenome[instructionIndex] = 'A'
    return "".join(knuckOutGenome)

def knockoutDatGenome(runDir,genome,orgCount, doubleKnockoutPrep = False):
    knuckOutGenomes = []
    
    if(doubleKnockoutPrep):
        for instructionIndex in np.arange(len(genome)):
            knuckOutGenome = knockItOut(genome,instructionIndex)
            knuckOutGenomes.append(knuckOutGenome + '\n')   
            
    else:
        for instructionIndex in np.arange(len(genome)):
            knuckOutGenome = knockItOut(genome,instructionIndex)   
            knuckOutGenomes.append('LOAD_SEQUENCE ' + knuckOutGenome + '\n')
    
    if(doubleKnockoutPrep):
        singleKnockoutFile = open(os.path.join(runDir,"data/singleKnockouts.dat"),'w')
        singleKnockoutFile.writelines(knuckOutGenomes)
        singleKnockoutFile.close()
    
    else:
        knuckOutGenomes.append('LOAD_SEQUENCE ' + genome + '\n')
        configFile = open(os.path.join(runDir,'data/doubleKnockoutInformationAnalyzer.cfg'),'a')
        configFile.write('SET_BATCH {} \n\n'.format(orgCount))
        configFile.writelines(knuckOutGenomes)
        configFile.write('RECALC\n\n')
        configFile.write('DETAIL detail_DoubleOrg{}FitnessDifferences.dat task_list gest_time comp_merit merit fitness efficiency viable length\n\n'.format(orgCount))
        configFile.close()
        
        
def knockoutDatFile(runDir, doubleKnockoutPrep = False):
    #os.system('pwd')
    if(doubleKnockoutPrep):
        datFile = os.path.join(runDir,"data/detail_MostNumerous.dat")
    else:
        datFile = os.path.join(runDir,"data/singleKnockouts.dat")
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
            if(doubleKnockoutPrep):
                knockoutDatGenome(runDir, genome, orgCount, True)
            else:
                knockoutDatGenome(runDir,genome,orgCount)
            orgCount+=1

def createDatDoubleKnockoutAnalyzeCfg(runDir):
        datDir = os.path.join(runDir,"data")
        configFile = os.path.join(datDir,'doubleKnockoutInformationAnalyzer.cfg')
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
        f.close()

        knockoutDatFile(runDir, True)
        knockoutDatFile(runDir)

def executeInfoAnalysis(runDir):
    os.chdir(runDir)
    os.system("./avida -set ANALYZE_FILE data/doubleKnockoutInformationAnalyzer.cfg -a > doubleKnockoutAnalyze.log")
    os.system('rm avida')
    os.system('rm avida.cfg')
    os.system('rm default-heads.org')
    os.system('rm environment.cfg')
    os.system('rm events.cfg')
    os.system('rm instset-heads___sensors_NONE.cfg')

def runDoubleKnockoutAnalysis():
        createDatDoubleKnockoutAnalyzeCfg(runDir)
        executeInfoAnalysis(runDir)
            
linDatFile = ".dat"

runDoubleKnockoutAnalysis()