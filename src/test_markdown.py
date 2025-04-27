import unittest

from markdown_to_textnode import split_nodes_delimiter
from textnode import TextNode, TextType

class TestMarkdownTextNode(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        # Test self equal
        node0 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node0_split = split_nodes_delimiter([node0], "`", TextType.CODE)
        self.assertEqual(split_nodes_delimiter([node0], "`", TextType.CODE), split_nodes_delimiter([node1], "`", "code"))

        # Test correct split prev TextType.TEXT
        node2 = TextNode("This is text with a ", TextType.TEXT)
        self.assertEqual(node0_split[0], node2)

        #Test correct left and right TEXT nodes
        node0 = TextNode("This is text with a **bold** text", TextType.TEXT)
        node1 = TextNode("This is text with a **bold**", TextType.TEXT)
        node2 = TextNode("**bold** text", TextType.TEXT)
        node3 = TextNode("This is text with a **** text", TextType.TEXT)
        node0_split = split_nodes_delimiter([node0], "**", TextType.BOLD)
        node1_split = split_nodes_delimiter([node1], "**", TextType.BOLD)
        node2_split = split_nodes_delimiter([node2], "**", TextType.BOLD)
        node3_split = split_nodes_delimiter([node3], "**", TextType.BOLD)
        self.assertEqual(node0_split,[TextNode('This is text with a ', TextType.TEXT), TextNode('bold', TextType.BOLD), TextNode(' text', TextType.TEXT)])
        self.assertEqual(node1_split,[TextNode('This is text with a ', TextType.TEXT), TextNode('bold', TextType.BOLD)])
        self.assertEqual(node2_split,[TextNode('bold', TextType.BOLD), TextNode(' text', TextType.TEXT)])
        self.assertEqual(node3_split,[TextNode('This is text with a ', TextType.TEXT), TextNode(' text', TextType.TEXT)])
