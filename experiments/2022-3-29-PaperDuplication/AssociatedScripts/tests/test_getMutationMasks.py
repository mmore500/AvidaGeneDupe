import pytest
import os
import pandas as pd
from typing import List
from generateMutationMasks import getMutationMasks



def test_singlePointMutation():
    parent_genome = "wzjagcczyovvccccAvocccpbclqxaycrcccoxurctaiAAlcrcyAccwyccucqcccqcuqylacycctbtcckyccztccctevzvvvvfcaxgab"
    child_genome = "wzjagcczyovvccccAvocccpbclqxaycrcccoxurctaiAAlcrcyAccjyccucqcccqcuqylacycctbtcckyccztccctevzvvvvfcaxgab"

    actualResult = getMutationMasks(
                     parent_genome,
                     child_genome,
                     [53],
                     [],
                     [])
    
    expectedResult = pd.DataFrame(
        {
            "CHILD_SOURCE_MAP": range(len(parent_genome)),
            "POINT_MUTATION_BOOL_MASK": [i == 53 for i in range(len(child_genome))],
            "SLIP_INSERTION_BOOL_MASK": [False] * len(parent_genome),
            "SINGLE_INSERTION_BOOL_MASK": [False] * len(parent_genome),
        }
    )

    pd.testing.assert_frame_equal(
        actualResult, expectedResult
    )