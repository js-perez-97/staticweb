from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code" #"```"
    QUOTE = "quote" #">"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class Block:
    def __init__(self, text, block_type):
        self.text = text
        self.block_type = block_type

    def __eq__(self, other):
        return self.text == other.text and self.block_type == other.block_type

    def __repr__(self):
        return f"Block('{self.text}', {self.block_type})"

def block_to_BlockType(text):
    if text.startswith("#"):
        return BlockType.HEADING
    elif text.startswith("```"):
        return BlockType.CODE
    elif text.startswith(">"):
        return BlockType.QUOTE
    elif text.startswith("-"):
        return BlockType.UNORDERED_LIST
    elif text.startswith("1."):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_markdownblocks(text):
    text = text.split('\n\n')
    block = []
    for i in range(len(text)):
        text[i] = text[i].strip()
        if text[i]:
            block.append(text[i])
    return block
