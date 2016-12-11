from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import PerspectiveLens
from panda3d.core import Point3,Spotlight,PointLight
from panda3d.core import LVector3
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Material
from panda3d.core import NodePath, PandaNode 
from panda3d.core import AudioSound
from math import pi, sin, cos
from direct.particles.ParticleEffect import ParticleEffect
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TextNode, TransparencyAttrib
from panda3d.core import NodePath, TextNode
from panda3d.core import PointLight, AmbientLight
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.interval.SoundInterval import SoundInterval
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from direct.interval.MetaInterval import Parallel
from direct.interval.LerpInterval import LerpHprInterval
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.LerpInterval import LerpColorInterval
import sys
import sys, copy,colorsys
from audio_clear import *
import os.path

# applies code of the panda3D sample disco
class musicGame(ShowBase):
    def makeInfo(self, i):
        return OnscreenText(
            parent=base.a2dTopLeft, align=TextNode.ALeft,
            style=1, fg=(1, 1, 0, 1), shadow=(0, 0, 0, .4),
            pos=(0.06, -0.1 -(.06 * i)), scale=.05, mayChange=True)
    
    def __init__(self):
        ShowBase.__init__(self)
        self.songButtonList=[]
        self.BGM=base.loader.loadSfx("music/Nyte - Lone Walker.mp3")
        self.taskMgr.add(self.BGMmanage,'manage')
        if os.path.isfile('musicGameData.txt'):
            print('here')
            file=open('musicGameData.txt','r')
        else:
            file=open('musicGameData.txt','w')
            file.write('Rather Be\n')
            file.write('music/Clean Bandit,Jess Glynne-Rather '+
        'Be (Robin Schulz Edit).mp3\n')
            file.write('0\n')
            file.write('Memory\n')
            file.write('music/Elaine Paige-Memory.mp3\n')
            file.write('0\n')
        file=open('musicGameData.txt','r')
        self.data=file.readlines()
        self.highestScores=dict()
        self.musicNames=[]
        self.musicPathes=dict()
        self.getSongs()
        self.difficultyLevel='easy'
        self.setBackgroundColor((0, 0, 0, 1))
        self.musicList=[]
        self.options=self.render.attachNewNode(PandaNode('options'))
        self.mainMenu=self.render.attachNewNode(PandaNode("mainMenu"))
        self.dance=self.render.attachNewNode(PandaNode('dance'))
        self.loading=self.render.attachNewNode(PandaNode('loading'))
        self.setting=self.render.attachNewNode(PandaNode('setting'))
        self.scoreBoard=self.render.attachNewNode(PandaNode('scoreBoard'))
        self.gameScore=self.render.attachNewNode(PandaNode('gameScore'))
        self.buttonDict={'options':[],'mainMenu':[],'dance':[],'loading':[],
        'setting':[],'scoreBoard':[],'gameScore':[]}
        self.taskMgr.add(self.spinCam,'spinCam')
        self.initoptions()
        self.options.show()
        self.mainMenu.hide()
        self.dance.hide()
        self.setting.hide()
        self.scoreBoard.hide()
        self.gameScore.hide()
        self.selected='options'
    
    def BGMmanage(self,task):
        if self.selected=='dance':
            self.BGM.stop()
        elif self.BGM.status()!=AudioSound.PLAYING:
            self.BGM.play()
        return task.cont
    
    def getSongs(self):
        dataList=[]
        for line in self.data:
            dataList.append(line.strip())
        for i in range(0,len(dataList),3):
            self.musicNames.append(dataList[i])
            self.musicPathes[dataList[i]]=dataList[i+1]
            self.highestScores[dataList[i]]=float(dataList[i+2])
            
    def initoptions(self):
        self.optionBackground = OnscreenImage(parent=render2dp, image=
        'MENU_ORG_text.jpg') 
        self.cam2dp.node().getDisplayRegion(0).setSort(-20) 
        self.settingButton = DirectButton(pos=(0.1, 0, 0), text=" Setting",
                                   scale=.08, pad=(.2, .2), frameColor=(0.02,0.3,0.5,0.4),
                                   text_fg=(0,0.4,0.7,1),
                                   text_align=TextNode.ALeft,frameSize=(-4.3,4,-0.6,1),
                                   text_pos=(-1,0,0),
                                   rolloverSound=None, clickSound=None,
                                   command=self.initSetting)
        self.settingButton.resetFrameSize()
        self.playButton = DirectButton(pos=(0.1, 0, .15), text="Start",
                                   scale=.08, pad=(.2, .2),frameColor=(0.02,0.3,0.5,0.4),
                                   text_fg=(0.1,0.4,0.7,1),
                                   text_align=TextNode.ALeft,
                                   frameSize=(-3,4,-0.6,1),
                                   rolloverSound=None, clickSound=None,
                                   command=self.changeToMenu)
        self.scoreBoardButton= DirectButton(pos=(0, 0, -.15), text="HighScore",
                                   scale=.08, pad=(.2, .2),frameColor=(0.02,0.3,0.5,0.4),
                                   text_pos=(-1,0,0),
                                   text_fg=(0.1,0.4,0.7,1),text_align=TextNode.ALeft,frameSize=(-5,5.3,-0.6,1),
                                   rolloverSound=None, clickSound=None,
                                   command=self.turnToScoreBoard)
        numItemsVisible = 4
        itemHeight = 0.25
        self.optionLists=DirectFrame(frameSize=(-0.3,0.3,-0.2,0.2),pos=(0.8,0,-0.5),frameColor=(0,0,0,0))
        self.settingButton.reparentTo(self.optionLists)
        self.playButton.reparentTo(self.optionLists)
        self.scoreBoardButton.reparentTo(self.optionLists)
        self.buttonDict['options']+=[self.optionLists]

    def changeToMenu(self):
        self.selected=='mainMenu'
        self.initMainMenu()
        self.optionBackground.hide()
        self.optionLists.hide()
        
    def initMainMenu(self):
        self.mainMenuBackground = OnscreenImage(parent=render2dp, 
                            image='BGM_ORG_text.jpg') 
        self.cam2dp.node().getDisplayRegion(0).setSort(-20) 
        self.createMainMenu()
        self.disableMouse()
    
    def createMainMenu(self):
        self.songList = DirectScrolledFrame(canvasSize = (-0.3,0.2,-1,1), 
                            frameSize = (-0.45,0.55,-0.2,0.2)) 
        self.songList['frameColor']=(0.5,0.5,1,0)
        self.songList.setPos(0, 0, -0.3)
        self.songList['verticalScroll_thumb_frameColor']=(1,1,1,0.3)
        self.songList['verticalScroll_incButton_frameColor']=(1,1,1,0)
        self.songList['verticalScroll_decButton_frameColor']=(1,1,1,0)
        self.songList['verticalScroll_frameColor']=(0.5,0.5,1,0)
        for i in range(len(self.musicNames)):
            defaultSong=DirectButton(pos=(0, 0, 0.9-i*0.15), text=(
                                    self.musicNames[i],'clicked',
                                    self.musicNames[i],self.musicNames[i]),
                                   scale=.1, pad=(.2, .2),
                                    frameColor=(0.058,0.294,0.545,0.7),
                                    text_pos=(1.3,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),
                                   rolloverSound=None, clickSound=None,
                                   command=self.preInitDance,extraArgs=(i,))
            defaultSong['frameSize']=(-4,6,-0.7,0.7)
            defaultSong.reparentTo(self.songList.getCanvas())
            self.musicList.append(defaultSong)
        self.importButton=DirectButton(pos=(0,0,-0.6),text='+ IMPORT NEW MUSIC ',
                                    scale=0.1,pad=(.2,.2),frameColor=(0.058,.294,0.545,0.7),
                                    text_fg=(0.88,0.98,1,1),frameSize=(-6.5,6.5,-0.8,0.8),
                                    text_scale=(0.85,0.85),
                        text_pos=(0.5,-0.4),rolloverSound=None, clickSound=None,
                                   command=self.changeToImport)
        self.backToOptionButton=DirectButton(text='<<BACK TO MENU',
                                    pos=(-1,0,0.8),scale=.1,pad=(.2, .2),
                                    frameColor=(1,1,1,0),
                                    text_pos=(1.3,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),
                                   rolloverSound=None, clickSound=None,
                                   command=self.backToOption)
    def backToOption(self):
        self.mainMenu.hide()
        self.mainMenuBackground.hide()
        self.songList.hide()
        self.importButton.hide()
        self.backToOptionButton.hide()
        self.options.show()
        self.optionBackground.show()
        self.optionLists.show()
        
    def changeToImport(self):
        self.songList.hide()
        self.importButton.hide()
        self.mainMenu.hide()
        self.mainMenuBackground.hide()
        self.backToOptionButton.hide()
        self.importBackground= OnscreenImage(parent=render2dp, 
        image='BGM_ORG.jpg') 
        self.cam2dp.node().getDisplayRegion(0).setSort(-20) 
        self.newNameBox = DirectEntry(text = "" ,pos=(-0.4,0,0.5),scale=.08,
                command=self.setNewSong,extraArgs=[str(0)],
                                        frameColor=(1,1,1,0.3),
        initialText="song name (please press enter after input)", 
                                                numLines = 3,focus=1) 
        self.newPathBox = DirectEntry(text = "" ,pos=(-0.4,0,0.2),
                                            frameColor=(1,1,1,0.3),
                scale=.08,command=self.setNewSong,extraArgs=[str(1)],
        initialText="song path (please press enter after input)", 
                                                numLines = 5,focus=1) 
        self.confirmationButton=DirectButton(text='IMPORT',pos=(0, 0, -0.3),
                                   scale=.1, pad=(.2, .2),
                                    frameColor=(0.058,.294,0.545,0.7),
                                    text_pos=(0,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),
                                    frameSize=(-6.5,6.5,-0.8,0.8),
                                   rolloverSound=None, clickSound=None,
                                   command=self.importNewSong)
    def importNewSong(self):
        self.musicPathes[self.newSongName]=self.newSongPath
        self.musicNames.append(self.newSongName)
        file=open('musicGameData.txt','a')
        file.write(self.newSongName+'\n')
        file.write(self.newSongPath+'\n')
        file.write('0\n')
        self.newSongName=''
        self.newSongPath=''
        self.newNameBox.destroy()
        self.newPathBox.destroy()
        self.confirmationButton.destroy()
        self.importBackground.destroy()
        self.mainMenuBackground.show()
        self.importButton.show()
        self.updateSongs()
        self.songList.show()
    
    def updateSongs(self):
        path=self.musicPathes[self.musicNames[-1]]
        self.musicList.append(DirectButton(text=self.musicNames[-1],
                                    pos=(0, 0,0.9-0.15*(len(self.musicList))),
                                   scale=.1, pad=(.2, .2),
                                    frameColor=(0.058,.294,0.545,0.7),
                                    text_pos=(1.3,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),
                                    frameSize=(-4,6,-0.7,0.7),
                                   rolloverSound=None, clickSound=None,
                                   command=self.preInitDance,extraArgs=
                                    (-1,)))
        self.highestScores[self.musicNames[-1]]=0
        self.musicList[-1].reparentTo(self.songList.getCanvas())
        
        
    def setNewSong(self,str,index):
        if index=='0':
            self.newSongName=str
        elif index=='1':
            self.newSongPath=str
    
    def preInitDance(self,index):
        self.selected='dance'
        self.initDance(self.musicPathes[self.musicNames[index]])
        self.mainMenu.hide()
        self.mainMenuBackground.hide()
        self.backToOptionButton.hide()
        self.importButton.hide()
        self.dance.show()
        self.GUIarrows.show()
        self.scoreText.show()
        self.songList.hide()
        self.currSong=self.musicNames[index]
    
    def changeDifficulty(self):
        if self.difficultyLevel=='hard':
            self.difficultyLevel='easy'
            self.setDifficultyButton['text']='easy'
        else:
            self.difficultyLevel='hard'
            self.setDifficultyButton['text']='hard'
        
    def initSetting(self):
        self.optionBackground.hide()
        self.optionLists.hide()
        self.options.hide()
        self.settingBackground = OnscreenImage(parent=render2dp, 
        image='SET_ORG.jpg') 
        self.cam2dp.node().getDisplayRegion(0).setSort(-20)
        self.difficulty=OnscreenText(pos=(0.4,0.3),scale=0.08,fg=(0.88,0.98,1,1),
                                    text='Difficulty:')
        
        self.setDifficultyButton=DirectButton(pos=(0.6,0,0),scale=.1, pad=(.2, .2),
                                    frameColor=(0.058,0.294,0.545,0.7),
                                    frameSize=(-1.5,5,-0.8,0.8),
                                    text_pos=(1,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),text=self.difficultyLevel,
                                    command=self.changeDifficulty)
        self.backToOptionButton3=DirectButton(text='<<BACK TO MENU',
                                    pos=(-1,0,0.8),scale=.1,pad=(.2, .2),
                                    frameColor=(1,1,1,0),
                                    text_pos=(1.3,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),
                                   rolloverSound=None, clickSound=None,
                                   command=self.backToOption3)
    
    def backToOption3(self):
        self.settingBackground.hide()
        self.setDifficultyButton.hide()
        self.backToOptionButton3.hide()
        self.optionBackground.show()
        self.difficulty.hide()
        self.optionLists.show()
        self.options.show()
        
    
    def turnToScoreBoard(self):
        self.options.hide()
        self.optionBackground.hide()
        self.optionLists.hide()
        self.initScoreBoard()
        self.scoreBoardBackground.show()
        self.highScoreFrame.show()
        
    def initScoreBoard(self):
        self.scoreBoardBackground=OnscreenImage(parent=render2dp, 
            image='HIGH_ORG_text.jpg')
        self.highScoreTitle1=DirectLabel(frameSize=(-0.6,0.6,-0.2,.2),pos=(0,0,0.2),
            text='Music',frameColor=(0,0,0,0),
            text_align=TextNode.ALeft,text_scale=0.08,text_fg=(1,1,1,1))
        self.highScoreTitle2=DirectLabel(frameSize=(-0.6,0.6,-0.6,.6),pos=(0.4,0,0.2),
            text='Highest Score',text_fg=(1,1,1,1),frameColor=(0,0,0,0),
            text_align=TextNode.ALeft,text_scale=0.08)
        self.cam2dp.node().getDisplayRegion(0).setSort(-20)
        self.highScoreFrame=DirectScrolledFrame(frameColor=(0.5,0.5,1,0),
                                        canvasSize = (-0.3,0.2,-1,1), 
                            frameSize = (-0.3,1.1,-0.8,0.3),pos=(0.2,0,0))
        self.highScoreFrame['verticalScroll_thumb_frameColor']=(1,1,1,0.3)
        self.highScoreFrame['verticalScroll_incButton_frameColor']=(1,1,1,0)
        self.highScoreFrame['verticalScroll_decButton_frameColor']=(1,1,1,0)
        self.highScoreFrame['verticalScroll_frameColor']=(0.5,0.5,1,0)
        self.highScoreTitle1.reparentTo(self.highScoreFrame)
        self.highScoreTitle2.reparentTo(self.highScoreFrame)
        for i in range(len(self.musicNames)):
            scoreLabel=DirectButton(frameSize=(-0.3,0.3,-0.2,.2),pos=(0,0,0-i*0.2),
            text='%s:  %d'%(self.musicNames[i],self.highestScores[self.musicNames[i]]),
            text_align=TextNode.ALeft,text_scale=0.08,frameColor=(0,0,0,0),
            text_fg=(1,1,1,1))
            scoreLabel.reparentTo(self.highScoreFrame)
        self.backToOptionButton2=DirectButton(text='<<BACK TO MENU',
                                    pos=(-1,0,0.8),scale=.1,pad=(.2, .2),
                                    frameColor=(1,1,1,0),
                                    text_pos=(1.3,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),
                                   rolloverSound=None, clickSound=None,
                                   command=self.backToOption2)
    
    def backToOption2(self):
        self.highScoreFrame.hide()
        self.scoreBoardBackground.hide()
        self.backToOptionButton2.hide()
        self.optionBackground.show()
        self.optionLists.show()
        self.options.show()
    
    def changeButtonState(self,mode):
        for key in list(self.buttonDict.keys()):
            if key==mode:
                for button in self.buttonDict[key]:
                    button.show()
            else:
                for otherButton in self.buttonDict[key]:
                    button.hide()

    def initDance(self,path):
        self.danceScene=self.loader.loadModel("models/disco_hall")
        self.danceScene.reparentTo(self.dance)
        self.danceScene.setPosHpr(0, 50, -4, 90, 0, 0)
        #startPoint of application of disco
        self.ambientLight = self.dance.attachNewNode(
                                            AmbientLight("ambientLight"))
        self.ambientLight.node().setColor((0.1, 0.1, 0.1, 1))
        self.directionalLight = self.dance.attachNewNode(
            DirectionalLight("directionalLight"))
        self.directionalLight.node().setColor((.1, .1, .1, 1))
        self.directionalLight.node().setDirection(LVector3(1, 1, -2))
        self.directionalLight.setZ(6)
        dlens = self.directionalLight.node().getLens()
        dlens.setFilmSize(41, 21)
        dlens.setNearFar(50, 75)
        self.spotlight = camera.attachNewNode(Spotlight("spotlight"))
        self.spotlight.node().setColor((.6, .6, .6, 1))
        self.spotlight.node().setSpecularColor((0, 0, 0, 1))
        self.spotlight.node().setLens(PerspectiveLens())
        self.spotlight.node().getLens().setFov(16, 16)
        self.spotlight.node().setAttenuation(LVector3(1, 0.0, 0.0))
        self.spotlight.node().setExponent(60.0)
        self.redHelper = loader.loadModel('models/sphere')
        self.redHelper.setColor((0.2, 0.2, .35, 1))
        self.redHelper.setPos(-6.5, -3.75, 0)
        self.redHelper.setScale(.25)
        self.redPointLight = self.redHelper.attachNewNode(
            PointLight("redPointLight"))
        self.redPointLight.node().setColor((.05, .3,.4, 1))
        self.redPointLight.node().setAttenuation(LVector3(.1, 0.04, 0.0))
        self.greenHelper = loader.loadModel('models/sphere')
        self.greenHelper.setColor((0.2, 0.2, .35, 1))
        self.greenHelper.setPos(0, 7.5, 0)
        self.greenHelper.setScale(.25)
        self.greenPointLight = self.greenHelper.attachNewNode(
            PointLight("greenPointLight"))
        self.greenPointLight.node().setAttenuation(LVector3(.1, .04, .0))
        self.greenPointLight.node().setColor((.05, .3, .4, 1))
        self.blueHelper = loader.loadModel('models/sphere')
        self.blueHelper.setColor((0.2, 0.2, .35, 1))
        self.blueHelper.setPos(6.5, -3.75, 0)
        self.blueHelper.setScale(.25)
        self.bluePointLight = self.blueHelper.attachNewNode(
            PointLight("bluePointLight"))
        self.bluePointLight.node().setAttenuation(LVector3(.1, 0.04, 0.0))
        self.bluePointLight.node().setColor((.1, .1, .4, 1))
        self.bluePointLight.node().setSpecularColor((1, 1, 1, 1))
        
        self.pointLightHelper = self.dance.attachNewNode("pointLightHelper")
        self.pointLightHelper.setPos(0, 50, 11)
        self.redHelper.reparentTo(self.pointLightHelper)
        self.greenHelper.reparentTo(self.pointLightHelper)
        self.blueHelper.reparentTo(self.pointLightHelper)
        self.pointLightsSpin = self.pointLightHelper.hprInterval(
            6, LVector3(360, 0, 0))
        self.pointLightsSpin.loop()
        self.arePointLightsSpinning = True
        #end point of the application(the data is different)
        self.playIndex=0
        self.animationDown=['pose','makeCircle','pose','makeCircle','pressKnee']
        self.animationRight=['jump','jump','wave','wave','leapSwitch']
        self.perPixelEnabled = True
        self.shadowsEnabled = False
        self.dance.setLight(self.ambientLight)
        self.dance.setLight(self.directionalLight)
        self.dance.setLight(self.spotlight)
        self.dance.setLight(self.redPointLight)
        self.dance.setLight(self.greenPointLight)
        self.dance.setLight(self.bluePointLight)
        self.dancer = Actor("dancer-final.egg",{"pressKnee": 
        '-pressKnee.egg',
        'leapSwitch':
        "-leapSwitch.egg",'pose':'-pose.egg','makeCircle':'-makeCircle.egg',
        'jump':'-jump.egg','wave':
            '-wave.egg'})
        self.dancer.setScale(1,1, 1)
        self.dancer.setPos(0,20,-4)
        self.dancer.reparentTo(self.dance)
        self.accept('arrow_down', self.danceDown)
        self.accept('arrow_right',self.danceRight)
        beats=getBeatFrame(path)
        onsets=getOnSet(path)
        self.heavy,self.lights=self.reduceBeats(beats,onsets)
        self.arrowTime=self.heavy+self.lights
        self.arrowIndexHeavy=0
        self.arrowIndexLight=0
        self.pressed=None
        self.speed=5
        self.arrowInts=[]
        self.startTimes=[]
        self.score=0
        self.miss=0
        self.perfect=0
        self.good=0
        if self.difficultyLevel=='easy':
            self.FULLSCORE=len(self.heavy)
        else:
            self.FULLSCORE=len(self.heavy)+len(self.lights)
        self.createGUI()
        self.startTime = globalClock.getFrameTime()
        self.sound=self.loader.loadSfx(path)
        self.sound.play()
        self.PRESSED,self.NPRESSED,self.PERFECT,self.GOOD,self.MISS=10,-10,2,1,0
        self.mode=self.NPRESSED
        self.perfectBuffer=0.15
        self.goodBuffer=0.25
        self.accept('space',self.stopSound)
        self.taskMgr.add(self.checkStop,'checkStop')
    
    def stopSound(self):
        self.sound.stop()
    
    def calculateScore(self):
        self.score=self.perfect*1.5+self.good
    
    def checkStop(self,task):
        if (self.sound.status()!=AudioSound.PLAYING) and self.selected=='dance':
            self.sound.stop()
            self.selected='gameScore'
            for child in self.dance.getChildren():
                child=None
            self.dance.removeNode()
            self.dance=self.render.attachNewNode(PandaNode('dance'))
            self.scoreCircle.destroy()
            self.hitSign.destroy()
            self.scoreReminder.destroy()
            self.GUIarrows.destroy()
            self.scoreText.destroy()
            self.initGameScore()
            self.gameScore.show()
        return task.cont
    
    
    def setGameScoreBackground(self):
        score=100*float(self.score)/self.FULLSCORE
        if score>=120:
            self.gameScoreBackground = OnscreenImage(parent=render2dp, 
            image='SCORE_S.jpg') 
        elif score>=100:
            self.gameScoreBackground = OnscreenImage(parent=render2dp, 
            image='SCORE_A.jpg') 
        elif score>=80:
            self.gameScoreBackground = OnscreenImage(parent=render2dp, 
            image='SCORE_B.jpg')
        elif score>=60:
            self.gameScoreBackground=OnscreenImage(parent=render2dp, 
            image='SCORE_C.jpg')
        else:
            self.gameScoreBackground=OnscreenImage(parent=render2dp, 
            image='SCORE_F.jpg')
    
    def checkHighScore(self):
        highScore=self.highestScores[self.currSong]
        flag=False
        if self.score > highScore:
            highScore=self.score
            self.highestScores[self.currSong]=highScore
            file=open('musicGameData.txt','r')
            lines=file.readlines()
            newLines=lines
            changeLine=-1
            for num,line in enumerate(lines):
                if line==self.currSong+'\n':
                    print('here')
                    changeLine=num+2
            file.close()
            file=open('musicGameData.txt','w')
            newLines[changeLine]=str(highScore)+'\n'
            for line in newLines:
                file.write(line)
            file.close()
            flag=True
        return highScore,flag
    
    
    def initGameScore(self):
        self.setGameScoreBackground()
        self.cam2dp.node().getDisplayRegion(0).setSort(-20) 
        self.highScoreTuple=self.checkHighScore()
        self.gameScoreText=OnscreenText(
                        text='Total: '+str(self.score),pos=(-0.8,0.7),
                                    scale = 0.2,fg=(1,0.78,0.18,1),mayChange=1)
        self.newHigh=OnscreenText(
                        text='New High!',pos=(-0.7,0.5),
                                    scale = 0.15,fg=(1,1,1,1),mayChange=1)
        if self.highScoreTuple[1]:
            self.newHigh.show()
        else:
            self.newHigh.hide()
        self.scoreFrame=DirectFrame(pos=(0.6,0,-0.6),
                    frameSize = (-0.2,0.6,-0.2,0.2),frameColor=(0,0.1,0.3,1))
        self.perfectLabel=DirectLabel(
                                    text='Perfect: '+str(self.perfect),
                                    pos=(0,0,.1),text_align=TextNode.ALeft,
                                    scale = 0.1,text_fg=(0.28,0.65,858,1),
                                    frameColor=(1,1,1,0),text_scale=(0.9,0.9))
        self.goodLabel=DirectLabel(
                                    text='Good: '+str(self.good),
                                    pos=(0,0,0),
                                    scale = 0.1,text_fg=(0.52,0.67,0.52,1),
                                    text_align=TextNode.ALeft,
                                    frameColor=(1,1,1,0),text_scale=(0.9,0.9))
        self.missLabel=DirectLabel(
                                    text='Miss: '+str(self.miss),
                                    pos=(0,0,-.1),
                                    scale = 0.1,text_fg=(0.72,0.67,0.67,1),
                                    text_align=TextNode.ALeft,
                                    frameColor=(1,1,1,0),text_scale=(0.9,0.9))
        self.perfectLabel.reparentTo(self.scoreFrame)
        self.goodLabel.reparentTo(self.scoreFrame)
        self.missLabel.reparentTo(self.scoreFrame)
        self.retryButton=DirectButton(frameColor=(0,0.1,0.3,1),
                                    pos=(-1,0,-0.5), text="Retry",
                                    text_fg=(1,1,1,1),text_scale=(1,1),
                                    text_align=TextNode.ALeft,
                                   scale=.1, pad=(.2, .2),frameSize=(-1,6.6,-0.6,1),
                                   rolloverSound=None, clickSound=None,
                                   command=self.retry)
        self.mainMenuButton=DirectButton(frameColor=(0,0.1,0.3,1),
                                    pos=(-1,0,-0.7), text="Back To Menu",
                                    text_fg=(1,1,1,1),text_scale=(1,1),text_align=TextNode.ALeft,
                                    text_pos=(-0.5,-0.1),
                                   scale=.1, pad=(.2, .2),frameSize=(-1,6.6,-0.8,0.8),
                                   rolloverSound=None, clickSound=None,
                                   command=self.backToMenu)
    
    def retry(self):
        self.selected='dance'
        self.initDance(self.musicPathes[self.currSong])
        self.gameScore.hide()
        self.gameScoreBackground.hide()
        self.gameScoreText.hide()
        self.scoreFrame.hide()
        self.newHigh.hide()
        self.retryButton.hide()
        self.mainMenuButton.hide()
        self.dance.show()
        self.GUIarrows.show()
        self.scoreText.show()
        self.songList.hide()       
        
    def backToMenu(self):
        self.gameScore.hide()
        self.gameScoreBackground.hide()
        self.gameScoreText.hide()
        self.scoreFrame.hide()
        self.newHigh.hide()
        self.retryButton.hide()
        self.mainMenuButton.hide()
        self.mainMenuBackground.show()
        self.importButton.show()
        self.backToOptionButton.show()
        self.songList.show()
        self.mainMenu.show()
        
                
    def createGUI(self):
        position=self.dancer.getPos()
        position[1]=0
        position[2]=-0.4
        self._2DArrows=[]
        self.scoreCircle=OnscreenImage(image =
        '/Users/jiatiansun/Desktop/15-112/'+
        'tp/deliver3-final/code/arrivalCircle.png', pos = (-1,0,0.8))
        self.scoreCircle.setTransparency(TransparencyAttrib.MAlpha)
        self.scoreCircle.setScale(0.2)
        self.scoreText= OnscreenText(text =str(self.score), pos = (-1.02,0.76), 
                            scale = 0.1,fg=(1,1,1,1))
        self.GUIarrows=DirectFrame(frameColor=(0.3,0.3,0.7,0.3),
                                    frameSize=(-0.8,.8,0.2,-0.2),
                                    pos=position)
        self._2DleftArrow=loader.loadTexture("left_arrow.png")
        self._2DupArrow=loader.loadTexture("up_arrow.png")
        self._2DrightArrow=("right_arrow.png")
        self._2DdownArrow=("down_arrow.png")
        if self.difficultyLevel=='easy':
            self.generate2DArrows(self.heavy,self._2DdownArrow,0)
        else:
            self.generate2DArrows(self.heavy,self._2DdownArrow,0)
            self.generate2DArrows(self.lights,self._2DrightArrow,1)
        self.colorStart=-1
        self.pressedStart=0
        self.taskMgr.add(self.checkInFrame,'checkInFrame')
        self.taskMgr.add(self.checkArrows,'checkArrows')
        self.taskMgr.add(self.checkColorStop,'checkColorStop')
        self.hitSign=OnscreenImage(image =
        'circle.png', pos = (-0.6, 0, -0.4))
        self.hitSign.setTransparency(TransparencyAttrib.MAlpha)
        self.hitSign.setScale(0.15)
        self.scoreReminder=OnscreenText(text ='PERFECT', pos = (-0.6,-0.4), 
                            scale = 0.04,fg=(1,1,1,1),shadow=(0.4,0.4,0.7,0.3))
        self.scoreReminder.hide()
    
    def checkColorStop(self,task):
        if self.selected=='dance':
            endTime=globalClock.getFrameTime()
            time=endTime-self.colorStart
            if (endTime-self.pressedStart)>=0.001:
                self.pressed=None
                self.mode=self.NPRESSED
            if time>=0.2:
                self.hitSign.setImage('circle.png')
                self.hitSign.setTransparency(TransparencyAttrib.MAlpha)
                self.scoreReminder.hide()
            return task.cont
        
    
    def reduceBeats(self,beats,onsets):
        newBeats=set(map(lambda x: int(10*x),beats))
        newOnsets=list(list(map(lambda x: int(10*x),onsets)))
        reducedList=[]
        lights=[]
        for i in range(len(newOnsets)):
            if newOnsets[i] in newBeats:
                reducedList.append(float(newOnsets[i])/10)
                lights.append(float(newOnsets[i])/10)
            else:
                lights.append(float(newOnsets[i])/10)
        
        checkOnsets=map(lambda x: [True,x],lights)
        for i in range(1,len(checkOnsets)-1):
            if (checkOnsets[i][1]-checkOnsets[i-1][1]>0.2 or
                    checkOnsets[i][1]-checkOnsets[i-1][1]>0.2):
                        checkOnsets[i][0]=True
            else:
                checkOnsets[i][0]=False
        groupLights=map(lambda x: x[1],filter(lambda x: not x[0], checkOnsets))
        lights=map(lambda x: x[1],filter(lambda x: x[0], checkOnsets))
        check=set(reducedList)
        for stuff in reversed(lights):
            for time in range(int(stuff*10-2),int(stuff*10+3)):
                if float(time)/10 in check:
                    lights.remove(stuff)
                    break
        return reducedList,lights
        
    def generate2DArrows(self,arrowList,imagePath,num):
        for i in range(len(arrowList)):
            arrow=OnscreenImage(image = imagePath, pos = (0.3, 0, 0))
            arrow.setTransparency(TransparencyAttrib.MAlpha)
            arrow.setScale(0.1)
            x,y,z=-0.6,0,0
            startX,startY,startZ=x+arrowList[i],y,z
            arrow.setPos(startX,startY,startZ)
            arrow.reparentTo(self.GUIarrows)
            arrowInt=arrow.posInterval(arrowList[i],
                                        Point3(-0.6,0,startZ),
                                    startPos=Point3(startX,startY,startZ))
            arrow.hide()
            self.arrowInts.append(arrowInt)
            self._2DArrows.append(arrow)
            startTime = globalClock.getFrameTime()
            self.startTimes.append(startTime)
            arrowInt.start()

    def generateArrows(self,arrowList,arrow):
        for i in range(len(arrowList)):
            self.arrows[i] = copy.deepcopy(arrow)
            self.arrows[i].setScale(0.5)
            x,y,z=self.dancer.getPos()
            startX,startY,startZ=x+self.speed*arrowList[i],y,z
            self.arrows[i].setPos(startX,startY,startZ)
            self.arrows[i].reparentTo(self.self.danceScene)
            arrowInt=self.arrows[i].posInterval(arrowList[i],
                                        Point3(-self.speed,startY,startZ),
                                    startPos=Point3(startX,startY,startZ))
            self.arrowInts.append(arrowInt)
            startTime = globalClock.getFrameTime()
            self.startTimes.append(startTime)
            arrowInt.start()
    
    def checkInFrame(self,task):
        for i in range(len(self._2DArrows)):
            endTime=globalClock.getFrameTime()
            startTime=self.startTimes[i]
            if int((self.arrowTime[i]-(endTime-startTime))*10)<=-1:
                self._2DArrows[i].hide()
            elif int(abs(self.arrowTime[i]-(endTime-startTime))*10)<=12:
                self._2DArrows[i].show()
        return task.cont


    def checkArrows(self,task):
        if self.selected=='dance':
            if self.difficultyLevel=='easy':
                stdTime=self.heavy[self.arrowIndexHeavy]
                startTime=self.startTimes[self.arrowIndexHeavy]
                checkStuff='h'
                endTime=globalClock.getFrameTime()
                time=endTime-startTime
                if (time-stdTime)>self.goodBuffer:
                    self.colorStart=globalClock.getFrameTime()
                    self.mode=self.MISS
                    self.miss+=1
                    self.scoreReminder.setText('MISS')
                    self.changeMissColor()
                    self.arrowIndexHeavy+=1
                elif (self.pressed==checkStuff and 
                                    abs(time-stdTime)<=self.perfectBuffer):
                    self.colorStart=globalClock.getFrameTime()
                    self.mode=self.PERFECT
                    self.perfect+=1
                    self.scoreReminder.setText('PERFECT')
                    self.changePassColor()
                    self.arrowIndexHeavy+=1
                elif (self.pressed==checkStuff and 
                                abs(time-stdTime)<=self.goodBuffer):
                    self.colorStart=globalClock.getFrameTime()
                    self.mode=self.GOOD
                    self.good+=1
                    self.scoreReminder.setText('GOOD')
                    self.changePassColor()
                    self.arrowIndexHeavy+=1
                self.calculateScore()
                self.scoreText['text']=(str(self.score))
            else:
                if (self.arrowIndexHeavy>=len(self.heavy) and self.arrowIndexLight>=
                                len(self.lights)):
                    return
                elif self.arrowIndexHeavy>=len(self.heavy):
                    stdTime=self.lights[self.arrowIndexLight]
                    startTime=self.startTimes[self.arrowIndexLight+len(self.heavy)]
                    checkStuff='l'
                elif self.arrowIndexLight>=len(self.lights):
                    stdTime=self.heavy[self.arrowIndexHeavy]
                    startTime=self.startTimes[self.arrowIndexHeavy]
                    checkStuff='h'
                else:
                    stdTime=self.heavy[self.arrowIndexHeavy]
                    startTime=self.startTimes[self.arrowIndexHeavy]
                    checkStuff='h'
                    if (self.heavy[self.arrowIndexHeavy]>
                                        self.lights[self.arrowIndexLight]):
                        stdTime=self.lights[self.arrowIndexLight]
                        startTime=(
                            self.startTimes[self.arrowIndexLight+len(self.heavy)])
                        checkStuff='l'
                endTime=globalClock.getFrameTime()
                time=endTime-startTime
                if (time-stdTime)>self.goodBuffer:
                    self.colorStart=globalClock.getFrameTime()
                    self.mode=self.MISS
                    self.miss+=1
                    self.scoreReminder.setText('MISS')
                    self.changeMissColor()
                    if checkStuff=='h':
                        self.arrowIndexHeavy+=1
                    else:
                        self.arrowIndexLight+=1
                elif (self.pressed==checkStuff and 
                                    abs(time-stdTime)<=self.perfectBuffer):
                    self.colorStart=globalClock.getFrameTime()
                    self.mode=self.PERFECT
                    self.perfect+=1
                    self.scoreReminder.setText('PERFECT')
                    self.changePassColor()
                    if checkStuff=='h':
                        self.arrowIndexHeavy+=1
                    else:
                        self.arrowIndexLight+=1
                elif (self.pressed==checkStuff and 
                                abs(time-stdTime)<=self.goodBuffer):
                    self.colorStart=globalClock.getFrameTime()
                    self.mode=self.GOOD
                    self.good+=1
                    self.scoreReminder.setText('GOOD')
                    self.changePassColor()
                    if checkStuff=='h':
                        self.arrowIndexHeavy+=1
                    else:
                        self.arrowIndexLight+=1
                self.calculateScore()
                self.scoreText['text']=(str(self.score))
            return task.cont

    def danceDown(self):
        if self.selected=='dance':
            self.pressed='h'
            self.pressedStart=globalClock.getFrameTime()
            if self.pressed==self.MISS:
                self.dancer.stop()
            else:
                self.dancer.play(self.animationDown[self.playIndex])
                self.playIndex+=1
                if self.playIndex>=5:
                    self.playIndex=self.playIndex%5
        
    def changePassColor(self):
        if self.selected=='dance':
            LerpColorInterval(
                self.hitSign,0.2,color=(0,0,1,0), startColor=(0,0,1,1)).start()
            self.scoreReminder.show()
            LerpColorInterval(
                self.scoreReminder,0.2,color=(0.4,0.4,0.7,0), 
                        startColor=(0.4,0.4,0.7,1)).start()
    
    def changeMissColor(self):
        if self.selected=='dance':
            LerpColorInterval(
            self.hitSign,0.2,color=(1,0,0,0), startColor=(1,0,0,1)).start()
            self.scoreReminder.show()
            LerpColorInterval(self.scoreReminder,0.2,color=(0.4,0.4,0.7,0), startColor=(0.4,0.4,0.7,1)).start()
    
    def danceRight(self):
        if self.selected=='dance':
            self.pressed='l'
            self.pressedStart=globalClock.getFrameTime()
            if self.pressed==self.MISS:
                self.dancer.stop()
            else:
                self.dancer.play(self.animationRight[self.playIndex])
                self.playIndex+=1
                if self.playIndex>=5:
                    self.playIndex=self.playIndex%5

    def spinCam(self,task):
        if self.selected=='mainMenu':
            self.camera.setPos(0, 0, 3)
            self.camera.setHpr(0, -5, 0)
        elif self.selected=='dance':
            time=task.time
            # THIS IS REALLY SIMILAR TO THE SAMPLE OF PANDA3D
            x,y,z=self.dancer.getPos()
            angleDegrees = task.time* 6.0
            angleRadians = angleDegrees * (pi / 180.0)
            self.camera.setPos(x+20 * sin(angleRadians), y+-20.0 * cos(angleRadians), 0)
            self.camera.setHpr(angleDegrees, -5, 0)
            #END POINT OF SIMILARITY
        return Task.cont

musicGame().run()


        
