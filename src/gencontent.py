import os
from pathlib import Path
from block_manipulation import markdown_to_html_node

# Generate a webpage recursively
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    # Get dir contents
    for filename in os.listdir(dir_path_content):
        
        # build the full paths
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        
        # if we have a file...
        if os.path.isfile(from_path):
            
            # copy it over
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
            
        # if we have a directory
        else:
            
            # run it again
            generate_pages_recursive(from_path, template_path, dest_path)
            
# Generate a web page based on markdown files and images
def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    
    # read the markdown file from our "from" path 
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()
    
    # read the template file from our template path
    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()
    
    # convert the markdown file into an html file
    node = markdown_to_html_node(markdown_content)
    html = node.to_html()
    
    # grab the title of the page
    title = extract_title(markdown_content)
    
    # replace placeholders with the title and content values
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    # get the destination path and if it doesn't exist, create it
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    
    # write the html to the destination
    to_file = open(dest_path, "w")
    to_file.write(template)
    
    
# pull the page title out of the markdown
def extract_title(markdown):
    
    # get a list of lines
    lines = markdown.split("\n")
    
    # check for the h1 header symbol
    for line in lines:
        
        # if # exists, return everything after it
        if line.startswith("# "):
            return line[2:]
            
    # if no # is found, we have an issue
    raise ValueError("no title found")
    
    