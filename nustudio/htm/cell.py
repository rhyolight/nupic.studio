from nustudio.htm import maxTimeSteps
from nustudio.ui import Global

class Cell:
	"""
	A class only to group properties related to cells.
	"""

	#region Constructor

	def __init__(self):
		"""
		Initializes a new instance of the Cell class.
		"""

		#region Instance fields

		self.index = -1
		"""Index of this cell in the temporal pooler."""

		self.z = -1
		"""Position on Z axis"""

		self.segments = []
		"""List of distal segments of this cell."""

		# States of this element
		self.isLearning = [False] * maxTimeSteps
		self.isActive = [False] * maxTimeSteps
		self.isPredicted = [False] * maxTimeSteps

		#region Statistics properties

		self.statsActivationCount = 0
		self.statsActivationRate = 0.
		self.statsPreditionCount = 0
		self.statsPrecisionRate = 0.

		#endregion

		#region 3d-tree properties (simulation form)

		self.tree3d_initialized = False
		self.tree3d_x = 0
		self.tree3d_y = 0
		self.tree3d_z = 0
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
		if len(self.isActive) > maxTimeSteps:
			self.isLearning.remove(self.isLearning[0])
			self.isActive.remove(self.isActive[0])
			self.isPredicted.remove(self.isPredicted[0])

			# Remove segments (and their synapses) that are marked to be removed
			for segment in self.segments:
				if segment.isRemoved[0]:
					for synapse in segment.synapses:
						segment.synapses.remove(synapse)
						del synapse
					self.segments.remove(segment)
					del segment
		self.isLearning.append(False)
		self.isActive.append(False)
		self.isPredicted.append(False)

		for segment in self.segments:
			segment.nextTimeStep()

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
