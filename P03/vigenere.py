#!/usr/bin/env python
# -*- coding: utf-8 -*-

def encrypt(plain, key, alphabet):
	""" encryption
		plain --- plain text
		key	--- symmetric key
		alphabet --- a list of characters consisting the alphabet
	"""
	rkey = key * ((len(plain)/len(key))+1)
	numofchar = len(alphabet)
	cipher = ''
	lenplain = len(plain)
	for i in range(lenplain):
		cipher += alphabet[(alphabet.index(plain[i])+alphabet.index(rkey[i])) % numofchar]
		 
	return cipher
		
def decrypt(cipher, key, alphabet):
	""" decryption
		cipher --- cipher text
		key	--- symmetric key
		alphabet --- a list of characters consisting the alphabet
	"""
	rkey = key * ((len(cipher)/len(key))+1)
	numofchar = len(alphabet)
	plain = ''
	lenplain = len(cipher)
	for i in range(lenplain):
		plain += alphabet[(alphabet.index(cipher[i]) - alphabet.index(rkey[i])) % numofchar]
		 
	return 	plain
		
if __name__ == '__main__':
	# generation of our printable alphabet
	alphabet = []
	for i in range(32, 127):
		alphabet.append(chr(i))
		
		
	print('alphabet:',''.join(alphabet))
	
	# test encryption
	key = 'hello'
	plain = "It's a nice day today!"
	print('plaintext:', plain)
	cipher = encrypt(plain, key, alphabet)
	print('ciphertext:',cipher)
	
	# test decryption
	deplain = decrypt(cipher, key, alphabet)
	print('decrypted plain:', deplain)