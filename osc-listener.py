#!/usr/bin/env python3
from OSC import OSCServer
import sys
from time import sleep
import pygame
import time

pygame.mixer.init()


SOUND_MAPPING = {
  0: ['samples/loop_amen.wav',0.7,True],
  1: ['samples/ambi_drone.wav',1,True],
  2: ['samples/bass_voxy_c.wav',0.5,True],
  3: ['samples/hello.ogg',1,False],
  4: ['samples/elec_ping.wav',1,False],
  5: ['samples/elec_plip.wav',1,False],
  6: ['samples/elec_pop.wav',1,False],
  7: ['samples/elec_triangle.wav',1,False],
  8: ['samples/guit_e_fifths.wav',1,False],
  9: ['samples/guit_em9.wav',1,False],
  10: ['samples/guit_e_slide.wav',1,False],
  11: ['samples/guit_harmonics.wav',1,False],
  12: ['samples/static.wav',1,False]
   
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


# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True



def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False


def multi_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    #print path, tags, args, source
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

def pot_callback(path, tags, args, source):
    data = path.split("/")
    
    pot = int(args[0])
    print pot

def static_callback(path, tags, args, source):
    data = path.split("/")
    
    state = int(args[0])
    if state == 1:
        static_sound.play()
    else:
        static_sound.stop()
    
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