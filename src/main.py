import os
import shutil

def main():
    print("main executed")
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    print(f"abspath is: {PROJECT_ROOT}")
    STATIC_DIR = os.path.join(PROJECT_ROOT, "static")
    print(f"static path is: {STATIC_DIR}")
    PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")
    print(f"public path is: {PUBLIC_DIR}")
    
    # Execute the copy
    # copy_file(STATIC_DIR, PUBLIC_DIR)
    # print("\nCopy operation completed successfully!")


def copy_files( source_dir: str, destination_dir: str) -> None:

    if os.path.exists(destination_dir):
        print(f"Deleting exdting directory: {destination_dir}")
        shutil.rmtree(destination_dir)

    print(f"Creating new directory: {destination_dir}")
    os.mkdir(destination_dir)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        destination_path = os.path.join(destination_dir, item)
        
        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)
            
        else:
            print(f"Copying directory: {source_path} -> {destination_path}")
            copy_files(source_path, destination_path)

          
        
main()
