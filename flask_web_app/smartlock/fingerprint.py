import time
import serial

import adafruit_fingerprint

uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)


def enroll_finger():

    finger.read_templates()
    freeTemplate = 0
    for template in finger.templates:
        if(template == freeTemplate):
            freeTemplate = freeTemplate + 1
        else:
            break    
  
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...")
        else:
            print("Place same finger again...")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break            
        
        i = finger.image_2_tz(fingerimg) #templating
        
        #if i == adafruit_fingerprint.OK:
        #    print("Templated")       

        if fingerimg == 1:
            print("Znovu daj prst")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="", flush=True)
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:      
        return False
    
    i = finger.store_model(freeTemplate)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:        
        return False

    return True


#print(enroll_finger(30))