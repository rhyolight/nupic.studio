from nustudio.htm import maxTimeSteps
from nustudio.ui import Global

class SegmentType:
	proximal = 0
	distal = 1

class Segment:
	"""
	A class only to group properties related to segments.
	"""

	#region Constructor

	def __init__(self, type):
		"""
		Initializes a new instance of the Segment class.
		"""

		#region Instance fields

		self.type = type
		"""Determine if this segment is proximal or distal."""

		self.index = -1
		"""Index of this segment in the temporal pooler."""

		self.synapses = []
		"""List of distal synapses of this segment."""

		# States of this element
		self.isActive = [False] * maxTimeSteps
		self.isPredicted = [False] * maxTimeSteps
		self.isRemoved = [False] * maxTimeSteps

		#region Statistics properties

		self.statsActivationCount = 0
		self.statsActivationRate = 0.
		self.statsPreditionCount = 0
		self.statsPrecisionRate = 0.

		#endregion

		#region 3d-tree properties (simulation form)

		self.tree3d_initialized = False
		self.tree3d_x1 = 0
		self.tree3d_y1 = 0
		self.tree3d_z1 = 0
		self.tree3d_x2 = 0
		self.tree3d_y2 = 0
		self.tree3d_z2 = 0
		self.tree3d_item = None
		self.tree3d_selected = False

		#endregion

		#endregion

	#endregion

	#region Methods

	def getSynapse(self, inputElem):
		"""
		Return the synapse connected to a given cell or sensor bit
		"""

		synapse = None
		for synapse in self.synapses:
			if synapse.inputElem == inputElem:
				return synapse

	def nextTimeStep(self):
		"""
		Perfoms actions related to time step progression.
		"""

		# Update states machine by remove the first element and add a new element in the end
		if len(self.isActive) > maxTimeSteps:
			self.isActive.remove(self.isActive[0])
			self.isPredicted.remove(self.isPredicted[0])
			self.isRemoved.remove(self.isRemoved[0])

			# Remove synapses that are marked to be removed
			for synapse in self.synapses:
				if synapse.isRemoved[0]:
					self.synapses.remove(synapse)
					del synapse
		self.isActive.append(False)
		self.isPredicted.append(False)
		self.isRemoved.append(False)

		for synapse in self.synapses:
			synapse.nextTimeStep()

		# Calculate statistics
		if self.isActive[maxTimeSteps - 1]:
			self.statsActivationCount += 1
		if self.isPredicted[maxTimeSteps - 1]:
			self.statsPreditionCount += 1
		if Global.currTime > 0:
			self.statsActivationRate = self.statsActivationCount / Global.currTime
		if self.statsActivationCount > 0:
			self.statsPrecisionRate = self.statsPreditionCount / self.statsActivationCount

	#endregion
