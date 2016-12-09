#!/usr/bin/env python
# -*- coding: utf-8 -*-


def encrypt(plain, key, rng, round):
	""" encryption
		plain --- plain text
		key	--- symmetric key, the seed
	"""
	plen = len(plain)
	plist = list(plain)
	
	pos = key
	
	for r in range(round):
		for i in range(plen):
			pos = rng(pos)%plen
			tmp = plist[i]
			plist[i] = plist[pos]
			plist[pos] = tmp
		
	return ''.join(plist)
		
def decrypt(cipher, key, rng, round):
	""" decryption
		cipher --- cipher text
		key	--- symmetric key, the seed
	"""
	clen = len(cipher)
	clist = list(cipher)
	
	pos = key
	swap = []
	
	for r in range(round):
		for i in range(clen):
			pos = rng(pos)%clen
			swap.append(pos)
		
	
	for r in range(round-1, -1, -1):
		for i in range(clen-1, -1, -1):
			tmp = clist[i]
			clist[i] = clist[swap[i+r*clen]]
			clist[swap[i+r*clen]] = tmp
		
	return ''.join(clist)
		
if __name__ == '__main__':
	rng = lambda x: (7**5)*x % (2**31 - 1)
	# test encryption
	plain = "What a nice day today!"
	print("original plaintext:", plain)
	key = 171
	cipher = encrypt(plain, key, rng, 10)
	print('cipher text:', cipher)
	
	#test decryption
	decrypted_plain = decrypt(cipher, key, rng, 10)
	print('decrepted plaintext:', decrypted_plain)