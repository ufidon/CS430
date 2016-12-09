#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
import subprocess
import argparse
import binascii


# 0    1     2  3                          4  5    6   7          8    9	
# AesU -e[d] -k key <-i initial_vector>    -m ecb  -in input_file -out output_file

ps = argparse.ArgumentParser()

ps.add_argument_group()
ps.add_argument('-k', action='store',  dest='key', help='key')
ps.add_argument('-i', action='store',  dest='iv', help='initial vector or counter')
ps.add_argument('-m', action='store',  dest='mode', help='operation mode')
ps.add_argument('-in', action='store',  dest='ifile', help='input file' )
ps.add_argument('-out', action='store',  dest='ofile', help='output file')
ps.add_argument('--version', action='version', version='%(prog)s 1.0')
ps.add_argument('-e', action='store_true',  dest='enc', help='encryption')
ps.add_argument('-d', action='store_true',  dest='dec', help='decryption')

params = ps.parse_args()

errorflag = 0
errormsg = ''

if((len(sys.argv) != 10) and (len(sys.argv) != 12)):
	errorflag |= (0x1 << 0)

if(params.dec == params.enc):
	errorflag |= (0x1 << 1)
	
if params.mode and (not ((params.mode.lower() == 'ecb') or \
   (params.mode.lower() == 'cbc') or \
   (params.mode.lower() == 'cfb') or \
   (params.mode.lower() == 'ofb') or \
   (params.mode.lower() == 'ctr'))):
	errormsg += 'unsupported mode!\n'
	errorflag |= (0x1 << 2)

keylen = len(params.key) * 4 if params.key else 0
ivlen = len(params.iv) * 4 if params.iv else 0	
if params.iv and (ivlen != 128):
	errormsg += 'the length of initial vector can only be 128\n'
	errorflag |= (0x1 << 3)
	
if params.key and ( not ((keylen == 128) or (keylen ==192) or (keylen ==256))):
	errormsg += 'key length is incorrect\n'
	errorflag |= (0x1 << 4)
	
# 0    1     2  3                          4  5    6   7          8    9	
# AesU -e[d] -k key <-i initial_vector>    -m ecb  -in input_file -out output_file
# 0    1     2  3    4  5    				6   7                8    9		    10  11
# AesU -e[d] -k key <-i initial_vector>    -m cbc[cfb,ofb,ctr]  -in input_file -out output_file
if not (((params.enc or params.dec) and params.key and params.mode and \
		 params.ifile and params.ofile and \
		 (params.enc != params.dec) and \
		 (params.key != None) and (params.mode.lower()=='ecb') and \
		 (params.ifile != None) and (params.ofile != None)) \
		or \
		((params.enc or params.dec) and params.key and params.mode and \
		 params.ifile and params.ofile and params.iv and \
		 (params.enc != params.dec) and \
		 (params.key != None) and (params.iv != None) and \
		 ((params.mode.lower()=='cbc') or (params.mode.lower()=='cfb') or \
		  (params.mode.lower()=='ofb') or (params.mode.lower()=='ctr') ) and \
		 (params.ifile != None) and (params.ofile != None))):
	errormsg += 'incorrect combination of parameters\n'
	errorflag |= (0x1 << 5)
	
if(errorflag):
	print('---------Error Message-----------')
	print('errorcode:', errorflag)
	print('errormsg:', errormsg)
	print('---------------------------------')
	ps.print_help()
	sys.exit(-1)

print('------parameters list---------')
print('encrypt     =', params.enc)
print('decrypt     =', params.dec)
print('key		   =', params.key)
print('initial vec =', params.iv)
print('mode		   =', params.mode)
print('input file  =', params.ifile)
print('output file =', params.ofile)
print('------------------------------')


# 0    1     2  3                          4  5    6   7          8    9	
# AesU -e[d] -k key <-i initial_vector>    -m ecb  -in input_file -out output_file	
# openssl enc -aes-128-ecb -d -K 11223344556677889900112233445566
# -v -nosalt -in poem128ecb.txt -out dpoem128ecb.txt
eord = ' -e '
if(params.dec): eord = ' -d '

# padding if only needed
inlen = os.stat(params.ifile).st_size if params.ifile else 0
padding = ' -nopad '
if ((inlen % 16 != 0) and ((params.mode.lower()=='ecb') or (params.mode.lower()=='cbc')) ):
	padding = ''

ofile = params.ofile
ifile = params.ifile
if(params.mode.lower()=='ctr'):
	eord = ' -e '
	#do ecb on counter then xor the cipher output and plaintext to get the ciphertext
	cipher = " -aes-"+str(keylen)+"-"+'ecb'
	ofile = 'otmp'
	ifile = 'itmp'
	ctrdatalen = inlen//16 + 1
	ctrdata=b''
	counter = binascii.a2b_hex(params.iv)
	x = int.from_bytes(counter, 'little')
	for i in range(ctrdatalen):
		ctrdata += counter		
		x += 1
		x %= 0x100000000000000000000000000000000
		counter = x.to_bytes(16, 'little')
		fitmp = open(ifile, 'wb+')
		fitmp.write(ctrdata)
		fitmp.flush()
		fitmp.close()
else:
	cipher = " -aes-"+str(keylen)+"-"+params.mode.lower()

if(params.iv == None):
	iv = ''
else:
	iv = ' -iv ' + params.iv + ' '


cmd = 'openssl enc ' + cipher + eord +  ' -K ' + params.key + iv +\
  ' -v -nosalt ' + padding + ' -in '+ifile + ' -out '+ ofile

print('......\n'+cmd+'\n......\n')
rc = subprocess.check_output(cmd)

if(params.mode.lower()=='ctr'):
	# handle ctr mode separately
	fikeystream = open(ofile, 'rb')
	ikeystream = fikeystream.read()
	fikeystream.close()
	
	focipher = open(params.ofile, 'wb+')
	
	fifile = open(params.ifile, 'rb')
	sinput = fifile.read()
	fifile.close()
	
	soutput=b''
	for i in range(inlen):
		soutput += bytes([sinput[i] ^ ikeystream[i]])
		#print(soutput)
	focipher.write(soutput)
	focipher.flush()
	focipher.close()
	
	os.remove(ofile)
	os.remove(ifile)

# handle ctr mode separately	
	
# 0    1     2  3    4  5    				6   7                8    9		    10  11
# AesU -e[d] -k key <-i initial_vector>    -m cbc[cfb,ofb,ctr]  -in input_file -out output_file
	


