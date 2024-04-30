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

    assert codingSites == [[6],
                           [3],
                           [3],
                           [3],
                           [0, 3],
                           [3],
                           [3],
                           [],
                           []]
    assert viabilitySites == [2, 4]
    assert numUniqueCodingSites == 3