import os
import csv
import numpy as np


stream = os.popen('pwd')
pwd = stream.read().rstrip()
runDir = pwd

experimentName = pwd.split('/')[-2]

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
    f = open(os.path.join(runDir,'data/codingSites.txt'),'r')
    codingSites = f.readlines()[0].split(',')
    codingSites.pop()

    for k, site in enumerate(codingSites):
        codingSites[k] = int(site)
    codingSites = np.array(codingSites)
    f.close()

    possibleIndices = np.arange(len(genome))
    
    nonCodingIndices = [idx for idx in possibleIndices if idx not in codingSites]
    
    if(doubleKnockoutPrep):
        for instructionIndex in nonCodingIndices:
            knuckOutGenome = knockItOut(genome,instructionIndex)
            knuckOutGenomes.append(knuckOutGenome + '\n')   
            
    else:
        for instructionIndex in nonCodingIndices:
            knuckOutGenome = knockItOut(genome,instructionIndex)   
            knuckOutGenomes.append('LOAD_SEQUENCE ' + knuckOutGenome + '\n')
    
    if(doubleKnockoutPrep):
        singleKnockoutFile = open(os.path.join(runDir,"data/singleKnockouts.dat"),'w')
        singleKnockoutFile.writelines(knuckOutGenomes)
        singleKnockoutFile.close()
    
    else:
        knuckOutGenomes.append('LOAD_SEQUENCE ' + genome + '\n')
        configFile = open(os.path.join(runDir,'data/informationAnalyzer.cfg'),'a')
        configFile.write('SET_BATCH {} \n\n'.format(orgCount))
        configFile.writelines(knuckOutGenomes)
        configFile.write('RECALC\n\n')
        configFile.write('DETAIL detail_Org{}FitnessDifferences.dat task_list gest_time comp_merit merit fitness efficiency viable length\n\n'.format(orgCount))
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
        f.close()

        knockoutDatFile(runDir, True)
        knockoutDatFile(runDir)

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

def runDoubleKnockoutAnalysis():
        createDatDoubleKnockoutAnalyzeCfg(runDir)
        executeInfoAnalysis(runDir)
            
linDatFile = ".dat"

runDoubleKnockoutAnalysis()