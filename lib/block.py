import json
import en_core_web_sm

from lib.lib import ContentType

class Block():
    def __init__(self,id: str, block_type:ContentType, header_context: str="", text: str=""):
        self.id = id
        self.block_type = block_type
        self.header_context = header_context
        self.text = text
    
    def as_json(self):
        return {
            "id": self.id,
            "block_type": self.block_type.name,
            "header_context": self.header_context,
            "text": self.text
        }
        

# a single file of notes is a document, or a collection of blocks
class Document:
    def __init__(self, blocks: list[Block],course_code: str, semester: str):
        self.blocks = blocks
        self.course_code = course_code
        self.semester = semester
        
    
    def add_block(self, b: Block):
        self.blocks.append(b)

    def as_json(self):
        return json.dumps({
            "course_code" : self.course_code,
            "semester" : self.semester,
            "blocks" : [block.as_json() for block in self.blocks]
        })
    
    def get_text(self):
        '''
        returns all text from document; all metadata stripped
        '''

        text = ""
        for b in self.blocks:
            text += f"{b.text} "
        return text
    
    def chunk_nouns(self):
        nlp = en_core_web_sm.load()
        res = []
        for block in self.blocks:
            process_doc = nlp(block.text)
            
            for chunk in process_doc.noun_chunks:
                res.append(Block(block.id,block.block_type, block.header_context, chunk))
            
        return res
        

        