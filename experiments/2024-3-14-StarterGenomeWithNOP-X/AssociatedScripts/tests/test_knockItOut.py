import pytest
from testPrep import prepSysPathForTests
prepSysPathForTests()
from CodingSiteGeneratorHPCCCopyFunctions import knockItOut

def test_knockItOut_replace_middle_character():
    assert knockItOut("CGTTCGT", 3) == "CGTACGT", "Should replace the middle character with 'A'"

def test_knockItOut_replace_first_character():
    assert knockItOut("CGTACGT", 0) == "AGTACGT", "Should replace the first character with 'A'"

def test_knockItOut_replace_last_character():
    assert knockItOut("CGTACGT", 6) == "CGTACGA", "Should replace the last character with 'A'"

def test_knockItOut_with_single_character_string():
    assert knockItOut("C", 0) == "A", "Should replace the single character with 'A'"

def test_knockItOut_index_out_of_bounds():
    with pytest.raises(IndexError):
        knockItOut("CGTACGT", 7), "Should raise IndexError if the index is out of bounds"

def test_knockItOut_negative_index():
    with pytest.raises(IndexError):
        knockItOut("CGTACGT", -1), "Should raise IndexError if the index is negative"

def test_knockItOut_empty_string():
    with pytest.raises(IndexError):
        knockItOut("", 0), "Should raise IndexError if the string is empty"

def test_knockItOut_replace_character_already_A():
    assert knockItOut("AAAA", 2) == "AAAA", "Should handle replacing 'A' with 'A'"

def test_knockItOut_large_index():
    with pytest.raises(IndexError):
        knockItOut("CGTACGT", 100), "Should raise IndexError if the index is excessively large"
