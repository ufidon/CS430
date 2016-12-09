#!/usr/bin/env python
# -*- coding: utf-8 -*-

def encrypt(plain, key, alphabet):
	""" encryption
		plain --- plain text
		key	--- symmetric key, a permutation of the alphabet
		alphabet --- a list of characters consisting the alphabet
	"""
	numofchar = len(alphabet)
	cipher = ''
	for ch in plain:
		cipher += key[alphabet.index(ch)]
	return cipher
		
def decrypt(cipher, key, alphabet):
	""" decryption
		cipher --- cipher text
		key	--- symmetric key
		alphabet --- a list of characters consisting the alphabet
	"""
	numofchar = len(alphabet)
	plain = ''
	for ch in cipher:
		plain += alphabet[key.index(ch)]
	return plain	
		
if __name__ == '__main__':
	# generation of our printable alphabet
	alphabet = []
	for i in range(32, 127):
		alphabet.append(chr(i))
		
		
	print('alphabet:',''.join(alphabet))
	
	key = []
	for i in range(127,31,-1):
		key.append(chr(i))
	
	# test encryption

	plain = "It's a nice day today!"
	print('plaintext:', plain)
	cipher = encrypt(plain, key, alphabet)
	print('ciphertext:',cipher)
	
	# test decryption
	deplain = decrypt(cipher, key, alphabet)
	print('decrypted plain:', deplain)