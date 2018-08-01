import bluetooth                        #Importing to use for getting data from mobile tthrough bluetooth
import RPi.GPIO as GPIO                 #Importing for using pins in output
from grove_rgb_lcd import *             #Importing to display using grove rgb display
import os
from gtts import gTTS                   #Importing library for text to speech
import pyowm                            #Importing for getting weather data from API
from pprint import pprint
from random import randint              #Importing to generate random nnumber to displaay jokes

BLUE=21                                 #The GPIO Pins to which  the LEDs are  connected
GREEN=20
YELLOW=16
RED=12

def getweather(c):               #Function to get weather data from API
    owm = pyowm.OWM("35eaa9264eefb54b29922d52532bdc32")  
    observation = owm.weather_at_place(c+",in")  
    w =observation.get_weather()
    status =w.get_status()
    wind = w.get_wind()
    temp=w.get_temperature()
    pprint(wind)
    pprint(temp)
    a=status+' temp:'+str(temp['temp_max']-273)+' wind:'+str(wind['speed'])+'m/s'               #Weather data being stored
    setText(a)                                                                                  #LCD Display willl display weather data
    s='The weather is '+status+' with temperature '+str(temp['temp_max']-273)+' degree and windspeed '+str(wind['speed'])+' meter per second'
    playaudio(s)                                                                                #Audio Data being spoken by speakers
    return s

def playaudio(a):                        #Function to play audio
    tts=gTTS(text=a,lang='en')
    tts.save("audio.mp3")               #Audio file being overwritten with audio converted from string input
    os.system("omxplayer audio.mp3")

GPIO.setmode(GPIO.BCM)              #Pins being setup in BCM Mode to use the pins as their GPIo Numbers
GPIO.setwarnings(False)             #Initialisation
GPIO.setup(BLUE,GPIO.OUT)  
GPIO.output(BLUE,0)
GPIO.setup(GREEN,GPIO.OUT)  
GPIO.output(GREEN,0)
GPIO.setup(YELLOW,GPIO.OUT)  
GPIO.output(YELLOW,0)
GPIO.setup(RED,GPIO.OUT)  
GPIO.output(RED,0)
setRGB(0,0,0)
setText("")

server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )   #Bluetooth connection initialisation
port = 1
server_socket.bind(("",port))
server_socket.listen(1)
client_socket,address = server_socket.accept()
print "Accepted connection from ",address         #Bluetooth Connection established
connected="Connection-"
connected+=str(address)

setText(connected)
data=""
loc=raw_input("Enter your location:")
playaudio("Hello")

while 1:
 
 data=data+client_socket.recv(1024)         # Data being received from Bluetooth
 print "Received: %s" % data
 setText(data)
 

 if (data == "blue on"):
     print ("GPIO 21 HIGH, LED ON")
     data=""
     GPIO.output(BLUE,1)
     setRGB(0,0,255)
     playaudio("Blue L E D is now ON")
    
 if (data == "blue off"):
     print ("GPIO 21 LOW, LED OFF")
     data=""
     GPIO.output(BLUE,0)
     playaudio("Blue L E D is now OFF")    
     
 if (data == "green on"):
     print ("GPIO 20 HIGH, LED ON")
     data=""
     GPIO.output(GREEN,1)
     setRGB(0,255,0)     
     playaudio("GREEN L E D is now ON")
     
 if (data == "green off"):
     print ("GPIO 20 LOW, LED OFF")
     data=""
     GPIO.output(GREEN,0)
     playaudio("Green L E D is now OFF")
     
 if (data == "yellow on"):
     print ("GPIO 16 HIGH, LED ON")
     data=""
     GPIO.output(YELLOW,1)
     setRGB(255,255,0)
     playaudio("Yellow L E D is now ON")
     
 if (data == "yellow off"):
     print ("GPIO 16 LOW, LED OFF")
     data=""
     GPIO.output(YELLOW,0)
     playaudio("Yellow L E D is now OFF")
     
 if (data == "red on"):
     print ("GPIO 12 HIGH, LED ON")
     data=""
     GPIO.output(RED,1)
     setRGB(255,0,0)
     playaudio("Red L E D is now ON")
     
 if (data == "red off"):
     print ("GPIO 12 LOW, LED OFF")
     data=""
     GPIO.output(RED,0)
     playaudio("Red LED is now OFF")
     
 if (data == "all on"):
     print ("GPIO 21,20,16,12 high, LED ON")
     data=""
     GPIO.output(RED,1)
     GPIO.output(YELLOW,1)
     GPIO.output(GREEN,1)
     GPIO.output(BLUE,1)
     setRGB(255,255,255)
     playaudio("All L E Ds are now ON")
     
 if (data == "all off"):
     print ("GPIO 21,20,16,12 LOW, LED OFF")
     data=""
     GPIO.output(RED,0)
     GPIO.output(YELLOW,0)
     GPIO.output(GREEN,0)
     GPIO.output(BLUE,0)
     playaudio("All L E Ds are now OFF")   
 
 if (len(data)>4 and data.endswith("clear")):
     print("Clear")
     data=""
     setText("")
     
     
 if (len(data)>3 and data.endswith("quit")):
     print ("Quit")
     data=""
     GPIO.output(RED,0)
     GPIO.output(YELLOW,0)
     GPIO.output(GREEN,0)
     GPIO.output(BLUE,0)
     setText("")
     setRGB(0,0,0)
     playaudio("Goodbye")
     break

 if (data=="weather"):
     data=""
     getweather(loc)

 if (data=="joke" or data=="tell me a joke"):
     joke=""
     jokeind=randint(0,4)
     if (jokeind==0):
         joke="A plateau is the highest form of flattery."
     if (jokeind==1):
         joke="Why is 6 afraid of 7?Because 7 8 9"
     if (jokeind==2):
         joke="Atheism is a non-prophet organization."
     if (jokeind==3):
         joke="Exaggerations went up a million percent last year"
     if (jokeind==4):
         joke="What do you call a magic dog? A Labracadabrador."    
     data=""
     setText(joke)
     playaudio(joke) 
    
client_socket.close()                    #Termination of program
server_socket.close()
