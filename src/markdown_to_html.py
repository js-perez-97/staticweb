from htmlnode import LeafNode, ParentNode

from markdowntext import BlockType, block_to_BlockType, markdown_to_markdownblocks
from textnode import text_node_to_html_node
from textnode_delimiter import text_to_textnodes

def markdown_to_html(text) -> str:
    text = markdown_to_markdownblocks(text)
    html = []
    print(text)
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
                _quote_to_html_node(block, html)
            case BlockType.LIST:
                _list_to_html_node(block, html)
            case _:
                return("invalid block type")
    return ParentNode("div", html).to_html()

def _paragraph_to_html_node(block, html) -> None:
    block = block.replace('\n', " ")
    block = text_to_textnodes(block)
    block = [text_node_to_html_node(node) for node in block]
    html.append(ParentNode("p", block))

def _heading_to_html_node(block, html) -> None:
    print(block)
    block = block.replace('\n', " ")
    block = block.split(" ", 1)
    tag = "h" + str(len(block[0]))
    block_text = block[1]
    block_text = text_to_textnodes(block_text)
    block_text = [text_node_to_html_node(node) for node in block_text]
    html.append(ParentNode(tag, block_text))

def _code_to_html_node(block, html) -> None:
    block = block[4:-4]
    block = [LeafNode("code", block)]
    html.append(ParentNode("pre", block))

def _quote_to_html_node(block, html) -> None:
    block = block.replace('\n', " ") #something like this??
    block = block.replace("> ", "")
    block = text_to_textnodes(block)
    block = [text_node_to_html_node(node) for node in block]
    html.append(ParentNode("blockquote", block))

def _list_to_html_node(block, html) -> None:
    if block[0] == "-":
        type_of_list = "u"
        num_of_chars = 2
    elif block[0] == "1":
        type_of_list = "o"
        num_of_chars = 3
    else:
        raise Exception("How did u end here?, wrong HTMLList")
    
    text = block.split("\n")
    for i in range(len(text)):
        inden_level = indentation_level(text[i])
        if len(text) > (i+1):
            next_inden_level = indentation_level(text[i+1])
        else:
            next_inden_level = 0
            
        text[i] = text[i][inden_level+num_of_chars::]
        text[i] = "<li>"+text[i]
        if inden_level < next_inden_level:
            text[i] += "<"+type_of_list+"l>"
        if inden_level == next_inden_level:
            text[i] += "</li>"
        if inden_level > next_inden_level:
            text[i] += "</li></"+type_of_list+"l>" + '</li>'*(inden_level//4 - next_inden_level//4)
        text[i] = text_to_textnodes(text[i])
        text[i] = [text_node_to_html_node(node) for node in text[i]]
    html.append(ParentNode(type_of_list+"l",sum(text,[])))

def indentation_level(text) -> int:
    level = 0
    for char in text:
        if char==" ":
            level += 1
        else:
            break
    if level%4 != 0:
        raise ValueError("Wrong indentation, it have to be: 4")
    return level
