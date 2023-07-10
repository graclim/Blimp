import qwiic_vl53l1x as qwiic
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
XSHUT = [23, 20] # 15
address = {23 : 0x2B, 20 : 0x2D, 15: 0x2F}

for pin in XSHUT:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

time.sleep(1)
print("VL53L1X Qwiic Test\n")
tofs = []
for i in range(len(XSHUT)):
    GPIO.output(XSHUT[i], GPIO.HIGH)
    time.sleep(1)
    tofs.append(qwiic.QwiicVL53L1X())
    tofs[i].set_i2c_address(address[XSHUT[i]])  
    if (tofs[i].sensor_init() == None):                                  # Begin returns 0 on a good init
        print("Sensor online!\n")


def measurement():
    global distances

    distances = []
    for tof in tofs:
        tof.start_ranging()
        time.sleep(.005)
        distances.append(tof.get_distance())
        time.sleep(.005)
        tof.stop_ranging()
    
    distances.append(10)
    return distances




if __name__ == '__main__':
    while True:
            try:
                for ToF in tofs:
                    ToF.start_ranging()                                              # Write configuration bytes to initiate measurement
                    time.sleep(.005)
                    distance = ToF.get_distance()    # Get the result of the measurement from the sensor
                    time.sleep(.005)
                    ToF.stop_ranging()

                    distanceInches = distance / 25.4
                    distanceFeet = distanceInches / 12.0

                    print("Distance(mm): %s Distance(ft): %s" % (distance, distanceFeet))
                    time.sleep(1)

            except Exception as e:
                    print(e)
