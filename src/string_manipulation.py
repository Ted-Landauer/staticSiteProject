import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    newNodes = []
    
    for nodes in old_nodes:
        tempList = []
        if nodes.text_type is not TextType.TEXT:
            newNodes.append(nodes)
            continue
        
        
        tempStrings = nodes.text.split(delimiter)
        
        if len(tempStrings) % 2 == 0:
            raise Exception("invalid markdown syntax")
            
            
        for i, section in enumerate(tempStrings):
            if tempStrings[i] != "":
                if i % 2 == 0:
                    
                    node = TextNode(tempStrings[i], TextType.TEXT)
                
                    tempList.append(node)
                    
                else:
                    
                    node = TextNode(tempStrings[i], text_type)
                    
                    tempList.append(node)
                
        
        
        newNodes.extend(tempList)
    
    
    return newNodes
    
    
# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    return matches
    
    
    
def extract_markdown_links(text):
    
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    return matches
    
    

def split_nodes_image(old_nodes):
    newNodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            newNodes.append(node)
            continue
            
        originalText = node.text
        images = extract_markdown_images(originalText)
        
        if len(images) == 0:
            newNodes.append(node)
            continue
        
        for image in images:
            sections = originalText.split(f'![{image[0]}]({image[1]})', 1)
            
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
                
            if sections[0] != "":
                newNodes.append(TextNode(sections[0], TextType.TEXT))
                
            newNodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            
            originalText = sections[1]
            
        if originalText != "":
            newNodes.append(TextNode(originalText, TextType.TEXT))
            
    return newNodes
            
            

def split_nodes_link(old_nodes):
    newNodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            newNodes.append(node)
            continue
            
        originalText = node.text
        links = extract_markdown_links(originalText)
        
        if len(links) == 0:
            newNodes.append(node)
            continue
            
        for link in links:
            sections = originalText.split(f"[{link[0]}]({link[1]})", 1)
            
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                newNodes.append(TextNode(sections[0], TextType.TEXT))
                
            newNodes.append(TextNode(link[0], TextType.LINK, link[1]))
            originalText = sections[1]
            
        if originalText != "":
            newNodes.append(TextNode(originalText, TextType.TEXT))
            
    return newNodes
    
    
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    