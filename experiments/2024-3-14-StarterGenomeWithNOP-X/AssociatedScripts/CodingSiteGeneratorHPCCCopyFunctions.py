'''
CodingSiteGeneratorHPCCCopyFunctions.py
Author: Cameron Haynes
Initial Date: 04/18/2024

The user-defined functions used in CodingSiteGeneratorHPCCCopy.py
'''

import os
import csv
import numpy as np
import pandas as pd
import sys
import uuid


#Use r"Path" to avoid any problems from special characters
def getOrganisms(filePath):
    '''
    Algorithm
    1. The data file, output from Avida analyze mode, is opened
    and the lines read into a list.
    2. The list of lines is iterated through until the first line
    without a '#' or '\n' at the beginning is found
    3. The index of that line is stored as initialOrgPos
    4. Then, the rest of the lines in the file are read into a list
    called organisms, each one representing the data for a given
    organism in a lineage
    5. This list of organism data lines is checked for non-emptiness
    and then it is returned.
    '''

    '''
    1. The data file, output from Avida analyze mode, is opened
    and the lines read into a list.
    '''
    with open(filePath,'r') as datFile:
        lines = datFile.readlines()

        '''
        2. The list of lines is iterated through until the first line
        without a '#' or '\n' at the beginning is found
        '''
        initalOrgPos = 0
        for k,line in enumerate(lines):
            if (line[0] != '') & (line[0] != '#') & (line[0] != '\n'):
                '''
                3. The index of that line is stored as initialOrgPos
                '''
                initialOrgPos = k
                break
            else:
                continue
        
        '''
        4. Then, the rest of the lines in the file are read into a list
        called organisms, each one representing the data for a given
        organism in a lineage
        '''
        organisms = []
        for i in range(initialOrgPos,len(lines)):
            if(lines[i] != ''):
                organisms.append(lines[i])
            else:
                continue

        '''
        5. This list of organism data lines is checked for non-emptiness
        and then it is returned.
        '''
        if(len(organisms) > 0):
            return organisms
        else:
            print("Error: please check code")

'''
def getDatFileHeaders(datFile):
    with open(datFile,'r') as dataF:
        datFileLines = dataF.readlines()
        formatLineTerms = (datFileLines[1].split())[1:-1]
        for k,term in enumerate(formatLineTerms):
            if term == 'task_list':
                formatLineTerms[k] = 'Task Count'
        return formatLineTerms
'''

def getOrganismID(organismString):
    '''
    Algorithm
    1. The input organism data line is split into its components.
    2. The ID is extracted from the first element on the
    line; this is then returned.
    '''
    analyzeOutputs = organismString.split()
    ID = analyzeOutputs[0]
    return ID

def getUpdateBorn(organismString):
    '''
    Algorithm
    1. The input organism data line is split into its components.
    2. The update born is extracted from the second element on the
    line; this is then returned.
    '''

    '''
    1. The input organism data line is split into its components.
    '''
    analyzeOutputs = organismString.split()

    '''
    2. The update born is extracted from the second element on the
    line; this is then returned.
    '''
    updateBorn = analyzeOutputs[1]
    return updateBorn

def getLength(runDir):
    '''
    Algorithm
    1. Assembles path to the data using the timepoint "desiredUpdateToAnalyze"
      passed into the command-line when script was run.
    2. getOrganisms() is used to extract a list of organism data lines from
    the data folder.
    3. The original organism is found at the end of that list.
    4. The original organism data line is split and the length is extracted
    from the second-to-last item. That value is returned as an integer.
    '''

    '''
    1. Assembles path to the data using the timepoint "desiredUpdateToAnalyze"
      passed into the command-line when script was run.
    '''
    replicateData = os.path.join(runDir, f'Timepoint_{desiredUpdateToAnalyze}/data/detail_MostNumerousAt{desiredUpdateToAnalyze}.dat')

    '''
    2. getOrganisms() is used to extract a list of organism data lines from
    the data folder.
    '''
    datFileContents = getOrganisms(replicateData)

    '''
    3. The original organism is found at the end of that list.
    '''
    analyzedOrganism = datFileContents[-1]

    '''
    4. The original organism data line is split and the length is extracted
    from the second-to-last item. That value is returned as an integer.
    '''
    #-2 is used here because the length is being pulled from the MostNumerous.dat file in which the length is second-to-last
    length = int(analyzedOrganism.split()[-2])
    return length

def getViability(organism):
    '''
    Algorithm
    1. The organism data line is split into its components and the viability
    is extracted from the second-to-last item; it's type-casted and returned
    as an integer.
    '''
    #-2 is used here because the viability is being pulled from the knockout analysis file in which the viability is second-to-last
    viability = int(organism.split()[-2])
    return viability

def getGenome(runDir):
    '''
    Algorithm
    1. Assembles path to the data using the timepoint "desiredUpdateToAnalyze"
      passed into the command-line when script was run.
    2. getOrganisms() is used to extract a list of organism data lines from
    the data folder.
    3. The original organism is found at the end of that list.
    4. Then, the original organism's genome is found at the end of the
    data line; this is the value that's returned.
    '''

    '''
    1. Assembles path to the data using the timepoint "desiredUpdateToAnalyze"
      passed into the command-line when script was run.
    '''
    replicateData = os.path.join(runDir, f'Timepoint_{desiredUpdateToAnalyze}/data/detail_MostNumerousAt{desiredUpdateToAnalyze}.dat')
    
    '''
    2. getOrganisms() is used to extract a list of organism data lines from
    the data folder.
    '''
    datFileContents = getOrganisms(replicateData)

    '''
    3. The original organism is found at the end of that list.
    '''
    analyzedOrganism = datFileContents[-1]
    
    '''
    4. Then, the original organism's genome is found at the end of the
    data string; this is the value that's returned.
    '''
    #-2 is used here because the length is being pulled from the MostNumerous.dat file in which the length is second-to-last
    genome = analyzedOrganism.split()[-1]
    return genome
    
def knockItOut(genomeString,instructionIndex):
    '''
    Algorithm
    1. Split the genome string into a list of its characters
    2. Replace the character at instructionIndex with 'A'
    3. Join the list of characters into a new string and return that string.
    '''

    #1. Split the genome string into a list of its characters
    knuckOutGenome = list(genomeString)

    #2.Replace the character at instructionIndex with 'A'
    knuckOutGenome[instructionIndex] = 'A'

    #3. Join the list of characters into a new string and return that string.
    return "".join(knuckOutGenome)


def knockoutDatGenome(dest,genome,orgCount):
    '''
knockoutDatGenome():
Generates a series of knockout genomes from an original genome and writes them, line-by-line, to a destination file.

Definition: A knockout genome is a mutation of an original genome where a NOP-X (an instruction that doesn't do anything)
has been substituted for one of the original instructions. This function creates one knockout genome for every instruction
in the original genome, going from left-to-right.

Here's an example (note: the single-letter representation of NOP-X is 'A')

Original Genome: 'abcdef'
1st Knockout Genome: 'Abcdef'
2nd Knockout Genome: 'aAcdef'
3rd Knockout Genome: 'abAdef'
...
6th Knockout Genome: 'abcdeA'

An n-instruction original genome will thus have n knockout genomes created from it in the manner shown in the example above.

Parameters
dest:= the file that the knockout genomes will be written to, line-by-line. This is always informationAnalyzer.cfg in this script.
genome:= the original genome that knockout genomes are being made from
orgCount:= the number of organisms that have been through the knockout process from the input Analyze mode data file; this allows
knockoutDatGenome() to separate each organism in a lineage into its own batch for Analyze mode to process

'''
    '''
    Algorithm
    1. Knockout genomes are generated one-by-one by applying knockItOut() to each instruction in the genome
        a. The resultant knockout genome is integrated into a string with the Analyze mode 'LOAD_SEQUENCE' command
        and then stored in a list for writing to informationAnalyzer.cfg
        b. The original genome is also included at the very end so that its data can be used for comparison with the
        knockout genomes.
    2. The 'SET_BATCH' Analyze mode command is written to informationAnalyzer.cfg before the 'LOAD_SEQUENCE' commands
    containing the new knockout genomes are so that the knockout genomes will be analyzed and their data displayed as
    a unit in one output file. This uses orgCount to determine the batch number.
    3. The new 'LOAD_SEQUENCE' commands for knockout genomes and the original genome are written to informationAnalyzer.cfg
    4. Final commands that are necessary for Analyze mode to generate data about the knockout genomes are written
        a. RECALC, which runs the loaded sequences through a series of tests to generate data about them
        b. DETAIL, which prints the specified data that are desired line-by-line in detail_...dat
    '''
    
    knuckOutGenomes = []

    '''
    1. Knockout genomes are generated one-by-one by applying knockItOut() to each instruction in the genome
    '''
    for instructionIndex,inst in enumerate(genome):
        knuckOutGenome = knockItOut(genome,instructionIndex)

        '''
        a. The resultant knockout genome is integrated into a string with the Analyze mode 'LOAD_SEQUENCE' command
        and then stored in a list for writing to informationAnalyzer.cfg
        '''
        knuckOutGenomes.append('LOAD_SEQUENCE ' + knuckOutGenome + '\n')
    #NOTE: This is another debugging artifact
    writeFile = dest

    '''
    b. The original genome is also included at the very end so that its data can be used for comparison with the
        knockout genomes.
    '''
    knuckOutGenomes.append('LOAD_SEQUENCE ' + genome + '\n')

    '''
    2. The 'SET_BATCH' Analyze mode command is written to informationAnalyzer.cfg before the 'LOAD_SEQUENCE' commands
    containing the new knockout genomes are so that the knockout genomes will be analyzed and their data displayed as
    a unit in one output file. This uses orgCount to determine the batch number.
    '''
    dest.write('SET_BATCH {} \n\n'.format(orgCount))

    '''
    3. The new 'LOAD_SEQUENCE' commands for knockout genomes and the original genome are written to
      informationAnalyzer.cfg
    '''
    dest.writelines(knuckOutGenomes)

    '''
    4. Final commands that are necessary for Analyze mode to generate data about the knockout genomes are written
    '''
    '''
    a. RECALC, which runs the loaded sequences through a series of tests to generate data about them
    '''
    dest.write('RECALC\n\n')

    '''
    b. DETAIL, which prints the specified data that are desired line-by-line in detail_...dat
    '''
    dest.write('DETAIL detail_Org{}FitnessDifferences.dat task_list gest_time comp_merit merit fitness efficiency viable length\n\n'.format(orgCount))


def knockoutDatFile(datFile,dest):

    '''
    Algorithm
    1. Read the lines of the dominant organism or dominant lineage output file into a list
    2. For each line, if it describes an organism:
        a. Parse the line to extract the organism's genome
        b. Generate a series of knockout genomes for that organism and writes them to the provided destination file
        c. Update the count of organisms read to inform knockoutDatGenome()'s next execution
    '''

    #NOTE: This is another debugging artifact
    #os.system('pwd')
    '''
    1. Read the lines of the dominant organism or dominant lineage output file into a list
    '''
    with open(datFile,'r') as X:
        lines = X.readlines()
        
        '''
        2. For each line,
        '''
        orgCount = 0
        for k,line in enumerate(lines):
            '''
            if it describes an organism
            '''
            if('#' in line):
                continue
            if(len(line) <= 1):
                continue

            '''
            a. Parse the line to extract the organism's genome
            '''
            orgData = line.split()
            genome = orgData[-1]

            '''
            b. Generate a series of knockout genomes for that organism and writes them to the provided destination file
            '''
            knockoutDatGenome(dest,genome,orgCount)

            '''
            c. Update the count of organisms read to inform knockoutDatGenome()'s next execution
            '''
            orgCount+=1


def createDatAnalyzeCfg(runDir):
    
    '''
    Algorithm
    1. Create variables to store the path to the data and the path for writing informationAnalyzer.cfg
    2. Open a file stream object to write informationAnalyzer.cfg
    3. Write the Analyze mode configuration file preamble to informationAnalyzer.cfg
    4. Use the data to write the original and knockout genomes to be analyzed
    by Avida Analyze mode into informationAnalyzer.cfg
    '''

    '''
    1. Create variables to store the path to the data and the path for writing informationAnalyzer.cfg
    '''
    datDir = os.path.join(runDir,f"Timepoint_{desiredUpdateToAnalyze}")
    datFile = os.path.join(datDir,f"data/detail_MostNumerousAt{desiredUpdateToAnalyze}.dat")
    configFile = os.path.join(datDir,'informationAnalyzer.cfg')

    '''
    2. Open a file stream object to write informationAnalyzer.cfg
    '''
    f = open(configFile,'w')

    '''
    3. Write the Analyze mode configuration file preamble to informationAnalyzer.cfg
    '''
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
    
    '''
    4. Use the data to write the original and knockout genomes to be analyzed
        by Avida Analyze mode into informationAnalyzer.cfg
    '''
    knockoutDatFile(datFile,f)

def executeInfoAnalysis(runDir):
    '''
    Algorithm
    1. On the HPCC, load the gcc-11.2 C++ compiler to accommodate the
    version requirements of the project's version of Avida.
    2. Assemble the path to the directory with data.
    3. Assemble the path to the directory with configuration files
    4. Copy the Avida executable from the avida directory
    5. Change the shell working directory to the directory
    with data.
    6. Copy the configuration files to the directory with data.
    7. Run Avida in analyze mode using informationAnalyzer.cfg,
    the file output by createDatAnalyzeCfg(), as its config file;
    this runs each knockout organism in Analyze mode to generate
    information about its viability and tasks.
    8. Remove all the configuration files and the Avida executable
    '''

    '''
    1. On the HPCC, load the gcc-11.2 C++ compiler to accommodate the
    version requirements of the project's version of Avida.
    '''
    os.system('module load gcc/11.2.0')

    '''
    2. Assemble the path to the directory with data.
    '''
    timepointRunDir = os.path.join(runDir, f"Timepoint_{desiredUpdateToAnalyze}")

    '''
    3. Assemble the path to the directory with configuration files
    '''
    configDir = os.path.join("~/Documents/AvidaGeneDupe/experiments/","{}/hpcc/config".format(experimentName))

    '''
    4. Copy the Avida executable from the avida directory
    '''
    os.system("cp ~/Documents/AvidaGeneDupe/avida/cbuild/work/avida {}".format(timepointRunDir))

    '''
    5. Change the shell working directory to the directory
    with data.
    '''
    os.chdir(timepointRunDir)

    '''
    6. Copy the configuration files to the directory with data.
    '''
    os.system('cp {}/avida.cfg .'.format(configDir)) 
    os.system('cp {}/default-headsWithNOP-X.org .'.format(configDir))
    os.system('cp {}/environment.cfg .'.format(configDir))
    os.system('cp {}/events.cfg .'.format(configDir))
    os.system('cp {}/instset-heads___sensors_NONE.cfg .'.format(configDir))

    '''
    7. Run Avida in analyze mode using informationAnalyzer.cfg,
    the file output by createDatAnalyzeCfg(), as its config file;
    this runs each knockout organism in Analyze mode to generate
    information about its viability and tasks.
    '''
    os.system(f"./avida -set ANALYZE_FILE informationAnalyzer.cfg -a > analyze.log")

    '''
    8. Remove all the configuration files and the Avida executable
    '''
    os.system('rm avida')
    os.system('rm avida.cfg')
    os.system('rm default-headsWithNOP-X.org')
    os.system('rm environment.cfg')
    os.system('rm events.cfg')
    os.system('rm instset-heads___sensors_NONE.cfg')


def getTasks(organismString):
    '''
    Algorithm
    1. 
    '''
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

'''
def writeTaskCodingSites(runDir,codingSites):
    writeDirectory = os.path.join(runDir,f"Timepoint_{desiredUpdateToAnalyze}/data/codingSites.txt")
    with open(writeDirectory,'w') as f:
        for site in codingSites:
            f.write('{},'.format(site))
'''

def writeExperimentTaskCodingSites(treatmentArray):
    
    '''
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