#!/usr/bin/env python
# -*- coding: utf-8 -*-

def i2j(strin):
	''' convert all 'i's in strin to 'j'
	'''
	ilist = list(strin)
	olist = []
	
	for ch in ilist:
		if ch == 'i':
			olist.append('j')
		else:
			olist.append(ch)
	
	return "".join(olist)


def rmdup(password):
	''' remove duplicates
	'''

	#charlist = [ch for ch in password if not (ch in occured or occured.add(ch))]
	newpass = i2j(password)

	occured = set()
	key = ""			
	for ch in newpass:
		if ch not in occured:
			key += ch
			occured.add(ch)
			
	return key

def gendigram(plain, pad='x'):
	jplain = i2j(plain)
	
	numchar = len(jplain)
	
	digram = []
	i = 0
	while((i < numchar) and (i+1<numchar)):
		if jplain[i] != jplain[i+1]:
			digram.append(jplain[i:i+2])
			i += 2
		else:
			digram.append(jplain[i]+pad)
			i += 1
		
		if(i == numchar-1):
				digram.append(jplain[i]+pad)
	return digram

def genmatrix(key):
	''' generate the 5x5 matrix used for playfair cipher from the key and alphabet
	'''
	alphabet = ['a','b','c','d','e',
				'f','g','h','j','k',
				'l','m','n','o','p',
				'q','r','s','t','u',
				'v','w','x','y','z']
	keylist = list(key)
	
	for ch in key:
		del alphabet[alphabet.index(ch)]
		
	matrix = keylist + alphabet
	return "".join(matrix)

def row(ch, matrix):
	return matrix.index(ch) // 5

def col(ch, matrix):
	return matrix.index(ch) % 5

def encrypt(plain, key):
	""" encryption
		plain --- plain text
		key	--- symmetric key
	"""
	jkey = i2j(key)
	rkey = rmdup(jkey)
	matrix = genmatrix(rkey)
	
	digrams = gendigram(plain)
	
	cipher = []
	cip0 = cip1 = ''
	
	for di in digrams:
		r0 = row(di[0], matrix)
		r1 = row(di[1], matrix)
		c0 = col(di[0], matrix)
		c1 = col(di[1], matrix)
		
		# same row
		if(r0 == r1):
			cip0 = matrix[r0*5 + (c0+1)%5]
			cip1 = matrix[r1*5 + (c1+1)%5]
		elif(c0 == c1):
			cip0 = matrix[((r0+1)%5)*5 + c0]
			cip1 = matrix[((r1+1)%5)*5 + c1]
		else:
			cip0 = matrix[r0*5 + c1]
			cip1 = matrix[r1*5 + c0]
			
		cipher.append(cip0+cip1)
		
	return cipher
		
def decrypt(cipher, key):
	""" encryption
		plain --- plain text
		key	--- symmetric key
	"""
	jkey = i2j(key)
	rkey = rmdup(jkey)
	matrix = genmatrix(rkey)
	
	
	digrams = []
	p0 = p1 = ''
	
	for di in cipher:
		r0 = row(di[0], matrix)
		r1 = row(di[1], matrix)
		c0 = col(di[0], matrix)
		c1 = col(di[1], matrix)
		
		# same row
		if(r0 == r1):
			p0 = matrix[r0*5 + (c0-1)%5]
			p1 = matrix[r1*5 + (c1-1)%5]
		elif(c0 == c1):
			p0 = matrix[((r0-1)%5)*5 + c0]
			p1 = matrix[((r1-1)%5)*5 + c1]
		else:
			p0 = matrix[r0*5 + c1]
			p1 = matrix[r1*5 + c0]
			
		digrams.append(p0+p1)
		
	plain = []
	for di in digrams:
		if(di[1] == 'x'):
			plain.append(di[0])
		else:
			plain.append(di)
		
	return plain
		
		
if __name__ == '__main__':
	# test key generation
	password = 'hello'
	plain = "itisawonderfulday"
	
	cipher = encrypt(plain, password)
	print ('ciphertext:', cipher)
	deplain = decrypt(cipher, password)
	print('decrypted plain:', ''.join(deplain))
	
	
	'''
	passwords = ("hello", "playfairexample")
	plain = "itisawonderfulday"
	for password in passwords:
		cipher = encrypt(plain, password)
		print (cipher)
		deplain = decrypt(cipher, password)
		print(deplain)
		
		print(gendigram(password))
		key = rmdup(password)
		matrix = genmatrix(key)
		print(key)
		print(matrix)
	'''