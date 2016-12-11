from aubio import source,tempo,onset,pitch
#from pysoundcard import Stream
import sys
from Tkinter import *
from time import *
import math

#referencing demo code of aubio and course note barebone animation
#includes demo_onset, demo_pitch, demo_tempo, demo_pysoundcard_play, 
#simple script from aubio documentation
#citing almostEqual and roundHalfUp from course note
import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def init(data):
    data.BOhopSize = 256 
    data.PhopSize=512
    data.endTime=0
    data.sourceB=createSource(data,data.BOhopSize)
    data.FRAMEB=1/data.sourceB.samplerate
    #print(data.FRAME)
    data.stuffs=list(map(lambda x: roundHalfUp(1000*x*data.FRAMEB), 
                                                            getOnSet()))
    data.sourceP=createSource(data,data.PhopSize)
    data.FRAMEP=1/data.sourceP.samplerate
    data.pitches=getPitch()
   # print(data.stuffs)
    data.initTime=clock()
    data.time=0
    data.buffer=60
    data.arrow=False
    data.R=30
    data.r=data.R
    data.mode='play'


def getBeatFrame(path):#cite
    #referencing demo
    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size
    samplerate = 0
    filename = path
    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("default", win_s, hop_s, samplerate)
    
    # tempo detection delay, in samples
    # default to 4 blocks delay to catch up with
    delay = 4. * hop_s
    
    # list of beats, in samples
    beats = []
    
    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = roundHalfUp(total_frames - delay + is_beat[0] * hop_s)
            beats.append(this_beat)
        total_frames += read
        if read < hop_s: break
    return list(map(lambda x: float(x)/samplerate, beats))# end


def getOnSet(path):#cite
    #referencing demo
    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size
    samplerate=0
    filename = path
    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate
    o = onset("default", win_s, hop_s, samplerate)
    delay = 4. * hop_s
    onsets = []
    total_frames = 0
    while True:
        samples, read = s()
        is_onset = o(samples)
        if is_onset:
            this_onset =roundHalfUp(total_frames - delay + is_onset[0] * hop_s)
            onsets.append(this_onset)
        total_frames += read
        if read < hop_s: break#end
    return list(map(lambda x: float(x)/samplerate, onsets))

def getPitch():#cite from the sample
    if len(sys.argv) < 2:
        print("Usage: %s <filename> [samplerate]" % sys.argv[0])
        sys.exit(1)
    
    filename = sys.argv[1]
    
    downsample = 1
    samplerate = 44100 // downsample
    if len( sys.argv ) > 2: samplerate = roundHalfUp(sys.argv[2])
    
    win_s = 4096 // downsample # fft size
    hop_s = 512  // downsample # hop size
    
    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate
    
    tolerance = 0.8
    
    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)
    
    pitches = dict()
    confidences = []
    time=[]
    
    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        currPitch = pitch_o(samples)[0]
        #pitch = roundHalfUp(round(pitch))
        confidence = pitch_o.get_confidence()
        #if confidence < 0.8: pitch = 0.
        pitches[roundHalfUp(1000*total_frames/float(samplerate))]=currPitch
        confidences += [confidence]
        #time+=[total_frames / float(samplerate)]
        total_frames += read
        if read < hop_s: break
    
    return pitches# end

def isContinuousPitch(data):
    formerTime=data.time-1
    currTimeInterval=range(data.time-roundHalfUp
                                    (data.PhopSize*data.FRAMEP*1000),data.time)
    #formerTimeInterval=range(data.time-2*roundHalfUp(
    # data.Phopsize*data.FRAMEP*1000),data.time-roundHalfUp
    #(data.Phopsize*data.FRAMEP*1000))
    for currTime in currTimeInterval:
        if currTime in data.pitches:
            formerTime=currTime-roundHalfUp(data.PhopSize*data.FRAMEP*1000)
            for formerT in [formerTime,formerTime-1,formerTime+1]:
                if formerT in data.pitches:
                    formerPitch,currPitch=(data.pitches[formerT],
                                                    data.pitches[currTime])
                    formerNote,currNote=getNote(formerPitch),getNote(currPitch)
                    return formerNote==currNote
    return False

def getNote(pitch):
    if almostEqual(pitch,0):
        return 0
    else:
        return roundHalfUp(12*math.log(float(pitch)/440,2)+49)

def play_source(source_path):#cite
    hop_size = 256
    f = source(source_path, hop_size = hop_size)
    samplerate = f.samplerate

    s = Stream(samplerate = samplerate, blocksize = hop_size)
    s.start()
    read = 0
    while 1:
        vec, read = f()
        s.write(vec)
        if read < hop_size: break
    s.stop()
    # end


def createSource(data,hopSize):# partially cite
    samplerate = 0  # use original source samplerate
    s = source(sys.argv[1], samplerate, hopSize)
    total_frames = 0
    while True: # reading loop
        samples, read = s()
        total_frames += read
        if read < hopSize: break # end of file reached
    fmt_string = "read {:d} frames at {:d}Hz from {:s}"
    print (fmt_string.format(total_frames, s.samplerate, sys.argv[1]))
    data.endTime=float(total_frames)/s.samplerate
    return s

def timerFired(data):
    #print(data.time)
    #if data.time==0:
       # play_source(sys.argv[1])
    data.time=roundHalfUp((clock()-data.initTime)*1000)
    print(data.time)
    if data.time==data.endTime:
        sys.exit()
        data.mode='end'
    if checkAllbuffer(data,data.time):
        data.arrow=True
    else:
        data.arrow=False
    if isContinuousPitch(data):
        data.r*=(1+1/30)
        data.buffer+=10
    else:
        data.r=data.R
        data.buffer=1


def checkAllbuffer(data,time):
    for curr in range(time,data.buffer+time):
        if curr in data.stuffs:
            return True
    return False

def keyPressed(event,data):
    pass

def mousePressed(event,data):
    pass

def redrawAll(canvas,data):
    if data.mode=='play':
        if data.arrow:
            r=data.r
            canvas.create_rectangle(data.width/2-r,data.height/2-r,
                                            data.width/2+r,data.height/2+r)
        else:
            return
    elif data.mode=='end':
        canvas.create_text(data.width/2,data.height/2,text='End')
    
def showArrows(width=600, height=600):#cite from the coursenote
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas,data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = width # so grid is width x width
    data.fullHeight = height
    data.timerDelay = 1 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    data.root = root # for showMessageBox parent
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas,data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")# end point
