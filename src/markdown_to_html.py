from htmlnode import LeafNode, ParentNode

from markdowntext import BlockType, block_to_BlockType, markdown_to_markdownblocks
from textnode import text_node_to_html_node
from textnode_delimiter import text_to_textnodes

def markdown_to_html(text) -> str:
    text = markdown_to_markdownblocks(text)
    html = []
    print(text)
    for block in text:
        block_type = block_to_BlockType(block)
        match block_type:
            case BlockType.PARAGRAPH:
                _paragraph_to_html_node(block, html)
            case BlockType.HEADING:
                _heading_to_html_node(block, html)
            case BlockType.CODE:
                _code_to_html_node(block, html)
            case BlockType.QUOTE:
                _quote_to_html_node(block, html)
            case BlockType.LIST:
                _list_to_html_node(block, html)
            case _:
                return("invalid block type")
    return ParentNode("div", html).to_html()

def _paragraph_to_html_node(block, html) -> None:
    block = block.replace('\n', " ")
    block = text_to_textnodes(block)
    block = [text_node_to_html_node(node) for node in block]
    html.append(ParentNode("p", block))

def _heading_to_html_node(block, html) -> None:
    print(block)
    block = block.replace('\n', " ")
    block = block.split(" ", 1)
    tag = "h" + str(len(block[0]))
    block_text = block[1]
    block_text = text_to_textnodes(block_text)
    block_text = [text_node_to_html_node(node) for node in block_text]
    html.append(ParentNode(tag, block_text))

def _code_to_html_node(block, html) -> None:
    block = block[4:-4]
    block = [LeafNode("code", block)]
    html.append(ParentNode("pre", block))

def _quote_to_html_node(block, html) -> None:
    block = block.replace('\n', " ") #something like this??
    block = block.replace("> ", "")
    block = text_to_textnodes(block)
    block = [text_node_to_html_node(node) for node in block]
    html.append(ParentNode("blockquote", block))

def _list_to_html_node(block, html) -> None:
    if block[0] == "-":
        type_of_list = "u"
        num_of_chars = 2
    elif block[0] == "1":
        type_of_list = "o"
        num_of_chars = 3
    else:
        raise Exception("How did u end here?, wrong HTMLList")
    
    text = block.split("\n")
    for i in range(len(text)):
        inden_level = indentation_level(text[i])
        if len(text) > (i+1):
            next_inden_level = indentation_level(text[i+1])
        else:
            next_inden_level = 0
            
        text[i] = text[i][inden_level+num_of_chars::]
        text[i] = "<li>"+text[i]
        if inden_level < next_inden_level:
            text[i] += "<"+type_of_list+"l>"
        if inden_level == next_inden_level:
            text[i] += "</li>"
        if inden_level > next_inden_level:
            text[i] += "</li></"+type_of_list+"l>" + '</li>'*(inden_level//4 - next_inden_level//4)
        text[i] = text_to_textnodes(text[i])
        text[i] = [text_node_to_html_node(node) for node in text[i]]
    html.append(ParentNode(type_of_list+"l",sum(text,[])))

def indentation_level(text) -> int:
    level = 0
    for char in text:
        if char==" ":
            level += 1
        else:
            break
    if level%4 != 0:
        raise ValueError("Wrong indentation, it have to be: 4")
    return level

text = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""
# print(markdown_to_html(text))
text = """
# Heading 1
an continuity

## Heading 2
jeje

### Headings have to
have 2 double taps to
dont be part of the heading

"""
print(markdown_to_html(text))
text = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
# print(markdown_to_html(text)=="<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")
test ="<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
# print(test==markdown_to_html(text))

text = """
> This is a quote
> with multiple lines

and

> Another quote
> with 2 lines
"""
test = "<div><blockquote>This is a quote with multiple lines</blockquote><p>and</p><blockquote>Another quote with 2 lines</blockquote></div>"
# print(markdown_to_html(text))
# print(test)
# print(test==markdown_to_html(text))

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
# print(markdown_to_html(text))##########33
text = """
- Milk
- Cheese
    - Blue
    - Feta
"""
test = "<ul><li>Milk</li><li>Cheese<ul><li>Bluecheese</li><li>Feta</li></ul></li></ul>"

text = """
- Milk
- Cheese
    - Blue
    -Feta
"""
# print(markdown_to_html(text))
#
# ordered list:
#
text = """
1. Tomar el pan
2. Tomar la mermelada
    1. Ver si la mermelada no esta **vencida**
    2. Ver si el pan no tiene *moho*
3. Acarisiar al perro
4. Olvidar por que fuiste a la cocina
"""
# print(markdown_to_html(text))
