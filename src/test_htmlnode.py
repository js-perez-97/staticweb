import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
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

if __name__ == "__main__":
    unittest.main()
