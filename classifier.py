
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os
# prevents redownloading model every time - don't want to hit
os.environ['HF_HUB_OFFLINE'] = '1'


if __name__ == "__main__":
    print("importing sentence transformer...")
    from sentence_transformers import SentenceTransformer
    print("finished!")

    # caching model avoids hitting the hugging face api everytime
    if os.listdir("/").index("model_cache") == -1:
        print("creating model_cache directory...")
    model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./model_cache')


    data = []
    try:
        with open('lib/labeled_data/labeled.txt', "rb") as f:
            while True:
                try:
                    data.append(pickle.load(f))
                except EOFError:
                    break
    except FileNotFoundError:
        print("No labeled directory found. Please create " \
        "labeled data using the labeling.py script in the " \
        "lib/labeled_data directory and rerun this script")

    texts = []
    labels = []
    for classified in data:
        texts.append(classified[0].text)
        labels.append(classified[1])
    
    X = model.encode(texts)
    y = np.array(labels)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = LogisticRegression()
    clf.fit(X_train, y_train)

    y_predict = clf.predict(X_test)

    print(classification_report(y_test, y_predict))
