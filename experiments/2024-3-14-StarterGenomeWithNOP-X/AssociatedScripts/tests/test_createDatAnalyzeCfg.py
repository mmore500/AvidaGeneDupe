import pytest
from testPrep import prepSysPathForTests
prepSysPathForTests()
from CodingSiteGeneratorHPCCCopyFunctions import createDatAnalyzeCfg
import CodingSiteGeneratorHPCCCopyFunctions

CodingSiteGeneratorHPCCCopyFunctions.desiredUpdateToAnalyze = 1000


import os

testDirectory = os.getcwd()

def test_createDatAnalyzeCfg_basicFunctionality():
    testRunningDirectory = os.getcwd()

    readDirPath = os.path.join(testDirectory, 'tests/testRunDir')
    createDatAnalyzeCfg(readDirPath)
 

    testSuccess = None

    testFilePath = os.path.join(readDirPath, 'Timepoint_1000/informationAnalyzer.cfg')
    comparisonFilePath = os.path.join(testRunningDirectory, 'tests/testComparisonFiles/testCreateDatAnalyzeCfg.dat')
    with open(testFilePath, 'r') as testFile, open(comparisonFilePath, 'r') as comparisonFile:
        testSuccess = testFile.read() == comparisonFile.read()
    

    assert testSuccess == True
