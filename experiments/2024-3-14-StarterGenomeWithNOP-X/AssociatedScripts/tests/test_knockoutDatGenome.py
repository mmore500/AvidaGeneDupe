import pytest
from testPrep import prepSysPathForTests
prepSysPathForTests()
from CodingSiteGeneratorHPCCCopyFunctions import knockoutDatGenome

import os

testDirectory = os.getcwd()

# Assuming you have imported the function knockoutDatGenome and knockItOut

def test_knockoutDatGenome_basic_functionality():
    testRunningDirectory = os.getcwd()

    testFilePath = os.path.join(testDirectory, 'knockoutDatGenomeTestFile.txt')
    with open(testFilePath, 'w') as testFile:
        knockoutDatGenome(testFile, 'abcdef', 0)
 

    testSuccess = None

    comparisonFilePath = os.path.join(testRunningDirectory, 'tests/testComparisonFiles/testKnockoutDatGenome.dat')
    with open(testFilePath, 'r') as testFile, open(comparisonFilePath, 'r') as comparisonFile:
        testSuccess = testFile.read() == comparisonFile.read()
    
    os.remove(testFilePath)

    assert testSuccess == True

# Additional tests can include different genome strings, different orgCount values,
# and scenarios where an exception might be raised during file operations.