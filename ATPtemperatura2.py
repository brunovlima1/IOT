import dht
import machine
import time
import network
import urequests
from wifi_lib import conecta

station = conecta("network", "password");
http_headers = {'content-Type': 'application/json'}
thingspeak_api_write_key = '01YHDV5ZOBZF9WR8'
update_time_interval = 5000
last_update = time.ticks_ms()



d = dht.DHT11(machine.Pin(4))
r = machine.Pin(2,machine.Pin.OUT)

while True:
    d.measure()
    temp = d.temperature()
    humid = d.humidity()
    if temp > 31 or humid > 70:
      r.value(1)
    else:
        r.value(0)
    print("Temperatura: {} Umidade: {}".format(d.temperature(), d.humidity()))
    time.sleep(15)
    
    if time.ticks_ms() - last_update >= update_time_interval: 
        
         
        dht_readings = {'field1':temp, 'field2':humid} 
        request = urequests.post( 
          'http://api.thingspeak.com/update?api_key=' +
          thingspeak_api_write_key, 
          json = dht_readings, 
          headers = http_headers )  
        request.close() 
        last_update = time.ticks_ms()
