import pytest
from testPrep import prepSysPathForTests
prepSysPathForTests()
from CodingSiteGeneratorHPCCCopyFunctions import knockoutDatFile

import os

testDirectory = os.getcwd()

def test_knockoutDatFile_basicFunctionality():
    testRunningDirectory = os.getcwd()

    testFilePath = os.path.join(testDirectory, 'knockoutDatFileTestFile.txt')
    readFilePath = os.path.join(testDirectory, 'tests/detail-knockoutDatFile.dat')
    with open(testFilePath, 'w') as testFile:
        knockoutDatFile(readFilePath, testFile)
 

    testSuccess = None

    comparisonFilePath = os.path.join(testRunningDirectory, 'tests/testComparisonFiles/testKnockoutDatFile.dat')
    with open(testFilePath, 'r') as testFile, open(comparisonFilePath, 'r') as comparisonFile:
        testSuccess = testFile.read() == comparisonFile.read()
    
    os.remove(testFilePath)

    assert testSuccess == True
