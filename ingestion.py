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
        sys.exit()
    
    return doc
    

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

def handle_directory_input(directory, course_code, semester) -> list[Document]:
    directory = directory.strip("/")
    res = []
    # TODO : handle subdirectories/non-files
    for file in os.listdir(directory):
        file_extension = get_extension(file)

        if file_extension == None:
            print("unable to read file extension")
            continue

        processed = parse_file(f"{directory}/{file}", file_extension, course_code, semester)

        # unlike individual file parsing, we don't want to kill script when we come across a file we cannot parse
        if processed == None:
            print(f"unable to parse file: {file}")
            continue

        res.append(processed)
    
    return res

def ingest(filename=None, directory=None, course_code="", semester=""):
    if filename != None and directory != None:
        print("cannot process both directory and file")

    if filename != None:
        return handle_file_input(filename, course_code, semester)
    
    elif directory != None:
        return handle_directory_input(directory, course_code, semester)


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

    ingest(filename,directory,course_code,semester)
