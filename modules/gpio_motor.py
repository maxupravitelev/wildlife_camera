import RPi.GPIO as GPIO
import time
import threading 



class GPIO_motor:
    def __init__(self):


        self.P_A1 = 4  # adapt to your wiring
        self.P_A2 = 27 # ditto
        self.P_B1 = 17 # ditto
        self.P_B2 = 22 # ditto
        self.delay = 0.005 # time to settle
        self._lock = threading.Lock()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.P_A1, GPIO.OUT)
        GPIO.setup(self.P_A2, GPIO.OUT)
        GPIO.setup(self.P_B1, GPIO.OUT)
        GPIO.setup(self.P_B2, GPIO.OUT)

    def forwardStep(self):
        self.setStepper(1, 0, 1, 0)
        self.setStepper(0, 1, 1, 0)
        self.setStepper(0, 1, 0, 1)
        self.setStepper(1, 0, 0, 1)

    def backwardStep(self):
        self.setStepper(1, 0, 0, 1)
        self.setStepper(0, 1, 0, 1)
        self.setStepper(0, 1, 1, 0)
        self.setStepper(1, 0, 1, 0)
    
    def setStepper(self, in1, in2, in3, in4):
        GPIO.output(self.P_A1, in1)
        GPIO.output(self.P_A2, in2)
        GPIO.output(self.P_B1, in3)
        GPIO.output(self.P_B2, in4)
        time.sleep(self.delay)

    def move(self, steps=256, direction="left"):
        with self._lock:
            # 512 steps for 360 degrees, adapt to your motor
            # while True:

            if direction == "right":
                print("right")
                for i in range(steps):
                    self.forwardStep()
            else:
                print("left")
                for i in range(steps):
                    self.backwardStep() 

    def start(self, steps, direction):
        t = threading.Thread(target=self.move, args=(steps, direction))
        t.daemon = True
        t.start()



# Built upon:
# http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/steppermotors.inc.php