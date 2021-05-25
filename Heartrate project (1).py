from microbit import *
import utime as time
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text

initialize()
clear_oled()
add_text(0, 2, "Isaac Wong")
sleep(2000)

initialize()
clear_oled()
add_text(0, 0, "The normal")
add_text(0, 1, "bpm is in ")
add_text(0, 2, "between")
add_text(0, 3, "60-100")

window = [] #list for moving average
threshold = 550 #initialise threshold value
count = 0
sample = 0
beat = False
values = []
listv = []

def mean(datalist): #mean function that takes a list as input and returns the mean
    sum = 0 #initialise a sum variable
    for i in datalist: #gets total sum of all values
        sum += i
    if len(datalist) > 0:   #handles empty list to avoid division by 0 error
        return sum/len(datalist)
    else:
        return None

while True:
    while True:
        signal = pin0.read_analog()    #reads a line of data, if reading data from sensor use 'signal = <pin name>.read_analog()'
        window.append(signal)
        avg = round(mean(window))
        values.append(avg)
        if len(window) == 11:    #moving average
            window.pop(0)
        if beat is False and avg >= threshold+10:   #counts beats, each beat is only counted once thanks to the beat boolean variable
            beat = True
            count += 1
            display.show(Image.HEART,wait=False)
            if count == 1:
                t1 = time.ticks_ms()    #gets time since start in milliseconds
            if count == 11:
                t2 = time.ticks_ms()
                T = t2 - t1     #time taken for 10 intervals of beats
                bpm = round(600*1000/(T)) #calculates heart rate in beats per minute
                display.scroll(str(bpm))
                count = 0
                if bpm<60:

                    display.show(Image.SKULL)
                    initialize()
                    clear_oled()
                    add_text(0, 1, "WARNING!!!")
                    add_text(0, 2, "Your bpm is")
                    add_text(0, 3, "LOW!")

                if bpm>100:
                    display.show(Image.SKULL)
                    initialize()
                    clear_oled()
                    add_text(0, 1, "WARNING!!!")
                    add_text(0, 2, "Your bpm is")
                    add_text(0, 3, "HIGH!")

                if bpm >60 and bpm < 100:
                    display.show(Image.HAPPY)
                    initialize()
                    clear_oled()
                    add_text(0, 1, "Healthy")
                    add_text(0, 2, "Your bpm is")
                    add_text(0, 3, "NORMAL")
                if(button_a.was_pressed()):
                    listv.append(bpm)
        elif beat is True and avg <= threshold-10:
            beat = False
            display.show(Image.HEART_SMALL)
        sample += 1
        if sample == 250: #every 250 readings, an average is taken and is defined as the threshold value
            threshold = mean(values)
            values = [] #Heartrate sensing module
            sample = 0
        if(button_b.was_pressed()):
            mean_value = mean(listv)
            display.scroll(str(mean_value))
        sleep(20)
    sleep(20)