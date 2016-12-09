#!/usr/bin/env python
# -*- coding: utf-8 -*-

def encrypt(plain, key, alphabet, pad = None):
	""" encryption
		plain --- plain text
		key	--- symmetric key
		alphabet --- a list of characters consisting the alphabet
		pad --- padding the last line if needed
	"""
	
	keylen = len(key)
	
	r = len(plain) % keylen
	if((r > 0) and (pad != None) and (len(pad) == keylen-r)):
		plain += pad
		
	pplen = len(plain)
		
	col = []
	for i in range(keylen):
		col.append("")
		
	for i in range(pplen):
		col[i % keylen] += plain[i]
	
	aindex = []
	for ch in key:
		aindex.append(alphabet.index(ch))
	
	aindex.sort()
	
	cipher = ''
	for i in aindex:
		cipher += col[key.index(alphabet[i])]

	return cipher
		
def decrypt(cipher, key, alphabet, pad = None):
	""" decryption
		cipher --- cipher text
		key	--- symmetric key
		alphabet --- a list of characters consisting the alphabet
		pad --- padding the last line if needed
	"""
	keylen = len(key)
	
	col = []
	for i in range(keylen):
		col.append('')	
	
	# no padding, plen==clen
	plen = len(cipher)
	r = len(cipher) % keylen
	
	# padding
	padded = False
	if((r == 0) and (pad != None)):
		padded = True
		plen = len(cipher) - len(pad)
	
	# the length of each column: in the order of key
	collen = []
	for i in range(keylen):
		collen.append(len(cipher) // keylen)
	for i in range(r):
		collen[i] += 1
		
	# get order in alphabetic
	aindex = []
	for ch in key:
		aindex.append(alphabet.index(ch))
	
	aindex.sort()
				
	
	# get columns in the order of key
	begin = 0	
	for i in range(keylen):
		col[key.index(alphabet[aindex[i]])] = cipher[begin:begin+collen[key.index(alphabet[aindex[i]])]]
		begin += collen[key.index(alphabet[aindex[i]])]
		
	plain = ''
	for i in range(plen):
		plain += col[i%keylen][i//keylen]

	if(padded):
		plain = plain[0:plen]

	return plain	

		
if __name__ == '__main__':
	# generation of our printable alphabet
	alphabet = []
	for i in range(ord('A'), ord('A')+26):
		alphabet.append(chr(i))
	print('alphabet:', ''.join(alphabet))
		
	# test encryption
	plain = 'WEAREDISCOVEREDFLEEATONCE'
	pad = None
	key = 'ZEBRAS'
	
	print("original plaintext:", plain)

	cipher = encrypt(plain, key, alphabet, pad)
	print('ciphertext:', cipher)
	
	#test decryption
	decrypted_plain = decrypt(cipher, key, alphabet, pad)
	print('decryted plaintext:', decrypted_plain)