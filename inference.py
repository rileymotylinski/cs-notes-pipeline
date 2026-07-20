import joblib
from sentence_transformers import SentenceTransformer
import spacy
import argparse
from lib.block import Block
from lib.ingestion import ingest
import sys
from lib.lib import is_candidate_concept
import json
import os
from dotenv import load_dotenv, dotenv_values 

def _encode__classify_blocks(blocks: list[Block]) -> list[Block]:
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
    for b in blocks:
        if b.text in classified:
            res.append(b)
    return res

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
    
    parser.add_argument("-f", "--filename") 

    args = parser.parse_args()
    filename = args.filename

    concepts = []
    parsed_document = ingest(filename=filename)

    if not parsed_document:
        print(f"unable to parse document: {filename}")
        sys.exit()
    
    classified = _encode__classify_blocks(parsed_document.as_concepts())
    found_links = _find_links(classified)

    nodes = []
    links = []

    for i in range(len(classified)):
        nodes.append({"id" : f"{classified[i].id}", "label": classified[i].text}) # this is the json format the frontend expects. RE: ./cs-notes-web-ui/app/components/GraphView.tsx

    links_created = 0
    for link in found_links:
        for i in range(len(found_links[link])):
            for j in range(i + 1, len(found_links[link])):
                links.append(
                    {
                        "id" : str(links_created),
                        # src
                        "source" : found_links[link][i].id,
                        # trgt
                        "target" : found_links[link][j].id,
                        # label. TODO : leaving empty for now to avoid visual clutter
                        "label" : "testing"
                    }
                )
                links_created += 1

    load_dotenv() 
    with open(os.getenv("CONCEPTS_DUMP"), "w") as f:
        json.dump({
            "nodes": nodes,
            "links" : links
        },f)
        
    print(f"wrote concepts to {os.getenv("CONCEPTS_DUMP")} in project directory")

    
