from textnode import TextNode, TextType

def markdown_to_lists(text):
    output = []
    delimeters = ["*","`"]
    string = ""
    for i in range(len(text)):
        if text[i] not in delimeters:
            string += text[i]
        if text[i] in delimeters:
            if string != "":
                output.append(string)
            output.append(text[i])
            string = ""
        if i == len(text)-1:
            if string != "":
                output.append(string)
    return output

def markdown_list_to_textnode(textlist):
    output = []
    delimeters = ["*","`"]
    end_delimeter = ""
    string = ""
    text_type = TextType.TEXT

    for i in range(len(textlist)):

        if textlist[i] == end_delimeter:
            if text_type == TextType.BOLD:
                i += 1
            output.append(TextNode(string, text_type))
            string = ""
            end_delimeter = ""
            text_type = TextType.TEXT
            continue

        if end_delimeter == "":
            if textlist[i] in delimeters and text_type == TextType.TEXT:
                if string != "":
                    output.append(TextNode(string, text_type))
                    string = ""
                if textlist[i] == "*":
                    if i < len(textlist) - 1:
                        if textlist[i+1] == "*":
                            text_type = TextType.BOLD
                        end_delimeter = "*"
                        i += 1
                    else:
                        text_type = TextType.ITALIC
                        end_delimeter = "*"
                    continue
                if textlist[i] == "`":
                    text_type = TextType.CODE
                    end_delimeter = "`"
                    continue
        string += textlist[i]

    if string != "":
        output.append(TextNode(string, text_type))

    return output

#test = "Hellooo worldo and *Hellooo* cosas **World** ... *lol* `banana`"
#test = "Hello world *italics*"
#markdown_to_lists(test)
#print(markdown_list_to_textnode(markdown_to_lists(test)))


#ahora vamos a hacerlo bien, que no sirve de nada tener un guia y no usarla kkkk

def split_nodes_delimiter(list_of_old_nodes, delimiter, text_type):
    output = []
    for node in list_of_old_nodes:
        nodeparts = node.text.split(delimiter)
        if nodeparts[0]!="":
            output.append(TextNode(nodeparts[0], TextType.TEXT))
        if nodeparts[1]!="":
            output.append(TextNode(nodeparts[1], text_type))
        if nodeparts[2]!="":
            output.append(TextNode(nodeparts[2], TextType.TEXT))
    return output

node = TextNode("This is text with a `code block` word", TextType.TEXT)
node = TextNode("This is text with a `code block`", TextType.TEXT)
node = TextNode("This is text with a ``", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
print(new_nodes)
