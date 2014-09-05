from nustudio.htm import maxTimeSteps
from nustudio.ui import Global

class Synapse:
	"""
	A class only to group properties related to synapses.
	"""

	#region Constructor

	def __init__(self):
		"""
		Initializes a new instance of the Synapse class.
		"""

		#region Instance fields

		self.index = -1
		"""Index of this synapse in the temporal pooler."""

		self.inputElem = None
		"""An input element is a cell in case of the source be a column or then a bit in case of the source be a sensor"""

		self.permanence = [0.] * maxTimeSteps
		"""Permanence of this synapse."""

		# States of this element
		self.isConnected = [False] * maxTimeSteps
		self.isPredicted = [False] * maxTimeSteps
		self.isRemoved = [False] * maxTimeSteps

		#region Statistics properties

		self.statsConnectionCount = 0
		self.statsConnectionRate = 0.
		self.statsPreditionCount = 0
		self.statsPrecisionRate = 0.

		#endregion

		#region 3d-tree properties (simulation form)

		self.tree3d_initialized = False
		self.tree3d_item = None
		self.tree3d_selected = False

		#endregion

		#endregion

	#endregion

	#region Methods

	def nextTimeStep(self):
		"""
		Perfoms actions related to time step progression.
		"""

		# Update states machine by remove the first element and add a new element in the end
		if len(self.isConnected) > maxTimeSteps:
			self.permanence.remove(self.permanence[0])
			self.isConnected.remove(self.isConnected[0])
			self.isPredicted.remove(self.isPredicted[0])
			self.isRemoved.remove(self.isRemoved[0])
		self.permanence.append(0.)
		self.isConnected.append(False)
		self.isPredicted.append(False)
		self.isRemoved.append(False)

		# Calculate statistics
		if self.isConnected[maxTimeSteps - 1]:
			self.statsConnectionCount += 1
		if self.isPredicted[maxTimeSteps - 1]:
			self.statsPreditionCount += 1
		if Global.currTime > 0:
			self.statsConnectionRate = self.statsConnectionCount / Global.currTime
		if self.statsConnectionCount > 0:
			self.statsPrecisionRate = self.statsPreditionCount / self.statsConnectionCount

	#endregion
