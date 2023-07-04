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
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QGridLayout, QPushButton, QMessageBox
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
        self.eConLayout = QGridLayout()
        
        file_path_text_box = QLineEdit()
        file_path_text_box.setFixedHeight(30)  
        file_path_text_box.setFixedWidth(800)
        self.eConLayout.addWidget(file_path_text_box, 0, 0, 1, 2)
        
        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(100, 30) 
        browse_button.clicked.connect(lambda: self.browse_path(file_path_text_box))
        self.eConLayout.addWidget(browse_button, 0, 2, 1, 1)

        upload_button = QPushButton("Upload schematics")
        upload_button.setFixedSize(170, 30) 
        upload_button.clicked.connect(lambda: self.upload_file(file_path_text_box.text()))
        self.eConLayout.addWidget(upload_button, 1, 0, 1, 1)
        
        convertPs_button = QPushButton("Convert Pspice to eSim")
        convertPs_button.setFixedSize(170, 30) 
        convertPs_button.clicked.connect(lambda: self.convert_Pspice(file_path_text_box.text()))
        self.eConLayout.addWidget(convertPs_button, 1, 1, 1, 1)

        convert_button1 = QPushButton("Convert LTspice to eSim")
        convert_button1.setFixedSize(170, 30) 
        self.eConLayout.addWidget(convert_button1, 1, 2, 1, 1)  

        self.eConLayout.setColumnStretch(0, 1)  # Set a stretch factor of 1 for column 0
        self.eConLayout.setColumnStretch(1, 0)  # Set a stretch factor of 0 for column 1
        self.eConLayout.setColumnStretch(2, 1)  # Set a stretch factor of 1 for column 2

        # Set alignment for button2 to center horizontally within the layout cell
        self.eConLayout.setAlignment(convertPs_button, Qt.AlignHCenter)

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

        # Get the base name of the file without the extension
        filename = os.path.splitext(os.path.basename(file_path))[0]
        conPath = os.path.dirname(file_path)
        command = f"cd /home/ubuntus/eSim/schematic_converters/lib/PythonLib && python3 parser.py {file_path} {conPath}/{filename}"

        try:
            subprocess.run(command, shell=True, check=True)
            # Show a message box with the conversion success message
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Conversion Successful")
            msg_box.setText("The file has been converted successfully. Do you want to include it under the project explorer")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.Yes)
            result = msg_box.exec_()
            print("Conversion of Pspice to eSim schematic Successful")

            if result == QMessageBox.Yes:
                # Add the converted file under the project explorer
                newFile = str(conPath + "/" + filename)
                print(newFile)
                self.app = Application()
                self.app.obj_Mainview.obj_projectExplorer.addTreeNode(newFile, [newFile])
                shutil.copytree(newFile, f"/home/ubuntus/eSim-Workspace/{filename}") 
                print("File added under the project explorer.")
            else:
                # User chose not to add the file
                print("File not added under the project explorer.")
        except subprocess.CalledProcessError as e:
            # Handle any errors that occurred during command execution
            print("Error:", e)



    def browse_path(self, text_box):
        file_dialog = QFileDialog()  # a dialog that allows the user to select files or directories
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Schematic Files (*.sch)")
        file_dialog.exec_()  # Execute the dialog
        selected_files = file_dialog.selectedFiles()  # Get the selected file(s)
        if selected_files:
            text_box.setText(selected_files[0])

    def upload_file(self, file_path):
        if file_path:
            print(file_path)
        else:
            print("No file selected.")



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
