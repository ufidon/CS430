#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
import subprocess

def sign(cfgfile, stdname, ext):
    # construct all file names
    csrfile = stdname + '.csr'
    csr64 = csrfile + '.64'
    crtfile = stdname + '.crt'
    crt64 = crtfile + '.64'
    
    # decode csrfile in base64
    cmd_d64 = 'openssl base64 -d -in ' + csr64 + ' -out ' + csrfile
    try:   
        r1 = subprocess.check_output(cmd_d64)
    except:
        print(cmd_d64 + ' failed')
        sys.exit(1)
        
    # sign  csr file   
    cmd_sign = 'openssl ca -config ' + cfgfile + ' -in ' + csrfile + ' -out '+crtfile + ext
    try:
        r2 = subprocess.check_output(cmd_sign)
    except:
        print(cmd_sign + ' failed')
        sys.exit(2)
        
    # encode crt to base64
    cmd_e64 = 'openssl base64 -e -in ' + crtfile + ' -out ' + crt64
    try:
        r3 = subprocess.check_output(cmd_e64)
    except:
        print(cmd_e64 + ' failed')
        sys.exit(3)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('usage: python sign.py [Subject Name]')
        sys.exit(-1)
    subject = sys.argv[1]
    sign('cis_ca.conf', subject, ' -extensions student_ext')
    