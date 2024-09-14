import pytest
from testPrep import prepSysPathForTests
prepSysPathForTests()
from CodingSiteGeneratorHPCCCopyFunctions import getGenome


def test_getGenome_with_single_word():
    assert getGenome("Escherichia") == "Escherichia", "Should return the single word as the genome"

def test_getGenome_with_full_line():
    assert getGenome("Homo sapiens chromosome genome") == "genome", "Should return 'genome' as the genome"

def test_getGenome_with_special_characters():
    assert getGenome("Virus COVID-19 variant delta") == "delta", "Should return 'delta' as the genome"

def test_getGenome_with_numbers_and_special_chars():
    with pytest.raises(Exception, match="Genome should only be made of alphabet characters"):
        getGenome("Yeast strain 456-2B")

def test_getGenome_empty_string():
    with pytest.raises(IndexError, match="Your organism data line is empty"):
        getGenome("")

def test_getGenome_spaces_only():
    with pytest.raises(IndexError, match="Your organism data line has no characters but spaces"):
        getGenome("    ")

def test_getGenome_with_multiple_spaces_between_words():
    assert getGenome("Saccharomyces   cerevisiae    SOCK ") == "SOCK", "Should handle multiple spaces and return the last non-empty word"