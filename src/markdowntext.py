
from textnode import TextNode, TextType
from textnode_delimiter import split_nodes_delimiter


def markdown_to_blockmarkdown(text):
    text = text.split('\n\n')
    block = []
    for i in range(len(text)):
        text[i] = text[i].replace('\n','')
        if text[i]:
            block.append(text[i])
    return block

def text_to_textnodes(text):
    text = TextNode(text, TextType.TEXT)
    text = split_nodes_delimiter([text], "`", TextType.CODE)
    text = split_nodes_delimiter(text, "*", TextType.ITALIC)
    text = split_nodes_delimiter(text, "**", TextType.BOLD)
    text = split_nodes_delimiter(text, "![", TextType.IMAGE)
    text = split_nodes_delimiter(text, "[", TextType.LINK)
    return text
