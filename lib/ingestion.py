import argparse
import sys
import os

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

def parse_file(filename, file_extension, course_code, semester) -> Document:

    doc = None

    if file_extension == "md":
        parser = MarkdownParser()
        with open(filename, "r") as f:

            lines = [line.strip(" ").strip("\n") for line in f.readlines()]
            res = parser.parse(lines)

            doc = Document(res, course_code, semester)

            f.close()

 
    elif file_extension == "typ":
        parser = TypstParser()

        with open(filename, "r") as f:

            lines = [line.strip(" ").strip("\n") for line in f.readlines()]
            res = parser.parse(lines)

            doc = Document(res, course_code, semester)

            f.close()
    
    return doc

def handle_file_input(filename, course_code, semester) -> Document:
    file_extension = get_extension(filename)

    if file_extension == None:
        print(f"unable to read filename: {filename}")
        return

    if file_extension not in FILETYPES:
        print(f"unable to process {filename} unsupported filetype: {file_extension}")
        return

    doc = parse_file(filename, file_extension, course_code, semester)

    if doc == None:
        print("unable to parse file")
        return None
    
    return doc

def handle_directory_input(directory, course_code, semester) -> list[Document]:
    directory = directory.strip("/")
    res = []
    for file in os.listdir(directory):
        processed = handle_file_input(f"{directory}/{file}", course_code, semester)

        if not processed:
            continue
        
        res.append(processed)
        print(f"parsed file: {file}")

    
    return res


def ingest(filename=None, directory=None, course_code="", semester="") -> (Document | list[Document] | None):
    """
    receives either a file or directory and spits out a processed document object
    """
    res = None

    if filename != None and directory != None:
        print("cannot process both directory and file")

    elif filename != None:
        res = handle_file_input(filename, course_code, semester)
    
    elif directory != None:
        res = handle_directory_input(directory, course_code, semester)

    return res

