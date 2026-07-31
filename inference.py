from sentence_transformers import SentenceTransformer
from lib.ingestion import ingest
from dotenv import load_dotenv
from lib.block import Block
import itertools
import argparse
import joblib
import spacy
from docarray import BaseDoc, DocList
from docarray.typing import NdArray
import numpy as np
from vectordb import InMemoryExactNNVectorDB
import json
import sys
import os


class ConceptDoc(BaseDoc):
    block: Block = None
    embedding: NdArray[128]




def _encode__classify_blocks(blocks: list[Block]) -> list[ConceptDoc]:
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
            res.append(ConceptDoc(blocks[i], X[i]))
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
    
    parser.add_argument("-d", "--directory")
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

    classified: list[ConceptDoc] = []
    i = 0

    # parse out files + flatten every concept into a single list
    while (max_files == -1 or i < max_files) and i < len(parsed_directory):
     
        if not parsed_directory[i]:
            print(f"unable to parse document!")
            sys.exit()
        
        classified += _encode__classify_blocks(parsed_directory[i].as_concepts())
        i += 1
    db = InMemoryExactNNVectorDB[ConceptDoc](workspace='./workspace_path')
    db.index(docs=DocList(docs=[classified]))
    # group concepts by heading
    found_links = _find_links(classified)

    nodes = []
    links = []

    # create nodes for each concept
    for i in range(len(classified)):
        nodes.append({"id" : classified[i].block.text, "label": classified[i].block.text}) # this is the json format the frontend expects. RE: ./cs-notes-web-ui/app/components/GraphView.tsx

    links_created = 0
    
    possible_edges = list(itertools.combinations(classified,2))

    # link all nodes to their respective header nodes
    for link in found_links:

        cur_header_node = {"id" : f"{link}", "label": link}
        nodes.append(cur_header_node)
    
        for i in range(len(found_links[link])):

            links.append(
                {
                    "id" : str(links_created),
                    "source" : found_links[link][i].text,
                    "target" : cur_header_node["id"],
                    "label" : "",
                }
                
            )
            links_created += 1

    
    # insane computation load; need a smart way to approach this
    # something w/ header nodes, finding links there , then grouping children
    prev_rounded = 0
    for i in range(len(classified)):
        percent = i / len(possible_edges)
        rounded = round(percent, 3)
        start = possible_edges[i][0].text
        end = possible_edges[i][1].text

        query = ConceptDoc(block=classified[i][1], embedding=classified[i][0])
        results = db.search(inputs=DocList(docs=[query]), limit=10)

        for m in results[0].matches:
           
                links.append({ 
                                "id" : str(links_created),
                                # src
                                "source" : m[1].text,
                                # trgt
                                "target" : classified[i][1].text,
                                "label" : "",
                            })
                links_created += 1

        
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

    
