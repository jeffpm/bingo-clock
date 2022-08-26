import time
import network
import ntptime
import random

from neopixel import Neopixel

numpix = 25
brightness = 50
pixels = Neopixel(numpix, 0, 28, "GRB")
pixels.brightness(brightness)

colorDict = dict()
colorDict['red'] = (225, 32, 32)
colorDict['rose'] = (255, 0, 128)
colorDict['orange'] = (255, 128, 0)
colorDict['green'] = (0, 255, 0)
colorDict['blue'] = (0, 0, 255)
colorDict['azure'] = (0, 128, 255)
colorDict['cyan'] = (0, 255, 255)
colorDict['yellow'] = (255, 255, 0)
colorDict['white'] = (255, 255, 255)

rows = [[0,1,2,3,4,5,6], [7,8,9,10,11,12], [13,14,15,16,17], [18,19,20,21], [22,23,24]]
pixelDict = dict()
pixelDict[-1] = -1
pixelDict[0] = 0
pixelDict[1] = 1
pixelDict[2] = 2
pixelDict[3] = 3
pixelDict[4] = 4
pixelDict[5] = 5
pixelDict[6] = 6
pixelDict[7] = 12
pixelDict[8] = 11
pixelDict[9] = 10
pixelDict[10] = 9
pixelDict[11] = 8
pixelDict[12] = 7
pixelDict[13] = 13
pixelDict[14] = 14
pixelDict[15] = 15
pixelDict[16] = 16
pixelDict[17] = 17
pixelDict[18] = 21
pixelDict[19] = 20
pixelDict[20] = 19
pixelDict[21] = 18
pixelDict[22] = 22
pixelDict[23] = 23
pixelDict[24] = 24
    
def test_strip():
    pixels.fill((255,0, 0))
    pixels.show()

def setup_wifi():
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets['ssid'], secrets['password'])

    max_wait = 30
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >=3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
        
    if wlan.status() !=3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip' + status[0])
    
    
def get_colors(hour, minutes):
    colors = dict()
    colors[hour] = "red"
    # show nothing for 0 minutes
    if not minutes[0] == 0:
        for min in minutes:
            if min in colors:
                colors[min] = "azure"
            else:
                colors[min] = "yellow"

    return colors

def flourish(iters=1):
    for x in range(iters):
        pixels.brightness(20)
        pixels.clear()
        for x in range(0, 5):
            pixels.fill((255,255,255))
            pixels.show()
            time.sleep(.5)
            pixels.clear()
            pixels.show()
            time.sleep(.5)
        pixels.brightness(brightness)
    
def startup(iters=1):
    for x in range(iters):
        pixels.brightness(10)
        pixels.clear()
        
        for row in rows:
            for light in row:
                pixels.set_pixel(pixelDict[light], colorDict['white'])
                pixels.show()
                time.sleep(.1)
        pixels.clear()
        pixels.show()
        pixels.brightness(brightness)
    
def explode(iters=1):
    pixels.brightness(10)
    
    for x in range(iters):
        start = 0
        end = numpix - 1
        
        while start-1 < end:
            pixels.clear()
            pixels.set_pixel(pixelDict[start], colorDict['white'])
            pixels.set_pixel(pixelDict[end], colorDict['white'])
            pixels.show()
            start += 1
            end -= 1
            time.sleep(.1)
            
        time.sleep(.5)
        while end < numpix-1:
            start -= 1
            end += 1
            pixels.set_pixel(pixelDict[start], colorDict['white'])
            pixels.set_pixel(pixelDict[end], colorDict['white'])
            pixels.show()
            
            time.sleep(.1)
        time.sleep(.5)
        
            
        
def break_down_minutes(num_holes, minutes):
    answer = list()
    if minutes <= num_holes:
        answer.append(minutes)
        return answer

    if minutes - num_holes < num_holes:
        answer.append(num_holes)
        answer.append(minutes-num_holes)
        return answer

    counter = 0
    for i in range(num_holes, 0, -1):
        if i == num_holes:
            answer.append(i)
            counter += i
            continue
        elif i + counter <= minutes:
            answer.append(i)
            counter += i
            continue
        if counter == minutes:
            return answer

    return answer


def show_time(should_wait):
    daTime = time.localtime()
    hour = daTime[3]
    minutes = daTime[4]
    seconds = daTime[5]
    if seconds == 0 or not should_wait:
        if minutes == 0:
            flourish()
        print(f'hour: {hour}')
        print(f'mins: {minutes}')
        colors = (get_colors(hour, break_down_minutes(numpix, minutes)))
        print(colors)

        pixels.clear()
        for led, color in colors.items():
            pixels.set_pixel(pixelDict[led - 1], colorDict[color])
        pixels.show()
    time.sleep(1)
    
# test_strip()
startup(2)

# light first led for wifi setup
pixels.set_pixel(0, colorDict['white'])
pixels.show()
setup_wifi()
# light second led for time setup
pixels.clear()
pixels.set_pixel(1, colorDict['white'])
pixels.show()
time.sleep(5)
for x in range(10):
    try:
        print('getting ntp time')
        ntptime.settime()
        break
    except:
        print("trying again")
    
print("Local time after synchronization：%s" %str(time.localtime()))
show_time(False)
while(True):
    show_time(True)
