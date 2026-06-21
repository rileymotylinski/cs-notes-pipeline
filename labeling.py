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
    # flattening out chunked nouns
    print("chunking nouns...")
    for doc in processed_docs:
        blocks += doc.blocks
    print("finished!")

    print("""you will now begin labeling blocks:
          
            (0) : not a concept
            (1) : concept
            (2) : unsure
          """)
    valid_responses = set(("0", "1", "2")) # re: above

    i, concepts, not_concepts, unsures = 0,0,0,0

    processed_blocks = []

    while i < len(blocks) and i < 50:
        print(i)
        block = blocks[i]
        print(block.text)
        res = encode_bool(is_candidate_concept(block))

        
        if res == 1:
            concepts += 1
            print("auto-labeled as concept")        
        elif res == 0:
            not_concepts += 1
            print("auto-labeled as not a concept")
        else:
            while res not in valid_responses:
                res = input("rate this block: ")

                if res not in valid_responses:
                    print("failed!")
                # TODO: this is repeat of code above; refactor
                else:
                    if res == 1:
                        concepts += 1
                        print("labeled as concept")        
                    elif res == 0:
                        not_concepts += 1
                        print("labeled as not a concept")

                    # TODO: refactor this
                    elif res == 2:
                        unsures += 1
                        print("labeled as unsure")

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

    
