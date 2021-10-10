# Uses Bluez for Linux
#
# sudo python3 -m pip install pybluez
# 
# sudo bluetoothctl
# power on
# agent NoInputNoOutput
# default-agent
# discoverable on
# scan on
# trust >adressmac<
# connect >adressmac<


import bluetooth
import threading
import time

class Bluetooth_rpi:
    def __init__(self,adresse,device_name):
        self.server_sock = None
        self.client_sock = None
        self.sock = None
        self.port = 1
        self.targetBluetoothMacAddress=adresse
        self.device_name=device_name
        self.increment = 0
    
    def connection(self):
        self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.sock.connect((self.targetBluetoothMacAddress, self.port))
        print ("connected")

    def start_server(self):
        print ("server run")
        self.server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.server_sock.bind(("",self.port))
        self.server_sock.listen(1)

        self.client_sock,address = self.server_sock.accept()
        print ("Accepted connection from " + str(address))

    def receiveMessages(self):
      data = self.client_sock.recv(1024)
      print ("received", data)
      
    def sendMessage(self):
      self.sock.send(str(self.device_name)+" : "+str(self.increment))
      self.increment+=1
      
    def lookUpNearbyBluetoothDevices(self):
      nearby_devices = bluetooth.discover_devices()
      for bdaddr in nearby_devices:
        print (str(bluetooth.lookup_name( bdaddr )) + " [" +bdaddr+ "]")

    def run_server(self):
        self.start_server()
        while 1:
            self.receiveMessages()
        
    def run_client(self):
        while 1:
            try:
                self.connection()
                while 1:
                    self.sendMessage()
                    time.sleep(0.1)
            except:
                print("Connection refused")
                time.sleep(2)
                
    def run_client1(self):
        self.connection()
        while 1:
            self.sendMessage()
    
    def cleanup(self):
        self.client_sock.close()
        self.server_sock.close()
        self.sock.close()

device = Bluetooth_rpi("B8:27:EB:08:8F:C2","controller")
#device = Bluetooth_rpi("DC:A6:32:80:00:FB","receiver")

th1 = threading.Thread(target=device.run_server)
th2 = threading.Thread(target=device.run_client)
    
th1.start()
th2.start()

th1.join()
th2.join()

device.cleanup


