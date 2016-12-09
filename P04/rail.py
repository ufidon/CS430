#!/usr/bin/env python
# -*- coding: utf-8 -*-

def encrypt(plain, key):
	""" encryption
	parameters:
		plain --- plain text
		key	--- number of rails
	returns:
		cipher
	"""
	if key == 1:
		return plain
	
	rails = []
	for i in range(key):
		rails.append('')
		
	d = 1
	rail = 0
	
	for ch in plain:
		rails[rail] += ch
		rail += d
		if rail == key:
			d = -1
			rail -= 2
		if rail == -1:
			d = 1
			rail += 2
			
	cipher = "".join(rails)
	return cipher
		
def decrypt(cipher, key):
	""" decryption
	parameters:
		cipher --- cipher text
		key	--- symmetric key
	returns:
		plain text
	"""
	if key == 1:
		return cipher
	
	# find the length of each rail
	raillens = []
	for i in range(key):
		raillens.append(0)
		
	d = 1
	rail = 0
	
	for ch in cipher:
		raillens[rail] += 1
		rail += d
		if rail == key:
			d = -1
			rail -= 2
		if rail == -1:
			d = 1
			rail += 2
			
	# populate each rail		
	rails = []
	for rail in range(key):
		rails.append([])
			
	begin = 0

	for rail in range(key):
		end = begin + raillens[rail]		
		rails[rail] = list(cipher[begin:end])
		begin = end

	d = 1
	rail = 0
	plain = ''
	
	for ch in cipher:
		plain += rails[rail].pop(0)
		rail += d
		if rail == key:
			d = -1
			rail -= 2
		if rail == -1:
			d = 1
			rail += 2	
			
	return plain	
	
	
		
if __name__ == '__main__':
	# test encryption
	plain = "what a nice day!"
	print("original plaintext:", plain)
	
	for key in (1,2,3,4):
		cipher = encrypt(plain, key)
		print(str(key)+':', cipher)
	
		#test decryption
		decrypted_plain = decrypt(cipher, key)
		print(str(key)+':', decrypted_plain)
		print('\n')