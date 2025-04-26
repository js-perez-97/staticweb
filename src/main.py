from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
    dummy = TextNode("This is some anchor text", "link", "https://example.com")
    print(dummy)
    dummy2 = TextNode("This is some anchor text", TextType.BOLD, "https://example.com")
    print(dummy2)
    node = LeafNode("img","IMAGEN",{"src":"https://example.com/image.jpg", "alt":"Image description"})
    print(node.to_html())
main()
