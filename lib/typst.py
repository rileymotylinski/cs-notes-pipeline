from lib.lib import ContentType
from lib.block import Block
import re
import uuid


def ident_to_content_type(ident: str):
    match ident:
        case "=":
            return ContentType.HEADING
        case "==":
            return ContentType.SUBHEADING
        case "===":
            return ContentType.SUBSUBHEADING
        case "-":
            return ContentType.BULLET_POINT
        case "$": 
            return ContentType.EQUATION
        
    # TODO: regex is not efficient
    if re.compile(r"\d+.").match(ident) or re.compile(r"\d+\)").match(ident):
        return ContentType.NUMBER_BULLET

    return ContentType.TEXT

class TypstParser():
    def __init__(self):
        self.current_header = ContentType.DOCUMENT.name
    
    def parse(self, lines) -> list[Block]:
        res = []
        for i in range(len(lines)):
            # empty line
            if len(lines[i]) <= 1:
                continue
            
            # identifiers will always be seperated by a space
            # e.g. `=== This is a heading`
            first_space = lines[i].find(" ")
            
            # TODO: currently consuming line by line; what about multiline bp?
            block_type = ident_to_content_type(lines[i][0:first_space])
            text = lines[i][first_space + 1:]

            if lines[i][0:1] == "$":
                text = lines[i].strip("$").strip()
                block_type = ContentType.EQUATION

            # update current_header
            # TODO: suggest depth by storing ALL parent headings
            if block_type.value >= ContentType.HEADING.value and block_type.value <= ContentType.SUBSUBHEADING.value:
                self.current_header = text
            elif block_type == ContentType.TEXT:
                # text will have no leading character
                text = lines[i][0:]

            # notes (probably) wont have > 9999 lines
            current_block: Block = Block(block_type,header_context=self.current_header,text=text)

            res.append(current_block)
        
        return res