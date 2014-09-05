﻿from PyQt4 import Qt, QtGui, QtCore
from nustudio.ui import Global
from nustudio.htm.node import NodeType, Node

class ArrayTableModel(QtGui.QStandardItemModel):

	def __init__(self, parent=None):
		QtGui.QStandardItemModel.__init__(self)

		self.header = []
		self.data = []

	def update(self, header, data):
		self.header = header
		self.data = data

		numCols = len(self.header)
		self.setColumnCount(numCols)
		numRows = len(self.data)
		self.setRowCount(numRows)

		for col in range(numCols):
			self.setHeaderData(col, QtCore.Qt.Horizontal, self.header[col])

		for row in range(numRows):
			for col in range(numCols):
				data = self.data[row][col]
				self.setData(self.index(row, col, QtCore.QModelIndex()), data)

	def data(self, index, role=QtCore.Qt.DisplayRole):
		column, row = index.column(), index.row()
		if role == QtCore.Qt.TextAlignmentRole:
			if column > 0:
				return QtCore.Qt.AlignLeft
			else:
				return QtCore.Qt.AlignRight
		elif role == QtCore.Qt.DisplayRole:
			return self.data[row][column]
		return 

	def columnCount(self, parent=QtCore.QModelIndex()):
		return len(self.header)

	def rowCount(self, parent=QtCore.QModelIndex()):
		return len(self.data)


class NodeInformationForm(QtGui.QWidget):

	#region Constructor

	def __init__(self):
		"""
		Initializes a new instance of the NodeInformationForm class.
		"""

		QtGui.QWidget.__init__(self)

		#region Instance fields

		self.previousSelectedNode = None

		self.selectedSensor = None
		self.selectedRegion = None
		self.selectedColumn = None
		self.selectedProximalSynapse = None
		self.selectedCell = None
		self.selectedDistalSegment = None
		self.selectedDistalSynapse = None

		#endregion

		self.initUI()

	#endregion

	#region Methods

	def initUI(self):

		# labelSensorName
		self.labelSensorName = QtGui.QLabel()
		self.labelSensorName.setText("Name")
		self.labelSensorName.setAlignment(QtCore.Qt.AlignRight)

		# textBoxSensorName
		self.textBoxSensorName = QtGui.QLineEdit()
		self.textBoxSensorName.setEnabled(False)
		self.textBoxSensorName.setAlignment(QtCore.Qt.AlignLeft)

		# labelEncodedInput
		self.labelEncodedInput = QtGui.QLabel()
		self.labelEncodedInput.setText("Encoded Input")
		self.labelEncodedInput.setAlignment(QtCore.Qt.AlignRight)

		# textBoxEncodedInput
		self.textBoxEncodedInput = QtGui.QLineEdit()
		self.textBoxEncodedInput.setEnabled(False)
		self.textBoxEncodedInput.setAlignment(QtCore.Qt.AlignRight)

		# labelDecodedOutput
		self.labelDecodedOutput = QtGui.QLabel()
		self.labelDecodedOutput.setText("Decoded Output")
		self.labelDecodedOutput.setAlignment(QtCore.Qt.AlignRight)

		# textBoxRegionDecodedOutput
		self.textBoxRegionDecodedOutput = QtGui.QLineEdit()
		self.textBoxRegionDecodedOutput.setEnabled(False)
		self.textBoxRegionDecodedOutput.setAlignment(QtCore.Qt.AlignRight)

		# tabPageSensorLayout
		self.tabPageSensorLayout = QtGui.QGridLayout()
		self.tabPageSensorLayout.addWidget(self.labelSensorName, 0, 0)
		self.tabPageSensorLayout.addWidget(self.textBoxSensorName, 0, 1)
		self.tabPageSensorLayout.addWidget(self.labelEncodedInput, 1, 0)
		self.tabPageSensorLayout.addWidget(self.textBoxEncodedInput, 1, 1)
		self.tabPageSensorLayout.addWidget(self.labelDecodedOutput, 2, 0)
		self.tabPageSensorLayout.addWidget(self.textBoxRegionDecodedOutput, 2, 1)
		self.tabPageSensorLayout.setRowStretch(3, 100)
		self.tabPageSensorLayout.setColumnStretch(2, 100)

		# tabPageSensor
		self.tabPageSensor = QtGui.QWidget()
		self.tabPageSensor.setLayout(self.tabPageSensorLayout)

		# dataGridBits
		self.dataGridBits = QtGui.QTableView()
		self.dataGridBits.setModel(ArrayTableModel())
		self.dataGridBits.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.dataGridBits.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.dataGridBits.setToolTip("Click on a row to see more details")
		self.dataGridBits.verticalHeader().setDefaultSectionSize(20)

		# tabPageBitsLayout
		self.tabPageBitsLayout = QtGui.QHBoxLayout()
		self.tabPageBitsLayout.addWidget(self.dataGridBits)

		# tabPageBits
		self.tabPageBits = QtGui.QWidget()
		self.tabPageBits.setLayout(self.tabPageBitsLayout)

		# labelRegionName
		self.labelRegionName = QtGui.QLabel()
		self.labelRegionName.setText("Name")
		self.labelRegionName.setAlignment(QtCore.Qt.AlignRight)

		# textBoxRegionName
		self.textBoxRegionName = QtGui.QLineEdit()
		self.textBoxRegionName.setEnabled(False)
		self.textBoxRegionName.setAlignment(QtCore.Qt.AlignLeft)

		# tabPageRegionsLayout
		self.tabPageRegionsLayout = QtGui.QGridLayout()
		self.tabPageRegionsLayout.addWidget(self.labelRegionName, 0, 0)
		self.tabPageRegionsLayout.addWidget(self.textBoxRegionName, 0, 1)
		self.tabPageRegionsLayout.setRowStretch(1, 100)
		self.tabPageRegionsLayout.setColumnStretch(2, 100)

		# tabPageRegions
		self.tabPageRegions = QtGui.QWidget()
		self.tabPageRegions.setLayout(self.tabPageRegionsLayout)

		# dataGridColumns
		self.dataGridColumns = QtGui.QTableView()
		self.dataGridColumns.setModel(ArrayTableModel())
		self.dataGridColumns.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.dataGridColumns.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.dataGridColumns.setToolTip("Click on a row to see more details")
		self.dataGridColumns.verticalHeader().setDefaultSectionSize(20)
		self.dataGridColumns.selectionModel().selectionChanged.connect(self.__dataGridColumns_SelectionChanged)

		# tabPageColumnsLayout
		self.tabPageColumnsLayout = QtGui.QHBoxLayout()
		self.tabPageColumnsLayout.addWidget(self.dataGridColumns)

		# tabPageColumns
		self.tabPageColumns = QtGui.QWidget()
		self.tabPageColumns.setLayout(self.tabPageColumnsLayout)

		# dataGridProximalSynapses
		self.dataGridProximalSynapses = QtGui.QTableView()
		self.dataGridProximalSynapses.setModel(ArrayTableModel())
		self.dataGridProximalSynapses.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.dataGridProximalSynapses.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.dataGridProximalSynapses.setToolTip("Click on a row to see more details")
		self.dataGridProximalSynapses.verticalHeader().setDefaultSectionSize(20)
		self.dataGridProximalSynapses.selectionModel().selectionChanged.connect(self.__dataGridProximalSynapses_SelectionChanged)

		# tabPageProximalSynapsesLayout
		self.tabPageProximalSynapsesLayout = QtGui.QHBoxLayout()
		self.tabPageProximalSynapsesLayout.addWidget(self.dataGridProximalSynapses)

		# tabPageProximalSynapses
		self.tabPageProximalSynapses = QtGui.QWidget()
		self.tabPageProximalSynapses.setLayout(self.tabPageProximalSynapsesLayout)

		# dataGridCells
		self.dataGridCells = QtGui.QTableView()
		self.dataGridCells.setModel(ArrayTableModel())
		self.dataGridCells.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.dataGridCells.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.dataGridCells.setToolTip("Click on a row to see more details")
		self.dataGridCells.verticalHeader().setDefaultSectionSize(20)
		self.dataGridCells.selectionModel().selectionChanged.connect(self.__dataGridCells_SelectionChanged)

		# tabPageCellsLayout
		self.tabPageCellsLayout = QtGui.QHBoxLayout()
		self.tabPageCellsLayout.addWidget(self.dataGridCells)

		# tabPageCells
		self.tabPageCells = QtGui.QWidget()
		self.tabPageCells.setLayout(self.tabPageCellsLayout)

		# dataGridDistalSegments
		self.dataGridDistalSegments = QtGui.QTableView()
		self.dataGridDistalSegments.setModel(ArrayTableModel())
		self.dataGridDistalSegments.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.dataGridDistalSegments.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.dataGridDistalSegments.setToolTip("Click on a row to see more details")
		self.dataGridDistalSegments.verticalHeader().setDefaultSectionSize(20)
		self.dataGridDistalSegments.selectionModel().selectionChanged.connect(self.__dataGridDistalSegments_SelectionChanged)

		# tabPageDistalSegmentsLayout
		self.tabPageDistalSegmentsLayout = QtGui.QHBoxLayout()
		self.tabPageDistalSegmentsLayout.addWidget(self.dataGridDistalSegments)

		# tabPageDistalSegments
		self.tabPageDistalSegments = QtGui.QWidget()
		self.tabPageDistalSegments.setLayout(self.tabPageDistalSegmentsLayout)

		# dataGridDistalSynapses
		self.dataGridDistalSynapses = QtGui.QTableView()
		self.dataGridDistalSynapses.setModel(ArrayTableModel())
		self.dataGridDistalSynapses.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.dataGridDistalSynapses.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.dataGridDistalSynapses.setToolTip("Click on a row to see more details")
		self.dataGridDistalSynapses.verticalHeader().setDefaultSectionSize(20)
		self.dataGridDistalSynapses.selectionModel().selectionChanged.connect(self.__dataGridDistalSynapses_SelectionChanged)

		# tabPageDistalSynapsesLayout
		self.tabPageDistalSynapsesLayout = QtGui.QHBoxLayout()
		self.tabPageDistalSynapsesLayout.addWidget(self.dataGridDistalSynapses)

		# tabPageDistalSynapses
		self.tabPageDistalSynapses = QtGui.QWidget()
		self.tabPageDistalSynapses.setLayout(self.tabPageDistalSynapsesLayout)

		# tabControlMain
		self.tabControlMain = QtGui.QTabWidget()

		# layout
		layout = QtGui.QHBoxLayout()
		layout.addWidget(self.tabControlMain)

		# NodeInformationForm
		self.setLayout(layout)
		self.setWindowTitle("Node Information")
		self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))
		self.setMinimumHeight(200)
		self.setMaximumHeight(300)

	def refreshControls(self):
		"""
		Refresh controls for each time step.
		"""

		selectedNode = Global.nodeTreeForm.selectedNode

		# Show information according to note type
		if selectedNode != self.previousSelectedNode:
			if self.previousSelectedNode == None or self.previousSelectedNode.type != selectedNode.type:
				while True:
					self.tabControlMain.removeTab(0)
					if self.tabControlMain.count() == 0:
						break
				if selectedNode.type == NodeType.region:
					self.textBoxRegionName.setText(selectedNode.name)
					self.showTab(self.tabPageRegions, "Region")
					self.showTab(self.tabPageColumns, "Columns")
					self.dataGridColumns.clearSelection()
				elif selectedNode.type == NodeType.sensor:
					self.textBoxSensorName.setText(selectedNode.name)
					self.showTab(self.tabPageSensor, "Sensor")
					self.showTab(self.tabPageBits, "Bits")
					self.dataGridBits.clearSelection()
				self.tabControlMain.selectedIndex = 0
			self.previousSelectedNode = selectedNode

		if selectedNode.type == NodeType.region:
			self.selectedRegion = selectedNode

			"""TODO:# Update node controls
			self.textBoxRegionStepCounter.setText("")
			self.textBoxRegionActivityRate.setText("")
			self.textBoxRegionPredictionPrecision.setText("")
			self.textBoxRegionPredictionCounter.setText("")
			self.textBoxRegionCorrectPredictionCounter.setText("")
			if selectedRegion != None:
				self.textBoxRegionStepCounter.setText(selectedRegion.Statistics.StepCounter.ToString())
				self.textBoxRegionActivityRate.setText(selectedRegion.Statistics.ActivityRate.ToString())
				self.textBoxRegionPredictionPrecision.setText(selectedRegion.Statistics.PredictPrecision.ToString())
				self.textBoxRegionPredictionCounter.setText(selectedRegion.Statistics.PredictionCounter.ToString())
				self.textBoxRegionCorrectPredictionCounter.setText(selectedRegion.Statistics.CorrectPredictionCounter.ToString())"""

			# Bind the columns from this region
			header, data = self.getColumnsData(self.selectedRegion)
			self.dataGridColumns.model().update(header, data)
			self.dataGridColumns.resizeColumnsToContents()

		elif selectedNode.type == NodeType.sensor:
			self.selectedSensor = selectedNode

			"""TODO:# Update node controls"""

			# Bind the bits from this sensor
			header, data = self.getBitsData(self.selectedSensor)
			self.dataGridBits.model().update(header, data)
			self.dataGridBits.resizeColumnsToContents()

	def getBitsData(self, selectedSensor):
		header = ['Pos (x,y)', 'Was Predicted', 'Is Active', 'Activation Rate', 'Precision Rate']
		data = []
		for bit in selectedSensor.bits:
			pos = str(bit.x) + ", " + str(bit.y)
			wasPredicted = bit.isPredicted[Global.selTime - 1]
			isActive = bit.isActive[Global.selTime]
			activationRate = bit.statsActivationRate
			precisionRate = bit.statsPrecisionRate
			data.append([pos, wasPredicted, isActive, activationRate, precisionRate])

		return header, data

	def getColumnsData(self, selectedRegion):
		header = ['Pos (x,y)', 'Was Predicted', 'Is Active', 'Activation Rate', 'Precision Rate']
		data = []
		for column in selectedRegion.columns:
			pos = str(column.x) + ", " + str(column.y)
			wasPredicted = column.segment.isPredicted[Global.selTime - 1]
			isActive = column.segment.isActive[Global.selTime]
			activationRate = column.segment.statsActivationRate
			precisionRate = column.segment.statsPrecisionRate
			data.append([pos, wasPredicted, isActive, activationRate, precisionRate])

		return header, data

	def getProximalSynapsesData(self, selectedSegment):
		#TODO: Put sensor bit position (x,y,z)
		header = ['Permanence', 'Is Connected', 'Connection Rate', 'Precision Rate']
		data = []
		for synapse in selectedSegment.synapses:
			permanence = "{0:.3f}".format(synapse.permanence[Global.selTime])
			isConnected = synapse.isConnected[Global.selTime]
			connectionRate = synapse.statsConnectionRate
			precisionRate = synapse.statsPrecisionRate
			data.append([permanence, isConnected, connectionRate, precisionRate])

		return header, data

	def getCellsData(self, selectedColumn):
		header = ['Pos (z)', 'Was Predicted', 'Is Active', 'Activation Rate', 'Precision Rate']
		data = []
		for cell in selectedColumn.cells:
			pos = str(cell.z)
			wasPredicted = cell.isPredicted[Global.selTime - 1]
			isActive = cell.isActive[Global.selTime]
			activationRate = cell.statsActivationRate
			precisionRate = cell.statsPrecisionRate
			data.append([pos, wasPredicted, isActive, activationRate, precisionRate])

		return header, data

	def getDistalSegmetsData(self, selectedCell):
		header = ['Is Active', 'Activation Rate', 'Activation Rate']
		data = []
		for segment in selectedCell.segments:
			isActive = segment.isActive[Global.selTime]
			activationRate = segment.statsActivationRate
			data.append([isActive, activationRate, activationRate])

		return header, data

	def getDistalSynapsesData(self, selectedSegment):
		#TODO: Put lateral cell position (x,y,z)
		header = ['Permanence', 'Is Connected', 'Connection Rate']
		data = []
		for synapse in selectedSegment.synapses:
			permanence = "{0:.3f}".format(synapse.permanence[Global.selTime])
			isConnected = synapse.isConnected[Global.selTime]
			connectionRate = synapse.statsConnectionRate
			data.append([permanence, isConnected, connectionRate])

		return header, data

	def showTab(self, tab, title):
		tabFound = False
		for tabIdx in range(self.tabControlMain.count()):
			if self.tabControlMain.tabText(tabIdx) == title:
				tabFound = True
		if not tabFound:
			self.tabControlMain.addTab(tab, title)

	#endregion

	#region Events

	def closeEvent(self, event):
		self.Hide()
		self.Parent = None
		event.Cancel = True

	def __dataGridColumns_SelectionChanged(self, event):
		if self.selectedColumn != None:
			self.selectedColumn.segment.tree3d_selected = False

		self.dataGridProximalSynapses.clearSelection()
		self.dataGridCells.clearSelection()

		selectedRows = self.dataGridColumns.selectionModel().selectedRows()
		if len(selectedRows) > 0:
			index = selectedRows[0].row()
			self.selectedColumn = self.selectedRegion.columns[index]
			self.selectedColumn.segment.tree3d_selected = True

			# Bind the synapses of the selected segment
			self.showTab(self.tabPageProximalSynapses, "Proximal Synapses")
			header, data = self.getProximalSynapsesData(self.selectedColumn.segment)
			self.dataGridProximalSynapses.model().update(header, data)
			self.dataGridProximalSynapses.resizeColumnsToContents()

			# Bind the cells of the selected column
			self.showTab(self.tabPageCells, "Cells")
			header, data = self.getCellsData(self.selectedColumn)
			self.dataGridCells.model().update(header, data)
			self.dataGridCells.resizeColumnsToContents()

		Global.simulationForm.refreshControls()

	def __dataGridProximalSynapses_SelectionChanged(self, event):
		if self.selectedProximalSynapse != None:
			self.selectedProximalSynapse.tree3d_selected = False

		selectedRows = self.dataGridProximalSynapses.selectionModel().selectedRows()
		if len(selectedRows) > 0:
			index = selectedRows[0].row()
			self.selectedProximalSynapse = self.selectedColumn.segment.synapses[index]
			self.selectedProximalSynapse.tree3d_selected = True

		Global.simulationForm.refreshControls()

	def __dataGridCells_SelectionChanged(self, event):
		if self.selectedCell != None:
			self.selectedCell.tree3d_selected = False

		self.dataGridDistalSegments.clearSelection()

		selectedRows = self.dataGridCells.selectionModel().selectedRows()
		if len(selectedRows) > 0:
			index = selectedRows[0].row()
			self.selectedCell = self.selectedColumn.cells[index]
			self.selectedCell.tree3d_selected = True

			# Bind the segments of the selected cell
			self.showTab(self.tabPageDistalSegments, "Distal Segments")
			header, data = self.getDistalSegmetsData(self.selectedCell)
			self.dataGridDistalSegments.model().update(header, data)
			self.dataGridDistalSegments.resizeColumnsToContents()

		Global.simulationForm.refreshControls()

	def __dataGridDistalSegments_SelectionChanged(self, event):
		if self.selectedDistalSegment != None:
			self.selectedDistalSegment.tree3d_selected = False

		self.dataGridDistalSynapses.clearSelection()

		selectedRows = self.dataGridDistalSegments.selectionModel().selectedRows()
		if len(selectedRows) > 0:
			index = selectedRows[0].row()
			self.selectedDistalSegment = self.selectedCell.segments[index]

			# Bind the synapses of the selected segment
			self.showTab(self.tabPageDistalSynapses, "Distal Synapses")
			header, data = self.getDistalSynapsesData(self.selectedDistalSegment)
			self.dataGridDistalSynapses.model().update(header, data)
			self.dataGridDistalSynapses.resizeColumnsToContents()

		Global.simulationForm.refreshControls()

	def __dataGridDistalSynapses_SelectionChanged(self, event):
		if self.selectedDistalSynapse != None:
			self.selectedDistalSynapse.tree3d_selected = False

		selectedRows = self.dataGridDistalSynapses.selectionModel().selectedRows()
		if len(selectedRows) > 0:
			index = selectedRows[0].row()
			self.selectedDistalSynapse = self.selectedDistalSegment.synapses[index]
			self.selectedDistalSynapse.tree3d_selected = True

		Global.simulationForm.refreshControls()

	#endregion
