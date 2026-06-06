from enum import Enum
from block import Block

def get_extension(filename: str):
    if filename.count(".") == 1:
        return filename.split(".")[1]
    return

class ContentType(Enum):
    DOCUMENT = 0
    HEADING = 1
    SUBHEADING = 2
    SUBSUBHEADING = 3
    NUMBER_BULLET = 4
    BULLET_POINT = 5
    EQUATION = 6
    TEXT = 7
    NULL = 8
                
def is_candidate_concept(block: Block) -> bool:
    if len(block.text.split()) > 5 or len(block.text) < 3:
        return False

    if block.block_type == ContentType.HEADING:
        return True
    
    return None # in need of classification
