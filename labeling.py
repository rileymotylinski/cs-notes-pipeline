from ingestion import handle_directory_input

"""
purpose: easier mass labeling of chunks for training data
"""

if __name__ == "__main__":
    processed_docs = handle_directory_input("../umn/csci2021/notes", "csci2021", "2")
  
    blocks = []

    for doc in processed_docs:
        for block in doc.blocks:
            blocks.append(block)
    
    processed_blocks = []

    print("""you will now begin labeling blocks:
          
            (0) : not a concept
            (1) : concept
            (2) : unsure
          
          """)
    valid_responses = set(("0", "1", "2")) # re: above

    for block in blocks:
        print(block.text)
        res = None

        while res not in valid_responses:
            res = input("rate this block: ")
        
        blocks.append((block, res))
        