import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("p", "This is a paragraph")
        node3 = HTMLNode()
        node4 = HTMLNode("h1", "This is a heading", [node,node3], {"href": "https://www.google.com","target": "_blank",})
        node5 = HTMLNode("h1", "This is a heading", [node], {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node4, node5)
        self.assertEqual(node4.props_to_html(), node5.props_to_html())
        self.assertEqual(node4.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_to_html_leafnode(self):
        leafnode1 = LeafNode("a", "Google", {"href": "https://www.google.com"})
        leafnode2 = LeafNode("a", "Google", {"href": "https://www.google.com"})
        leafnode3 = LeafNode("p", "Hello, world!")
        leafnode4 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        leafnode5 = LeafNode(None, "Normal text")
        self.assertEqual(leafnode1, leafnode2)
        self.assertEqual(leafnode3.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(leafnode4.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertRaises(ValueError, LeafNode, tag="p", value=None)
        self.assertEqual(leafnode5.to_html(), "Normal text")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        node = TextNode("THIS IS BOLD", "bold")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "THIS IS BOLD")
        node = TextNode("Click me!", "link", "https://github.com/sebaperz")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://github.com/sebaperz"})

if __name__ == "__main__":
    unittest.main()
