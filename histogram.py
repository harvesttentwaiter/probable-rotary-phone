import math
import sys
def histogram(ary, bins = 10, fh = sys.stdout):
    sum  = 0.0
    sum2 = 0.0
    min = 1.0e99
    max = -1.0e99
    for v in ary:
        sum2 += v*v
        sum  += v
        if v < min:
            min = v
        if v > max:
            max = v
    #binLower = []
    binCnt = []
    binSz = (max*(1+1e-306) - min)/bins
    for i in range(bins+1):
        binCnt.append(0)
        #binLower.append( min + (max-min)/bins*i )
    for v in ary:
        idx = int( (v-min)/binSz )
        if idx < 0 or idx >= len(binCnt):
            print '20150903kkang out of range', v, binSz, idx, min
            continue
        binCnt[idx] += 1
    binCntMax = 0
    for curBinCnt in binCnt:
        if curBinCnt > binCntMax:
            binCntMax = curBinCnt
    avg=sum/len(ary)
    stddev = math.sqrt(sum2/len(ary) - avg*avg)
    fh.write('min:%f max:%f avg:%f stddev:%f count:%i\n'%(min,max,avg,stddev,len(ary)) )
    for i in range(bins):
        hashStr = hashes(binCnt[i]*40./binCntMax)
        fh.write('%22.16g %10i %s\n'%(min+binSz*i, binCnt[i], hashStr) )

g_hashes = ['']
def hashes(num):
    num = int(num)
    while len(g_hashes) <= num:
        g_hashes.append( g_hashes[-1] + '#' )
    return g_hashes[num]

def main():
    ary = []
    for l in sys.stdin:
        ary.append(int(l))
    histogram(ary)

if __name__ == '__main__':
    main()
