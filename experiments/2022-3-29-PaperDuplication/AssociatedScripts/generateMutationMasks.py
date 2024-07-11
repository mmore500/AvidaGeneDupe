import pandas as pd
from typing import List

def getMutationMasks(parent_sequence: str,
                     child_sequence: str,
                     point_mutants: List[int],
                     insertion_mutants: List[int],
                     deletion_mutants: List[int]) -> pd.DataFrame:
    
    
    return pd.DataFrame(
        {
            "CHILD_SOURCE_MAP": range(len(parent_sequence)),
            "POINT_MUTATION_BOOL_MASK": [i in point_mutants for i in range(len(child_sequence))],
            "SLIP_INSERTION_BOOL_MASK": [False] * len(child_sequence),
            "SINGLE_INSERTION_BOOL_MASK": [False] * len(child_sequence),
        }
    )