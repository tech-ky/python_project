from time import sleep
import requests

def send_data(temp,humi,ldr,lat,lon):
        resp=requests.get("https://api.thingspeak.com/update?api_key=6R7GEDR50YBXEMG8&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s"%(temp,humi,ldr,lat,lon))

