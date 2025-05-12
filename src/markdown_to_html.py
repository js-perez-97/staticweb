from htmlnode import HTMLNode, LeafNode, ParentNode

from markdowntext import BlockType, block_to_BlockType, markdown_to_markdownblocks
from textnode import TextNode, text_node_to_html_node
from textnode_delimiter import text_to_textnodes

def markdown_to_html(text) -> str:
    text = markdown_to_markdownblocks(text)
    # print(f"1: {text}")
    html = []
    for block in text:
        block_type = block_to_BlockType(block)
        match block_type:
            case BlockType.PARAGRAPH:
                _paragraph_to_html_node(block, html)
            case BlockType.HEADING:
                _heading_to_html_node(block, html)
            case BlockType.CODE:
                _code_to_html_node(block, html)
            case BlockType.QUOTE:
                print(block)
                _quote_to_html_node(block, html)
            case BlockType.UNORDERED_LIST:
                _unorderedlist_to_html_node(block, html)
            case BlockType.ORDERED_LIST:
                _orederedlist_to_html_node(block, html)
            case _:
                return("invalid block type")
    return ParentNode("div", html).to_html()

def _paragraph_to_html_node(block, html) -> None:
    block = block.replace('\n', " ")
    block = text_to_textnodes(block)
    block = [text_node_to_html_node(node) for node in block]
    html.append(ParentNode("p", block))

def _heading_to_html_node(block, html) -> None:
    block = block.replace('\n', " ")
    block = block.split(" ", 1)
    tag = "h" + str(len(block[0]))
    block_text = block[1]
    block_text = text_to_textnodes(block_text)
    block_text = [text_node_to_html_node(node) for node in block_text]
    html.append(ParentNode(tag, block_text))

def _code_to_html_node(block, html) -> None:
    block = block[4:-3]
    block = [LeafNode("code", block)]
    html.append(ParentNode("pre", block))

def _quote_to_html_node(block, html) -> None:
    block = block.replace('\n', " ") #something like this??
    block = block.replace("> ", "")
    block = text_to_textnodes(block)
    block = [text_node_to_html_node(node) for node in block]
    html.append(ParentNode("blockquote", block))

def _unorderedlist_to_html_node(block, html) -> None:
    print("todo")

def _orederedlist_to_html_node(block, html) -> None:
    print("todo")
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
text = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
# print(markdown_to_html(text)=="<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")
test ="<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
# print(test==markdown_to_html(text))

text = """
> This is a quote
> with multiple lines

and

> Another quote
> with 2 lines
"""
test = "<div><blockquote>This is a quote with multiple lines</blockquote><p>and</p><blockquote>Another quote with 2 lines</blockquote></div>"
print(markdown_to_html(text))
print(test)
print(test==markdown_to_html(text))
