import json
import en_core_web_sm

from lib.lib import ContentType, remove_articles

class Block():
    def __init__(self,id: str, block_type:ContentType, header_context: str="", text: str=""):
        self.id = id
        self.block_type = block_type
        self.header_context = header_context
        self.text = text
    
    def as_json(self):
        """
        returns formatted version of a block fo easier json parsing
        args: none
        returns: json-fied version of a block
        """
        return {
            "id": self.id,
            "block_type": self.block_type.name,
            "header_context": self.header_context,
            "text": self.text
        }


# a single file of notes is a document, or a collection of blocks
class Document:
    def __init__(self, blocks: list[Block],course_code: str, semester: str):
        nlp = en_core_web_sm.load()
        self.blocks = []
        for block in blocks:
            # if it's some sort of heading, we assume it doesn't need to be split
            # this is the second pass of split blocks
            # TODO: I think this is the best way to do it? Constructing it in the parser would require having two sources of truth which I don't like
            if block.block_type.value <= ContentType.SUBSUBHEADING.value and block.block_type.value  >= ContentType.HEADING.value:
                block.text = remove_articles(block.text.lower())
                self.blocks.append(block)
                continue

            res = []
            
            process_doc = nlp(block.text)
            
            for chunk in process_doc.noun_chunks:
                res.append(Block(block.id,block.block_type, block.header_context, remove_articles(chunk.text).lower()))
            
            self.blocks += res
  
        self.course_code = course_code
        self.semester = semester
        
    
    def add_block(self, b: Block):
        self.blocks.append(b)

    def as_json(self):
        """
        returns formatted version of a block fo easier json parsing
        args: none
        returns: json-fied version of a document
        """
        return json.dumps({
            "course_code" : self.course_code,
            "semester" : self.semester,
            "blocks" : [block.as_json() for block in self.blocks]
        })
    
    def get_text(self):
        '''
        returns all text from document; all metadata stripped
        args: none
        returns: all text from composite chunks of a document
        '''

        text = ""
        for b in self.blocks:
            text += f"{b.text} "
        return text
    

        
        

        