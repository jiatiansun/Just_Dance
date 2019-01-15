class Music(object):
	def __init__(self,name,path,score):
		self.name = name
		self.path = path
		self.score = score

	def getHighScore(self):
		return self.score

	def getPath(self):
		return self.path

	def getName(self):
		return self.name

	def setScore(self,score):
		self.score = score

class Arrow(object):
	def __init__(self, startTime, duration, type):
		self.type = type
		self.startTime = startTime
		self.expectedTime = duration

	def getType(self):
		return self.type

	def getStartTime(self):
		return self.startTime

	def getExpectedTime(self):
		return self.expectedTime