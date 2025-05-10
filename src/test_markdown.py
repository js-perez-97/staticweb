import unittest

from markdown_to_textnode import split_nodes_delimiter, text_to_textnodes, markdown_to_blockmarkdown
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
            [node0], "`", TextType.CODE), split_nodes_delimiter([node1], "`", TextType.CODE))

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

        # Test text to text nodes
        text = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        text_nodes = text_to_textnodes(text)
        self.assertEqual(text_nodes, [TextNode(
            'This is ', TextType.TEXT), TextNode('text', TextType.BOLD), TextNode(' with an ', TextType.TEXT), TextNode('italic', TextType.ITALIC), TextNode(' word and a ', TextType.TEXT), TextNode('code block', TextType.CODE), TextNode(' and an ', TextType.TEXT), TextNode('obi wan image', TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(' and a ', TextType.TEXT), TextNode('link', TextType.LINK, "https://boot.dev")])
        text = 'This is a [link](https://boot.dev), and another one [here](https://boot.dev) and **bold** text, and a ![image](https://boot.dev) and another ![image](https://boot.dev) and a `code block` and another `code block`'
        text_nodes = text_to_textnodes(text)
        self.assertEqual(text_nodes, [TextNode(
            'This is a ', TextType.TEXT), TextNode('link', TextType.LINK, "https://boot.dev"), TextNode(', and another one ', TextType.TEXT), TextNode('here', TextType.LINK, "https://boot.dev"), TextNode(' and ', TextType.TEXT), TextNode('bold', TextType.BOLD), TextNode(' text, and a ', TextType.TEXT), TextNode('image', TextType.IMAGE, "https://boot.dev"), TextNode(' and another ', TextType.TEXT), TextNode('image', TextType.IMAGE, "https://boot.dev"), TextNode(' and a ', TextType.TEXT), TextNode('code block', TextType.CODE), TextNode(' and another ', TextType.TEXT), TextNode('code block', TextType.CODE)])

        # Test markdwon to markdown block
        text = '# This is a heading\n\n\nThis is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n\nThis\n\n\naja\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item\n\n\n\n\n\nah\n\n'
        self.assertEqual(markdown_to_blockmarkdown(text), ['# This is a heading', 'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.', 'This', 'aja', '- This is the first list item in a list block- This is a list item- This is another list item', 'ah'])
