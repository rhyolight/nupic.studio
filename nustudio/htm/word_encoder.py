import sys

class Dictionary:

	def __init__(self):
		self._entries = dict()

	def addWord(self, word, hashCode):
		"""
		Adds a word to the lookup table to future search.
		Hashing methods are irreversible, so the only way to know which exact word the HTM returned, is searching by its hash code.
		"""

		self._entries[hashCode] = word

	def recoverWord(self, hashCode):
		"""
		Search for a word in lookup table through its hash code.
		"""

		word = ""
		if hashCode in self._entries.keys():
			word = self._entries[hashCode]

		return word

	def getHashFromString(self, str):
		"""
		This method transforms a word to a number using Dan Bernstein's algorithm with k=33.
		"""

		hash = int(0)
		for c in range(len(str)):
			hash = (hash * 33) + str[c]

		return hash

class WordEncoder(Encoder):
	"""
	Words should be encoded to map of bits which are readable for HTM's
	This encoder works as follow:
	  1. Hashes the word to a numerical representation;
	  2. Arrange each character to a respective kth position in Y axis.
		 I.e. the second char ('5') ocupies a bit in 5th position.
	Example:
	  Word: 'dog'
	  Hash: 15081376
	  Map of bits:
		00100000
		10001000
		00000000
		00000100
		00000000
		01000000
		00000001
		00000010
		00010000
		00000000
	"""

	def __init__(self):
		"""
		Constructor.
		"""

		self.updateDictionary = False
		self._dictionary = None
		self.maxHashSize = len(str(sys.maxint))

	def encodeToHtm(self, rawData):
		"""
		Transform a word to map of bits and return this.
		Words should be encoded to map of bits which are readable for HTMs.
		This method works as follow:
		  1. Hashes the word to a numerical representation;
		  2. Add the word and its hash code to the lookup table for future search;
		  3. Arrange each character in hash code to a respective kth position in Y axis.
			 I.e. a '5' character in hash code will ocupy a bit in 5th position in Y axis.
		Example:
		  Word: 'dog'
		  Hash: 95081376
		  Map of bits:
			00100000 => __0_____
			00001000
			00000000
			00000100
			00000000
			01000000 => _5______
			00000001
			00000010
			00010000
			10000000 => 9_______
		"""

		word = str(rawData)

		# Get an hash representation to the word
		hashCode = int(self._dictionary.getHashFromString(word))
		if self.updateDictionary:
			self._dictionary.addWord(word, hashCode)

		# Create a map of bits to this word
		htmData = [self.maxHashSize, 10]

		# Arrange each character to a respective kth position in Y axis
		hashString = str(hashCode)
		hashString = ('0' * (self.maxHashSize - len(hashString))) + hashString
		for c in range(self.maxHashSize):
			kthPosition = int(char.ConvertFromUtf32(hashString[c]))
			htmData[c, kthPosition] = 1

		"""TODO: Remove:
		#str = "\nWord:" + word + "\n<bitmap>\n"
		for kth in range(10):
			for c in range(self.maxHashSize):
				str += str(htmData[c, kth])
			str += "\n"
		str += "</bitmap>"
		print str
		"""

		return htmData

	def decodeFromHtm(self, htmData):
		"""
		Transform a map of bits to word and return this.
		Words should be decoded from map of bits returned by HTMs.
		This method works as follow:
		  1. Deciphers each character through its respective kth position in Y axis.
			 I.e. a bit ocupping the 5th position in Y axis means '5' character.
		  2. Concatenate all characters to hash code.
		  3. Search the word in lookup table through its hash code;
		Example:
		  Word: 'dog'
		  Hash: 15081376
		  Map of bits:
			00100000 => __0_____
			00001000
			00000000
			00000100
			00000000
			01000000 => _5______
			00000001
			00000010
			00010000
			10000000 => 9_______
		"""

		# Arrange each character from a respective kth position in Y axis.
		hashString = ""
		for c in range(self.maxHashSize):
			kthPosition = -1
			bestActivity = 0.0
			for kth in range(10):
				activity = htmData[c, kth]
				if activity > bestActivity:
					bestActivity = activity
					kthPosition = kth

			# If found any bit in Y axis
			if kthPosition >= 0:
				hashString += kthPosition
			else:
				# If not found any bit in Y axis then we do not have a valid word
				hashString = ""
				break

		# Get the word from hash representation
		word = ""
		if hashString != "":
			hashCode = int(hashString)
			word = self._dictionary.recoverWord(hashCode)

		return word