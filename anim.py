import machine, math, time
from random import randint
from machine import Pin, PWM

pinlist = [32, 33, 25, 26, 22, 27, 14, 12, 2]

class ANIM:
    led = []
    def __init__(self, pinlist=pinlist, n=len(pinlist), frequency=1000):
        for i in range(n):
            ledObject=[] 
            ledObject.append(PWM(Pin(pinlist[i]), frequency))
            ledObject.append(0) # 0 to initiate all leds as off
            ANIM.led.append(ledObject)
        time.sleep(1)
        for i in range(n):
            ANIM.led[i][0].duty(ANIM.led[i][1])
            time.sleep(.1)
        self.n = n
        
    def alert(self, wait=500):
        for duty_cycle in range(0, 1023):
            for i in range(self.n):
                ANIM.led[i][0].duty(duty_cycle)
                time.sleep_us(50)
        time.sleep_ms(wait)
        for duty_cycle in range(1023, 0, -1):
            for i in range(self.n):
                ANIM.led[i][0].duty(duty_cycle)
                time.sleep_us(100)
        
    def runningLight(self, maxBright=1023, wait=200):
        position = 0
        for j in range(self.n * 2):
            position += 1
            for i in range(self.n):
                duty_cycle = int(((math.sin(i+position) * 127 + 128)/255)*maxBright)
                ANIM.led[i][0].duty(duty_cycle)
            time.sleep_ms(wait)
            
    def centreLight(self):              
        for duty_cycle in range(0, 1023):
                ANIM.led[4][0].duty(duty_cycle)
                time.sleep_us(200)
        mirror = 3
        for seq in range(5, 9, 1):    
            for duty_cycle in range(0, 1023):
                ANIM.led[seq][0].duty(duty_cycle)
                ANIM.led[mirror][0].duty(duty_cycle)
                time.sleep_us(100)
            mirror -= 1
        mirror = 3    
        for seq in range(5, 9, 1):    
            for duty_cycle in range(1023, 0, -1):
                ANIM.led[seq][0].duty(duty_cycle)
                ANIM.led[mirror][0].duty(duty_cycle)
                time.sleep_us(250)
            mirror -= 1
        for duty_cycle in range(1023, 0, -1):
            ANIM.led[4][0].duty(duty_cycle)
            time.sleep_us(800)
            
    def meteorBounce(self, size=1,trail_decay=260,random_decay=True,delay=170,maxBright=1023, overScan=18):

        def fadeToBlack(ledNo, fadeValue):
        
            l = self.led[ledNo][1]
     
            l = (0 if (l<=100) else l-int(l*fadeValue/maxBright))
            
            self.led[ledNo][1]=l

        for i in range(self.n):

            for j in range(self.n):
                if (not random_decay) or (randint(0,10) > 5) :
                    fadeToBlack(j, trail_decay)      

            for j in range(size):
                if (i-j < self.n) and (i-j>=0) :
                    self.led[i-j][1] = maxBright
                    
            for ledCount in range(self.n):
                self.led[ledCount][0].duty(self.led[ledCount][1])
                
            time.sleep_ms(delay)

        for i in range(self.n, 0-overScan, -1):
            for j in range(self.n):
                if (not random_decay) or (randint(0,10) > 5) :
                    fadeToBlack(j, trail_decay)      

            for j in range(size):
                if (i-j < self.n) and (i-j>=0) :
                    self.led[i-j][1] = maxBright
                    
            for ledCount in range(self.n):
                self.led[ledCount][0].duty(self.led[ledCount][1])
                
            time.sleep_ms(delay)

    def stack(self, size=1,trail_decay=600,random_decay=False,delay=100,maxBright=1023):
        for i in range(self.n):
            self.led[i][1] = 0
            self.led[i][0].duty(self.led[i][1])
        def fadeToBlack(ledNo, fadeValue):
            l = self.led[ledNo][1]
            l = (0 if (l<=100) else l-int(l*fadeValue/maxBright))
            self.led[ledNo][1]=l
        for x in range(self.n):
            for i in range(self.n-x):
                for j in range(self.n-x):
                    if (not random_decay) or (randint(0,10) > 5) :
                        fadeToBlack(j, trail_decay)
                for j in range(size):
                    if (i-j < self.n) and (i-j>=0) :
                        self.led[i-j][1] = maxBright
                for ledCount in range(self.n):
                    self.led[ledCount][0].duty(self.led[ledCount][1])
                time.sleep_ms(delay)
        for duty_cycle in range(1023, 0, -1):
            for i in range(self.n):
                self.led[i][0].duty(duty_cycle)
                time.sleep_us(delay)



