class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method must be implemented")

    def props_to_html(self):
        if self.props:
            return ''.join([f' {key}="{value}"' for key, value in self.props.items()])
        return ''

    def __repr__(self):
        return f"HtmlNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
