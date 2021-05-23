#!/usr/bin/env python3
''' openssl sha256 * | sed -e 's/^SHA256/SHA256 /' > SHA256
untrusted comment: verify with openbsd-66-base.pub
RWSvK/c+cFe24Kg9osvG0aOTqPwzBQf5qhWkXjudus4XopPuyyO49ONTPMcgHtm+Xrb19WksbEDbjnQ+e9d436keaYPiCnduRwU=
SHA256 (BOOTIA32.EFI) = 2663559dc14ac6514295f2d4e8deff53e8d6a344de927e9f9de8ca94683c534c
SHA256 (BOOTX64.EFI) = ceaaf139a9454d3a27723350db99b2f5f7fd07a594a1a6b90900ee57d7c7715b'''

import base64
import hashlib
import re
import sys


#new', 'pbkdf2_hmac', 'sha1', 'sha224', 'sha256', 'sha384', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'sha512', 'shake_128', 'shake_256']
#>>> hashlib.algorithms_available
#{'SHA256', 'sha224', 'SHA', 'md4', 'SHA224', 'RIPEMD160', 'blake2b', 'ecdsa-with-SHA1', 'md5', 'sha', 'DSA', 'dsaEncryption', 'SHA384', 'MD5', 'sha3_384', 'DSA-SHA', 'SHA512', 'sha384', 'SHA1', 'ripemd160', 'blake2s', 'shake_256', 'sha3_256', 'sha3_512', 'dsaWithSHA', 'sha256', 'MD4', 'sha3_224', 'sha1', 'shake_128', 'sha512', 'whirlpool'

hashName = [ 'SHA256', 'SHA384', 'BLAKE2b', 'sha3_256' ]
#hashName = [ 'sha256' ]
def doFile(fn):
	hstate = {}
	for hn in hashName:
		hstate[hn] = hashlib.new(hn.lower())
	fh = open(fn,'rb')
	sz = 1024*1024
	while True:
		buf = fh.read(sz)
		if len(buf) == 0:
			break
		for hs in hstate.values():
			hs.update(buf)
	fh.close()
	for hn,hs in hstate.items():
		if hn=='sha256':
			print('%s  %s'%(hs.hexdigest(),fn))
		b64=base64.b64encode(hs.digest()).decode('utf-8')
		if b64[-2] == '=':
			b64=b64[:-2]
		elif b64[-1] == '=':
			b64=b64[:-1]
		print('%s (%s) = %s'%(hn,fn,hs.hexdigest()))
def chk(fn):
	hs = hashlib.sha256()
	fh = open(fn,'rb')
	sz = 1024*1024
	while True:
		buf = fh.read(sz)
		if len(buf) == 0:
			break
		hs.update(buf)
	fh.close()
	return hs.hexdigest()
chkBsdFa = re.compile('(?P<hn>[^ ]*) \((?P<fn>[^)]*)\) = (?P<hd>.*)')
def chkBsd(ln):
	#print('chkBsd %s'%(ln))
	mo = chkBsdFa.search(ln)
	if mo == None:
		return 0
	hn = mo.group('hn')
	fn = mo.group('fn')
	hd = mo.group('hd')
	print('chkBsd hn:%s fh:%s hd:%s'%(hn,fn,hd))
	hs = hashlib.new(hn.lower())
	fh = open(fn,'rb')
	sz = 1024*1024
	while True:
		buf = fh.read(sz)
		if len(buf) == 0:
			break
		hs.update(buf)
	fh.close()
	if hd != hs.hexdigest():
		print('%s: FAILED'%(fn))
		return 1
	print('%s: OK'%(fn))
	return 0
	

start=1
if sys.argv[1] == '-c':
	rv = 0
	cnt=0
	with open(sys.argv[2]) as fh:
		for l in fh:
			cnt += 1
			if l.find('(') != -1:
				rv += chkBsd(l.strip())
				continue
			sha2h = l[0:64]
			fn = l[66:].strip()
			curh = chk(fn)
			if curh != sha2h:
				#print('%s %s debug'%(curh, sha2h))
				print('%s: FAILED'%(fn))
				rv += 1
			else:
				print('%s: OK'%(fn))
	if rv > 0:
		print("WARNING: %d of %d computed checksums did NOT match"%(rv,cnt))
	sys.exit(rv)
			
for fn in sys.argv[1:]:
	doFile(fn)
