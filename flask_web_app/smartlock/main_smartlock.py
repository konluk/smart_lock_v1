import time
from website.models import User, Reservation
from main import app
from website import db
import serial 
import struct

from smartlock.fingerprint import enroll_finger

ser = serial.Serial(
      port='/dev/ttyS0',
      baudrate =9600,           
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE,
      bytesize=serial.EIGHTBITS,
      timeout=0.1)


tlog = b'e\x00\x01\x00\xff\xff\xff'
treg = b'e\x00\x02\x00\xff\xff\xff'

k1 = b'e\x01\x02\x00\xff\xff\xff'
k2 = b'e\x01\x03\x00\xff\xff\xff'
k3 = b'e\x01\x04\x00\xff\xff\xff'
k4 = b'e\x01\x05\x00\xff\xff\xff'

def sendSerial(command):
  k=struct.pack('B', 0xff)
  ser.write(command.encode())
  ser.write(k)
  ser.write(k)
  ser.write(k)

def create_smartlock():
  time.sleep(1) 
  
  sendSerial('page 0')  

  while True: 
    
    output = ser.readline() 
        
    if (output == tlog):
      enroll_finger()    
    
    if (output == treg):
      start_registration() 

     
    time.sleep(0.5)



def start_registration():
  sendSerial('page 1')  
  sendSerial('text1.txt="Heslo:"')  
  password = ""
  
  while True:
    output = ser.readline()
               
    if output == k1:      
      password = password + "1"
    if output == k2:
      password = password + "2"
    if output == k3:
      password = password + "3"
    if output == k4:
      password = password + "4"

    command = 'text2.txt="' + password + '"'
    sendSerial(command)

    if(len(password) == 4):
      break

  with app.app_context():
    user = User.query.filter_by(log_password=int(password)).first()
  
  if(user):
    sendSerial('text2.txt="OK"')
    time.sleep(4)
    sendSerial('page 0') #osetri vynimky pri registraci otlacku
    print("finded") # zavolaj proceduru pre registraciu odtalcku, vrati templateID, updatni ho userovi, zmaz mu log password
    #ak procedura vrati chybu tak to vypis a nic nemen, vrat ho na obrazovvku a skusi to znovu
  else:    
    sendSerial('text2.txt="ZLE HESLO"')
    time.sleep(4)
    sendSerial('page 0') 






#command = 'page 1'
#command = 'text1.txt="Priloz"'
#command = 'vis text1,1'


  #with app.app_context():        
    #    reservation = Reservation(test=17, user_id = 1)
     #   db.session.add(reservation)
      #  db.session.commit()   


        #with app.app_context():
        #    user = User.query.filter_by(email='koncallukas@gmail.com').first()
        
       #reservationX = user.reservation[0]

        #print(reservationX.user_id)   
        #print("test")
        