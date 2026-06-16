import joblib
from sentence_transformers import SentenceTransformer
import spacy
import argparse
from ingestion import ingest


if __name__ == "__main__":
    clf = joblib.load("models/concept_classifier.pk1")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    nlp = spacy.load("en_core_web_sm")

    parser = argparse.ArgumentParser(
        prog="Document Inferencer",
        description="Extracts Concepts from Document",
    )
    # positional argument (1) for file
    # TODO: assumes file is in cwd
    
    parser.add_argument("-f", "--filename") 

    args = parser.parse_args()
    filename = args.filename

    parsed_document = ingest(filename)

    for chunk in parsed_document.chunk_nouns()
