# cs-notes-pipeline
nlp pipeline for processing & visualizing my computer science notes.

## Setup

```
1) create virtual environment: python3 -m venv venv
2) activate virtual environment:
- macos: source venv/bin/activate
- windows: venv\Scripts\activate.bat
3) install dependencies: pip install -r requirements.txt
3) create a /models/ directory in the project directory
4) place your typst/markdown notes in /lib/test_notes/ (create if doesn't exist)
5) run labeling.py to label data for training
6) run classifier.py to train the model
7) run inference.py to extract concepts from a new file
```
### Labeling.py
Expedites concept labeling/encoding from `/lib/test_notes/`. Any file placed in that directory will flow throw ingestion pipeline; some will be processed, others won't depending on what files are in the directory
### Classifier.py
Trains the model on the data from the labeling script. Stored as a seperate script for now, but may combine with labeling in the future.

### Inference.py
using the `-f` flag, attempts to extract concept with trained model.
