from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
    block = markdown.split("\n")
    
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
        
    if len(block) > 1 and block[0].startswith("```") and block[-1].startswith("```"):
        return BlockType.CODE
        
    if markdown.startswith(">"):
        for line in block:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
            
            return BlockType.QUOTE
        
    if markdown.startswith("- "):
        for line in block:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
            
            return BlockType.UNORDERED_LIST
        
    if markdown.startswith("1. "):
        i = 1
        for line in block:
            if not line.startswith(f'{i}. '):
                return BlockType.PARAGRAPH
            
            i += 1
            return BlockType.ORDERED_LIST
        
    return BlockType.PARAGRAPH
        
        
    
    
    
    
    
    
    
    
    return typeOfBlockType



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filteredBlocks = []
    
    for item in blocks:
        if item == "":
            continue
        
        filteredBlocks.append(item.strip())
    
    return filteredBlocks