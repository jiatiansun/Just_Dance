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
import os.path
from util import *
from panel import *
import musicGameCore

'''
This is the GUI of the JustDance music rythm game using
Panda3D engine
Author: Jiatian SUn
'''
class JustDanceGUI(ShowBase):
    def __init__(self):
        # Basic initialization of panda3D engine
        ShowBase.__init__(self)

        self.songButtonList=[]
        self.createDefaultMusicList()
        self.loadMusicScores()

        self.difficultyLevel='easy'

        self.configureGUIPanels()
        self.displayPanel('options')

        self.BGM=base.loader.loadSfx("../music/Nyte - Lone Walker.mp3")
        self.BGM.play()


    # create a local file that stores local music paths and scores
    @staticmethod
    def createDefaultMusicList():
        # check if the file is created
        if os.path.isfile('musicGameData.txt'):
            print('here')
            file=open('musicGameData.txt','r')
        else:
            file=open('musicGameData.txt','w')
            file.write('Rather Be\n')
            file.write('../music/Clean Bandit,Jess Glynne-Rather '+
        'Be (Robin Schulz Edit).mp3\n')
            file.write('0\n')
            file.write('Memory\n')
            file.write('../music/Elaine Paige-Memory.mp3\n')
            file.write('0\n')

    # Load history of music scores 
    def loadMusicScores(self):
        file=open('musicGameData.txt','r')
        self.data=file.readlines()
        self.highestScores=dict()
        self.musicNames=[]
        self.musicPathes=dict()

        dataList=[]
        for line in self.data:
            dataList.append(line.strip())
        for i in range(0,len(dataList),3):
            self.musicNames.append(dataList[i])
            self.musicPathes[dataList[i]]=dataList[i+1]
            self.highestScores[dataList[i]]=float(dataList[i+2])

    # configure all GUI panels
    def configureGUIPanels(self):
        self.setBackgroundColor((0, 0, 0, 1))
        self.panels = dict()
        self.cam2dp.node().getDisplayRegion(0).setSort(-20)
        self.configureStartMenu()
        self.configureMainMenu()
        self.configureScoreBoard()
        self.configureSetting()
        self.configureDance()
        self.configureImportMenu()

    # the function displays a single panel and hides
    # all other panels
    def displayPanel(self, displayPanel):
        for panel in self.panels:
            if(panel == displayPanel):
                self.panels[panel].show()
            else:
                self.panels[panel].hide()

    def getPanel(self,panelName):
        return self.panels[panelName]

    def setPanel(self,panelName,panel):
        self.panels[panelName] = panel
        return

    # swich from displaying one panel to displaying the other panel
    def switchPanel(self,oldP,newP):
        self.panels[oldP].hide()
        self.panels[newP].show()

    # get activities from the keybboard
    def getEvent(self):
        return self.pressed

    # configure the start menu
    def configureStartMenu(self):
        optionBackground = OnscreenImage(parent=render2dp, image=
        '../textures/MENU_ORG_text.jpg') 

        settingButton = DirectButton(pos=(0.1, 0, 0), text=" Setting",
                                   scale=.08, pad=(.2, .2), frameColor=(0.02,0.3,0.5,0.4),
                                   text_fg=(0,0.4,0.7,1),
                                   text_align=TextNode.ALeft,frameSize=(-4.3,4,-0.6,1),
                                   text_pos=(-1,0,0),
                                   rolloverSound=None, clickSound=None,
                                   command=lambda:self.switchPanel('options','setting'))
        settingButton.resetFrameSize()
        playButton = DirectButton(pos=(0.1, 0, .15), text="Start",
                                   scale=.08, pad=(.2, .2),frameColor=(0.02,0.3,0.5,0.4),
                                   text_fg=(0.1,0.4,0.7,1),
                                   text_align=TextNode.ALeft,
                                   frameSize=(-3,4,-0.6,1),
                                   rolloverSound=None, clickSound=None,
                                   command=lambda: self.switchPanel('options','mainMenu'))
        scoreBoardButton= DirectButton(pos=(0, 0, -.15), text="HighScore",
                                   scale=.08, pad=(.2, .2),frameColor=(0.02,0.3,0.5,0.4),
                                   text_pos=(-1,0,0),
                                   text_fg=(0.1,0.4,0.7,1),text_align=TextNode.ALeft,frameSize=(-5,5.3,-0.6,1),
                                   rolloverSound=None, clickSound=None,
                                   command=lambda: self.switchPanel('options','scoreBoard'))

        optionsList=DirectFrame(frameSize=(-0.3,0.3,-0.2,0.2),pos=(0.8,0,-0.5),frameColor=(0,0,0,0))
        settingButton.reparentTo(optionsList)
        playButton.reparentTo(optionsList)
        scoreBoardButton.reparentTo(optionsList)

        self.setPanel('options', Panel(optionBackground, {'optionList': optionsList}))
        
    # configure the main menu (music list page)
    def configureMainMenu(self):
        self.mainMenuBackground = OnscreenImage(parent=render2dp, 
                            image='../textures/BGM_ORG_text.jpg') 
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
        importButton=DirectButton(pos=(0,0,-0.6),text='+ IMPORT NEW MUSIC ',
                                    scale=0.1,pad=(.2,.2),frameColor=(0.058,.294,0.545,0.7),
                                    text_fg=(0.88,0.98,1,1),frameSize=(-6.5,6.5,-0.8,0.8),
                                    text_scale=(0.85,0.85),
                                    text_pos=(0.5,-0.4),rolloverSound=None, clickSound=None,
                                   command= lambda: self.switchPanel('mainMenu','import'))
        backToOptionButton=DirectButton(text='<<BACK TO MENU',
                                    pos=(-1,0,0.8),scale=.1,pad=(.2, .2),
                                    frameColor=(1,1,1,0),
                                    text_pos=(1.3,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),
                                   rolloverSound=None, clickSound=None,
                                   command=lambda: self.switchPanel('mainMenu','options'))

        self.setPanel('mainMenu', Panel(self.mainMenuBackground,
                                        {'songs': self.songList,
                                        'import': importButton,
                                        'back': backToOptionButton}))
        self.disableMouse()

    # configure the import menu
    def configureImportMenu(self):
        importBackground= OnscreenImage(parent=render2dp, 
        image='../textures/BGM_ORG.jpg') 
        newNameBox = DirectEntry(text = "" ,pos=(-0.4,0,0.5),scale=.08,
                                        frameColor=(1,1,1,0.3),initialText="", 
                                                numLines = 3,focus=1) 
        newPathBox = DirectEntry(text = "" ,pos=(-0.4,0,0.2),
                                            frameColor=(1,1,1,0.3),
                scale=.08,
                initialText="", numLines = 5,focus=1)
        confirmationButton=DirectButton(text='IMPORT',pos=(0, 0, -0.3),
                                   scale=.1, pad=(.2, .2),
                                    frameColor=(0.058,.294,0.545,0.7),
                                    text_pos=(0,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),
                                    frameSize=(-6.5,6.5,-0.8,0.8),
                                   rolloverSound=None, clickSound=None,
                                   command=self.importNewSong)
        backToOptionButton=DirectButton(text='<<BACK TO MUSIC LIST',
                                    pos=(-1,0,0.8),scale=.1,pad=(.2, .2),
                                    frameColor=(1,1,1,0),
                                    text_pos=(1.3,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),
                                   rolloverSound=None, clickSound=None,
                                   command=lambda: self.switchPanel('import','mainMenu'))
        self.setPanel('import',Panel(importBackground, {'newName': newNameBox,
                        'newPath': newPathBox,'confirmButton': confirmationButton,
                        'back':backToOptionButton}))
    
    # function that loads new music from the import page
    def importNewSong(self):
        songName = self.getPanel('import').getItem('newName')
        songPath = self.getPanel('import').getItem('newPath')

        self.musicPathes[songName.get()] = songPath.get()
        self.musicNames.append(songName.get())
        file=open('musicGameData.txt','a')
        file.write(songName.get()+'\n')
        file.write(songPath.get()+'\n')
        file.write('0\n')
        self.updateSongs()
        songName.enterText("")
        songPath.enterText("")
        self.switchPanel('import','mainMenu')
    
    # update songs in the list
    def updateSongs(self):
        name = self.musicNames[-1]
        path=self.musicPathes[name]
        idx = len(self.musicNames)-1
        song = DirectButton(text=name,
                                    pos=(0, 0,0.9-0.15*idx),
                                   scale=.1, pad=(.2, .2),
                                    frameColor=(0.058,.294,0.545,0.7),
                                    text_pos=(1.3,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),
                                    frameSize=(-4,6,-0.7,0.7),
                                   rolloverSound=None, clickSound=None,
                                   command=self.preInitDance,extraArgs=
                                    (-1,))
        self.highestScores[name]=0
        song.reparentTo(self.songList.getCanvas())

        scoreLabel=DirectButton(frameSize=(-0.3,0.3,-0.2,.2),pos=(0,0,0-idx*0.2),
            text='%s:  %d'%(name,self.highestScores[name]),
            text_align=TextNode.ALeft,text_scale=0.08,frameColor=(0,0,0,0),
            text_fg=(1,1,1,1))
        scoreLabel.reparentTo(self.getPanel('scoreBoard').getItem('frame').getCanvas())
        
    # function that configures the setting panel
    def configureSetting(self):
        self.settingBackground = OnscreenImage(parent=render2dp, image='../textures/SET_ORG.jpg') 

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
                                   command=lambda: self.switchPanel('setting', 'options'))

        self.panels['setting'] = Panel(self.settingBackground,
                                        {'level': self.difficulty,
                                          'change': self.setDifficultyButton,
                                          'back': self.backToOptionButton3})

    # function that helps create the dance
    def preInitDance(self,index):
        self.currSong=self.musicNames[index]
        self.createDance(self.musicPathes[self.musicNames[index]])
        self.switchPanel('mainMenu','dance')
    
    # switch difficult level of the game
    def changeDifficulty(self):
        if self.difficultyLevel=='hard':
            self.difficultyLevel='easy'
            self.setDifficultyButton['text']='easy'
        else:
            self.difficultyLevel='hard'
            self.setDifficultyButton['text']='hard'

    def createHighScoreFrame(self):
        highScoreFrame=DirectScrolledFrame(frameColor=(0.5,0.5,1,0),
                                        canvasSize = (-0.3,0.2,-2,1), 
                            frameSize = (-0.3,1.1,-0.8,0.3),pos=(0.2,0,0.2))

        highScoreFrame['verticalScroll_thumb_frameColor']=(1,1,1,0.3)
        highScoreFrame['verticalScroll_incButton_frameColor']=(1,1,1,0)
        highScoreFrame['verticalScroll_decButton_frameColor']=(1,1,1,0)
        highScoreFrame['verticalScroll_frameColor']=(0.5,0.5,1,0)

        highScoreTitle1=DirectLabel(frameSize=(-0.6,0.6,-0.2,.2),pos=(0,0,0.9),
            text='Music',frameColor=(0,0,0,0),
            text_align=TextNode.ALeft,text_scale=0.08,text_fg=(1,1,1,1))
        highScoreTitle2=DirectLabel(frameSize=(-0.6,0.6,-0.6,.6),pos=(0.4,0,0.9),
            text='Highest Score',text_fg=(1,1,1,1),frameColor=(0,0,0,0),
            text_align=TextNode.ALeft,text_scale=0.08)

        highScoreTitle1.reparentTo(highScoreFrame.getCanvas())
        highScoreTitle2.reparentTo(highScoreFrame.getCanvas())

        for i in range(len(self.musicNames)):
            scoreLabel=DirectButton(frameSize=(-0.3,0.3,-0.2,.2),pos=(0,0,0.7-i*0.2),
            text='%s:  %d'%(self.musicNames[i],self.highestScores[self.musicNames[i]]),
            text_align=TextNode.ALeft,text_scale=0.08,frameColor=(0,0,0,0),
            text_fg=(1,1,1,1))
            scoreLabel.reparentTo(highScoreFrame.getCanvas())
        return highScoreFrame

    
    # configure the high score board
    def configureScoreBoard(self):
        scoreBoardBackground=OnscreenImage(parent=render2dp, 
            image='../textures/HIGH_ORG_text.jpg')

        highScoreFrame =  self.createHighScoreFrame()
        # for i in range(len(self.musicNames)):
        #     scoreLabel=DirectButton(frameSize=(-0.3,0.3,-0.2,.2),pos=(0,0,0.7-i*0.2),
        #     text='%s:  %d'%(self.musicNames[i],self.highestScores[self.musicNames[i]]),
        #     text_align=TextNode.ALeft,text_scale=0.08,frameColor=(0,0,0,0),
        #     text_fg=(1,1,1,1))
        #     scoreLabel.reparentTo(self.highScoreFrame.getCanvas())

        backToOptionButton2=DirectButton(text='<<BACK TO MENU',
                                    pos=(-1,0,0.8),scale=.1,pad=(.2, .2),
                                    frameColor=(1,1,1,0),
                                    text_pos=(1.3,-0.3),text_scale=(0.8,0.8),
                                    text_fg=(0.88,0.98,1,1),
                                   rolloverSound=None, clickSound=None,
                                   command=lambda: self.switchPanel('scoreBoard','options'))

        self.panels['scoreBoard'] = Panel(scoreBoardBackground,
                                    {'frame':highScoreFrame,'back':backToOptionButton2})

    # configure the dance scene
    def configureDance(self):
        self.PRESSED,self.NPRESSED,self.PERFECT,self.GOOD,self.MISS=10,-10,2,1,0
        danceNode = self.render.attachNewNode(PandaNode('dance'))

        # load and set up scene
        danceScene = self.loader.loadModel("../models/disco_hall")
        danceScene.reparentTo(danceNode)
        danceScene.setPosHpr(0, 50, -4, 90, 0, 0)

        self.configureLights(danceNode)
        self.configureDancer(danceNode)

        scoreCircle=OnscreenImage(
                        image = '../textures/arrivalCircle.png', pos = (-1,0,0.8))
        scoreCircle.setTransparency(TransparencyAttrib.MAlpha)
        scoreCircle.setScale(0.2)
        scoreText= OnscreenText(text =str(0), pos = (-1.02,0.76), 
                            scale = 0.1,fg=(1,1,1,1))

        position=self.dancer.getPos()
        position[1]=0
        position[2]=-0.4
        GUIarrows=DirectFrame(frameColor=(0.3,0.3,0.7,0.3),
                                    frameSize=(-0.8,.8,0.2,-0.2),
                                    pos=position)

        hitSign=OnscreenImage(image ='../textures/circle.png', pos = (-0.6, 0, -0.4))
        hitSign.setTransparency(TransparencyAttrib.MAlpha)
        hitSign.setScale(0.15)
        scoreReminder=OnscreenText(text ='PERFECT', pos = (-0.6,-0.4), 
                            scale = 0.04,fg=(1,1,1,1),shadow=(0.4,0.4,0.7,0.3))

        self.setPanel('dance',Panel(danceNode, {'scoreCircle': scoreCircle,
            'GUIarrows':GUIarrows,'hitSign': hitSign,'scoreText': scoreText,
            'scoreReminder': scoreReminder}))

    # configure lights in the scene
    def configureLights(self, danceNode):
        # set up ambient light
        ambientLight = danceNode.attachNewNode(AmbientLight("ambientLight"))
        ambientLight.node().setColor((0.1, 0.1, 0.1, 1))

        # set up directional light directional Light
        directionalLight = danceNode.attachNewNode(DirectionalLight("directionalLight"))
        directionalLight.node().setColor((.1, .1, .1, 1))
        directionalLight.node().setDirection(LVector3(1, 1, -2))
        directionalLight.setZ(6)

        dlens = directionalLight.node().getLens()
        dlens.setFilmSize(41, 21)
        dlens.setNearFar(50, 75)

        # set up spotlight
        spotlight = self.camera.attachNewNode(Spotlight("spotlight"))
        spotlight.node().setColor((.6, .6, .6, 0))
        spotlight.node().setSpecularColor((0, 0, 0, 1))
        spotlight.node().setLens(PerspectiveLens())
        spotlight.node().getLens().setFov(24, 24)
        spotlight.node().setAttenuation(LVector3(0.6, 0.0, 0.0))
        spotlight.node().setExponent(60.0)

        # set up red light ball
        redBall = loader.loadModel('../models/sphere')
        redBall.setColor((0.2, 0.2, .35, 1))
        redBall.setPos(-6.5, -3.75, 0)
        redBall.setScale(.25)
        redPointLight = redBall.attachNewNode(PointLight("redPointLight"))
        redPointLight.node().setColor((.05, .3,.4, 1))
        redPointLight.node().setAttenuation(LVector3(.1, 0.04, 0.0))

        # set up green light ball
        greenBall = loader.loadModel('../models/sphere')
        greenBall.setColor((0.2, 0.2, .35, 1))
        greenBall.setPos(0, 7.5, 0)
        greenBall.setScale(.25)
        greenPointLight = greenBall.attachNewNode(
                                    PointLight("greenPointLight"))
        greenPointLight.node().setAttenuation(LVector3(.1, .04, .0))
        greenPointLight.node().setColor((.05, .3, .4, 1))

        # set up blue light ball
        blueBall = loader.loadModel('../models/sphere')
        blueBall.setColor((0.2, 0.2, .35, 1))
        blueBall.setPos(6.5, -3.75, 0)
        blueBall.setScale(.25)
        bluePointLight = blueBall.attachNewNode(PointLight("bluePointLight"))
        bluePointLight.node().setAttenuation(LVector3(.1, 0.04, 0.0))
        bluePointLight.node().setColor((.1, .1, .4, 1))
        bluePointLight.node().setSpecularColor((1, 1, 1, 1))


        # set up light group
        lightGroup = danceNode.attachNewNode("pointLightHelper")
        lightGroup.setPos(0, 50, 11)
        redBall.reparentTo(lightGroup)
        greenBall.reparentTo(lightGroup)
        blueBall.reparentTo(lightGroup)
        danceNode.setLight(ambientLight)
        danceNode.setLight(directionalLight)
        danceNode.setLight(spotlight)
        danceNode.setLight(redPointLight)
        danceNode.setLight(greenPointLight)
        danceNode.setLight(bluePointLight)

        # spin three light balls in the scene
        pointLightsSpin = lightGroup.hprInterval(6, LVector3(360, 0, 0))
        pointLightsSpin.loop()

    # configure the dancing avatar in the scene
    def configureDancer(self,danceNode):
        self.dancer = Actor("../animation/dancer.egg",{"pressKnee": 
        '../animation/-pressKnee.egg',
        'leapSwitch': "../animation/-leapSwitch.egg",
        'pose':'../animation/-pose.egg',
        'makeCircle':'../animation/-makeCircle.egg',
        'jump':'../animation/-jump.egg',
        'wave': '../animation/-wave.egg'})
        self.dancer.setScale(1,1, 1)
        self.dancer.setPos(0,20,-4)
        self.dancer.reparentTo(danceNode)

        self.actionIndex=0
        self.animationDown=['pose','makeCircle','pose','makeCircle','pressKnee']
        self.animationRight=['jump','jump','wave','wave','leapSwitch']

    # create the dance sequence according to the 
    def createDance(self,path):
        self.game = musicGameCore.DanceGame(self, path,self.difficultyLevel)
        self.FULLSCORE, self.arrows = self.game.processMusic()
        self.accept('arrow_down', lambda: self.pressKey('h'))
        self.accept('arrow_right',lambda: self.pressKey('l'))
        self.createArrows()
        self.getPanel('dance').getItem('scoreText').setText('0') 

        self.sound=self.loader.loadSfx(path)
        self.BGM.stop()
        self.mode = self.NPRESSED

        self.sound.play()
        self.game.startDance(globalClock.getFrameTime())
        self.move2DArrows()
        self.colorStart=-1
        self.pressedStart=0
        self.taskMgr.add(self.checkInFrame,'checkInFrame')
        self.taskMgr.add(self.game.isArrowMissed,'checkArrows')
        self.taskMgr.add(self.checkColorStop,'checkColorStop')
        self.taskMgr.add(self.spinCam,'spinCam')
        
        self.accept('space',self.stopSound)
        self.taskMgr.add(self.checkStop,'checkStop')

    # load texture and create arrows
    def createArrows(self):
        self._2DleftArrow="../textures/left_arrow.png"
        self._2DupArrow="../textures/up_arrow.png"
        self._2DrightArrow=("../textures/right_arrow.png")
        self._2DdownArrow=("../textures/down_arrow.png")
        self.generate2DArrows(self.arrows)
        
    # generate a sequence of arrows to be displayed on screen
    def generate2DArrows(self,arrowList):
        self.movingArrows =[None] * self.FULLSCORE
        for i in range(len(arrowList)):
            imagePath = self._2DdownArrow
            if(arrowList[i].type == 'l'):
                imagePath = self._2DrightArrow
            arrow=OnscreenImage(image = imagePath, pos = (0.3, 0, 0))
            arrow.setTransparency(TransparencyAttrib.MAlpha)
            arrow.setScale(0.1)
            x,y,z=-0.6,0,0
            startX,startY,startZ=x+arrowList[i].getExpectedTime(),y,z
            arrow.setPos(startX,startY,startZ)
            arrow.reparentTo(self.getPanel('dance').getItem('GUIarrows'))
            arrow.hide()
            self.movingArrows[i] = arrow

    # let a sequence of arrows to move
    def move2DArrows(self):
        musicStartTime = self.game.getStartTime() 
        for i in range(self.FULLSCORE):
            arrow = self.movingArrows[i]
            actualDuration =  musicStartTime + self.arrows[i].getExpectedTime() - globalClock.getFrameTime() 
            x,y,z=-0.6,0,0
            startX,startY,startZ=x+self.arrows[i].getExpectedTime(),y,z
            animation=arrow.posInterval( actualDuration, Point3(-0.6,0,startZ),
                                        startPos=Point3(startX,startY,startZ))
            animation.start()

    # function that stops the whole dance
    def stopSound(self):
        self.sound.stop()
    
    # check if the dance game ends
    def checkStop(self,task):
        if (self.sound.status()!=AudioSound.PLAYING):
            position=self.dancer.getPos()
            position[1]=0
            position[2]=-0.4
            self.getPanel('dance').getItem('GUIarrows').destroy()
            self.getPanel('dance').setItem('GUIarrows',
                                    DirectFrame(frameColor=(0.3,0.3,0.7,0.3),
                                    frameSize=(-0.8,.8,0.2,-0.2),
                                    pos=position))
            self.taskMgr.remove('checkInFrame')
            self.taskMgr.remove('checkArrows')
            self.taskMgr.remove('checkColorStop')
            self.taskMgr.remove('checkStop')
            self.taskMgr.remove('spinCam')
            self.initGameScore()
            self.BGM.play()

        return task.cont     
    
    # show all the arrows in displaying frame
    def checkInFrame(self,task):
        for i in range(len(self.movingArrows)):
            endTime=globalClock.getFrameTime()
            startTime = self.game.getStartTime()
            if int((self.arrows[i].getExpectedTime()-(endTime-startTime))*10)<=-1:
                self.movingArrows[i].hide()
            elif int(abs(self.arrows[i].getExpectedTime()-(endTime-startTime))*10)<=12:
                self.movingArrows[i].show()
        return task.cont

    # check if the effect of shining circle should stop
    def checkColorStop(self,task):
        endTime=globalClock.getFrameTime()
        time=endTime-self.colorStart
        if (endTime-self.pressedStart)>=0.001:
            self.pressed=None
            self.mode=self.NPRESSED
        if time>=0.2:
            hitSign = self.getPanel('dance').getItem('hitSign')
            scoreReminder = self.getPanel('dance').getItem('scoreReminder')
            hitSign.setImage('../textures/circle.png')
            hitSign.setTransparency(TransparencyAttrib.MAlpha)
            scoreReminder.hide()
        return task.cont

    #  spin the camera
    def spinCam(self,task):
        time=task.time
        # THIS IS REALLY SIMILAR TO THE SAMPLE OF PANDA3D
        x,y,z=self.dancer.getPos()
        angleDegrees = task.time* 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(x+20 * sin(angleRadians), y+-20.0 * cos(angleRadians), 0)
        self.camera.setHpr(angleDegrees, -5, 0)
        #END POINT OF SIMILARITY
        return Task.cont

    # function to be called after pressing key
    def pressKey(self, key):
        self.pressed=key
        self.pressedStart=globalClock.getFrameTime()
        self.game.keyPressed(key)
        
    # function that let the any icon to disappear
    def iconDisappear(self, icon, effectColor):
        LerpColorInterval(icon,0.2,color=(effectColor[0],effectColor[1],effectColor[2],0), 
                        startColor= (effectColor[0],effectColor[1],effectColor[2],1)).start()

    # the effect should display after some arrow events happen
    def pressEffect(self, type, idx):
        self.colorStart=globalClock.getFrameTime()
        self.getPanel('dance').getItem('scoreReminder').setText(type)
        if(type == 'MISS'):
            self.blinkColor((1,0,0))
            self.mode = self.MISS
            if(idx != -1):
                self.iconDisappear(self.movingArrows[idx],(0.8,0.8,1))
        elif(type == 'GOOD'):
            self.blinkColor((0,0,1))
            self.mode = self.GOOD
        elif(type == 'PERFECT'):
            self.blinkColor((0,0,1))
            self.mode = self.PERFECT
        if self.mode == self.GOOD or self.mode == self.PERFECT:
            self.dancer.play(self.animationDown[self.actionIndex])
            self.actionIndex+=1
            if self.actionIndex>=5:
                self.actionIndex=self.actionIndex%5
        elif self.mode == self.MISS:
            self.dancer.stop()

    # let the stop circle blinks speficied light
    def blinkColor(self, effectColor):
        hitSign = self.getPanel('dance').getItem('hitSign')
        self.iconDisappear(hitSign,effectColor)
        scoreReminder = self.getPanel('dance').getItem('scoreReminder')
        scoreReminder.show()
        self.iconDisappear(scoreReminder, (0.4,0.4,0.7))
        self.colorStart = globalClock.getFrameTime()

    # let the game score 
    def initGameScore(self):
        score,miss,good,perfect = self.game.getScoreReport()
        self.setGameScoreBackground(score)
        self.highScoreTuple=self.updateHighestScore(score)
        self.gameScoreText=OnscreenText(
                        text='Total: '+str(score),pos=(-0.8,0.7),
                                    scale = 0.2,fg=(1,0.78,0.18,1),mayChange=1)
        self.newHigh=OnscreenText(
                        text='New High!',pos=(-0.7,0.5),
                                    scale = 0.15,fg=(1,1,1,1),mayChange=1)
        self.scoreFrame=DirectFrame(pos=(0.6,0,-0.6),
                    frameSize = (-0.2,0.6,-0.2,0.2),frameColor=(0,0.1,0.3,1))
        self.perfectLabel=DirectLabel(
                                    text='Perfect: '+str(perfect),
                                    pos=(0,0,.1),text_align=TextNode.ALeft,
                                    scale = 0.1,text_fg=(0.28,0.65,858,1),
                                    frameColor=(1,1,1,0),text_scale=(0.9,0.9))
        self.goodLabel=DirectLabel(
                                    text='Good: '+str(good),
                                    pos=(0,0,0),
                                    scale = 0.1,text_fg=(0.52,0.67,0.52,1),
                                    text_align=TextNode.ALeft,
                                    frameColor=(1,1,1,0),text_scale=(0.9,0.9))
        self.missLabel=DirectLabel(
                                    text='Miss: '+str(miss),
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
                                   command=lambda: self.switchPanel('gameScore','mainMenu'))
        self.setPanel('gameScore',Panel(self.gameScoreBackground,{'scoreText':self.gameScoreText, 'newHigh':self.newHigh,
            'scoreFrame':self.scoreFrame,'retry':self.retryButton,'mainMenu':self.mainMenuButton}))
        self.switchPanel('dance','gameScore')
        if self.highScoreTuple[1]:
            self.newHigh.show()
        else:
            self.newHigh.hide()

    # display different backgrounds for different scores
    def setGameScoreBackground(self, score):
        score=100*float(score)/self.FULLSCORE
        if score>=120:
            self.gameScoreBackground = OnscreenImage(parent=render2dp, 
            image='../textures/SCORE_S.jpg') 
        elif score>=100:
            self.gameScoreBackground = OnscreenImage(parent=render2dp, 
            image='../textures/SCORE_A.jpg') 
        elif score>=80:
            self.gameScoreBackground = OnscreenImage(parent=render2dp, 
            image='../textures/SCORE_B.jpg')
        elif score>=60:
            self.gameScoreBackground=OnscreenImage(parent=render2dp, 
            image='../textures/SCORE_C.jpg')
        else:
            self.gameScoreBackground=OnscreenImage(parent=render2dp, 
            image='../textures/SCORE_F.jpg')
    
    # compare the score to the highest score of the music
    def updateHighestScore(self,score):
        highScore=self.highestScores[self.currSong]
        flag=False
        if score > highScore:
            highScore=score
            self.highestScores[self.currSong]=highScore
            oldFrame = self.getPanel('scoreBoard').getItem('frame')
            newFrame = self.createHighScoreFrame()
            self.getPanel('scoreBoard').setItem('frame',newFrame)
            newFrame.hide()
            oldFrame.destroy()
            file=open('musicGameData.txt','r')
            lines=file.readlines()
            newLines=lines
            changeLine=-1
            for num,line in enumerate(lines):
                if line==self.currSong+'\n':
                    changeLine=num+2
            file.close()
            file=open('musicGameData.txt','w')
            newLines[changeLine]=str(highScore)+'\n'
            for line in newLines:
                file.write(line)
            file.close()
            flag=True
        return highScore,flag

    # function called to restart the dance
    def retry(self):
        self.createDance(self.musicPathes[self.currSong])
        self.switchPanel('gameScore','dance') 

JustDanceGUI().run()


        
