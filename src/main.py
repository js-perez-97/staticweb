from textnode import TextNode, TextType

def main():
    dummy = TextNode("This is some anchor text", "link", "https://example.com")
    print(dummy)
    dummy2 = TextNode("This is some anchor text", TextType.BOLD, "https://example.com")
    print(dummy2)

main()
