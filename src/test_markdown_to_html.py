import unittest

from src.markdown_to_html import indentation_level, markdown_to_html, extract_title


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_paragraph(self):
        text = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here
"""
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(markdown_to_html(text), expected)

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
        expected = "<div><p>This is <b>a</b> test in <b>a</b> single paragraph</p><p>and other paragraph</p></div>"
        self.assertEqual(markdown_to_html(text), expected)

    def test_markdown_heading(self):
        text = """
# Heading 1
This is a heading

## Heading 2
This is another heading

### Heading 3
This is a third heading
"""
        expected = "<div><h1>Heading 1 This is a heading</h1><h2>Heading 2 This is another heading</h2><h3>Heading 3 This is a third heading</h3></div>"
        self.assertEqual(markdown_to_html(text), expected)

    def test_markdown_code(self):
        text = """
```
This is a *code* block
with multiple lines
and some **formatting**
```
"""
        expected = "<div><pre><code>This is a *code* block\nwith multiple lines\nand some **formatting**</code></pre></div>"
        self.assertEqual(markdown_to_html(text), expected)

    def test_markdown_quote(self):
        text = """
> This is a quote
> with *multiple* lines
> and some **formatting**

> Another quote
> with more lines
"""
        expected = "<div><blockquote>This is a quote with <i>multiple</i> lines and some <b>formatting</b></blockquote><blockquote>Another quote with more lines</blockquote></div>"
        self.assertEqual(markdown_to_html(text), expected)

        text = """
> This is a quote
> with multiple lines

and

> Another quote
> with 2 lines
"""
        expected = "<div><blockquote>This is a quote with multiple lines</blockquote><p>and</p><blockquote>Another quote with 2 lines</blockquote></div>"
        self.assertEqual(markdown_to_html(text), expected)

    def test_markdown_unordered_list(self):
        text = """
- Milk
- Cheese
    - Blue cheese
        - Feta
    - Mozzarella
- Bread
    - Sourdough
    - Rye
"""
        expected = "<div><ul><li>Milk</li><li>Cheese<ul><li>Blue cheese<ul><li>Feta</li></ul></li><li>Mozzarella</li></ul></li><li>Bread<ul><li>Sourdough</li><li>Rye</li></ul></li></ul></div>"
        self.assertEqual(markdown_to_html(text), expected)

        text = """
- This **a** list
- inside
    - inside
        - inside
    - continue
    - second
- and
- final
"""
        expected = "<div><ul><li>This <b>a</b> list</li><li>inside<ul><li>inside<ul><li>inside</li></ul></li><li>continue</li><li>second</li></ul></li><li>and</li><li>final</li></ul></div>"
        self.assertEqual(markdown_to_html(text), expected)

    def test_markdown_ordered_list(self):
        text = """
1. First item
2. Second item
    1. Nested item
    2. Another nested item
3. Third item
    1. More nesting
        1. Deep nesting
    2. Back to level 2
4. Final item
"""
        expected = "<div><ol><li>First item</li><li>Second item<ol><li>Nested item</li><li>Another nested item</li></ol></li><li>Third item<ol><li>More nesting<ol><li>Deep nesting</li></ol></li><li>Back to level 2</li></ol></li><li>Final item</li></ol></div>"
        self.assertEqual(markdown_to_html(text), expected)

    def test_markdown_mixed_content(self):
        text = """
# Main Heading

This is a paragraph with **bold** and *italic* text.

- First list item
- Second list item
    - Nested item
    - Another nested item

> This is a quote
> with multiple lines

```
This is a code block
with multiple lines
```
"""
        expected = "<div><h1>Main Heading</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><ul><li>First list item</li><li>Second list item<ul><li>Nested item</li><li>Another nested item</li></ul></li></ul><blockquote>This is a quote with multiple lines</blockquote><pre><code>This is a code block\nwith multiple lines</code></pre></div>"
        self.assertEqual(markdown_to_html(text), expected)

    def test_indentation_level(self):
        # Test valid indentation
        self.assertEqual(indentation_level("    - Item"), 4)
        self.assertEqual(indentation_level("        - Nested item"), 8)
        self.assertEqual(indentation_level("- No indentation"), 0)

        # Test invalid indentation
        with self.assertRaises(ValueError):
            indentation_level("  - Invalid indentation")  # 2 spaces
        with self.assertRaises(ValueError):
            indentation_level("   - Invalid indentation")  # 3 spaces
        with self.assertRaises(ValueError):
            indentation_level("     - Invalid indentation")  # 5 spaces

    def test_extract_title_exceptions(self):

        # Test markdown without heading
        with self.assertRaises(Exception) as context:
            extract_title("This is some content without a title")
        self.assertEqual(str(context.exception), "First Paragrath of Markdown sould be <# Title>")

        # Test markdown with wrong heading level
        with self.assertRaises(Exception) as context:
            extract_title("## This is not a level 1 heading")
        self.assertEqual(str(context.exception), "First Paragrath of Markdown sould be <# Title>")

        # Test markdown with heading not at start
        with self.assertRaises(Exception) as context:
            extract_title("Some text\n\n# Title")
        self.assertEqual(str(context.exception), "First Paragrath of Markdown sould be <# Title>")

    def test_extract_title_success(self):
        # Test simple title
        text = """
# My Title

Some more text
"""
        expected = "My Title"
        self.assertEqual(extract_title(text), expected)

        # Test title with formatting
        text = """
# My **Bold** Title

This is some content
"""
        expected = "My **Bold** Title"
        self.assertEqual(extract_title(text), expected)

        # Test title with multiple words and formatting
        text = """
# Title With Many spaces:          

Another paragrath
"""
        expected = "Title With Many spaces:"
        self.assertEqual(extract_title(text), expected)

if __name__ == "__main__":
    unittest.main()

