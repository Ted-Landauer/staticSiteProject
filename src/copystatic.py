import os
import shutil


# Copies files from a source directory to a destination, recursively
def copy_files_recursive(source_dir_path, dest_dir_path):
    
    # Checks that the path exists and creates it if it doesn't
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        
    # Loops over the items in the source directory
    for filename in os.listdir(source_dir_path):
        
        # builds the full filepath for the source and destination files
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        
        # Print out what our dest and source paths are
        print(f" * {from_path} -> {dest_path}")
        
        # check that the item we have is a file and if it is, copy it
        ## if not, then call all this again
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
            
        else:
            copy_files_recursive(from_path, dest_path)