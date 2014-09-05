import os
import sys
import time
from PyQt4 import QtGui, QtCore
from nustudio.project import Project
from nustudio.ui import Global
from nustudio.ui.start_form import StartForm
from nustudio.ui.main_form import MainForm
from nustudio.ui.node_tree_form import NodeTreeForm
from nustudio.ui.node_information_form import NodeInformationForm
from nustudio.ui.simulation_form import SimulationForm

def main():
	app = QtGui.QApplication(sys.argv)
	app.setStyleSheet("QGroupBox { border: 1px solid gray; }")

	Global.appPath = os.path.abspath(os.path.join(__file__, '..'))
	Global.loadConfig()

	Global.project = Project()
	Global.nodeTreeForm = NodeTreeForm()
	Global.nodeInformationForm = NodeInformationForm()
	Global.simulationForm = SimulationForm()
	Global.mainForm = MainForm()

	# Create and display the splash screen
	start = time.time()
	splash_pix = QtGui.QPixmap(Global.appPath + '/images/splash.png')
	splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
	splash.setMask(splash_pix.mask())
	splash.show()
	while time.time() - start < 3:
		time.sleep(0.001)
		app.processEvents()
	splash.close()

	# Show start form
	startForm = StartForm()
	startForm.show()

	sys.exit(app.exec_())


if __name__ == '__main__':
	main()