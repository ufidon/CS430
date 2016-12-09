#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Sep 6, 2016

@author: Ufidon
'''

def str2hex(str, encoding='ascii'):
    '''convert a text string to a hex string
    Keyword arguments:
        str             --- input text string
        encoding        --- encoding of str and strhex
    
    Returns: 
        strhex            --- string of hex
    '''
    shex = []
    
    for ch in str:
        shex.append(hex(ord(ch))[2:])
    
    strhex = "".join(shex)    
    return strhex

def hex2str(shex, encoding='ascii'):
    '''convert a hex string into a text string
    Keyword arguments:
        shex            --- input hex string
        encoding        --- encoding of shex and str        
    Returns:
        ostr             --- output string encoded with encoding
    '''
    
    sl = []
    for (a,b) in zip(shex[0::2],shex[1::2]):
        sl.append(chr(int(a+b, 16)))
    ostr = "".join(sl)
    
    return ostr;


if __name__ == '__main__':
    data = 'Attack our enemy'
    key = 'the lake is blue'
    print('size of data:', len(data),' ', 'size of key', len(key))
    print('data=', str2hex(data))
    print(hex2str(str2hex(data)))
    print('key=', str2hex(key))
    print(hex2str(str2hex(key)))
    
    print(hex2str('6e4317850cce7931225ed2ee59a0b802'))

    pass
