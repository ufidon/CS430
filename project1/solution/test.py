#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
import subprocess



if len(sys.argv) != 3:
    print('usage: python test [your program] [program type]')
    print('program type: java csharp python')
    sys.exit(-1)

plainfiles = ['poem712', 'poem720']
keys = ['11223344556677889900112233445566', '112233445566778899001122334455667788990011223344', '1122334455667788990011223344556611223344556677889900112233445566']
iv0 = '11223344556677889900112233445566'
modes = ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']

success = 0
fails = []
goods = []
count = 0
prog = sys.argv[1]
progtype = sys.argv[2]

ecmd0 = ''
if progtype == 'java':
    ecmd0 = 'java '+ prog + ' '
elif progtype == 'csharp':
    ecmd0 = prog + ' '
else:
    ecmd0 = 'python '+prog+' '
dcmd0 = ecmd0    
    
# 0    1     2  3                          4  5    6   7          8    9    
# AesU -e[d] -k key <-i initial_vector>    -m ecb  -in input_file -out output_file
# 0    1     2  3    4  5                    6   7                8    9            10  11
# AesU -e[d] -k key <-i initial_vector>    -m cbc[cfb,ofb,ctr]  -in input_file -out output_file    
    
print('------test begin------:')
for file in plainfiles:
    for key in keys:
        for mode in modes:
            count += 1
            pfile = file+'.txt'
            print('\ntest #'+str(count))
            print('plain file: '+pfile)
            print('key: '+key)
            print('mode: '+mode)
            keylen = str(len(key)*4)
            iv = '' if mode == 'ecb' else ' -i '+iv0+' '
            cipherfile = file+keylen+mode+'.txt'
            rcipherfile = 'r'+cipherfile
            dplain='d'+cipherfile
            rdplain = 'r'+dplain
            
            # encryption
            ecmd = ecmd0 + ' -e -k ' + key + iv + ' -m '+mode + ' ' + ' -in '+pfile + ' -out '+cipherfile
            print('encryption:\n'+ecmd)
            
            try:
                rce = subprocess.check_output(ecmd)
                rcc = subprocess.check_output('fc /b '+cipherfile+' '+rcipherfile)
                #print(rcc)
                if(rcc.decode('utf-8').find('no differences') != -1):
                    success += 1
                    goods.append(ecmd)
                else:
                    fails.append(ecmd)
            except:
                fails.append(ecmd)
                    
            # decryption
            dcmd = dcmd0 + ' -d -k ' + key + iv + ' -m '+mode + ' ' + ' -in '+cipherfile + ' -out '+dplain
            print('decryption:\n'+dcmd)
            
            try:
                rcd = subprocess.check_output(dcmd)
                rdc = subprocess.check_output('fc /b '+dplain+' '+rdplain)
                if(rdc.decode('utf-8').find('no differences') != -1):
                    success += 1
                    goods.append(dcmd)
                else:
                    fails.append(dcmd)
            except:
                fails.append(dcmd)
                 
                            
print('\n------test summary------:\n')
print('successs times: '+str(success))
for s in goods:
    print(s)

print('\n\n\n')
print('fails: ' + str(len(fails)))
for f in fails:
    print(f)
