class HTMLNode:
    
    # Constructor
    def __init__(self, paraTag = None, paraValue = None, paraChild = None, paraProps = None):
        self.tag = paraTag
        self.value = paraValue
        self.children = paraChild
        self.props = paraProps
        
    
    # Method to override
    def to_html(self):
        raise NotImplementedError
        
    
    # Convert properties dictionary to html
    def props_to_html(self):
        
        #make sure it's not empty
        if self.props == None or self.props == "":
            return ""
        
        propString = ""
        
        #loop over each item in the dictionary
        ##get the key-value pairs and build the properties string
        for item in self.props:
            tempKey = item
            tempVal = self.props[item]
            
            propString += f' {tempKey}="{tempVal}"'
        
        return propString
        
    
    # ToString Function
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
        

# Inherrits from HTMLNode
class LeafNode(HTMLNode):
    
    # Constructor
    def __init__(self, leafTag, leafValue, leafProps = None):
        
        super().__init__(leafTag, leafValue, None, leafProps)
        

    # Overridden function
    def to_html(self):
        
        # Check if the required value and tag fields are empty
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return self.value
        
        # Build the leaf node text
        leafText = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
        return leafText
        
    
    # ToString Method
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
     

# Inherrits from HTMLNode
class ParentNode(HTMLNode):
    
    # Constructor
    def __init__(self, parentTag, parentChild, parentProps = None):
        super().__init__(parentTag, None, parentChild, parentProps)
    
    # Overridden function
    def to_html(self):
        
        # Check to see if the required tag and child values are empty
        if self.tag == None:
            raise ValueError
        
        if self.children == None or not self.children:
            raise ValueError("no children for the parent")
        
        
        # Build the parent node text
        builtText = f'<{self.tag}{self.props_to_html()}>'
            
        # Loop over all of the child nodes and nest them in the parent node
        for item in self.children:
            builtText += f'{item.to_html()}'
        
        # Close the parent tag and return the text representation
        builtText += f'</{self.tag}>'
        
        return builtText
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"