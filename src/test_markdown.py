import unittest

from markdown_to_textnode import split_nodes_delimiter
from textnode import TextNode, TextType


class TestMarkdownTextNode(unittest.TestCase):
    def test_split_nodes_delimiter(self):

        # Test self equal
        node0 = TextNode(
            "This is text with a `code block` word", TextType.TEXT)
        node1 = TextNode(
            "This is text with a `code block` word", TextType.TEXT)
        node0_split = split_nodes_delimiter([node0], "`", TextType.CODE)
        self.assertEqual(split_nodes_delimiter(
            [node0], "`", TextType.CODE), split_nodes_delimiter([node1], "`", "code"))

        # Test correct split prev TextType.TEXT
        node2 = TextNode("This is text with a ", TextType.TEXT)
        self.assertEqual(node0_split[0], node2)

        # Test correct left and right TEXT nodes
        node0 = TextNode("This is text with a **bold** text", TextType.TEXT)
        node1 = TextNode("This is text with a **bold**", TextType.TEXT)
        node2 = TextNode("**bold** text", TextType.TEXT)
        node3 = TextNode("This is text with a **** text", TextType.TEXT)
        node0_split = split_nodes_delimiter([node0], "**", TextType.BOLD)
        node1_split = split_nodes_delimiter([node1], "**", TextType.BOLD)
        node2_split = split_nodes_delimiter([node2], "**", TextType.BOLD)
        node3_split = split_nodes_delimiter([node3], "**", TextType.BOLD)
        self.assertEqual(node0_split, [TextNode('This is text with a ', TextType.TEXT), TextNode(
            'bold', TextType.BOLD), TextNode(' text', TextType.TEXT)])
        self.assertEqual(node1_split, [TextNode(
            'This is text with a ', TextType.TEXT), TextNode('bold', TextType.BOLD)])
        self.assertEqual(node2_split, [TextNode(
            'bold', TextType.BOLD), TextNode(' text', TextType.TEXT)])
        self.assertEqual(node3_split, [TextNode(
            'This is text with a ', TextType.TEXT), TextNode(' text', TextType.TEXT)])

        # Test correct image and link nodes
        node0 = TextNode(
            "This is a [link](https://boot.dev)", TextType.TEXT)
        node1 = TextNode(
            "This is a ![image, alt text include](https://boot.dev)", TextType.TEXT)
        node0_split = split_nodes_delimiter([node0], "[", TextType.LINK)
        node1_split = split_nodes_delimiter([node1], "![", TextType.IMAGE)
        self.assertEqual(node0_split, [TextNode(
            'This is a ', TextType.TEXT), TextNode('link', TextType.LINK, "https://boot.dev")])
        self.assertEqual(node1_split, [TextNode(
            'This is a ', TextType.TEXT), TextNode('image, alt text include', TextType.IMAGE, "https://boot.dev")])

        # Test recursive split
        node = TextNode(
            "This is text with a `ton of` code, like `3 or 4`, amazing, lol look a **bold** text", TextType.TEXT)
        node = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(node, [TextNode(
            'This is text with a ', TextType.TEXT), TextNode('ton of', TextType.CODE), TextNode(' code, like ', TextType.TEXT), TextNode('3 or 4', TextType.CODE), TextNode(', amazing, lol look a **bold** text', TextType.TEXT)])
        node = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(node, [TextNode(
            'This is text with a ', TextType.TEXT), TextNode('ton of', TextType.CODE), TextNode(' code, like ', TextType.TEXT), TextNode('3 or 4', TextType.CODE), TextNode(', amazing, lol look a ', TextType.TEXT), TextNode('bold', TextType.BOLD), TextNode(' text', TextType.TEXT)])
