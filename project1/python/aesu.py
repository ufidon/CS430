#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from subprocess import call

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))


print ('show in another way:')

for a in sys.argv:
	print (a)
	

# 0    1     2  3                          4  5    6   7          8    9	
# AesU -e[d] -k key <-i initial_vector>    -m ecb  -in input_file -out output_file
print ('acess parameters one by one')

for i in range(len(sys.argv)):
	print (sys.argv[i])
	
	
# aes-128-ecb -d -K 11223344556677889900112233445566
# -v -nosalt -in poem128ecb.txt -out dpoem128ecb.txt
keylen = len(sys.argv[3])
cipher = "-aes-"+str(keylen*4)+"-"+sys.argv[5]

call(["openssl", "enc", cipher, "-K", sys.argv[3], "-v", "-nosalt", sys.argv[6], sys.argv[7],sys.argv[8],sys.argv[9]])	