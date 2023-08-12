from PyQt5 import QtCore, QtWidgets
from ngspiceSimulation.pythonPlotting import plotWindow
from ngspiceSimulation.NgspiceWidget import NgspiceWidget
from configuration.Appconfig import Appconfig
from modelEditor.ModelEditor import ModelEditorclass
from subcircuit.Subcircuit import Subcircuit
from maker.makerchip import makerchip
from kicadtoNgspice.KicadtoNgspice import MainWindow
from browser.Welcome import Welcome
from browser.UserManual import UserManual
from ngspicetoModelica.ModelicaUI import OpenModelicaEditor
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QLabel, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import os
import subprocess
from Application import Application
import shutil

dockList = ['Welcome']
count = 1
dock = {}


class DockArea(QtWidgets.QMainWindow):
    """
    This class contains function for designing UI of all the editors
    in dock area part:

        - Test Editor.
        - Model Editor.
        - Python Plotting.
        - Ngspice Editor.
        - Kicad to Ngspice Editor.
        - Subcircuit Editor.
        - Modelica editor.
    """

    def __init__(self):
        """This act as constructor for class DockArea."""
        QtWidgets.QMainWindow.__init__(self)
        self.obj_appconfig = Appconfig()

        for dockName in dockList:
            dock[dockName] = QtWidgets.QDockWidget(dockName)
            self.welcomeWidget = QtWidgets.QWidget()
            self.welcomeLayout = QtWidgets.QVBoxLayout()
            self.welcomeLayout.addWidget(Welcome())  # Call browser

            # Adding to main Layout
            self.welcomeWidget.setLayout(self.welcomeLayout)
            dock[dockName].setWidget(self.welcomeWidget)
            # CSS
            dock[dockName].setStyleSheet(" \
            QWidget { border-radius: 15px; border: 1px solid gray;\
                padding: 5px; width: 200px; height: 150px;  } \
            ")
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName])

        # self.tabifyDockWidget(dock['Notes'],dock['Blank'])
        self.show()

    def createTestEditor(self):
        """This function create widget for Library Editor"""
        global count

        self.testWidget = QtWidgets.QWidget()
        self.testArea = QtWidgets.QTextEdit()
        self.testLayout = QtWidgets.QVBoxLayout()
        self.testLayout.addWidget(self.testArea)

        # Adding to main Layout
        self.testWidget.setLayout(self.testLayout)
        dock['Tips-' + str(count)] = \
            QtWidgets.QDockWidget('Tips-' + str(count))
        dock['Tips-' + str(count)].setWidget(self.testWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['Tips-' + str(count)])
        self.tabifyDockWidget(
            dock['Welcome'], dock['Tips-' + str(count)])

        dock['Tips-' + str(count)].setVisible(True)
        dock['Tips-' + str(count)].setFocus()

        dock['Tips-' + str(count)].raise_()

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock['Tips-' + str(count)]
            )
        count = count + 1

    def plottingEditor(self):
        """This function create widget for interactive PythonPlotting."""
        self.projDir = self.obj_appconfig.current_project["ProjectName"]
        self.projName = os.path.basename(self.projDir)
        dockName = f'Plotting-{self.projName}-'
        # self.project = os.path.join(self.projDir, self.projName)

        global count
        self.plottingWidget = QtWidgets.QWidget()

        self.plottingLayout = QtWidgets.QVBoxLayout()
        self.plottingLayout.addWidget(plotWindow(self.projDir, self.projName))

        # Adding to main Layout
        self.plottingWidget.setLayout(self.plottingLayout)
        dock[dockName + str(count)
             ] = QtWidgets.QDockWidget(dockName
                                       + str(count))
        dock[dockName + str(count)] \
            .setWidget(self.plottingWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock[dockName + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock[dockName + str(count)])

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock[dockName + str(count)]
            )
        count = count + 1

    def ngspiceEditor(self, projName, netlist, simEndSignal):
        """ This function creates widget for Ngspice window."""
        global count
        self.ngspiceWidget = QtWidgets.QWidget()

        self.ngspiceLayout = QtWidgets.QVBoxLayout()
        self.ngspiceLayout.addWidget(
            NgspiceWidget(netlist, simEndSignal)
        )

        # Adding to main Layout
        self.ngspiceWidget.setLayout(self.ngspiceLayout)
        dockName = f'Simulation-{projName}-'
        dock[dockName + str(count)
             ] = QtWidgets.QDockWidget(dockName
                                       + str(count))
        dock[dockName + str(count)] \
            .setWidget(self.ngspiceWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock[dockName + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock[dockName
                                   + str(count)])

        # CSS
        dock[dockName + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray; padding: 0px;\
            width: 200px; height: 150px;  } \
        ")

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock[dockName + str(count)]
            )
        count = count + 1

    def eSimConverter(self):
        """This function creates a widget for eSimConverter."""
        global count

        dockName = 'Schematics Converter-'

        self.eConWidget = QtWidgets.QWidget()
        self.eConLayout = QVBoxLayout()  # QVBoxLayout for the main layout

        file_path_layout = QHBoxLayout()  # QHBoxLayout for file path line

        file_path_text_box = QLineEdit()
        file_path_text_box.setFixedHeight(30)
        file_path_text_box.setFixedWidth(800)
        file_path_layout.setAlignment(Qt.AlignCenter)
        file_path_layout.addWidget(file_path_text_box)

        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(100, 30)
        browse_button.clicked.connect(lambda: self.browse_path(file_path_text_box))
        file_path_layout.addWidget(browse_button)

        self.eConLayout.addLayout(file_path_layout)  # Add file path layout to main layout

        button_layout = QHBoxLayout()  # QHBoxLayout for the buttons

        upload_button1 = QPushButton("Upload Pspice schematics")
        upload_button1.setFixedSize(180, 30)
        upload_button1.clicked.connect(lambda: self.upload_file_Pspice(file_path_text_box.text()))
        button_layout.addWidget(upload_button1)

        upload_button = QPushButton("Upload LTspice schematics")
        upload_button.setFixedSize(184, 30)
        upload_button.clicked.connect(lambda: self.upload_file_LTspice(file_path_text_box.text()))
        button_layout.addWidget(upload_button)

        self.convert_button = QPushButton("Convert Schematics to eSim")
        self.convert_button.setFixedSize(190, 30)
        self.convert_button.setEnabled(False)
        button_layout.addWidget(self.convert_button)
        self.eConLayout.addLayout(button_layout)

        self.eConWidget.setLayout(self.eConLayout)

        # Add the description HTML content
        description_html = """
            <html>
                <head>
                    <style>
                        body {
                            font-family: sans-serif;
                            margin: 0px;
                            padding: 0px;
                            background-color: white;
                            border: 4px solid  black;
                            font-size: 10pt; /* Adjust the font size as needed */
                        }

                        h1{
                            font-weight: bold;
                            font-size: 9pt;
                            color: #eeeeee;
                            padding: 10px;
                            background-color: #165982;
                            border: 4px outset  #0E324B;
                        }
                    </style>
                </head>

                <body>
                    <h1>About eSim Converter</h1>
                    <p>
                        <b>Pspice to eSim </b> will convert the PSpice Schematic and Library files to KiCad Schematic and
                        Library files respectively with proper mapping of the components and the wiring. By this way one 
                        will be able to simulate their schematics in PSpice and get the PCB layout in KiCad.</b> 
                        <br/><br/>
                        <b>LTspice to eSim </b> will convert symbols and schematics from LTspice to Kicad.The goal is to design and
                        simulate under LTspice and to automatically transfer the circuit under Kicad to draw the PCB.</b>
                    </p>
                </body>
            </html>
        """

        self.description_label = QLabel()
        self.description_label.setFixedHeight(160)
        self.description_label.setFixedWidth(950)
        self.description_label.setAlignment(Qt.AlignBottom)
        self.description_label.setWordWrap(True)
        self.description_label.setText(description_html)
        self.eConLayout.addWidget(self.description_label)  # Add the description label to the layout

        self.eConWidget.setLayout(self.eConLayout)

        dock[dockName + str(count)] = QtWidgets.QDockWidget(dockName + str(count))
        dock[dockName + str(count)].setWidget(self.eConWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock[dockName + str(count)])
        self.tabifyDockWidget(dock['Welcome'], dock[dockName + str(count)])

        # CSS
        dock[dockName + str(count)].setStyleSheet(" \
            .QWidget { border-radius: 15px; border: 1px solid gray;\
                padding: 5px; width: 200px; height: 150px;  } \
            ")

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()

        count = count + 1


    def convert_Pspice(self, file_path):
        self.convert_button.clicked.disconnect()
        # Get the base name of the file without the extension
        filename = os.path.splitext(os.path.basename(file_path))[0]
        conPath = os.path.dirname(file_path)
        
        # Check if the file is not empty
        if os.path.getsize(file_path) > 0:
            command = f"cd /home/ubuntus/eSim/schematic_converters/lib/PythonLib && python3 parser.py {file_path} {conPath}/{filename}"
            
            try:
                subprocess.run(command, shell=True, check=True)
                self.convert_button.setEnabled(False)
                # Show a message box with the conversion success message
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("Conversion Successful")
                msg_box.setText("The file has been converted successfully. Do you want to include it under the project explorer?")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_box.setDefaultButton(QMessageBox.Yes)
                result = msg_box.exec_()
                print("Conversion of Pspice to eSim schematic Successful")

                if result == QMessageBox.Yes:
                    # Add the converted file under the project explorer
                    newFile = str(conPath + "/" + filename)
                    print(newFile)
                    
                    self.app = Application(self)
                    self.app.obj_Mainview.obj_projectExplorer.addTreeNode(newFile, [newFile])
                    #shutil.copytree(newFile, f"/home/ubuntus/eSim-Workspace/{filename}") 
                    shutil.rmtree(f"/home/ubuntus/eSim-Workspace/{filename}", ignore_errors=True)
                    shutil.copytree(newFile, f"/home/ubuntus/eSim-Workspace/{filename}")

                    print("File added under the project explorer.")

                    QtWidgets.QMainWindow.close(self)

                else:
                    # User chose not to add the file
                    print("File not added under the project explorer.")
            except subprocess.CalledProcessError as e:
                # Handle any errors that occurred during command execution
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

    def convert_LTspice(self, file_path):
        self.convert_button.clicked.disconnect()
        # Get the base name of the file without the extension
        filename = os.path.splitext(os.path.basename(file_path))[0]
        conPath = os.path.dirname(file_path)
        
        # Check if the file is not empty
        if os.path.getsize(file_path) > 0:
            print("con lt")
            self.convert_button.setEnabled(False)
        else:
            print("File is empty. Cannot perform conversion.")
            # A message box indicating that the file is empty
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Empty File")
            msg_box.setText("The selected file is empty. Conversion cannot be performed.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

    def browse_path(self, text_box):
        file_dialog = QFileDialog()  # a dialog that allows the user to select files or directories
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Schematic Files (*.sch)")
        file_dialog.exec_()  # Execute the dialog
        selected_files = file_dialog.selectedFiles()  # Get the selected file(s)
        if selected_files:
            text_box.setText(selected_files[0])

    def upload_file_Pspice(self, file_path):
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
            print(file_path)
            self.convert_button.setEnabled(True)
            self.convert_button.clicked.connect(lambda: self.convert_Pspice(file_path))
            
        else:
            print("No file selected.")
            self.convert_button.setEnabled(False)

            # Message box indicating that no file is selected
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("No File Selected")
            msg_box.setText("Please select a file before uploading.")
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
            print(file_path)
            self.convert_button.setEnabled(True)
            self.convert_button.clicked.connect(lambda: self.convert_LTspice(file_path))
            
        else:
            print("No file selected.")
            self.convert_button.setEnabled(False)

            # Message box indicating that no file is selected
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("No File Selected")
            msg_box.setText("Please select a file before uploading.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()


    def modelEditor(self):
        """This function defines UI for model editor."""
        print("in model editor")
        global count

        projDir = self.obj_appconfig.current_project["ProjectName"]
        projName = os.path.basename(projDir)
        dockName = f'Model Editor-{projName}-'

        self.modelwidget = QtWidgets.QWidget()

        self.modellayout = QtWidgets.QVBoxLayout()
        self.modellayout.addWidget(ModelEditorclass())

        # Adding to main Layout
        self.modelwidget.setLayout(self.modellayout)

        dock[dockName +
             str(count)] = QtWidgets.QDockWidget(dockName
                                                 + str(count))
        dock[dockName + str(count)] \
            .setWidget(self.modelwidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock[dockName + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock[dockName + str(count)])

        # CSS
        dock[dockName + str(count)].setStyleSheet(" \
            .QWidget { border-radius: 15px; border: 1px solid gray; \
                padding: 5px; width: 200px; height: 150px;  } \
            ")

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()

        count = count + 1

    def kicadToNgspiceEditor(self, clarg1, clarg2=None):
        """
        This function is creating Editor UI for Kicad to Ngspice conversion.
        """
        global count

        projDir = self.obj_appconfig.current_project["ProjectName"]
        projName = os.path.basename(projDir)
        dockName = f'Netlist-{projName}-'

        self.kicadToNgspiceWidget = QtWidgets.QWidget()
        self.kicadToNgspiceLayout = QtWidgets.QVBoxLayout()
        self.kicadToNgspiceLayout.addWidget(MainWindow(clarg1, clarg2))

        self.kicadToNgspiceWidget.setLayout(self.kicadToNgspiceLayout)
        dock[dockName + str(count)] = \
            QtWidgets.QDockWidget(dockName + str(count))
        dock[dockName +
             str(count)].setWidget(self.kicadToNgspiceWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock[dockName + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock[dockName + str(count)])

        # CSS
        dock[dockName + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()
        dock[dockName + str(count)].activateWindow()

        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock[dockName + str(count)]
            )
        count = count + 1 

    def subcircuiteditor(self):
        """This function creates a widget for different subcircuit options."""
        global count

        projDir = self.obj_appconfig.current_project["ProjectName"]

        """ Checks projDir variable has valid value 
        & is not None before calling os.path.basename """

        if projDir is not None:
            projName = os.path.basename(projDir)
            dockName = f'Subcircuit-{projName}-'

            self.subcktWidget = QtWidgets.QWidget()
            self.subcktLayout = QtWidgets.QVBoxLayout()
            self.subcktLayout.addWidget(Subcircuit(self))

            self.subcktWidget.setLayout(self.subcktLayout)
            dock[dockName +
                str(count)] = QtWidgets.QDockWidget(dockName
                                                    + str(count))
            dock[dockName + str(count)] \
                .setWidget(self.subcktWidget)
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                            dock[dockName + str(count)])
            self.tabifyDockWidget(dock['Welcome'],
                                dock[dockName + str(count)])

            # CSS
            dock[dockName + str(count)].setStyleSheet(" \
            .QWidget { border-radius: 15px; border: 1px solid gray;\
                padding: 5px; width: 200px; height: 150px;  } \
            ")

            dock[dockName + str(count)].setVisible(True)
            dock[dockName + str(count)].setFocus()
            dock[dockName + str(count)].raise_()

            count = count + 1

        else:
            """ when projDir is None that is clicking on subcircuit icon
                without any project selection """
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Please select the project first.'
                ' You can either create new project or open existing project'
            )
            self.msg.exec_()

    def makerchip(self):
        """This function creates a widget for different subcircuit options."""
        global count

        projDir = self.obj_appconfig.current_project["ProjectName"]
        projName = os.path.basename(projDir)
        dockName = f'Makerchip-{projName}-'

        self.makerWidget = QtWidgets.QWidget()
        self.makerLayout = QtWidgets.QVBoxLayout()
        self.makerLayout.addWidget(makerchip(self))

        self.makerWidget.setLayout(self.makerLayout)
        dock[dockName +
             str(count)] = QtWidgets.QDockWidget(dockName
                                                 + str(count))
        dock[dockName + str(count)].setWidget(self.makerWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock[dockName + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock[dockName + str(count)])

        # CSS
        dock[dockName + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()

        count = count + 1

    def usermanual(self):
        """This function creates a widget for user manual."""
        global count
        self.usermanualWidget = QtWidgets.QWidget()
        self.usermanualLayout = QtWidgets.QVBoxLayout()
        self.usermanualLayout.addWidget(UserManual())

        self.usermanualWidget.setLayout(self.usermanualLayout)
        dock['User Manual-' +
             str(count)] = QtWidgets.QDockWidget('User Manual-' + str(count))
        dock['User Manual-' + str(count)].setWidget(self.usermanualWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock['User Manual-' + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                              dock['User Manual-' + str(count)])

        # CSS
        dock['User Manual-' + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")

        dock['User Manual-' + str(count)].setVisible(True)
        dock['User Manual-' + str(count)].setFocus()
        dock['User Manual-' + str(count)].raise_()

        count = count + 1

    def modelicaEditor(self, projDir):
        """This function sets up the UI for ngspice to modelica conversion."""
        global count

        projName = os.path.basename(projDir)
        dockName = f'Modelica-{projName}-'

        self.modelicaWidget = QtWidgets.QWidget()
        self.modelicaLayout = QtWidgets.QVBoxLayout()
        self.modelicaLayout.addWidget(OpenModelicaEditor(projDir))

        self.modelicaWidget.setLayout(self.modelicaLayout)
        dock[dockName + str(count)
             ] = QtWidgets.QDockWidget(dockName + str(count))
        dock[dockName + str(count)] \
            .setWidget(self.modelicaWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                           dock[dockName
                                + str(count)])
        self.tabifyDockWidget(dock['Welcome'], dock[dockName
                                                    + str(count)])

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()

        # CSS
        dock[dockName + str(count)].setStyleSheet(" \
        .QWidget { border-radius: 15px; border: 1px solid gray;\
            padding: 5px; width: 200px; height: 150px;  } \
        ")
        temp = self.obj_appconfig.current_project['ProjectName']
        if temp:
            self.obj_appconfig.dock_dict[temp].append(
                dock[dockName + str(count)]
            )

        count = count + 1

    def closeDock(self):
        """
        This function checks for the project in **dock_dict**
        and closes it.
        """
        self.temp = self.obj_appconfig.current_project['ProjectName']
        for dockwidget in self.obj_appconfig.dock_dict[self.temp]:
            dockwidget.close()
