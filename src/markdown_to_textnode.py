import re
from textnode import TextNode, TextType


def split_nodes_delimiter(list_of_old_nodes, delimiter, text_type):
    # Split text nodes based on a delimiter and assign appropriate TextType to the split parts.

    # TODO: IF list_of_old_nodes != type(list) then list_of_old_nodes = [list_of_old_nodes]
    output = []
    text_type = TextType(text_type)

    # Handle simple delimiters (code and bold)
    if delimiter in ("`", "**"):
        return _handle_simple_delimiter(list_of_old_nodes, delimiter, text_type, output)

    # Handle single asterisk
    elif delimiter == "*":
        return _handle_asterisk_delimiter(list_of_old_nodes, text_type, output)

    # Handle link format
    elif delimiter == "[":
        return _handle_link_delimiter(list_of_old_nodes, text_type, output)

    # Handle image format
    elif delimiter == "![":
        return _handle_image_delimiter(list_of_old_nodes, text_type, output)

    # Handle errors
    else:
        raise ValueError(f"Unsupported delimiter: {delimiter}")


def _handle_simple_delimiter(list_of_old_nodes, delimiter, text_type, output):
    for node in list_of_old_nodes:
        if delimiter in node.text:
            nodeparts = node.text.split(delimiter)
            for i in range(len(nodeparts)):
                if nodeparts[i] == "":
                    continue

                if i % 2 == 0:
                    output.append(TextNode(nodeparts[i], TextType.TEXT))
                else:
                    output.append(TextNode(nodeparts[i], text_type))
        else:
            output.append(node)
    return output


def _handle_asterisk_delimiter(list_of_old_nodes, text_type, output):
    for node in list_of_old_nodes:
        if "*" in node.text:
            # Regex to match single asterisks | (?<!\*) - not preceded by an asterisk (negative lookbehind) | \* - match an asterisk | (?!\*) - not followed by an asterisk (negative lookahead)
            nodeparts = re.split(r'(?<!\*)\*(?!\*)', node.text)
            for i in range(len(nodeparts)):
                if nodeparts[i] == "":
                    continue

                if i % 2 == 0:
                    output.append(TextNode(nodeparts[i], TextType.TEXT))
                else:
                    output.append(TextNode(nodeparts[i], text_type))
        else:
            output.append(node)
    return output


def _handle_link_delimiter(list_of_old_nodes, text_type, output):
    for node in list_of_old_nodes:
        if "[" in node.text:
            nodeparts = node.text.split("[", 1)
            if nodeparts[0]:
                output.append(TextNode(nodeparts[0], TextType.TEXT))

            two_nodeparts = nodeparts[1].split(")", 1)
            link_and_url = two_nodeparts[0].split("](")
            output.append(
                TextNode(link_and_url[0], text_type, link_and_url[1]))

            if two_nodeparts[1]:
                output.extend(split_nodes_delimiter(
                    [TextNode(two_nodeparts[1], TextType.TEXT)], "[", TextType.LINK))
        else:
            output.append(node)
    return output


def _handle_image_delimiter(list_of_old_nodes, text_type, output):
    for node in list_of_old_nodes:
        if "![" in node.text:
            nodeparts = node.text.split("![", 1)
            if nodeparts[0]:
                output.append(TextNode(nodeparts[0], TextType.TEXT))

            two_nodeparts = nodeparts[1].split(")", 1)
            link_and_url = two_nodeparts[0].split("](")
            output.append(
                TextNode(link_and_url[0], text_type, link_and_url[1]))

            if two_nodeparts[1]:
                output.extend(split_nodes_delimiter(
                    [TextNode(two_nodeparts[1], TextType.TEXT)], "![", TextType.IMAGE))
        else:
            output.append(node)
    return output

def markdown_to_blockmarkdown(text):
    text = text.split('\n\n')
    for i in range(len(text)):
        text[i] = text[i].replace('\n','')
    return text

aja = '''# This is a heading



This is a paragraph of text. It has some **bold** and _italic_ words inside of it.


This

aja

- This is the first list item in a list block
- This is a list item
- This is another list item




'''

print(markdown_to_blockmarkdown(aja))
print('\nThis'.replace('\n',''))