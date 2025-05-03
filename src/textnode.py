from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"          # Regular text
    BOLD = "bold"          # **bold text**
    ITALIC = "italic"      # *italic text*
    CODE = "code"          # `code snippet`
    LINK = "link"          # [link text](url)
    IMAGE = "image"        # ![alt text](image_url)


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        if self.url:
            return f"TextNode('{self.text}', {self.text_type}, {self.url})"
        return f"TextNode('{self.text}', {self.text_type})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        # should return LeafNode with "img" tag, empty string vales, props("src" is the image URL, "alt" is the alt Text
        case TextType.IMAGE:
            return LeafNode("img", text_node.text, props={"src": text_node.url, "alt": text_node.text})

    raise Exception("Invalid text type")
