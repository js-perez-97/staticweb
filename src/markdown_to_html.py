from htmlnode import HTMLNode, LeafNode, ParentNode

from markdowntext import BlockType, block_to_BlockType, markdown_to_markdownblocks
from textnode import text_node_to_html_node
from textnode_delimiter import text_to_textnodes

def markdown_to_html(text):
    text = markdown_to_markdownblocks(text)
    print(f"1: {text}")
    html = []
    for block in text:
        block_type = block_to_BlockType(block)
        match block_type:
            case BlockType.PARAGRAPH:
                _paragraph_to_html_node(block, html)
            case BlockType.HEADING:
                # print(f"2: {block_type == BlockType.HEADING}")
                _heading_to_html_node(block, html)
            case BlockType.CODE:
                return
            case BlockType.QUOTE:
                return
            case BlockType.UNORDERED_LIST:
                return
            case BlockType.ORDERED_LIST:
                return
            case _:
                return("invalid block type")
    return ParentNode("div", html).to_html()

def _paragraph_to_html_node(block, html):
    block = block.replace('\n', " ")
    block = text_to_textnodes(block)
    block = [text_node_to_html_node(node) for node in block]
    html.append(ParentNode("p", block))

def _heading_to_html_node(block, html):
    block = block.replace('\n', " ")
    block = block.split(" ", 1)
    print(block)
    tag = "h" + str(len(block[0]))
    block_text = block[1]
    block_text = text_to_textnodes(block_text)
    block_text = [text_node_to_html_node(node) for node in block_text]
    html.append(ParentNode(tag, block_text))



text = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""
text = """
# Heading 1
an continuity

## Heading 2
jeje

### Headings have to
have 2 double taps to
dont be part of the heading

"""

# print(markdown_to_html(text)=="<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")
print(markdown_to_html(text))
