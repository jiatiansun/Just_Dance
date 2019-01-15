
from core import *
from util import *
import decimal

class DanceGame(object):

	def __init__(self, gui, musicPath, level):
		self.GUI = gui
		
		self.musicPath = musicPath
		self.difficulty = level
		self.arrows = []
		self.startTime = 0
		self.currArrowIdx = 0

		self.score = 0
		self.good = 0
		self.miss = 0
		self.perfect = 0
		self.length = 0

		self.perfectBuffer=0.15
		self.goodBuffer=0.25

	@staticmethod
	def mergeArrowList(heavy, light):
		length = len(heavy) + len(light)
		heavyLen = len(heavy)
		lightLen = len(light)
		arrows = [None] * length
		heavyIdx = 0
		lightIdx = 0
		processedArrow = 0
		while(processedArrow != length):
			if(heavyIdx >= heavyLen):
				arrows[processedArrow] = Arrow(0, light[lightIdx], 'l')
				lightIdx += 1
			elif(lightIdx >= lightLen):
				arrows[processedArrow] = Arrow(0, heavy[heavyIdx], 'h')
				heavyIdx += 1
			else:
				hTime = heavy[heavyIdx]
				lTime = light[lightIdx]
				if(hTime < lTime):
					arrows[processedArrow] = Arrow(0, hTime, 'h')
					heavyIdx += 1
				else:
					arrows[processedArrow] = Arrow(0, lTime, 'l')
					lightIdx += 1
			processedArrow+=1
		return (length, arrows)

	def processMusic(self):
		beats=getBeatFrame(self.musicPath)
		onsets=getOnSet(self.musicPath)
		heavy, light =reduceBeats(beats,onsets)
		# Generate All Arrows
		if(self.difficulty == 'easy'):
			self.length = len(heavy)
			self.arrows = [None] * self.length
			for i in range(self.length):
				self.arrows[i] = Arrow(0, heavy[i], 'h')
		elif(self.difficulty == 'hard'):
			self.length, self.arrows = mergeArrowList(heavy, light)
		return (self.length,self.arrows)

	def startDance(self, time):
		self.startTime = globalClock.getFrameTime()

	def getStartTime(self):
		return self.startTime

	def calculateScore(self):
		self.score=self.perfect*1.5+self.good

	def getScoreReport(self):
		return (self.score,self.miss,self.good,self.perfect)

	def isArrowMissed(self,task):
		if(self.currArrowIdx>=self.length):
			return
		arrow=self.arrows[self.currArrowIdx]
		startTime = self.startTime
		expectedTime = arrow.expectedTime
		arrowType = arrow.type
		arrowIdx=self.currArrowIdx
		endTime = globalClock.getFrameTime()
		pressTime=endTime-startTime
		if (pressTime-expectedTime)>self.goodBuffer:
			self.miss+=1
			self.GUI.pressEffect('MISS',-1)
			self.currArrowIdx+=1

		return task.cont

	def keyPressed(self, key):
		if(self.currArrowIdx>=self.length):
			return
		arrow=self.arrows[self.currArrowIdx]
		startTime = self.startTime
		expectedTime = arrow.expectedTime
		endTime = globalClock.getFrameTime()
		pressTime=endTime-startTime
		arrowType = arrow.type
		arrowIdx=self.currArrowIdx
		if (key == arrowType and abs(pressTime-expectedTime)<=self.perfectBuffer):
			self.perfect+=1
			self.GUI.pressEffect('PERFECT', arrowIdx)
			self.currArrowIdx+=1
			self.calculateScore()
			self.GUI.getPanel('dance').getItem('scoreText')['text']=(str(self.score))
		elif (key == arrowType and 
			abs(pressTime-expectedTime)<=self.goodBuffer):
			self.good+=1
			self.GUI.pressEffect('GOOD', arrowIdx)
			self.currArrowIdx += 1
			self.calculateScore()
			self.GUI.getPanel('dance').getItem('scoreText')['text']=(str(self.score))
		else:
			self.miss+=1
			self.GUI.pressEffect('MISS', arrowIdx)
			self.currArrowIdx += 1

