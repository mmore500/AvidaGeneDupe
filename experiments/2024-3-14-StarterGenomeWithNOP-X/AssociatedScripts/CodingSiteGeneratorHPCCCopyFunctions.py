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


desiredUpdateToAnalyze = None
'''
None is the default setting; when CodingSiteGeneratorHPCCCopy.py
is run, it is changed to the desired update by accessing this
module's namespace.
'''

#Use r"Path" to avoid any problems from special characters
def getOrganisms(filePath):
    '''
    Extracts organism data lines from an Avida data file.

    Parameters:
    filePath (str): Path to the Avida data file.

    Returns:
    list: List of organism data lines.
    '''

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
        initialOrgPos = None
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

        if initialOrgPos is not None:
          for i in range(initialOrgPos,len(lines)):
              if(lines[i] != ''):
                  if(list(lines[i])[-1] == '\n'):
                      lines[i] = lines[i][:-1]
                  organisms.append(lines[i])
              else:
                  continue

        '''
        5. This list of organism data lines is checked for
          non-emptiness and then it is returned.
        '''
        return organisms

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
    Extracts the ID of an organism from its data line.

    Parameters:
    organismString (str): Organism data line.

    Returns:
    str: Organism ID.
    '''

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
    Extracts the update born of an organism from its data line.

    Parameters:
    organismString (str): Organism data line.

    Returns:
    str: Update born of the organism.
    '''

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

def getLength(organismString):
    '''
    Gets the length of the specified organism's genome.

    Parameters:
    organismString (str): Organism data line

    Returns:
    int: Length of the genome.
    '''

    '''
    Algorithm
    1. The organism data line is split and the length
       is extracted from the second-to-last item. That value is
       returned as an integer.
    '''

    if len(organismString) == 0:
        raise IndexError("Your organism data line is empty")

    if len(organismString) == 1:
        raise IndexError("Your organism data line should have more than one element")

    #-2 is used here because the length is being pulled from the MostNumerous.dat file in which the length is second-to-last
    try:
      length = int(organismString.split()[-2])
    except(ValueError) as err:
        raise ValueError("Your data file has a non-integer where the integer length should be.") from err
    
    if length >= 1500:
        raise Exception("Length value too large: index used to retrieve length is likely wrong")
    
    return length

def getViability(organismString):
    '''
    Extracts the viability of an organism from its data.

    Parameters:
    organism (str): Organism data line.

    Returns:
    int: Viability of the organism.
    '''

    '''
    Algorithm
    1. The organism data line is split into its components
      and the viability is extracted from the second-to-last item;
        it's type-casted and returned as an integer.
    '''
    #-2 is used here because the viability is being pulled from the knockout analysis file in which the viability is second-to-last
    viability = int(organismString.split()[-2])
    return viability

def getGenome(organismString):
    '''
    Gets the genome of the specified organism.

    Parameters:
    organismString (str): Organism data line

    Returns:
    str: Genome of the specified organism.
    '''

    '''
    Algorithm
    1. Then, the original organism's genome is found at the end of the
    data line; this is the value that's returned.
    '''
    if len(organismString) == 0:
        raise IndexError("Your organism data line is empty")
    elif len(organismString.split()) == 0:
        raise IndexError("Your organism data line has no characters but spaces")
    
    genome = organismString.split()[-1]

    if not genome.isalpha():
        raise Exception("Genome should only be made of alphabet characters")

    return genome
    
def knockItOut(genomeString,instructionIndex):
    '''
    Creates a knockout genome by replacing a character in the genome.

    Parameters:
    genomeString (str): Original genome.
    instructionIndex (int): Index of the instruction to be replaced.

    Returns:
    str: Knockout genome.
    '''

    '''
    Algorithm
    1. Split the genome string into a list of its characters
    2. Replace the character at instructionIndex with 'A'
    3. Join the list of characters into a new string and
      return that string.
    '''

    if instructionIndex < 0:
        raise IndexError("You must generate knockouts going forward")

    #1. Split the genome string into a list of its characters
    knuckOutGenome = list(genomeString)

    #2.Replace the character at instructionIndex with 'A'
    knuckOutGenome[instructionIndex] = 'A'

    #3. Join the list of characters into a new string and return that string.
    return "".join(knuckOutGenome)


def knockoutDatGenome(dest,genome,orgCount):
    '''
    Generates a series of knockout genomes from an original genome
    and writes them, line-by-line, to a destination file.

    Definition: A knockout genome is a mutation of an original genome
    where a NOP-X (an instruction that doesn't do anything)
    has been substituted for one of the original instructions. This 
    function creates one knockout genome for every instruction
    in the original genome, going from left-to-right.

    Here's an example
    (note: the single-letter representation of NOP-X is 'A')
    Original Genome: 'abcdef'
    1st Knockout Genome: 'Abcdef'
    2nd Knockout Genome: 'aAcdef'
    3rd Knockout Genome: 'abAdef'
    ...
    6th Knockout Genome: 'abcdeA'

    An n-instruction original genome will thus have n knockout genomes
    created from it in the manner shown in the example above.

    Parameters
    dest:= the file that the knockout genomes will be written to,
    line-by-line. This is always informationAnalyzer.cfg in this script
    genome:= the original genome used as template for knockout genomes
    orgCount:= the number of organisms that have been through the
    knockout process from the input Analyze mode data file
    '''

    '''
    Algorithm
    1. Knockout genomes are generated one-by-one by applying knockItOut()
       to each instruction in the genome
        a. The resultant knockout genome is integrated into a string
           with the Analyze mode 'LOAD_SEQUENCE' command
           and then stored in a list for writing to
           informationAnalyzer.cfg
        b. The original genome is also included at the very end so
           that its data can be used for comparison with the
           knockout genomes.
    2. The 'SET_BATCH' Analyze mode command is written to
       informationAnalyzer.cfg before the 'LOAD_SEQUENCE' commands
       containing the new knockout genomes are so that the knockout
        genomes will be analyzed and their data displayed as a unit in
        one output file. This uses orgCount to determine the
        batch number.
    3. The new 'LOAD_SEQUENCE' commands for knockout genomes and the
      original genome are written to informationAnalyzer.cfg
    4. Final commands that are necessary for Analyze mode to generate
      data about the knockout genomes are written
        a. RECALC, which runs the loaded sequences through a series
          of tests to generate data about them
        b. DETAIL, which prints the specified data that are desired
          line-by-line in detail_...dat
    '''
    
    knuckOutGenomes = []

    '''
    1. Knockout genomes are generated one-by-one by applying
      knockItOut() to each instruction in the genome
    '''
    for instructionIndex,inst in enumerate(genome):
        knuckOutGenome = knockItOut(genome,instructionIndex)

        '''
        a. The resultant knockout genome is integrated into a string
          with the Analyze mode 'LOAD_SEQUENCE' command and then
          stored in a list for writing to informationAnalyzer.cfg
        '''
        knuckOutGenomes.append('LOAD_SEQUENCE ' + knuckOutGenome + '\n')

    '''
    b. The original genome is also included at the very end so that
      its data can be used for comparison with the knockout genomes.
    '''
    knuckOutGenomes.append('LOAD_SEQUENCE ' + genome + '\n')

    '''
    2. Write the 'SET_BATCH' Analyze mode command to 
    informationAnalyzer.cfg before the 'LOAD_SEQUENCE' commands
    containing the new knockout genomes, so that the knockout
    genomes will be analyzed and their data displayed as
    a unit in one output file, using orgCount to determine batch number
    '''
    dest.write('SET_BATCH {} \n\n'.format(orgCount))

    '''
    3. Write the new 'LOAD_SEQUENCE' commands for knockout genomes and
      the original genome to informationAnalyzer.cfg
    '''
    dest.writelines(knuckOutGenomes)

    '''
    4. Final commands that are necessary for Analyze mode to generate
      data about the knockout genomes are written
    '''
    '''
    a. RECALC, which runs the loaded sequences through a series of
      tests to generate data about them
    '''
    dest.write('RECALC\n\n')

    '''
    b. DETAIL, which prints the specified data that are desired
      line-by-line in detail_...dat
    '''
    dest.write('DETAIL detail_Org{}FitnessDifferences.dat task_list gest_time comp_merit merit fitness efficiency viable length\n\n'.format(orgCount))


def knockoutDatFile(datFile,dest):
    '''
    Generates knockout genomes and writes them to a destination file.

    Parameters:
    datFile (str): Path to the Avida data file.
    dest (file object): Destination file for writing knockout genomes.
    '''

    '''
    Algorithm
    1. Read the lines of the dominant organism or dominant lineage
      output file into a list
    2. For each line, if it describes an organism:
        a. Parse the line to extract the organism's genome
        b. Generate a series of knockout genomes for that organism
          and writes them to the provided destination file
        c. Update the count of organisms read to inform
          knockoutDatGenome()'s next execution
    '''

    '''
    1. Read the lines of the dominant organism or dominant lineage
      output file into a list
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
            b. Generate a series of knockout genomes for that
              organism and writes them to the provided destination file
            '''
            knockoutDatGenome(dest,genome,orgCount)

            '''
            c. Update the count of organisms read to inform
              knockoutDatGenome()'s next execution
            '''
            orgCount+=1


def createDatAnalyzeCfg(runDir):
    '''
    Creates an Analyze mode configuration file for Avida.

    Parameters:
    runDir (str): Path to the run directory.
    '''
    
    '''
    Algorithm
    1. Create variables to store the path to the data and the path for
      writing informationAnalyzer.cfg
    2. Open a file stream object to write informationAnalyzer.cfg
    3. Write the Analyze mode configuration file preamble to
      informationAnalyzer.cfg
    4. Use the data to write the original and knockout genomes to be
      analyzed by Avida Analyze mode into informationAnalyzer.cfg
    '''

    '''
    1. Create variables to store the path to the data and the path for
      writing informationAnalyzer.cfg
    '''
    datDir = os.path.join(runDir,f"Timepoint_{desiredUpdateToAnalyze}")
    datFile = os.path.join(datDir,f"data/detail_MostNumerousAt{desiredUpdateToAnalyze}.dat")
    configFile = os.path.join(datDir,'informationAnalyzer.cfg')

    '''
    2. Open a file stream object to write informationAnalyzer.cfg
    '''
    f = open(configFile,'w')

    '''
    3. Write the Analyze mode configuration file preamble
      to informationAnalyzer.cfg
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
    4. Use the data to write the original and knockout genomes
      to be analyzed by Avida Analyze mode into informationAnalyzer.cfg
    '''
    knockoutDatFile(datFile,f)

def executeInfoAnalysis(runDir):
    '''
    Executes Avida in analyze mode to generate data about knockout organisms.

    Parameters:
    runDir (str): Path to the run directory.
    '''

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
    Extracts tasks from an organism's data.

    Parameters:
    organismString (str): Organism data line.

    Returns:
    numpy.ndarray: Array of tasks.
    '''

    '''
    Algorithm
    1. Split the organism data line into its different elements.
    2. In the output of executeInfoAnalysis, the task list is the
    first element -- a string; Convert that into a list
    of numeral characters 
    ('0' for task not present; '1' if task present)
    3. Type-cast each task character into an integer for later use.
    4. Return this list of integers as a NumPy array
    '''

    if len(organismString) == 0:
        raise Exception("Your organism data line is empty")

    '''
    1. Split the organism data line into its different elements.
    '''
    analyzeOutputs = organismString.split()
    
    '''
     2. In the output of executeInfoAnalysis, the task list is the
    first element -- a string; Convert that into a list
    of numeral characters 
    ('0' for task not present; '1' if task present)
    '''
    tasks = list(analyzeOutputs[0])

    '''
    3. Type-cast each task character into an integer for later use.
    '''
    for k,task in enumerate(tasks):
        if (tasks[k] == '0' or tasks[k] == '1'):
          tasks[k] = int(task)
        else:
            raise ValueError("Task count values should be 0 or 1")

    '''
    4. Return this list of integers as a NumPy array
    '''
    return np.array(tasks)

def getTaskCodingSitesOverRun(runDir):
    '''
    Analyzes knockout genomes to identify coding and viability sites.

    Parameters:
    runDir (str): Path to the run directory.

    Returns:
    tuple: Tuple containing coding sites, viability sites, and number of unique coding sites.
    '''

    '''
    Algorithm
    1. Retrieve the output organism data lines from executeInfoAnalysis
        a. Separate the last line, the original organism,
        into a named string variable
    2. Extract the tasks of the original organism
    3. Create objects to hold the coding sites and viability sites data
    4. For each knockout organism
        a. Extract its tasks
        b. Extract its viability and compare it to the original
        organism's viability
        c. If viability has changed (viabilitySite = True), then
        add the index of the knockout site to viabilitySites and do not
        perform coding site analysis.
        d. If viability has not changed (viabilitySite = False), then
        perform coding site analysis as follows.
        e. Iterate through each task
                i. Check to see if the presence of the task has changed
                  between the original organism and the
                  knockout organism.
                ii. If it has, add the index of the knockout site to
                  that task's coding sites list, and mark the
                  codingSite flag as true.
        f. If the codingSite flag is true, increment the count of
        unique coding sites in the genome.
        g. Sort the list of viability site indices in ascending order
        h. Return the coding sites, viability sites, and the number
        of unique coding sites in the genome as a 3-tuple
    '''

    '''
    1. Retrieve the output organism data lines from executeInfoAnalysis
    '''
    replicateData = os.path.join(runDir, f"Timepoint_{desiredUpdateToAnalyze}/data/detail_Org0FitnessDifferences.dat")
    datFileContents = getOrganisms(replicateData)

    '''
    a. Separate the last line, the original organism,
        into a named string variable
    '''
    (knockoutOrganisms,analyzedOrganism) = (datFileContents[:-1],datFileContents[-1])

    '''
    2. Extract the tasks of the original organism
    '''
    organismsTasks = getTasks(analyzedOrganism)
    
    '''
    3. Create objects to hold the coding sites and viability sites data
    '''
    codingSites = [[] for k in range(len(organismsTasks))]

    numCodingSites = 0

    viabilitySites = set()

    '''
    4. For each knockout organism
    '''
    for site, knockoutOrg in enumerate(knockoutOrganisms):
        '''
        a. Extract its tasks
        '''
        knockoutOrganismTasks = getTasks(knockoutOrg)
        
        '''
        b. Extract its viability and compare it to the original
        organism's viability
        '''
        viabilityKnockout = bool(int(getViability(knockoutOrg)))
        viabilityOriginal = bool(int(getViability(analyzedOrganism)))

        #If the viability of the knockout is different than the original, then it is true that the knockout
        #is a viability site
        viabilitySite = not viabilityKnockout == viabilityOriginal

        '''
        c. If viability has changed (viabilitySite = True), then
        add the index of the knockout site to viabilitySites and do not
        perform coding site analysis.
        '''
        if viabilitySite:
            viabilitySites.add(site)
        else:
            '''
            d. If viability has not changed (viabilitySite = False),
            then perform coding site analysis as follows.
            '''
            codingSite = False

            '''
            e. Iterate through each task 
            '''
            for j in range(len(organismsTasks)):
                '''
                i. Check to see if the presence of the task has changed
                  between the original organism and the knockout
                  organism.
                '''
                if organismsTasks[j] != knockoutOrganismTasks[j]:
                    '''
                    ii. If it has, add the index of the knockout site
                    to that task's coding sites list, and mark the
                      codingSite flag as true.
                    '''
                    codingSite = True
                    codingSites[j].append(site)
            
            '''
            f. If the codingSite flag is true, increment the count of
            unique coding sites in the genome.
            '''
            if codingSite:
                numCodingSites = numCodingSites + 1

    '''
    g. Sort the list of viability site indices in ascending order
    '''
    viabilitySites = sorted(list(viabilitySites))

    '''
    h. Return the coding sites, viability sites, and the number
        of unique coding sites in the genome as a 3-tuple
    '''
    return codingSites, viabilitySites, numCodingSites

def writeTaskCodingSitesInPandasDataFrame(treatment, runDir, taskCodingSites, viabilitySites, numUniqueCodingSites):
    '''
    Writes coding and viability sites data to a Pandas dataframe.

    Parameters:
    treatment: Object representing treatment information.
    runDir (str): Path to the run directory.
    taskCodingSites (list): List of coding sites for each task.
    viabilitySites (list): List of viability sites.
    numUniqueCodingSites (int): Number of unique coding sites in the genome.
    '''

    '''
    Algorithm
    1. Extract the run name from the directory path
    2. Enumerate task names to be used for demarcating data rows
    3. Extract the original organism's genome length and its length
    4. Calculate the fractions of the genome occupied by
    coding sites and viability sites, respectively
    5. Compute the ratio of viability sites to coding sites
    6. For each task, add a row to the data frame with the
    Run Name, Task Name, Timepoint, Treatment Name, Coding Sites for
    that task, the number of coding sites for that task, the number of
    unique coding sites in the genome, the Viability Sites of
    the genome, the number of viability sites, and the previously
    computed metrics. Also, report the original genome in
    single-letter representation.
    '''

    '''
    1. Extract the run name from the directory path
    '''
    runDirElements = runDir.split('/')
    runName = runDirElements[-1]

    '''
    2. Enumerate task names to be used for demarcating data rows
    '''
    taskNames = ["NOT",
                 "NAND",
                 "AND",
                 "ORNOT",
                 "OR",
                 "ANDNOT",
                 "NOR",
                 "XOR",
                 "EQUALS"]

    '''
    3. Extract the original organism's genome and its length
    '''
    replicateData = os.path.join(runDir, f'Timepoint_{desiredUpdateToAnalyze}/data/detail_MostNumerousAt{desiredUpdateToAnalyze}.dat')
    organisms = getOrganisms(replicateData)

    #The original organism data line is the last in the list
    genomeLength = getLength(organisms[-1])
    genome = getGenome(organisms[-1])
    

    '''
    4. Calculate the fractions of the genome occupied by
    coding sites and viability sites, respectively
    '''
    fracCodingSites = numUniqueCodingSites / genomeLength
    fracViabilitySites = len(viabilitySites) / genomeLength

    '''
    5. Compute the ratio of viability sites to coding sites
    '''
    try:
        viabilityToCodingRatio = fracViabilitySites / fracCodingSites
    except(ZeroDivisionError):
        viabilityToCodingRatio = 0

    '''
    6. For each task, add a row to the data frame with the
    Run Name, Task Name, Timepoint, Treatment Name, Coding Sites for
    that task, the number of coding sites for that task, the number of
    unique coding sites in the genome, the Viability Sites of
    the genome, the number of viability sites, and the previously
    computed metrics. Also, report the original genome in
    single-letter representation.
    '''
    for k in range(9):
        rowName = f"{runName}," + f"{taskNames[k]}"
        treatment.treatmentDataframe.loc[rowName] = [runName, taskNames[k], desiredUpdateToAnalyze, treatment.treatmentName, taskCodingSites[k], len(taskCodingSites[k]), numUniqueCodingSites, viabilitySites, len(viabilitySites), genomeLength, fracCodingSites, fracViabilitySites, viabilityToCodingRatio, genome]

'''
def writeTaskCodingSites(runDir,codingSites):
    writeDirectory = os.path.join(runDir,f"Timepoint_{desiredUpdateToAnalyze}/data/codingSites.txt")
    with open(writeDirectory,'w') as f:
        for site in codingSites:
            f.write('{},'.format(site))
'''

def writeExperimentTaskCodingSites(treatmentArray):
    '''
    Writes coding and viability sites data for each treatment in the experiment.

    Parameters:
    treatmentArray (list): List of treatment objects.
    '''

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