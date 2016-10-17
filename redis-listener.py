import pygame
import time
import redis

r = redis.Redis()

pygame.mixer.init()


SOUND_MAPPING = {
  3: ['samples/loop_amen.wav',0.7,True],
  1: ['samples/ambi_drone.wav',1,True],
  2: ['samples/bass_voxy_c.wav',0.5,True],
  0: ['samples/hello.ogg',1,True]
}

sounds = [0,0,0,0]
is_loop = [False,False,False,False]

for key,data in SOUND_MAPPING.iteritems():
        soundfile, volume, loop = data
        sounds[key] =  pygame.mixer.Sound(soundfile)
        sounds[key].set_volume(volume);
        is_loop[key] = loop

sounds_playing = [False,False,False,False]
print is_loop



def playSound(sound_id):
    if is_loop[sound_id]:
        if not sounds_playing[sound_id]:
            sounds[sound_id].play(loops = -1)
            sounds_playing[i] = True
    else:
        sounds[sound_id].play()
        sounds_playing[i] = True

def stopSound(sound_id):
    sounds[i].stop()
    sounds_playing[i] = False



pubsub = r.pubsub()
pubsub.subscribe(['quad'])


for item in pubsub.listen():
    if item['data'] == "KILL":
        pubsub.unsubscribe()
        print "unsubscribed and finished"
        break
    else:
        try:
            quad = eval(item['data'])
            print quad
            for i in range(4) :
                if quad[i]:
                    playSound(i)
                else:
                    stopSound(i)               

        except:
            pass



time.sleep(1)
print 'done'