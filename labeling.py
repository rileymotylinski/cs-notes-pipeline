from lib.ingestion import ingest
from lib.lib import is_candidate_concept
import sys
import argparse

import pickle

"""
purpose: easier mass labeling of chunks for training data
"""

def encode_bool(val: bool):
    """
    purpose: encodes a boolean value as classified concept, e.g. true -> 1 (see below)
    """

    match val:
        case True: 
            return 1
        case False:
            return 0
    return 2

if __name__ == "__main__":
    dir = "/lib/test_notes/"

    # TODO: accept course_code and semester as arguments
    processed_docs = ingest(directory=dir, course_code="csci2021", semester="2")
    
    if not processed_docs:
        print(f"unable to read directory: {dir}")
        sys.exit()

    blocks = []

    for doc in processed_docs:
        for block in doc.blocks:
                blocks.append(block)
    

    print("""you will now begin labeling blocks:
          
            (0) : not a concept
            (1) : concept
            (2) : unsure
          """)
    valid_responses = set(("0", "1", "2")) # re: above

    i, concepts, not_concepts, unsures = 0,0,0,0

    processed_blocks = []

    while i < len(blocks) and i < 500:
        print(i)
        block = blocks[i]
        res = encode_bool(is_candidate_concept(block))

        print(block.text)
        
        if res == 1 or res == 0:
            match res:
                case 1:
                    concepts += 1
                    print("auto-labeled as concept")
                case 0:
                    not_concepts += 1
                    print("auto-labeled as not a concept")

        # TODO: refactor this
        else:
            while res not in valid_responses:
                res = input("rate this block: ")

                if res not in valid_responses:
                    print("failed!")
            unsures += 1
            

        processed_blocks.append((block, res))
        i += 1

        print()
    
    print(f"""
        Final Report
          concepts: {concepts}
          not concepts: {not_concepts}
          unsure: {unsures}
    """)
    
    with open("lib/labeled_data/labeled.txt", "wb") as f: # where the labeled data exists
        for block in processed_blocks:
            pickle.dump(block,f,pickle.DEFAULT_PROTOCOL)
    
    print("wrote objects to file!")

    
