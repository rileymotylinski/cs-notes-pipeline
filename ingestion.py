import argparse
import sys

from lib.lib import *
from lib.markdown import *
from lib.block import Document
from lib.typst import TypstParser


# supported filetypes
FILETYPES = (
    "md",
    "typ",
    "pdf"
)

if __name__ == "__main__":
    # setup
    parser = argparse.ArgumentParser(
        prog="Document Ingester",
        description="Converts markdown/typst/pdfs into clean JSON objects",
    )
    # positional argument (1) for file
    # TODO: assumes file is in cwd
    parser.add_argument("filename") 
    parser.add_argument("course_code")
    parser.add_argument("semester")

    # reading args
    args = parser.parse_args()
    filename = args.filename
    course_code = args.course_code
    semester = args.semester
    file_extension = get_extension(filename)

    if file_extension == None:
        print("unable to read filename")
        sys.exit()

    if file_extension not in FILETYPES:
        print("unsupported filetype")
        sys.exit()

    doc = None

    if file_extension == "md":
        parser = MarkdownParser()
        with open(filename, "r") as f:

            lines = [line.strip(" ").strip("\n") for line in f.readlines()]
            res = parser.parse(lines)

            doc = Document(res, course_code, semester)

            print(doc.as_json())
            f.close()

 
    elif file_extension == "typ":
        parser = TypstParser()

        with open(filename, "r") as f:

            lines = [line.strip(" ").strip("\n") for line in f.readlines()]
            res = parser.parse(lines)

            doc = Document(res, course_code, semester)

            print(doc.as_json())
            f.close()

    if doc == None:
        print("unable to process file")
        sys.exit()
    
    print(doc.chunk_nouns())

    
    

