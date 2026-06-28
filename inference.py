import joblib
from sentence_transformers import SentenceTransformer
import spacy
import argparse
from lib.ingestion import ingest
import sys
from lib.lib import is_candidate_concept



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
    possible_concepts = []
    parsed_document = ingest(filename=filename)

    if not parsed_document:
        print(f"unable to parse document: {filename}")
        sys.exit()
    
    for chunk in parsed_document.as_concepts():
      
        match is_candidate_concept(chunk):
            case 1:
                concepts.append(chunk.text)
            case 2:
                possible_concepts.append(chunk.text)

    text_blocks = [b.text for b in parsed_document.as_concepts()]
    print(text_blocks)
    
    X = embedder.encode(text_blocks)

    preds = clf.predict(X)
    classified = [(c,p) for c, p in zip(text_blocks, preds)]
    
    for row in classified:
        if row[1] == "1":
            print(row[0]) 

    
