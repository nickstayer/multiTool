import os
import shutil


def main():
    current_dir = current_dir = os.path.dirname(__file__)
    in_folder = os.path.join(current_dir, "in")
    out_folder = os.path.join(current_dir, "out")
    move_folder_contents(in_folder, out_folder)


def move_folder_contents(root_folder, destination_folder):
    for package_name in os.listdir(root_folder):
        package_path = os.path.join(root_folder, package_name)
        
        if os.path.isdir(package_path):
            for version_folder in os.listdir(package_path):
                version_path = os.path.join(package_path, version_folder)
                
                if os.path.isdir(version_path):
                    new_folder_name = f"{package_name}_{version_folder}"
                    new_folder_path = os.path.join(destination_folder, new_folder_name)
                    
                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path)
                    
                    for item in os.listdir(version_path):
                        item_path = os.path.join(version_path, item)
                        destination_item_path = os.path.join(new_folder_path, item)
                        
                        if os.path.isdir(item_path):
                            shutil.copytree(item_path, destination_item_path)
                        else:
                            shutil.copy(item_path, destination_item_path)
   
    print("Копирование завершено")


if __name__ == "__main__":
    main()