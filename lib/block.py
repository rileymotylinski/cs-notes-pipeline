import json
import en_core_web_sm
from sentence_transformers import SentenceTransformer


from lib.lib import ContentType, remove_articles

class Block():
    def __init__(self, block_type:ContentType, position: int=0, header_context: str="", text: str=""):
        self.block_type = block_type
        self.header_context = header_context
        self.text = text
        self.position = 0 # what numbered header the block is under
    
    def as_json(self):
        """
        returns formatted version of a block fo easier json parsing
        args: none
        returns: json-fied version of a block
        """
        return {
            "block_type": self.block_type.name,
            "header_context": self.header_context,
            "text": self.text
        }



# a single file of notes is a document, or a collection of blocks
class Document:
    def __init__(self, blocks: list[Block],course_code: str, semester: str):
        self.nlp = en_core_web_sm.load()
        self.blocks = blocks

        self.course_code = course_code
        self.semester = semester
        
    def add_block(self, b: Block):
        self.blocks.append(b)
    
    def as_concepts(self) -> list[Block]:
        """
        purpose: chunks all the text/blocks of the document into possible concepts; normalize such that they are as uniform as possible
        """
        res = []
        for block in self.blocks:
                
            process_doc = self.nlp(block.text)

            for chunk in process_doc.noun_chunks:
                res.append(Block(block.block_type, block.position, block.header_context, remove_articles(chunk.text.lower())))
        
        return res  


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

    
    

        
        

        