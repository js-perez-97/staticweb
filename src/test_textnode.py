import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", "bold")
        node4 = TextNode("This is a text", "link", "example.com")
        node5 = TextNode("This is a text", TextType.LINK, "example.com")
        self.assertEqual(node, node2)
        self.assertEqual(node, node3)
        self.assertEqual(node4, node5)
        self.assertNotEqual(node, node5)

    def test_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

        node = TextNode("This is a text node in bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node in bold")
        self.assertEqual(html_node.props, None)

        node = TextNode("This is a text node in italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node in italic")
        self.assertEqual(html_node.props, None)

        node = TextNode("This is a text node in code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node in code")
        self.assertEqual(html_node.props, None)

        node = TextNode("This is a text node link", TextType.LINK, "example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node link")
        self.assertEqual(html_node.props, {"href": "example.com"})

        node = TextNode("This is a text node image", TextType.IMAGE, "example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "This is a text node image")
        self.assertEqual(html_node.props, {"src": "example.com", "alt": "This is a text node image"})


if __name__ == "__main__":
    unittest.main()
