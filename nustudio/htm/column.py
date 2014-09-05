from nustudio.htm.segment import Segment, SegmentType

class Column:
	"""
	A class only to group properties related to columns.
	"""

	#region Constructor

	def __init__(self):
		"""
		Initializes a new instance of the Column class.
		"""

		#region Instance fields

		self.x = -1
		"""Position on X axis"""

		self.y = -1
		"""Position on Y axis"""

		self.segment = Segment(SegmentType.proximal)
		"""Proximal segment of this column"""

		self.cells = []
		"""List of cells that compose this column."""

		#region 3d-tree properties (simulation form)

		self.tree3d_x = 0
		self.tree3d_y = 0
		self.tree3d_z = 0

		#endregion

		#endregion

	#endregion

	#region Methods

	def getCell(self, z):
		"""
		Return the cell located at given position
		"""

		for cell in self.cells:
			if cell.z == z:
				return cell

	def nextTimeStep(self):
		"""
		Perfoms actions related to time step progression.
		"""

		self.segment.nextTimeStep()
		for cell in self.cells:
			cell.nextTimeStep()

	#endregion
