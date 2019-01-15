#referencing demo code of aubio and course note barebone animation
#includes demo_onset, demo_pitch, demo_tempo, demo_pysoundcard_play, 
#simple script from aubio documentation

from aubio import source,tempo,onset,pitch
import decimal

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))


def reduceBeats(beats,onsets):
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


def getBeatFrame(path):#cite
    #referencing example code
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
    #referencing example code
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