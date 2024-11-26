import pytest
from testPrep import prepSysPathForTests
prepSysPathForTests()
from CodingSiteGeneratorHPCCCopyFunctions import getOrganismID

def test_basic_input():
    # A basic input where the ID is the first element in the string
    input_data = "12345 data about organism"
    assert getOrganismID(input_data) == "12345"

def test_input_with_extra_spaces():
    # Input string with extra spaces
    input_data = "   12345    data about organism   "
    assert getOrganismID(input_data) == "12345"

def test_empty_input():
    # An empty input string should be handled or raise an error
    with pytest.raises(IndexError):  # Assuming it should raise IndexError if empty
        getOrganismID("")

def test_input_with_no_spaces():
    # Input that contains only an ID and no spaces
    input_data = "12345"
    assert getOrganismID(input_data) == "12345"

def test_input_with_non_string_types():
    # Non-string input should raise an error if not handled
    with pytest.raises(AttributeError):  # Assuming the split method will fail on non-string
        getOrganismID(None)

'''
def test_getLength():
    pass

def test_getViability():
    pass

def test_getGenome():
    pass

def test_knockItOut():
    pass

def test_knockoutDatGenome():
    pass

def test_knockoutDatFile():
    pass

def test_createDatAnalyzeCfg():
    pass

def test_executeInfoAnalysis():
    pass

def test_getTasks():
    pass

def test_getTaskCodingSitesOverRun():
    pass

def test_writeTaskCodingSitesInPandasDataFrame():
    pass
'''