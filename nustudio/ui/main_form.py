import sys
import webbrowser
from PyQt4 import QtGui, QtCore
from nustudio.htm import maxTimeSteps
from nustudio.ui import Global
from nustudio.ui.project_properties_form import ProjectPropertiesForm

class MainForm(QtGui.QMainWindow):

	#region Constructor

	def __init__(self):
		"""
		Initializes a new instance of the MainForm class.
		"""

		QtGui.QMainWindow.__init__(self)

		#region	Instance fields

		self._pendingProjectChanges = False

		#endregion

		self.initUI()

	#endregion

	#region Methods

	def initUI(self):

		# menuFileNew
		self.menuFileNew = QtGui.QAction(self)
		self.menuFileNew.setText("&New Project")
		self.menuFileNew.setShortcut('Ctrl+N')
		self.menuFileNew.triggered.connect(self.newProject)

		# menuFileOpen
		self.menuFileOpen = QtGui.QAction(self)
		self.menuFileOpen.setText("&Open  Project")
		self.menuFileOpen.setShortcut('Ctrl+O')
		self.menuFileOpen.triggered.connect(self.openProject)

		# menuFileSave
		self.menuFileSave = QtGui.QAction(self)
		self.menuFileSave.setText("&Save Project")
		self.menuFileSave.setShortcut('Ctrl+S')
		self.menuFileSave.triggered.connect(self.saveProject)

		# menuFileExit
		self.menuFileExit = QtGui.QAction(self)
		self.menuFileExit.setText("&Exit")
		self.menuFileExit.setShortcut('Ctrl+Q')
		self.menuFileExit.triggered.connect(self.__menuFileExit_Click)

		# menuFile
		self.menuFile = QtGui.QMenu()
		self.menuFile.addAction(self.menuFileNew)
		self.menuFile.addAction(self.menuFileOpen)
		self.menuFile.addAction(self.menuFileSave)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.menuFileExit)
		self.menuFile.setTitle("&File")

		# menuViewSimulation
		self.menuViewSimulation = QtGui.QAction(self)
		self.menuViewSimulation.setText("View Simulation")
		self.menuViewSimulation.triggered.connect(self.__menuViewSimulation_Click)

		# menuViewNodeInformation
		self.menuViewNodeInformation = QtGui.QAction(self)
		self.menuViewNodeInformation.setText("View &Node Information")
		self.menuViewNodeInformation.triggered.connect(self.__menuViewNodeInformation_Click)

		# menuView
		self.menuView = QtGui.QMenu()
		self.menuView.addAction(self.menuViewSimulation)
		self.menuView.addAction(self.menuViewNodeInformation)
		self.menuView.setTitle("&View")

		# menuEdit
		self.menuEdit = QtGui.QMenu()
		self.menuEdit.setTitle("&Edit")

		# menuProjectProperties
		self.menuProjectProperties = QtGui.QAction(self)
		self.menuProjectProperties.setText("Properties...")
		self.menuProjectProperties.triggered.connect(self.__menuProjectProperties_Click)

		# menuProject
		self.menuProject = QtGui.QMenu()
		self.menuProject.addAction(self.menuProjectProperties)
		self.menuProject.setTitle("&Project")

		# menuTools
		self.menuTools = QtGui.QMenu()
		self.menuTools.setTitle("&Tools")

		# menuUserWiki
		self.menuUserWiki = QtGui.QAction(self)
		self.menuUserWiki.setText("User Wiki")
		self.menuUserWiki.triggered.connect(self.__menuUserWiki_Click)

		# menuGoToWebsite
		self.menuGoToWebsite = QtGui.QAction(self)
		self.menuGoToWebsite.setText("Project Website")
		self.menuGoToWebsite.triggered.connect(self.__menuGoToWebsite_Click)

		# menuAbout
		self.menuAbout = QtGui.QAction(self)
		self.menuAbout.setText("About")
		self.menuAbout.triggered.connect(self.__menuAbout_Click)

		# menuHelp
		self.menuHelp = QtGui.QMenu()
		self.menuHelp.addAction(self.menuUserWiki)
		self.menuHelp.addAction(self.menuGoToWebsite)
		self.menuHelp.addAction(self.menuAbout)
		self.menuHelp.setTitle("&Help")

		# menuMain
		self.menuMain = self.menuBar()
		self.menuMain.addMenu(self.menuFile)
		self.menuMain.addMenu(self.menuView)
		self.menuMain.addMenu(self.menuProject)
		self.menuMain.addMenu(self.menuHelp)

		# buttonInitHTM
		self.buttonInitHTM = QtGui.QAction(self)
		self.buttonInitHTM.setEnabled(False)
		self.buttonInitHTM.setIcon(QtGui.QIcon(Global.appPath + '/images/buttonInitializeHTM.png'))
		self.buttonInitHTM.setToolTip("Initialize simulation")
		self.buttonInitHTM.triggered.connect(self.__buttonInitHTM_Click)

		# buttonStepHTM
		self.buttonStepHTM = QtGui.QAction(self)
		self.buttonStepHTM.setEnabled(False)
		self.buttonStepHTM.setIcon(QtGui.QIcon(Global.appPath + '/images/buttonStepHTM.png'))
		self.buttonStepHTM.setToolTip("Forward one time step")
		self.buttonStepHTM.triggered.connect(self.__buttonStepHTM_Click)

		# buttonFastStepHTM
		self.buttonFastStepHTM = QtGui.QAction(self)
		self.buttonFastStepHTM.setEnabled(False)
		self.buttonFastStepHTM.setIcon(QtGui.QIcon(Global.appPath + '/images/buttonStepFastHTM.png'))
		self.buttonFastStepHTM.setToolTip("Run all time steps")
		self.buttonFastStepHTM.triggered.connect(self.__buttonFastStepHTM_Click)

		# buttonPauseHTM
		self.buttonPauseHTM = QtGui.QAction(self)
		self.buttonPauseHTM.setEnabled(False)
		self.buttonPauseHTM.setIcon(QtGui.QIcon(Global.appPath + '/images/buttonPauseHTM.png'))
		self.buttonPauseHTM.setToolTip("Pause simulation")
		self.buttonPauseHTM.triggered.connect(self.__buttonPauseHTM_Click)

		# buttonStopHTM
		self.buttonStopHTM = QtGui.QAction(self)
		self.buttonStopHTM.setEnabled(False)
		self.buttonStopHTM.setIcon(QtGui.QIcon(Global.appPath + '/images/buttonStopHTM.png'))
		self.buttonStopHTM.setToolTip("Stop simulation")
		self.buttonStopHTM.triggered.connect(self.__buttonStopHTM_Click)

		# sliderTime
		self.sliderTime = QtGui.QSlider()
		self.sliderTime.setEnabled(False)
		self.sliderTime.setOrientation(QtCore.Qt.Horizontal)
		self.sliderTime.setSingleStep(1)
		self.sliderTime.valueChanged.connect(self.__sliderTime_ValueChanged)

		# toolBar
		self.toolBar = QtGui.QToolBar()
		self.toolBar.addAction(self.buttonInitHTM)
		self.toolBar.addAction(self.buttonStepHTM)
		self.toolBar.addAction(self.buttonFastStepHTM)
		self.toolBar.addAction(self.buttonPauseHTM)
		self.toolBar.addAction(self.buttonStopHTM)
		self.toolBar.addWidget(self.sliderTime)

		# dockNodeTreeForm
		self.dockNodeTreeForm = QtGui.QDockWidget()
		self.dockNodeTreeForm.setWidget(Global.nodeTreeForm)

		# dockSimulationForm
		self.dockSimulationForm = QtGui.QDockWidget()
		self.dockSimulationForm.setWidget(Global.simulationForm)

		# dockNodeInformationForm
		self.dockNodeInformationForm = QtGui.QDockWidget()
		self.dockNodeInformationForm.setWidget(Global.nodeInformationForm)

		# MainForm
		self.addToolBar(self.toolBar)
		self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockNodeTreeForm)
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockSimulationForm)
		self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dockNodeInformationForm)
		self.setCentralWidget(self.dockSimulationForm)
		self.setWindowTitle("NuPIC Studio")
		self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))

	def __showDefaultTools(self):
		"""
		Show all tool windows.
		"""

		# Show simulation
		Global.simulationForm.refreshControls()
		Global.simulationForm.show()

		# Show node information
		Global.nodeInformationForm.show()
		Global.nodeInformationForm.refreshControls()

		# Show network controller
		Global.nodeTreeForm.show()

	def __cleanUp(self):
		"""
		Prepare UI to load a new configuration.
		"""

		self.__enableSimulationButtons(False)
		self.__enableSteeringButtons(False)

		# Highlight the top region
		Global.nodeTreeForm.selectedNode = Global.project.topRegion
		Global.nodeTreeForm.repaint()

		# Reset the simulation
		Global.simulationForm.clearControls()

	def __enableSimulationButtons(self, enable):
		"""
		Enables or disables controls related to simulation.
		"""

		Global.simulationInitialized = enable
		self.menuViewSimulation.setEnabled(enable)
		self.sliderTime.setRange(0, 0)
		self.sliderTime.setEnabled(enable)
		self.buttonInitHTM.setEnabled(not enable)

	def __enableSteeringButtons(self, enable):
		"""
		Enables or disables buttons in toolbar.
		"""

		self.buttonStepHTM.setEnabled(enable)
		self.buttonFastStepHTM.setEnabled(enable)
		self.buttonStopHTM.setEnabled(enable)

	def markProjectChanges(self, hasChanges):
		"""
		Provides an UI reaction to any project changes or a new or saved unchanged project.
		"""

		self._pendingProjectChanges = hasChanges
		self.menuFileSave.setEnabled(hasChanges)

	def __checkCurrentConfigChanges(self):
		"""
		Checks if the current file has changed.
		"""

		result = QtGui.QMessageBox.No

		# If changes happened, ask to user if he wish saves them
		if self._pendingProjectChanges:
			result = QtGui.QMessageBox.question(self, "Question", "Current project has changed. Do you want save these changes?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)
			if result == QtGui.QMessageBox.Yes:
				self.saveProject()

		return result

	def newProject(self):
		"""
		Creates a new project.
		"""

		# Check if the current project has changed before continue operation
		if self.__checkCurrentConfigChanges() != QtGui.QMessageBox.Cancel:
			# Create new project
			Global.project.new()

			# Initialize project state
			self.setWindowTitle(Global.project.name + " - NuPIC Studio")
			self.markProjectChanges(False)
			self.__cleanUp()

			return True

		return False

	def openProject(self):
		"""
		Open an existing project
		"""

		# Check if the current project has changed before continue operation
		if self.__checkCurrentConfigChanges() != QtGui.QMessageBox.Cancel:

			# Ask user for an existing file
			selectedFile = str(QtGui.QFileDialog().getOpenFileName(self, "Open File", Global.appPath + '/projects', "NuPIC project files (*.nuproj)"))

			# If file exists, continue operation
			if selectedFile != '':
				# Open the selected project
				Global.project.open(selectedFile)

				# Initialize project state
				self.setWindowTitle(Global.project.name + " - [" + Global.project.fileName + "] - NuPIC Studio")
				self.markProjectChanges(False)
				self.__cleanUp()

				return True

		return False

	def saveProject(self):
		"""
		Save the current project
		"""

		# If current project is new, ask user for valid file
		fileName = Global.project.fileName
		if fileName == '':
			# Ask user for valid file
			selectedFile = str(QtGui.QFileDialog().getOpenFileName(self, "Open File", Global.appPath + '/projects', "NuPIC project files (*.nuproj)"))

			# If file exists, continue operation
			if selectedFile != '':
				fileName = selectedFile

		# If file is Ok, continue operation
		if fileName != '':
			# Save to the selected location
			Global.project.save(fileName)

			# Initialize project state
			self.setWindowTitle(Global.project.name + " - [" + Global.project.fileName + "] - NuPIC Studio")
			self.markProjectChanges(False)

			return True

		return False

	def stopSimulation(self):

		# Disable relevant buttons to reset
		self.__enableSteeringButtons(False)
		self.__enableSimulationButtons(False)

		# Stop the simulation
		Global.simulationForm.clearControls()

	def pauseSimulation(self):
		self.buttonPauseHTM.setEnabled(False)

	#endregion

	#region Events

	#region Form

	def closeEvent(self, event):
		if self.__checkCurrentConfigChanges() == QtGui.QMessageBox.Cancel:
			event.ignore()
		else:
			if self.buttonStopHTM.isEnabled():
				self.stopSimulation()
			sys.exit()

	#endregion

	#region Menus

	def __menuFileExit_Click(self, event):
		self.close()

	def __menuProjectProperties_Click(self, event):
		# Open Project properties form
		projectPropertiesForm = ProjectPropertiesForm()
		projectPropertiesForm.setControlsValues()
		dialogResult = projectPropertiesForm.exec_()

		if dialogResult == QtGui.QDialog.Accepted:
			Global.mainForm.markProjectChanges(True)

	def __menuViewSimulation_Click(self, event):
		"""
		Open visualisation of HTM-Network 1: spatial and temporal pooling
		"""

		Global.simulationForm.refreshControls()
		Global.simulationForm.show()

	def __menuViewNodeInformation_Click(self, event):
		Global.nodeInformationForm.refreshControls()
		Global.nodeInformationForm.show()

	def __menuUserWiki_Click(self, event):
		webbrowser.open('https://github.com/numenta/nupic.studio/wiki')

	def __menuGoToWebsite_Click(self, event):
		webbrowser.open('https://github.com/numenta/nupic.studio')

	def __menuAbout_Click(self, event):
		QtGui.QMessageBox.information(self, "Information", "v. " + Global.version + "\nGet more info at our home page.")

	#endregion

	#region Toolbar

	def __buttonInitHTM_Click(self, event):
		"""
		Initializes the HTM-Network by creating the htm-controller to connect to events database
		"""

		# Disable relevant buttons:
		self.__enableSteeringButtons(True)
		self.__enableSimulationButtons(True)

		# Initialize time steps parameters
		Global.currTime = 0

		# Initialize the network starting from top region.
		Global.project.topRegion.initialize()
		Global.project.topRegion.nextTimeStep()

		# Update controls
		Global.simulationForm.topRegion = Global.project.topRegion
		Global.simulationForm.initializeControls()
		Global.simulationForm.refreshControls()
		Global.nodeInformationForm.refreshControls()

	def __buttonStepHTM_Click(self, event):
		"""
		Performs a single simulation step.
		"""

		# Update time steps parameters
		Global.currTime += 1
		if Global.currTime < maxTimeSteps:
			if Global.currTime == 1:
				self.sliderTime.setEnabled(True)
			self.sliderTime.setRange(0, Global.currTime)
		Global.selTime = self.sliderTime.maximum()

		# Perfoms actions related to time step progression.
		Global.project.topRegion.nextTimeStep()

		# Update controls
		if self.sliderTime.value() != self.sliderTime.maximum():
			self.sliderTime.setValue(self.sliderTime.maximum())
		else:
			Global.simulationForm.refreshControls()
			Global.nodeInformationForm.refreshControls()

	def __buttonFastStepHTM_Click(self, event):
		"""
		Performs full HTM simulation.
		"""

		# Get number of steps to perform simulation
		numberSteps = -1
		enteredInteger, ok = QtGui.QInputDialog.getInt(self, "Input Dialog", "Enter number of steps:")
		if ok:
			if enteredInteger < 2:
				QtGui.QMessageBox.warning(self, "Warning", "Invalid value specified!")
			else:
				numberSteps = enteredInteger

		if numberSteps != -1:
			# In case, simulation will be asynchronous.
			self.buttonPauseHTM.setEnabled(True)

			try:
				for i in range(numberSteps):
					self.__buttonStepHTM_Click(event)
			except Exception, ex:
				QtGui.QMessageBox.warning(self, "Warning", ex.message)

			self.pauseSimulation()

	def __buttonPauseHTM_Click(self, event):
		# TODO: Pause stepping.
		self.pauseSimulation()

	def __buttonStopHTM_Click(self, event):
		dialogResult = QtGui.QMessageBox.question(self, "Question", "Current simulation (learning) will stop!\r\nDo you want proceed?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

		if dialogResult == QtGui.QMessageBox.Yes:
			self.stopSimulation()

	def __sliderTime_ValueChanged(self, value):
		Global.selTime = self.sliderTime.value()
		Global.simulationForm.refreshControls()
		Global.nodeInformationForm.refreshControls()

	#endregion

	#endregion
