#!/usr/bin/env python
# -*- coding: utf-8 -*-

def encrypt(plain, key, alphabet):
	""" encryption
		plain --- plain text
		key	--- symmetric key
		alphabet --- a list of characters consisting the alphabet
	"""
	numofchar = len(alphabet)
	lenplain = len(plain)
	cipher = []
	for i in range(lenplain):
		cipher.append( alphabet.index(plain[i]) ^ key.index(key[i]))
	return cipher	
		
def decrypt(cipher, key, alphabet):
	""" decryption
		cipher --- cipher text
		key	--- symmetric key
		alphabet --- a list of characters consisting the alphabet
	"""
	numofchar = len(alphabet)
	lencipher = len(cipher)
	plain = ''
	for i in range(lencipher):
		plain += alphabet[cipher[i] ^ key.index(key[i])]
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