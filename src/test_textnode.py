import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
