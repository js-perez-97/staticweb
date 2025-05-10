import unittest

from markdowntext import markdown_to_markdownblocks, BlockType, block_to_block_type

class TestMarkdownText(unittest.TestCase):

    def test_markdown_to_markdownblocks(self):
        # Test markdown to markdown block
        text = '# This is a heading\n\n\nThis is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n\nThis\n\n\naja\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item\n\n\n\n\n\nah\n\n'
        self.assertEqual(markdown_to_markdownblocks(text), ['# This is a heading', 'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.', 'This', 'aja', '- This is the first list item in a list block\n- This is a list item\n- This is another list item', 'ah'])
        text = '\n\n\n Test test test, i lo\nve\n\n\n writting test\n\n\n there are the on\nly\n\n\nway to be sure this c\no\nd\ne\n\n\n WORK \n\n\n -work \n - work \n -  work\n'
        self.assertEqual(markdown_to_markdownblocks(text), ['Test test test, i lo\nve', 'writting test', 'there are the on\nly', 'way to be sure this c\no\nd\ne', 'WORK', '-work \n - work \n -  work'])

    def test_block_to_block_type(self):
        # Test block to block type
        self.assertEqual(block_to_block_type("# This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```"), BlockType.CODE)
        self.assertEqual(block_to_block_type(">"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("-"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1."), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("This is a paragraph of text. It has some **bold** and _italic_ words inside of it."), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
