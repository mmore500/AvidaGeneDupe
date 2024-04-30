import pytest
from testPrep import prepSysPathForTests
prepSysPathForTests()
from CodingSiteGeneratorHPCCCopyFunctions import getOrganisms

def test_empty_file(tmp_path):
    # Create a temporary empty file
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text('')
    assert getOrganisms(str(empty_file)) == []

def test_file_with_only_comments(tmp_path):
    # Create a file with only comments
    comments_file = tmp_path / "comments.txt"
    comments_file.write_text('# This is a comment\n# Another comment\n')
    assert getOrganisms(str(comments_file)) == []

def test_file_with_valid_data_lines(tmp_path):
    # Create a file with valid data lines after comments
    data_file = tmp_path / "data.txt"
    data_file.write_text('# Comment line\nData1\nData2\n')
    assert getOrganisms(str(data_file)) == ['Data1', 'Data2']

def test_file_with_no_valid_data_lines(tmp_path):
    # Create a file with comments and no data lines
    no_data_file = tmp_path / "nodata.txt"
    no_data_file.write_text('# Comment\n# Another comment\n\n')
    assert getOrganisms(str(no_data_file)) == []

def test_exception_handling_for_file_not_found():
    # Try to open a file that does not exist
    with pytest.raises(IOError):
        getOrganisms("/path/to/nonexistent/file.txt")