import re

from textnode import TextNode, TextType
# ^Import regex

## Helper Functions

# Split a node based on a delimeter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    # Output value
    newNodes = []
    
    # Loop over the un-split nodes
    for nodes in old_nodes:
        tempList = []
        
        # Check if to see if we've got something other than a text node type and append it to the output
        if nodes.text_type is not TextType.TEXT:
            newNodes.append(nodes)
            continue
        
        # Split a node into an array based on the passed delimiter
        tempStrings = nodes.text.split(delimiter)
        
        # Make sure we had good data to split in the first place
        if len(tempStrings) % 2 == 0:
            raise Exception("invalid markdown syntax")
            
        
        # Loop over out split strings array
        for i, section in enumerate(tempStrings):
            
            # Check that we're not adding empty strings
            if tempStrings[i] != "":
                
                # Check that the index we're looking at is even or not, because...
                if i % 2 == 0:
                    
                    # Set the text type to the Enum Text type on even indicies
                    node = TextNode(tempStrings[i], TextType.TEXT)
                
                    tempList.append(node)
                    
                else:
                    
                    # Set the text type to the passed in text type on odd indicies
                    node = TextNode(tempStrings[i], text_type)
                    
                    tempList.append(node)
                
        
        # Build and return the output value after the loop
        newNodes.extend(tempList)
    
    return newNodes
    

    
# Regex methods to split images and links out of a text string
## EX: text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    return matches
    
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    return matches
    
# Split an image node 
def split_nodes_image(old_nodes):
    
    # Output value
    newNodes = []
    
    # Loop over the nodes passed in
    for node in old_nodes:
        
        # Look for non-text nodes and append as is
        if node.text_type != TextType.TEXT:
            newNodes.append(node)
            continue
        
        # Store the original text and run our regex from above on it
        originalText = node.text
        images = extract_markdown_images(originalText)
        
        # If there's nothing extracted, add it and move on
        if len(images) == 0:
            newNodes.append(node)
            continue
        
        # Loop over all of the returned images
        for image in images:
            
            # Strip the image data out of the string
            sections = originalText.split(f'![{image[0]}]({image[1]})', 1)
            
            # Check that the markdown delimiters were input correctly
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
                
            # Check that we have a value
            if sections[0] != "":
                
                # Add the text that was before the image data to the output value as a text node
                newNodes.append(TextNode(sections[0], TextType.TEXT))
            
            # Add the image value to the output value as an image type
            newNodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            
            # Grab the text that was after the image data
            originalText = sections[1]
            
        # Check that we have a value
        if originalText != "":
            
            # Add the text that was after the image data to the output value as a text node
            newNodes.append(TextNode(originalText, TextType.TEXT))
            
    return newNodes
    
# Split a link node
def split_nodes_link(old_nodes):
    
    # Output value
    newNodes = []
    
    # Loop over our nodes
    for node in old_nodes:
        
        # If we don't have a text node, add it as is
        if node.text_type != TextType.TEXT:
            newNodes.append(node)
            continue
            
        # Store the node text and extract the links
        originalText = node.text
        links = extract_markdown_links(originalText)
        
        # Check that we have links to parse
        if len(links) == 0:
            newNodes.append(node)
            continue
        
        # Loop over all the link entries
        for link in links:
            
            # Strip the link data out of the string
            sections = originalText.split(f"[{link[0]}]({link[1]})", 1)
            
            # Check that the markdown was closed correctly
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
                
            # Check that we have a value
            if sections[0] != "":
                
                # Add the text that was before the link data to the output value as a text node
                newNodes.append(TextNode(sections[0], TextType.TEXT))
            
            # Add the link value to the output value as a link type
            newNodes.append(TextNode(link[0], TextType.LINK, link[1]))
            
            # Grab the text that was after the link data
            originalText = sections[1]
            
        if originalText != "":
            
            # Add the text that was after the link data to the output value as a text node
            newNodes.append(TextNode(originalText, TextType.TEXT))
            
    return newNodes
    
# Run our helper functions from above to split an input into all the necessary bits
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
    
    
