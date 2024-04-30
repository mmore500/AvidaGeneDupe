import pytest
from testPrep import prepSysPathForTests
prepSysPathForTests()
from CodingSiteGeneratorHPCCCopyFunctions import getLength

def test_empty_string():
    inputDataLine = ''
    with pytest.raises(IndexError):
        getLength(inputDataLine)

def test_string_in_place_of_integer(tmp_path):
    inputDataString = 'ID1 Update_Born Length1 Genome1'
    with pytest.raises(ValueError):
        getLength(inputDataString)

def test_organism_data_line_incorrectly_ordered():
    '''
    In this example, the update born and length have
    been swapped -- it is very, very unlikely to have
    an organism of 50000 instructions in our context.
    '''

    inputDataString = '10000 280 50000 abcdefg'
    with pytest.raises(Exception):
        getLength(inputDataString)
    
def test_hidden_tab_in_input():
    inputDataString = 'ID1 Update_Born  200 Genome'
    assert getLength(inputDataString) == 200

def test_valid_input():
    inputDataString = '100 200 300 abcdefg'
    assert getLength(inputDataString) == 300