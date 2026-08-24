from sentence_transformers import SentenceTransformer
from lib.ingestion import ingest
from dotenv import load_dotenv
from lib.block import Block

import argparse
import joblib
import spacy
import chromadb
import json
import sys
import os



def _encode__classify_blocks(blocks: list[Block]) -> list[tuple[list[int], Block]]:
    """
    purpose: custom wrapper for pytorch embedding + prediction funciton. 
    Handles custom blocks instead of raw text. Important 
    for retaining metadata from blocks
    """

    text_blocks = [b.text for b in blocks]
    X = embedder.encode(text_blocks)

    preds = clf.predict(X)
    classified = [(c,p) for c, p in zip(text_blocks, preds)]
    # only return text classified as concepts
    classified = [c[0] for c in list(filter(lambda c : c[1] == "1", classified))]

    res = []
    for i in range(len(blocks)):
        if blocks[i].text in classified:
            res.append((X[i],blocks[i]))
    return res

def magnitude(v: list[int]):
    res = 0

    for n in v:
        res += n * n   
    return res ** 0.5



def dot_product(b1: Block, b2: Block):
    i = min(len(b1), len(b2))
    total = 0
    for j in range(i):
        total += b1[j] * b2[j]

    return total / (magnitude(b1) * magnitude(b2))


def _find_links(blocks: list[Block]) -> dict:
    links = {}
    for b in blocks:
        if b.header_context not in links:
            links[b.header_context] = []
        
   
        links[b.header_context].append(b)

    return links



if __name__ == "__main__":
    clf = joblib.load("models/concept_classifier.pkl")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    nlp = spacy.load("en_core_web_sm")

    parser = argparse.ArgumentParser(
        prog="Document Inferencer",
        description="Extracts Concepts from Document",
    )
    # positional argument (1) for file
    
    parser.add_argument("directory")
    parser.add_argument("-m", "--max")  

    args = parser.parse_args()
    directory = args.directory
    max_files = args.max
    if max_files != None:
        max_files = int(max_files)
    else: 
        max_files = -1

    concepts = []
    parsed_directory = ingest(directory=directory, max_files=max_files)

    classified: list[Block] = []
    i = 0
    
    # parse out files + flatten every concept into a single list
    while (max_files == -1 or i < max_files) and i < len(parsed_directory):
        
        if not parsed_directory[i]:
            print(f"unable to parse document!")
            sys.exit()
        
        classified += _encode__classify_blocks(parsed_directory[i].as_concepts())
        i += 1

    chroma_client = chromadb.Client()
    vectordb = chroma_client.create_collection(name="concepts")
    ids = [str(i) for i in range(len(classified))]
    embeddings = [c[0] for c in classified]
    blocks = [c[1] for c in classified]
    vectordb.add(ids=ids,embeddings=embeddings)
    
    nodes = []
    links = []

    # create nodes for each concept
    for i in range(len(blocks)):
        nodes.append({"id" : blocks[i].text, "label": blocks[i].text}) # this is the json format the frontend expects. RE: ./cs-notes-web-ui/app/components/GraphView.tsx

    links_created = 0

    # group concepts by heading
    found_links = _find_links(blocks)
    

    # link all nodes to their respective header nodes
    for link in found_links:

        cur_header_node = {"id" : f"{link}", "label": link}
        end = cur_header_node["id"]
        nodes.append(cur_header_node)
    
        for i in range(len(found_links[link])):
            start = found_links[link][i].text
            if start == end:
                continue
            links.append(
                {
                    "id" : str(links_created),
                    "source" : start,
                    "target" : end,
                    "label" : "",
                }
                
            )
            links_created += 1

    
    # insane computation load; need a smart way to approach this
    # something w/ header nodes, finding links there , then grouping children
    prev_rounded = 0
    for i in range(len(classified)):
        percent = i / len(classified)
        rounded = round(percent, 3)
        start = blocks[i].text


        # TODO : use custom embedding function wrapper
        results = vectordb.query(query_texts=[start])
        
        for res in results:
            if start == res:
                continue
            candidate_edge = {
                "id" : str(links_created),
                # src
                "source" : start,
                # trgt
                "target" : res,
                "label" : "",
            }
            
            if candidate_edge not in links:
                links.append(candidate_edge)

        if abs(rounded - prev_rounded) > 0.01:
            print(f"{int(rounded * 100)}%")
            prev_rounded = rounded
    # write to file
    load_dotenv() 
    with open(os.getenv("CONCEPTS_DUMP"), "w") as f:
        json.dump({
            "nodes": nodes,
            "links" : links
        },f)
        
    print(f"wrote concepts to {os.getenv("CONCEPTS_DUMP")} in project directory")



