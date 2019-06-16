from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
import json

import board
import busio
#import adafruit_pca9685
from adafruit_pca9685 import PCA9685

i2c_bus = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50
pca.channels[0].duty_cycle = int(3.3983 * 1500) # 1 ms

class Server(SimpleHTTPRequestHandler):
    def do_POST(self):
        callableHandler = getattr(Handlers, self.path[1:], False)
        if callableHandler != False:
            callableHandler(self)
            return

        self.outputResult("error, wrong url")

    def outputResult(self, output):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Cache-Control', 'no-cache ')
        self.end_headers()
        self.wfile.write(bytes(output, "UTF-8"))

class Handlers():
    def setServo(req):
        print("setServo")
        #print(req.rfile)
        #print(req.rfile.peek())
        input = req.rfile.read(int(req.headers['Content-Length']))
        input = input.decode("utf-8") 
        print(input)
        jsonInput = json.loads(input)

        try:
            sliderValue = int(jsonInput['sliderValue'])
        except:
            print("setServo missing or invalid sliderValue property")
            return


        pca.channels[0].duty_cycle = int(3.3983 * sliderValue)
        req.outputResult("OK")


httpd = HTTPServer(('', 8000), Server)

httpd.serve_forever()