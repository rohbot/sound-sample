import time
from MovingAvg import MovingAvg
import Adafruit_MPR121.MPR121 as MPR121
import sys
import OSC
pins = [0,2,4,6]

send_address = '127.0.0.1' , 9995
#send_address = '10.42.0.1' , 9995

c = OSC.OSCClient()
c.connect(send_address)

last_reset = time.time()

def init(cap):
    # Soft reset of device.
    cap._i2c_retry(cap._device.write8, MPR121.MPR121_SOFTRESET, 0x63)
    time.sleep(0.001) # This 1ms delay here probably isn't necessary but can't hurt.
    # Set electrode configuration to default values.
    cap._i2c_retry(cap._device.write8, MPR121.MPR121_ECR, 0x00)
    # Check CDT, SFI, ESI configuration is at default values.
    c = cap._i2c_retry(cap._device.readU8, MPR121.MPR121_CONFIG2)
    if c != 0x24:
        return False
    # Set threshold for touch and release to default values.
    cap.set_thresholds(1,1)
    # Configure baseline filtering control registers.

    # Set other configuration registers.
    cap._i2c_retry(cap._device.write8, MPR121.MPR121_DEBOUNCE, 3)
    cap._i2c_retry(cap._device.write8, MPR121.MPR121_CONFIG1, 0x3F) # default, 16uA charge current
    cap._i2c_retry(cap._device.write8, MPR121.MPR121_CONFIG2, 0x20) # 0.5uS encoding, 1ms period
    # Enable all electrodes.
    cap._i2c_retry(cap._device.write8, MPR121.MPR121_ECR, 0x8F) # start with first 5 bits of baseline tracking
    
    # Setup the autoconfig
    cap1._i2c_retry(cap1._device.write8, MPR121.MPR121_AUTOCONFIG0, 0b10101110)
    cap1._i2c_retry(cap1._device.write8, MPR121.MPR121_AUTOCONFIG1, 0)

    last_reset = time.time()

# Create MPR121 instance
cap1 = MPR121.MPR121()

# Initialize communication with MPR121
cap1.begin( 0x5a )
init(cap1)

#logFile = open('singing_plants.log', 'a')

ccount = 0
avg = 0
buffer = [0, 0, 0, 0]
pState = 0
bs = 5
mavg = [MovingAvg(bs), MovingAvg(bs), MovingAvg(bs), MovingAvg(bs)]
sounds_playing = [False,False,False,False]
is_loop = [True,True,True,True]
cap1.touched()

def sendMessage(address, value):
    msg = OSC.OSCMessage()
    msg.setAddress(address)
    msg.append(value)
    try:
        c.send(msg)
    except:
        print "Error sending OSC message"
        print msg

def playSound(sound_id):
    if is_loop[sound_id]:
        if not sounds_playing[sound_id]:
            sendMessage('/cap'+ str(sound_id),1)

            #sounds[sound_id].play(loops = -1)
            sounds_playing[i] = True
    else:
        #sounds[sound_id].play()
        sendMessage('/cap'+ str(sound_id),1)

        sounds_playing[i] = True

def stopSound(sound_id):
    #sounds[i].stop()
    sounds_playing[i] = False
    sendMessage('/cap'+ str(sound_id),0)

    
# Start loop
while True:

    # Get current state
    tcd = cap1.touched()
    
    # Send zeros once if released
    if pState > 0 and tcd == 0:
        
        for i in range(4):
            mavg[i].reset()
            #stop sounds
            stopSound(i)
            # try:
            #     # play sound

            #     #pd.sendValue('pin' + str(i), 0)
            # except Exception as e:
            #     logFile.write('\n' + str(e))
    
    # Send values if touching
    elif tcd > 0:

        # Calculate difference for all pins
        diff1 = [cap1.baseline_data(i) - cap1.filtered_data(i) for i in pins]

        # Print the differences
        print 'Diff:\t', '\t'.join(map(str, diff1))
        
    
        # Moving average
        for i in range(4):
            mavg[i].add(diff1[i])
            avg = mavg[i].get()
            # print 'Avg' + str(i), ':\t', avg
            try:
                #pd.sendValue('pin' + str(i), avg if cap1.is_touched(pins[i]) else 0)
                if cap1.is_touched(pins[i]):
                    playSound(i)
                else:
                    stopSound(i)

            except Exception as e:
                print str(e)
                #logFile.write('\n' + str(e))

    # Reset every minute
    if time.time() - last_reset > 60:
        init(cap1)
        print 'Reinitializing the sensor'
        last_reset = time.time()
    
    # Save previous state
    pState = tcd

    # Short pause before repeating loop
    time.sleep(0.1)

    # Increase cycle counter
    #ccount += 1
