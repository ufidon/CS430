#!/usr/bin/env python
# -*- coding: utf-8 -*-

# reviszed from https://gist.github.com/williame/94beef4b9afea659864950c29d402b90
# http://wiki.franklinheath.co.uk/index.php/Enigma/Paper_Enigma
#

def Ord(ch): return ord(ch) - ord('A') # convert A-Z to 0-25
def Chr(ch): return chr(ch + ord('A')) # convert 0-25 to A-Z

# skip every character other than A-Z
def Text(s): return "".join(ch for ch in s if ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# compare with carrying of number system,
# notches are carries to higher position
Rotors = { # name: (wiring, notches) 
        "I":    ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"), # 1930 Enigma I
        "II":   ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"), # 1930 Enigma I
        "III":  ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"), # 1930 Enigma I
        "IV":   ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"), # December 1938 M3 Army
        "V":    ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"), # December 1938 M3 Army
        "VI":   ("JPGVOUMFYQBENHZRDKASXLICTW", "ZM"), # 1939 M3 & M4 Naval (FEB 1942)
        "VII":  ("NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM"), # 1939 M3 & M4 Naval (FEB 1942)
        "VIII": ("FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM"), # 1939 M3 & M4 Naval (FEB 1942)
        "Beta": ("LEYJVCNIXWPBQMDRTAKZGFUHOS", ""), # Spring 1941 M4 R2
        "Gamma":("FSOKANUERHMBTIYCWLQPZXVGJD", ""), # Spring 1942 M4 R2
        
        # reflectors
        "A":    ("EJMZALYXVBWFCRQUONTSPIKHGD", ""),
        "B":    ("YRUHQSLDPXNGOKMIEBFZCWVJAT", ""), 
        "C":    ("FVPJIAOYEDRZXWGCTKUQSBNMHL", ""), 
        "B Thin": ("ENKQAUYWJICOPBLMDXZVFTHRGS", ""), # 1940 M4 R1 (M3 + Thin)
        "C Thin": ("RDOBJNTKVEHMLFCWZAXGYIPSUQ", ""), # 1940 M4 R1 (M3 + Thin)
    }

class Rotor:
    # Rotor("B"), Rotor("I", 'A', 1)
    def __init__(self, table, ofs='A', ring=1):
        self.rotor, (table, notches) = table, Rotors[table]
        self.atable =  table

        self.akey = ofs
        self.anotches = notches
        self.aring = str(ring)
        
        self.table = [Ord(ch) for ch in table] 
        self.reciprocal = [self.table.index(i) for i in range(26)]

        
        self.ring = ring - 1        
        self.notches = [(n - self.ring) % 26 for n in map(Ord, notches)]
        self.ofs = Ord(ofs) - self.ring
        
        self.nenter = self.ofs;
        self.nexit = self.table[self.ofs]
        
        self.ringtable=[(self.ofs+i)%26 for i in range(26)]
        self.aringtable = "".join(Chr(i) for i in self.ringtable)

        
    def knocks(self): return (self.ofs % 26) in self.notches
    
    def config(self):
        print(self.rotor.rjust(6), ':'+self.atable+':'+self.anotches.rjust(3)+':'+self.akey+':'+self.aring)
        
    def status(self, enter=1):
        print('')
        print(''.rjust(19), "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        print(''.rjust(19), self.aringtable)
        if enter:
            print(self.rotor.rjust(6), ':', str(self.ofs).rjust(2),':', str(self.nenter).rjust(2) ,':', self.atable.rjust(27))
        else:
            print(self.rotor.rjust(6), ':', str(self.ofs).rjust(2),':', str(self.nexit).rjust(2) ,':', self.atable.rjust(27))
    
    def advance(self): 
        self.ofs += 1
        self.ringtable = [(self.ofs+i)%26 for i in range(26)]
        self.aringtable = "".join(Chr(i) for i in self.ringtable)
        self.atable = "".join([Chr(self.table[(i+self.ofs) % 26]) for i in range(26)])
    
    def enter(self, ch, ofs):
        self.nenter = self.table[(ch + self.ofs - ofs) % 26]
        return self.nenter
    def exit(self, ch, ofs): 
        self.nexit = self.reciprocal[(ch + self.ofs - ofs) % 26]
        return self.nexit

class Machine:
    def __init__(self, plugboard, *rotors):
        self.plugboard = list(range(26))
        for pair in plugboard.split():
            a, b = map(Ord, pair)
            self.plugboard[a] = b
            self.plugboard[b] = a
        self.rotors = rotors # natural order is reflector, left, middle, right
        
    def transcode(self, message, expected=None):
        out = ""
        for ch in message:
            if not Text(ch): # whitespace etc
                out += ch
                continue
            # advance rotors; the three rightmost can rotate
            left, middle, right = self.rotors[-3:]
            if middle.knocks():
                left.advance()
                middle.advance()
            elif right.knocks():
                middle.advance()
            right.advance()
            # transcode character
            
            ofs = 0
            ch = self.plugboard[Ord(ch)] # through the plugboard
            for rotor in self.rotors[::-1]: # through the rotors right to left and then reflector
                rotor.status()
                ch, ofs = rotor.enter(ch, ofs), rotor.ofs
            for rotor in self.rotors[1:]: # and back through the rotors left to right
                rotor.status()
                ch, ofs = rotor.exit(ch, ofs), rotor.ofs          
            ch = (ch - rotor.ofs) % 26 # unmap it
            ch = self.plugboard[ch] # and back through the plugboard
            
            out += Chr(ch)
        if expected: assert Text(expected) == Text(out), "\nEXP: %s\nGOT: %s" % (expected, out)
        return out


if __name__ == '__main__':
    # from http://wiki.franklinheath.co.uk/index.php/Enigma/Paper_Enigma
    print( Machine("", Rotor("B"), Rotor("I", 'A', 1), Rotor("II", 'B', 1), Rotor("III", 'C', 1)).\
        transcode("AEFAE JXXBN XYJTY", "CONGRATULATIONS"))
    
    print( Machine("", Rotor("B"), Rotor("I", 'A', 1), Rotor("II", 'B', 1), Rotor("III", 'C', 1)).\
        transcode("CONGRATULATIONS"))
    print( Machine("", Rotor("B"), Rotor("I", 'A', 1), Rotor("II", 'B', 1), Rotor("III", 'R', 1)).\
        transcode("MABEK GZXSG", "TURN MIDDLE"))
    print( Machine("", Rotor("B"), Rotor("I", 'A', 1), Rotor("II", 'D', 1), Rotor("III", 'S', 1)).\
        transcode("RZFOG FYHPL", "TURNS THREE"))
    print( Machine("", Rotor("B"), Rotor("I", 'X', 10), Rotor("II", 'Y', 14), Rotor("III", 'Z', 21)).\
        transcode("QKTPE BZIUK", "GOOD RESULT"))
    print( Machine("AP BR CM FZ GJ IL NT OV QS WX", Rotor("B"), Rotor("I", 'V', 10), Rotor("II", 'Q', 14), Rotor("III", 'Q', 21)).\
        transcode("HABHV HLYDF NADZY", "THATS IT WELL DONE"))
    
    # from http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages
    # Enigma Instruction Manual, 1930
    print( Machine("AM FI NV PS TU WZ", Rotor("A"), Rotor("II", 'A', 24), Rotor("I", 'B', 13), Rotor("III", 'L', 22)).\
        transcode("GCDSE AHUGW TQGRK VLFGX UCALX VYMIG MMNMF DXTGN VHVRM MEVOU YFZSL RHDRR XFJWC FHUHM UNZEF RDISI KBGPM YVXUZ",
                  "FEIND LIQEI NFANT ERIEK OLONN EBEOB AQTET XANFA NGSUE DAUSG ANGBA ERWAL DEXEN DEDRE IKMOS TWAER TSNEU STADT"))
    # Operation Barbarossa, 1941
    print( Machine("AV BS CG DL FU HZ IN KM OW RX", Rotor("B"), Rotor("II", 'B', 2), Rotor("IV", 'L', 21), Rotor("V", 'A', 12)).\
        transcode("EDPUD NRGYS ZRCXN UYTPO MRMBO FKTBZ REZKM LXLVE FGUEY SIOZV EQMIK UBPMM YLKLT TDEIS MDICA GYKUA CTCDO MOHWX MUUIA UBSTS LRNBZ SZWNR FXWFY SSXJZ VIJHI DISHP RKLKA YUPAD TXQSP INQMA TLPIF SVKDA SCTAC DPBOP VHJK-",
                  "AUFKL XABTE ILUNG XVONX KURTI NOWAX KURTI NOWAX NORDW ESTLX SEBEZ XSEBE ZXUAF FLIEG ERSTR ASZER IQTUN GXDUB ROWKI XDUBR OWKIX OPOTS CHKAX OPOTS CHKAX UMXEI NSAQT DREIN ULLXU HRANG ETRET ENXAN GRIFF XINFX RGTX-"))
    print( Machine("AV BS CG DL FU HZ IN KM OW RX", Rotor("B"), Rotor("II", 'L', 2), Rotor("IV", 'S', 21), Rotor("V", 'D', 12)).\
        transcode("SFBWD NJUSE GQOBH KRTAR EEZMW KPPRB XOHDR OEQGB BGTQV PGVKB VVGBI MHUSZ YDAJQ IROAX SSSNR EHYGG RPISE ZBOVM QIEMM ZCYSG QDGRE RVBIL EKXYQ IRGIR QNRDN VRXCY YTNJR",
                  "DREIG EHTLA NGSAM ABERS IQERV ORWAE RTSXE INSSI EBENN ULLSE QSXUH RXROE MXEIN SXINF RGTXD REIXA UFFLI EGERS TRASZ EMITA NFANG XEINS SEQSX KMXKM XOSTW XKAME NECXK"))
    # U-264 (Kapitänleutnant Hartwig Looks), 1942
    print( Machine("AT BL DF GJ HM NW OP QY RZ VX", Rotor("B Thin"), Rotor("Beta", 'V', 1), Rotor("II", 'J', 1), Rotor("IV", 'N', 1), Rotor("I", 'A', 22)).\
        transcode("NCZW VUSX PNYM INHZ XMQX SFWX WLKJ AHSH NMCO CCAK UQPM KCSM HKSE INJU SBLK IOSX CKUB HMLL XCSJ USRR DVKO HULX WCCB GVLI YXEO AHXR HKKF VDRE WEZL XOBA FGYU JQUK GRTV UKAM EURB VEKS UHHV OYHA BCJW MAKL FKLM YFVN RIZR VVRT KOFD ANJM OLBG FFLE OPRG TFLV RHOW OPBE KVWM UQFM PWPA RMFH AGKX IIBG",
                  "VONV ONJL OOKS JHFF TTTE INSE INSD REIZ WOYY QNNS NEUN INHA LTXX BEIA NGRI FFUN TERW ASSE RGED RUEC KTYW ABOS XLET ZTER GEGN ERST ANDN ULAC HTDR EINU LUHR MARQ UANT ONJO TANE UNAC HTSE YHSD REIY ZWOZ WONU LGRA DYAC HTSM YSTO SSEN ACHX EKNS VIER MBFA ELLT YNNN NNNO OOVI ERYS ICHT EINS NULL"))
    # Scharnhorst (Konteradmiral Erich Bey), 1943
    print( Machine("AN EZ HK IJ LR MQ OT PV SW UX", Rotor("B"), Rotor("III", 'U', 1), Rotor("VI", 'Z', 8), Rotor("VIII", 'V', 13)).\
        transcode("YKAE NZAP MSCH ZBFO CUVM RMDP YCOF HADZ IZME FXTH FLOL PZLF GGBO TGOX GRET DWTJ IQHL MXVJ WKZU ASTR",
                  "STEUE REJTA NAFJO RDJAN STAND ORTQU AAACC CVIER NEUNN EUNZW OFAHR TZWON ULSMX XSCHA RNHOR STHCO"))