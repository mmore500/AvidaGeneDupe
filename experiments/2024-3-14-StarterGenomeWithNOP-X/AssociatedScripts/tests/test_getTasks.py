import pytest
from testPrep import prepSysPathForTests
prepSysPathForTests()
from CodingSiteGeneratorHPCCCopyFunctions import getTasks

import numpy as np

def test_get_tasks_basic():
    organismString = "110101001 1234567 additional data"
    expected_output = np.array([1, 1, 0, 1, 0, 1, 0, 0, 1])
    assert np.array_equal(getTasks(organismString), expected_output), "The tasks array does not match the expected output"

def test_get_tasks_empty_string():
    with pytest.raises(Exception):
        getTasks('')

def test_get_tasks_invalid_input():
    organismString = "abcde"
    with pytest.raises(ValueError):
        getTasks(organismString)

def test_get_tasks_non_binary_input():
    organismString = "20102 123456"
    with pytest.raises(ValueError):
        getTasks(organismString)

def test_get_tasks_large_input():
    organismString = "1" * 1000 + " 123456"
    expected_output = np.array([1] * 1000)
    assert np.array_equal(getTasks(organismString), expected_output), "The function should handle large inputs correctly"

