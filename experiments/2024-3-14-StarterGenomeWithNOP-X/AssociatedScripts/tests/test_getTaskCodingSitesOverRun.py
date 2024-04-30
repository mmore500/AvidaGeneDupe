import pytest
from testPrep import prepSysPathForTests
prepSysPathForTests()
from CodingSiteGeneratorHPCCCopyFunctions import getTaskCodingSitesOverRun
import CodingSiteGeneratorHPCCCopyFunctions

CodingSiteGeneratorHPCCCopyFunctions.desiredUpdateToAnalyze = 1000


import os

testDirectory = os.getcwd()

def test_getting_task_coding_sites_from_valid_data():
    runDirPath = os.path.join(testDirectory, 'tests/testRunDir')

    (codingSites, viabilitySites, numUniqueCodingSites) = getTaskCodingSitesOverRun(runDirPath)

    '''assert codingSites == [[7],
                           [4],
                           [4],
                           [4],
                           [1, 4],
                           [4],
                           [4],
                           [],
                           []]'''
    assert viabilitySites == [3, 5]
    assert numUniqueCodingSites == 3