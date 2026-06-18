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
        sys.exit()

    if file_extension not in FILETYPES:
        print(f"unsupported filetype: {file_extension}")
        sys.exit()

    doc = parse_file(filename, file_extension, course_code, semester)

    if doc == None:
        print("unable to parse file")
        return None
    
    return doc

def handle_directory_input(directory, course_code, semester) -> list[Document]:
    directory = directory.strip("/")
    res = []
    for file in os.listdir(directory):
        processed = handle_file_input(file, course_code, semester)

        if not processed:
            continue
        
        res.append(processed)

    
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

# command line interface for ingest function
if __name__ == "__main__":
    # setup
    parser = argparse.ArgumentParser(
        prog="Document Ingester",
        description="Converts markdown/typst/pdfs into clean JSON objects",
    )
    # positional argument (1) for file
    # TODO: assumes file is in cwd
    
    parser.add_argument("-f", "--filename") 
    parser.add_argument('-d', '--directory')
    parser.add_argument("course_code")
    parser.add_argument("semester")
    
    # reading args
    args = parser.parse_args()
    filename = args.filename
    directory = args.directory
    course_code = args.course_code
    semester = args.semester

    # normalize as document object
    res = ingest(filename,directory,course_code,semester)

    if not res:
        print("unable to read document(s)")
        sys.exit()
    
    if filename:
        for block in res.blocks:
            print(block.text)
    elif directory:
        for file in res:
            for block in file.blocks:
                print(block.text)