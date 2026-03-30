from enum import Enum
from textnode import text_node_to_html_node, TextNode, TextType
from string_manipulation import text_to_textnodes
from htmlnode import ParentNode

# Create a BlockType Enum for markdown blocks
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

# Return the type of markdown block we're working with
def block_to_block_type(markdown):
    
    # Split it all on a new line
    block = markdown.split("\n")
    
    # Check for Headers
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    # Check for code
    if len(block) > 1 and block[0].startswith("```") and block[-1].startswith("```"):
        return BlockType.CODE
    
    ## Last few here also check to see if we've got a paragraph as their markdown types are signaled line by line
    # Check for quotes
    if markdown.startswith(">"):
        for line in block:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
            
            return BlockType.QUOTE
        
    # Check for un ordered list
    if markdown.startswith("- "):
        for line in block:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
            
            return BlockType.UNORDERED_LIST
    
    # Check for ordered list
    if markdown.startswith("1. "):
        i = 1
        for line in block:
            if not line.startswith(f'{i}. '):
                return BlockType.PARAGRAPH
            
            i += 1
            return BlockType.ORDERED_LIST
    
    # if not any of the above, it must be a paragraph
    return BlockType.PARAGRAPH

    
# Split a chunk of markdown into the individual blocks
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filteredBlocks = []
    
    # Loop over our blocks
    for item in blocks:
        if item == "":
            continue
        
        # Add the blocks, sans whitespace, to a list
        filteredBlocks.append(item.strip())
    
    return filteredBlocks
    
    
# Convert markdown to the appropriate html node types
def markdown_to_html_node(markdown):
    
    # Get our list of blocks
    blocks = markdown_to_blocks(markdown)
    nodeList = []
    
    # Loop over our list of blocks
    ## Check the type for the block
    ## Create a node of the appropriate type
    for block in blocks:
        type = block_to_block_type(block)
        
        if type == BlockType.PARAGRAPH:
            nodeList.append(paragraph_handler(block))
            
        if type == BlockType.HEADING:
            nodeList.append(heading_handler(block))
        
        if type == BlockType.CODE:
            nodeList.append(code_handler(block))
        
        if type == BlockType.QUOTE:
            nodeList.append(quote_handler(block))
        
        if type == BlockType.ORDERED_LIST:
            nodeList.append(orList_handler(block))
        
        if type == BlockType.UNORDERED_LIST:
            nodeList.append(unorList_handler(block))
        
    return ParentNode("div", nodeList, None)

# Handle paragraph blocks
## splits the block on new lines
## rejoins the block into one line
## Creates an html paragraph parent node with applicable child nodes
def paragraph_handler(block):
    lines = block.split("\n")
    line = " ".join(lines)
    
    return ParentNode("p", text_to_children(line))
    
# Handle heading blocks
## determines the heading level
## gets the text after the heading characters
## creates an html header parent node wiht applicable child nodes
def heading_handler(block):
    
    headerLevel = 0
    for char in block:
        if char == "#":
            headerLevel += 1
        else:
            break
    
    bareHeader = block[headerLevel + 1:]
    
    return ParentNode(f'h{headerLevel}', text_to_children(bareHeader))
    
# Handle code blocks
## check that we're actually working with a code block
## get the text between the ``` markdown
## create text nodes for the text
## create child nodes for the text nodes
## creates a parent node with the preformated text tag
def code_handler(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
        
    text = block[4:-3]
    textNode = TextNode(text, TextType.TEXT)
    childNode = text_node_to_html_node(textNode)
    code = ParentNode("code", [childNode])
    
    return ParentNode("pre", [code])
    
# Handle ordered list blocks
## generates a list of lines of text
## loops over the list
## splits on the numeral ". " and gets the text before and after it
## creates child nodes for the text
## builds parent nodes based off of the list with applicable child nodes
def orList_handler(block):
    items = block.split("\n")
    htmlItems = []
    
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        htmlItems.append(ParentNode("li", children))
        
    return ParentNode("ol", htmlItems)
    

# Handle unordered list blocks
## Same as above but without the need to strip off numerals
def unorList_handler(block):
    items = block.split("\n")
    htmlItems = []
    
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        htmlItems.append(ParentNode("li", children))
        
    return ParentNode("ul", htmlItems)
    

# Handle quote blocks
## Create the list of lines of text
## Check that we're starting with the correct quote identifier
## strip off the > character and whitespace
## create the parent node with applicable child nodes
def quote_handler(block):
    lines = block.split("\n")
    newLines = []
    
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
            
        newLines.append(line.lstrip(">").strip())
        
    content = " ".join(newLines)
    children = text_to_children(content)
    
    return ParentNode("blockquote", children)


# Turn markdown into a format that nodes can use
def text_to_children(text):
    
    # create a list of text nodes
    nodeList = text_to_textnodes(text)
    outputList = []
    
    # Loop over the list
    for node in nodeList:
        
        # Turn the text nodes into html nodes and add it to the output
        outputList.append(text_node_to_html_node(node))
        
    return outputList
    
    
    
    
    