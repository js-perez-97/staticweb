import unittest

from textnode import TextNode, TextType
from markdowntext import text_to_textnodes, markdown_to_blockmarkdown

class TestMarkdownText(unittest.TestCase):

    def test_text_to_textnodes(self):
        # Test text to text nodes
        text = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        text_nodes = text_to_textnodes(text)
        self.assertEqual(text_nodes, [TextNode(
            'This is ', TextType.TEXT), TextNode('text', TextType.BOLD), TextNode(' with an ', TextType.TEXT), TextNode('italic', TextType.ITALIC), TextNode(' word and a ', TextType.TEXT), TextNode('code block', TextType.CODE), TextNode(' and an ', TextType.TEXT), TextNode('obi wan image', TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), TextNode(' and a ', TextType.TEXT), TextNode('link', TextType.LINK, "https://boot.dev")])
        text = 'This is a [link](https://boot.dev), and another one [here](https://boot.dev) and **bold** text, and a ![image](https://boot.dev) and another ![image](https://boot.dev) and a `code block` and another `code block`'
        text_nodes = text_to_textnodes(text)
        self.assertEqual(text_nodes, [TextNode(
            'This is a ', TextType.TEXT), TextNode('link', TextType.LINK, "https://boot.dev"), TextNode(', and another one ', TextType.TEXT), TextNode('here', TextType.LINK, "https://boot.dev"), TextNode(' and ', TextType.TEXT), TextNode('bold', TextType.BOLD), TextNode(' text, and a ', TextType.TEXT), TextNode('image', TextType.IMAGE, "https://boot.dev"), TextNode(' and another ', TextType.TEXT), TextNode('image', TextType.IMAGE, "https://boot.dev"), TextNode(' and a ', TextType.TEXT), TextNode('code block', TextType.CODE), TextNode(' and another ', TextType.TEXT), TextNode('code block', TextType.CODE)])

    def test_markdown_to_blockmarkdown(self):
        # Test markdown to markdown block
        text = '# This is a heading\n\n\nThis is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n\nThis\n\n\naja\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item\n\n\n\n\n\nah\n\n'
        self.assertEqual(markdown_to_blockmarkdown(text), ['# This is a heading', 'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.', 'This', 'aja', '- This is the first list item in a list block- This is a list item- This is another list item', 'ah'])
        text = '\n\n\n Test test test, i lo\nve\n\n\n writting test\n\n\n there are the on\nly\n\n\nway to be sure this c\no\nd\ne\n\n\n WORK\n'
        self.assertEqual(markdown_to_blockmarkdown(text), [' Test test test, i love', ' writting test', ' there are the only', 'way to be sure this code', ' WORK'])
