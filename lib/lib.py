from enum import Enum

def get_extension(filename: str):
    
    return filename[filename.rindex(".")+1:]


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
                
# TODO : cannot import block module here? I want type annotations
def is_candidate_concept(block) -> bool:
    '''
    algorithmic categorization of blocks
    args: block - block to be classified
    returns: bool - True if possible "concept", False, if it's _not_ a candidate concept, and `None` if it's unsure.
    '''

    # not enough words/letters
    if len(block.text.split()) >= 5 or len(block.text) < 3:
        return False
    
    # bullet points
    if block.text.split()[0] == "*" or block.text.split()[0] == "-":
        return False

    if block.block_type == ContentType.HEADING:
        return True
    
    return None # in need of classification

# have to have spaces so they actually don't remove *every* character
# only problem would be if a concept ends in an article, which I don't 
# really see as possible, but may be something to consider
articles = ("the ", "this", "*", "a ", "an", "or", "some")
def remove_articles(s: str):
    s = s.strip()
    for a in articles:
        s = s.removeprefix(a)

    return s.strip()
