
'''
bond0     Link encap:Ethernet  HWaddr E4:11:5B:D7:55:40
          inet addr:10.57.210.39  Bcast:10.57.210.255  Mask:255.255.255.0
          inet6 addr: fe80::e611:5bff:fed7:5540/64 Scope:Link
          UP BROADCAST RUNNING MASTER MULTICAST  MTU:1500  Metric:1
          RX packets:43084077351 errors:0 dropped:0 overruns:0 frame:0
          TX packets:32223803856 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:50664377309431 (46.0 TiB)  TX bytes:16264729316279 (14.7 TiB)

eth0      Link encap:Ethernet  HWaddr E4:11:5B:D7:55:40
          UP BROADCAST RUNNING SLAVE MULTICAST  MTU:1500  Metric:1
          RX packets:43066076417 errors:0 dropped:0 overruns:0 frame:0
          TX packets:32223803856 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:50663074956353 (46.0 TiB)  TX bytes:16264729316279 (14.7 TiB)
'''

import re
import subprocess
import sys
import time
interface_fa = re.compile('^([a-z0-9]*) *Link encap:')
packets_fa = re.compile('([RT])X packets:([0-9]*)')
bytes_fa = re.compile('([RT])X bytes:([0-9]*)')
def scan():
    lns = subprocess.check_output('/sbin/ifconfig')
    interface = 'unk'
    nics = {}
    data = {}
    for l in lns.split('\n'):
        mo = interface_fa.search(l)
        if mo != None:
            nics[interface] = data
            interface = mo.group(1)
            data = {}
        mo  = packets_fa.search(l)
        if mo != None:
            data['p'+mo.group(1)] = int(mo.group(2))
        mos = bytes_fa.findall(l)
        for b in mos:
            data['b'+b[0]] = int(b[1])
    nics[interface] = data
    return nics
def main():
    pause = float(sys.argv[1])
    maxLoop = int(sys.argv[2])
    last = scan()
    i=0
    while i<maxLoop:
        time.sleep(pause)
        cur = scan()
        print time.strftime('%Y%m%d-%H%M%S'),
        print 'pR',cur['br0']['pR'] - last['br0']['pR'],
        print 'pT',cur['br0']['pT'] - last['br0']['pT'],
        print 'bR',cur['br0']['bR'] - last['br0']['bR'],
        print 'bT',cur['br0']['bT'] - last['br0']['bT'],
        print ''
        sys.stdout.flush()
        last = cur
        i+=1
if __name__ == '__main__':
    main()
