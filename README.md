# cs-notes-pipeline
nlp pipeline for processing & visualizing my computer science notes.

## Setup
1) create virtual environment: `python3 -m venv venv`
2) activate virtual environment:
- macos: `source venv/bin/activate`
- windows: `venv\Scripts\activate.bat`
3) install dependencies: pip install -r requirements.txt
3) create a /models/ directory in the project directory
8) set path to output txt file in `.env` (e.g. `CONCEPTS_DUMP=path_to_file`)
5) `python3 labeling.py ~/a/path/to/notes`
6) `python3 classifier.py`
7) `python3 inference.py ~/same/path/to/notes`
- optional argument `-m <int>` which limits the number of inferred concepts. Useful if you just want a small graph visualization 
9) `cd cs-notes-web-ui`
10) `bun run dev`

### Labeling.py
Expedites concept labeling/encoding from `/lib/test_notes/`. Any file placed in that directory will flow throw ingestion pipeline; some will be processed, others won't depending on whether the file format is supported. Currently, `.md` and `.typ` fiels are the only supported formats.

### Classifier.py
Trains the model on the data from the labeling script. Stored as a seperate script for now, but may combine with labeling in the future.

### Inference.py
using the `-f` flag, attempts to extract concept with trained model.
