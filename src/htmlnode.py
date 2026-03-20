


class HTMLNode:
    def __init__(self, paraTag = None, paraValue = None, paraChild = None, paraProps = None):
        self.tag = paraTag
        self.value = paraValue
        self.children = paraChild
        self.props = paraProps
        
        
    def to_html(self):
        raise NotImplementedError
        
    def props_to_html(self):
        if self.props == None or self.props == "":
            return ""
            
        propString = ""
        
        for item in self.props:
            tempKey = item
            tempVal = self.props[item]
            
            propString += f' {tempKey}="{tempVal}"'
        
        
        return propString
        
    def __repr__(self):
        #print(self)
        
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
        
        
class LeafNode(HTMLNode):
    def __init__(self, leafTag, leafValue, leafProps = None):
        
        super().__init__(leafTag, leafValue, None, leafProps)
        
        
    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return self.value
        
        leafText = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
        return leafText
        
    def __repr__(self):
        #print(self)
        
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
        
            
            
            
            


class ParentNode(HTMLNode):
    def __init__(self, parentTag, parentChild, parentProps = None):
        super().__init__(parentTag, None, parentChild, parentProps)
        
    def to_html(self):
        if self.tag == None:
            raise ValueError
        
        if self.children == None or not self.children:
            raise ValueError("no children for the parent")
            
        builtText = f'<{self.tag}{self.props_to_html()}>'
            
        for item in self.children:
            builtText += f'{item.to_html()}'
            
        builtText += f'</{self.tag}>'
        
        return builtText
        
        