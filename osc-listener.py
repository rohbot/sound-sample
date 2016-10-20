#!/usr/bin/env python3
from OSC import OSCServer
import sys
from time import sleep
import pygame
import time

pygame.mixer.init()

NUM_SCENES = 6
CURRENT_SCENE = 0

SOUND_MAPPING = {
  0: ['samples/ambi-key.ogg',1,True],
  1: ['samples/choir1.wav',1,True],
  2: ['samples/choir2.wav',1,True],
  3: ['samples/choir3.wav',1,True],

  4: ['samples/goreng.wav',1,True],
  5: ['samples/ada.wav',1,False],
  6: ['samples/teh.wav',1,True],
  7: ['samples/bungkus.wav',1,False],
  
  8: ['samples/hello.wav',1,False],
  9: ['samples/massage.wav',1,False],
  10: ['samples/mmm.wav',1,True],
  11: ['samples/callme.wav',1,False],
  
  12: ['samples/freeky-alot2.wav',1,False],
  13: ['samples/freeky-synth.wav',1,True],
  14: ['samples/freeky-alot.wav',1,True],
  15: ['samples/sheep-baa.wav',1,False],
  
  16: ['samples/whip-crack.wav',1,False],
  17: ['samples/neigh-neigh.wav',1,False],
  18: ['samples/whip.wav',1,True],
  19: ['samples/stanky-leg.wav',1,True],
  
  20: ['samples/pen-beat.wav',0.5,True],
  21: ['samples/pen.wav',1,False],
  22: ['samples/pineapple.wav',1,False],
  23: ['samples/ppap.wav',1,True],
 
  


   
}

sounds = []
is_loop = []
sounds_playing = []
for key,data in SOUND_MAPPING.iteritems():
        soundfile, volume, loop = data
        sounds.append(0)
        is_loop.append(False)
        sounds_playing.append(False)
        sounds[key] =  pygame.mixer.Sound(soundfile)
        sounds[key].set_volume(volume);
        is_loop[key] = loop

#sounds_playing = [False,False,False,False,False,False,False,False]
#print is_loop

static_sound = pygame.mixer.Sound('samples/radio-static.wav')
ping_sound = pygame.mixer.Sound('samples/elec_pop.wav')

def playSound(sound_id):
    print "playing ", sound_id
    if sounds_playing[sound_id]:
        sounds[sound_id].stop()
        

    if is_loop[sound_id]:
        if not sounds_playing[sound_id]:
            sounds[sound_id].play(loops = -1)
            sounds_playing[sound_id] = True
    else:
        sounds[sound_id].play()
        sounds_playing[sound_id] = True

def stopSound(sound_id):
    sounds[sound_id].stop()
    sounds_playing[sound_id] = False

def stopAllSounds():
    for sound_id,data in SOUND_MAPPING.iteritems():
        sounds[sound_id].stop()
        sounds_playing[sound_id] = False



# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True



def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

def cap_callback(path, tags, args, source):
    global CURRENT_SCENE
    
    # don't do this at home (or it'll quit blender)
    #print path, tags, args, source
    data = path.split("/")
    cap = int(data[1][3]) + (CURRENT_SCENE * 4)  
    val = int(args[0])

    print "cap:", cap, val 
    if val == 1:
        playSound(cap)
    if val == 0:
        stopSound(cap)

def pot_callback(path, tags, args, source):
    global CURRENT_SCENE

    data = path.split("/")
    
    pot = float(args[0])

    new_scene = int(pot / 100 * NUM_SCENES)
    if new_scene != CURRENT_SCENE:
        #for i in range(new_scene+1):
        playSound(new_scene * 4)
        time.sleep(1)
        stopSound(new_scene * 4)

        CURRENT_SCENE = new_scene
    print pot, CURRENT_SCENE


def multi_callback(path, tags, args, source):
    data = path.split("/")
    btn = int(data[1][3]) 
    val = int(data[2])

    print "btn:", btn + 1,val
    if val == 1:
        playSound(btn)
    if val == 0:
        stopSound(btn)


def seekbar_callback(path, tags, args, source):
    data = path.split("/")
    btn = int(data[1]) 
    val = int(data[2])

    print "bar:", btn, val


def static_callback(path, tags, args, source):
    global CURRENT_SCENE
    
    data = path.split("/")
    
    state = int(args[0])
    if state == 1:
        static_sound.play()
        stopAllSounds()
    else:
        static_sound.stop()
        #playSound(CURRENT_SCENE * 4)
        #time.sleep(1)
        #stopSound(CURRENT_SCENE * 4)

stopAllSounds()    
#static_sound.play()
server = OSCServer( ("0.0.0.0", 9995) )
server.timeout = 0
run = True
# funny python's way to add a method to an instance of a class
import types
server.handle_timeout = types.MethodType(handle_timeout, server)

server.addMsgHandler( "/multi", multi_callback )
server.addMsgHandler( "/btn0/0", multi_callback )
server.addMsgHandler( "/btn0/1", multi_callback )
server.addMsgHandler( "/btn1/0", multi_callback )
server.addMsgHandler( "/btn1/1", multi_callback )
server.addMsgHandler( "/btn2/0", multi_callback )
server.addMsgHandler( "/btn2/1", multi_callback )
server.addMsgHandler( "/btn3/0", multi_callback )
server.addMsgHandler( "/btn3/1", multi_callback )
server.addMsgHandler( "/btn4/0", multi_callback )
server.addMsgHandler( "/btn4/1", multi_callback )
server.addMsgHandler( "/btn5/0", multi_callback )
server.addMsgHandler( "/btn5/1", multi_callback )
server.addMsgHandler( "/btn6/0", multi_callback )
server.addMsgHandler( "/btn6/1", multi_callback )
server.addMsgHandler( "/btn7/0", multi_callback )
server.addMsgHandler( "/btn7/1", multi_callback )
server.addMsgHandler( "/btn8/0", multi_callback )
server.addMsgHandler( "/btn8/1", multi_callback )
server.addMsgHandler( "/btn9/0", multi_callback )
server.addMsgHandler( "/btn9/1", multi_callback )
server.addMsgHandler( "/btn10/0", multi_callback )
server.addMsgHandler( "/btn10/1", multi_callback )
server.addMsgHandler( "/btn11/0", multi_callback )
server.addMsgHandler( "/btn11/1", multi_callback )
server.addMsgHandler( "/btn12/0", multi_callback )
server.addMsgHandler( "/btn12/1", multi_callback )
server.addMsgHandler( "/btn13/0", multi_callback )
server.addMsgHandler( "/btn13/1", multi_callback )
server.addMsgHandler( "/btn14/0", multi_callback )
server.addMsgHandler( "/btn14/1", multi_callback )
server.addMsgHandler( "/btn15/0", multi_callback )
server.addMsgHandler( "/btn15/1", multi_callback )
server.addMsgHandler( "/btn16/0", multi_callback )
server.addMsgHandler( "/btn16/1", multi_callback )

server.addMsgHandler( "/tog1/0", multi_callback )
server.addMsgHandler( "/tog1/1", multi_callback )
server.addMsgHandler( "/tog2/0", multi_callback )
server.addMsgHandler( "/tog2/1", multi_callback )
server.addMsgHandler( "/tog3/0", multi_callback )
server.addMsgHandler( "/tog3/1", multi_callback )
server.addMsgHandler( "/tog4/0", multi_callback )
server.addMsgHandler( "/tog4/1", multi_callback )
server.addMsgHandler( "/tog5/0", multi_callback )
server.addMsgHandler( "/tog5/1", multi_callback )
server.addMsgHandler( "/tog6/0", multi_callback )
server.addMsgHandler( "/tog6/1", multi_callback )
server.addMsgHandler( "/tog7/0", multi_callback )
server.addMsgHandler( "/tog7/1", multi_callback )
server.addMsgHandler( "/tog8/0", multi_callback )
server.addMsgHandler( "/tog8/1", multi_callback )

server.addMsgHandler( "/cap0", cap_callback )
server.addMsgHandler( "/cap1", cap_callback )
server.addMsgHandler( "/cap2", cap_callback )
server.addMsgHandler( "/cap3", cap_callback )


server.addMsgHandler( "/seekBar1", seekbar_callback )
server.addMsgHandler( "/seekBar1/1", seekbar_callback )

server.addMsgHandler( "/seekBar2/0", seekbar_callback )
server.addMsgHandler( "/seekBar2/1", seekbar_callback )

server.addMsgHandler( "/seekBar3/0", seekbar_callback )
server.addMsgHandler( "/seekBar3/1", seekbar_callback )

server.addMsgHandler( "/seekBar4/0", seekbar_callback )
server.addMsgHandler( "/seekBar4/1", seekbar_callback )

server.addMsgHandler( "/pot", pot_callback )
server.addMsgHandler( "/static", static_callback )


server.addMsgHandler( "/quit", quit_callback )


# user script that's called by the game engine every frame
def each_frame():
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()

# simulate a "game engine"
while run:
    # do the game stuff:
    #sleep(1)
    # call user script
    each_frame()

server.close()