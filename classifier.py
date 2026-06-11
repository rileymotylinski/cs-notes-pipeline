# from sentence_transformers import SentenceTransformer
import numpy as np
import pickle


if __name__ == "__main__":
    # model = SentenceTransformer('all-MiniLM-L6-v2')
    data = []

    with open('lib/labeled_data/labeled.txt', "rb") as f:
        while True:
            try:
                data.append(pickle.load(f))
            except EOFError:
                break

    print(data[0][1])