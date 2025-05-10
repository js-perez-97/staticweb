import re
from textnode import TextNode, TextType


def split_nodes_delimiter(list_of_old_nodes: list, delimiter: str, text_type: TextType) -> list:
    # Split text nodes based on a delimiter and assign appropriate TextType to the split parts.

    if not isinstance(list_of_old_nodes, list):
        raise ValueError("list_of_old_nodes must be a list")

    # TODO: IF list_of_old_nodes != type(list) then list_of_old_nodes = [list_of_old_nodes]
    list_new_nodes = []
    text_type = TextType(text_type)

    # Handle simple delimiters (code and bold)
    if delimiter in ("`", "**"):
        return _handle_simple_delimiter(list_of_old_nodes, delimiter, text_type, list_new_nodes)

    # Handle single asterisk
    elif delimiter == "*":
        return _handle_asterisk_delimiter(list_of_old_nodes, text_type, list_new_nodes)

    # Handle image format
    elif delimiter == "![":
        return _handle_image_delimiter(list_of_old_nodes, text_type, list_new_nodes)

    # Handle link format
    elif delimiter == "[":
        return _handle_link_delimiter(list_of_old_nodes, text_type, list_new_nodes)

    # Handle errors
    else:
        raise ValueError(f"Unsupported delimiter: {delimiter}")


def _handle_simple_delimiter(list_of_old_nodes: list, delimiter: str, text_type: TextType, list_new_nodes: list) -> list:
    for node in list_of_old_nodes:
        if delimiter not in node.text:
            list_new_nodes.append(node)
            continue
        nodeparts = node.text.split(delimiter)
        for i in range(len(nodeparts)):
            if nodeparts[i] == "":
                continue
            if i % 2 == 0:
                list_new_nodes.append(TextNode(nodeparts[i], TextType.TEXT))
            else:
                list_new_nodes.append(TextNode(nodeparts[i], text_type))
    return list_new_nodes


def _handle_asterisk_delimiter(list_of_old_nodes: list, text_type: TextType, list_new_nodes: list) -> list:
    for node in list_of_old_nodes:
        if "*" not in node.text:
            list_new_nodes.append(node)
            continue
            # Regex to match single asterisks | (?<!\*) - not preceded by an asterisk (negative lookbehind) | \* - match an asterisk | (?!\*) - not followed by an asterisk (negative lookahead)
        nodeparts = re.split(r'(?<!\*)\*(?!\*)', node.text)
        for i in range(len(nodeparts)):
            if nodeparts[i] == "":
                continue
            if i % 2 == 0:
                list_new_nodes.append(TextNode(nodeparts[i], TextType.TEXT))
            else:
                list_new_nodes.append(TextNode(nodeparts[i], text_type))
    return list_new_nodes

def _handle_image_delimiter(list_of_old_nodes: list, text_type: TextType, list_new_nodes: list) -> list:
    for node in list_of_old_nodes:
        if "![" not in node.text:
            list_new_nodes.append(node)
            continue
        nodeparts = node.text.split("![", 1)
        if nodeparts[0]:
            list_new_nodes.append(TextNode(nodeparts[0], TextType.TEXT))
        two_nodeparts = nodeparts[1].split(")", 1)
        link_and_url = two_nodeparts[0].split("](")
        list_new_nodes.append(
            TextNode(link_and_url[0], text_type, link_and_url[1]))
        if two_nodeparts[1]:
            list_new_nodes.extend(split_nodes_delimiter(
                [TextNode(two_nodeparts[1], TextType.TEXT)], "![", TextType.IMAGE))
    return list_new_nodes

def _handle_link_delimiter(list_of_old_nodes: list, text_type: TextType, list_new_nodes: list) -> list:
    for node in list_of_old_nodes:
        if "[" not in node.text:
            list_new_nodes.append(node)
            continue
        nodeparts = node.text.split("[", 1)
        if nodeparts[0]:
            list_new_nodes.append(TextNode(nodeparts[0], TextType.TEXT))
        two_nodeparts = nodeparts[1].split(")", 1)
        link_and_url = two_nodeparts[0].split("](")
        list_new_nodes.append(
            TextNode(link_and_url[0], text_type, link_and_url[1]))
        if two_nodeparts[1]:
            list_new_nodes.extend(split_nodes_delimiter(
                [TextNode(two_nodeparts[1], TextType.TEXT)], "[", TextType.LINK))
    return list_new_nodes
