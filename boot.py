from machine import Pin, I2C
import network, time, gc, esp, pca9685, framebuf
import usocket as socket

#init i2c interface
i2c = I2C(0)

# Output enable is active low
driver_oe = Pin(13, Pin.OUT)
driver_oe.value(False) 


# check if motordriver is connected

try:
    # init driver
    pca = pca9685.PCA9685(i2c, address=0x41)
    pca.freq(50)
    print("Driver found")
    
except:
    # throw error if driver is not connected
    print("Driver not connected, check connection")
    
finally:
    pass

esp.osdebug(None)
gc.collect()


##### AP Mode #####

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP32 handcontroller", password="handshake22")
ipstr = str(ap.ifconfig()[0])

print("Accesspoint open")
while not ap.isconnected():
    print('.')
    time.sleep(1)
    
print("Connected! ESP IP: ", ap.ifconfig()[0])


