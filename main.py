#__________________Connecting to the network, need essid an password of Ome joost________________________
import network
import utime

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)


def do_connect():
    if not sta_if.isconnected():
        print("connecting to network")
        sta_if.active(True)
        sta_if.connect('Guest','freeinternet')
        while not sta_if.isconnected():
            pass
    print("network config:", sta_if.ifconfig())

do_connect()


ap_if.active(False)

#________Getting the time_______________________________________ 

try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600

host = "pool.ntp.org"

def time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA

# There's currently no timezone support in MicroPython, so
# utime.localtime() will return UTC time (as if it was .gmtime())
def settime():
    t = time()
    import machine
    import utime
    tm = utime.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)

settime()

#____________init______________

from machine import Pin
#available: 16,15,14,13,12,2,0,4,5
p1h = Pin(16, Pin.OUT)
p2h = Pin(5, Pin.OUT)
p3h = Pin(4, Pin.OUT)
p4h = Pin(0, Pin.OUT)

p1m = Pin(2, Pin.OUT)                       
p2m = Pin(14, Pin.OUT)
p3m = Pin(12, Pin.OUT)
p4m = Pin(13, Pin.OUT)
p5m = Pin(15, Pin.OUT)
p6m = Pin(3, Pin.OUT)

ph = [p1h,p2h,p3h,p4h]
pm = [p1m,p2m,p3m,p4m,p5m,p6m]


#____________periodicly check for time _________________
cval = 0

while True:

    decvalh = (int(utime.localtime()[3]) + 1)%12
    binvalh = list("{0:b}".format(decvalh))
    binvalh = list(map(int,binvalh))

    decvalm = utime.localtime()
    decvalm = decvalm[4]
    binvalm = list("{0:b}".format(decvalm))
    binvalm = list(map(int,binvalm))

    #syncing every 15 minutes, and only once.
    if decvalm%15 ==0:
        if cval:
            settime()
            cval = 0
    else:
        cval = 1

    #lengte goed zetten van de array van binval
    if not(len(binvalh) == 4):
        cnt = 4- len(binvalh)
        for i in range(cnt):
            binvalh.insert(0,0)

    if not(len(binvalm) == 6):
        cnt = 6- len(binvalm)
        for i in range(cnt):
            binvalm.insert(0,0)


    for i in range(4):
        ph[i].value(binvalh[i])

    for i in range(6):
        pm[i].value(binvalm[i])

    utime.sleep(3)
    #print("hours ", binvalh, '\n minutes ', binvalm)