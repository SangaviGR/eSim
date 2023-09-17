import os
import subprocess
import shutil
from PyQt5.QtWidgets import QMessageBox

class LTspiceConverter:
    def __init__(self, parent):
        self.parent = parent

    def convert(self, file_path):
        
        # Get the base name of the file without the extension
        filename = os.path.splitext(os.path.basename(file_path))[0]
        conPath = os.path.dirname(file_path)
        
        # Check if the file is not empty
        if os.path.getsize(file_path) > 0:
            # Get the absolute path of the current script's directory
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Define the relative path to parser.py from the current script's directory
            # Check the current operating system
            if os.name == 'nt':  # Windows
                relative_parser_path = "LTSpiceToKiCadConverter/src/Windows"
            else:
                relative_parser_path = "LTSpiceToKiCadConverter/src/Ubuntu"

            # Construct the full path to parser.py
            parser_path = os.path.join(script_dir, relative_parser_path)
            
            command = f"cd {parser_path} && python3 sch_LTspice2Kicad.py {file_path}"
            try:
                subprocess.run(command, shell=True, check=True)
                # Message box with the conversion success message
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("Conversion Successful")
                msg_box.setText("The file has been converted successfully. Do you want to include it under the project explorer?")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_box.setDefaultButton(QMessageBox.Yes)
                result = msg_box.exec_()
                print("Conversion of LTspice to eSim schematic Successful")
            
                if result == QMessageBox.Yes:
                    # Add the converted file under the project explorer
                    newFile = str(conPath + "/LTspice_" + filename)
                    
                    target_directory_name = "eSim-Workspace"

                    # Find the eSim-Workspace directory
                    workspace_directory = find_workspace_directory(target_directory_name)

                    if workspace_directory:
                        print(f"{target_directory_name} is at: {workspace_directory}")

                        merge_copytree(newFile, workspace_directory,filename)
                        print("File added under the project explorer.")
                        # Message box with the Added Successfully message
                        msg_box = QMessageBox()
                        msg_box.setIcon(QMessageBox.Information)
                        msg_box.setWindowTitle("Added Successfully")
                        msg_box.setText("File added under the project explorer successfully.")
                        result = msg_box.exec_()
                        #QtWidgets.QMainWindow.close(QWidget)

                    else:
                        print(f"{target_directory_name} directory not found.")

                else:
                    # User chose not to add the file
                    print("File not added under the project explorer.")

            except subprocess.CalledProcessError as e:
                print("Error:", e)
        else:
            print("File is empty. Cannot perform conversion.")
            # A message box indicating that the file is empty
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Empty File")
            msg_box.setText("The selected file is empty. Conversion cannot be performed.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

    def upload_file_LTspice(self, file_path):
        if file_path:
            # Check if the file path contains spaces
            if ' ' in file_path:
                # Show a message box indicating that spaces are not allowed
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Invalid File Path")
                msg_box.setText("Spaces are not allowed in the file path.")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                return
            
            if ".asc" in file_path:
                print(file_path)
                self.convert(file_path)
            else:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Invalid File Path")
                msg_box.setText("Only .asc file can be converted.")
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
                return

        else:
            print("No file selected.")

            # Message box indicating that no file is selected
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("No File Selected")
            msg_box.setText("Please select a file before uploading.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

def find_workspace_directory(target_directory_name):
    for root, dirs, files in os.walk("/"):
        if target_directory_name in dirs or target_directory_name in files:
            return os.path.join(root, target_directory_name)
    return None  # Return None if the directory is not found

def merge_copytree(src, dst, filename):
    if not os.path.exists(dst):
        os.makedirs(dst)

    folder_path = f"{dst}/LTspice_{filename}" # Folder to be created in eSim-Workspace

    # Create the folder 
    try:
        os.makedirs(folder_path)
        print(f"Folder created at {folder_path}")
    except OSError as error:
        print(f"Folder creation failed: {error}")
        
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(folder_path, item)

        if os.path.isdir(src_item):
            merge_copytree(src_item, dst_item)
        else:
            if not os.path.exists(dst_item) or os.stat(src_item).st_mtime > os.stat(dst_item).st_mtime:
                shutil.copy2(src_item, dst_item)