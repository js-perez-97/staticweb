import unittest

from src.markdown_to_html import markdown_to_html

class TestMarkdownToHTML(unittest.TestCase):

    def test_markdown_paragraph(self):
        text = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

        """
        self.assertEqual(markdown_to_html(text), "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")
        text = """
This is **a**
test
in
**a**
single
paragraph

and other
paragraph
        """
        self.assertEqual(markdown_to_html(text),"<div><p>This is <b>a</b> test in <b>a</b> single paragraph</p><p>and other paragraph</p></div>")

