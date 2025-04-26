from textnode import TextNode, TextType

def split_nodes_delimiter(list_of_old_nodes, delimiter, text_type):
    output = []
    for node in list_of_old_nodes:
        if delimiter in node.text:
            nodeparts = node.text.split(delimiter)
            for i in range(len(nodeparts)):
                if i%2==0 and nodeparts[i]!="":
                    output.append(TextNode(nodeparts[i], TextType.TEXT))
                if i%2==1 and nodeparts[i]!="":
                    output.append(TextNode(nodeparts[i], text_type))
        else:
            output.append(node)
    return output

node = TextNode("This is text with a `code block` word", TextType.TEXT)
node = TextNode("This is text with a `code block`", TextType.TEXT)
node = TextNode("This is text with a **bold** text", TextType.TEXT)
node = TextNode("This is text with a `ton of` code, like `3 or 4`, amazing, lol look a **bold** text", TextType.TEXT)
node = TextNode("**bold** text", TextType.TEXT)

new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
print(new_nodes)
