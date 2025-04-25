from textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method must be implemented")

    def props_to_html(self):
        if self.props:
            return ''.join([f' {key}="{value}"' for key, value in self.props.items()])
        return ''

    def __repr__(self):
        return f"HtmlNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

    def to_html(self):
        if self.tag != None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"{self.value}"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes must have children")

    def to_html(self):
        if self.children is not None:
            return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
        raise ValueError("All parent nodes must have children")

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
        case TextType.IMAGE:
            return LeafNode("img", None, props={"src": text_node.url})
        case _:
            raise Exception("Invalid text type")
