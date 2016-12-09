#!/usr/bin/env python
# -*- coding: utf-8 -*-

def encrypt(plain, key, alphabet):
	""" encryption
		plain --- plain text
		key	--- symmetric key
		alphabet --- a list of characters consisting the alphabet
	"""
	numofchar = len(alphabet)
	cipher = []
	for ch in plain:
		cipher.append(alphabet[(alphabet.index(ch)+key) % numofchar])
	return "".join(cipher)	
		
def decrypt(cipher, key, alphabet):
	""" decryption
		cipher --- cipher text
		key	--- symmetric key
		alphabet --- a list of characters consisting the alphabet
	"""
	numofchar = len(alphabet)
	plain = []
	for ch in cipher:
		plain.append(alphabet[(alphabet.index(ch)-key) % numofchar])
	return "".join(plain)	
		
if __name__ == '__main__':
	# test encryption
	alphabet = ['0','1','2','3','4','5','6','7','8','9']
	plain = "19990808"
	print("original plaintext:", plain)
	key = 3
	cipher = encrypt(plain, key, alphabet)
	print(cipher)
	
	#test decryption
	decrypted_plain = decrypt(cipher, key, alphabet)
	print(decrypted_plain)