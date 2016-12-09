#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 参考 from https://gist.github.com/williame/94beef4b9afea659864950c29d402b90
# http://wiki.franklinheath.co.uk/index.php/Enigma/Paper_Enigma
#

def 字转位(字): return ord(字) - ord('A') # 转 A-Z 为 0-25
def 位转字(字): return chr(字 + ord('A')) #  转 0-25为 A-Z

# 跳过非 A-Z 符号
def 列转串(文): return "".join(字 for 字 in 文  if 字 in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# 当前轮转至缺口时高位轮转一格(齿), 一个字母或一个数字
轮集 = { # 轮名: (绕线, 缺口集 ) 
        # 每个轮定义了一个字母集的绕线映射, 面对德密机, 轮子从右至左的绕线;  
        # 轮子右边定义:从其轴线看轮子,其上面的数字是顺时针递增排列的; 左边反之
        # 从左至右可以得到相应的逆射表
         #      ('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        "I":    ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"), # 1930 Enigma I型
        "II":   ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"), # 1930 Enigma I型
        "III":  ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"), # 1930 Enigma I型
        "IV":   ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"), #  1938亥月 M3 陆军型
        "V":    ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"), #   1938亥月 M3陆军型
        "VI":   ("JPGVOUMFYQBENHZRDKASXLICTW", "ZM"), # 1939 M3型 & M4海军型  (FEB 1942)
        "VII":  ("NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM"), # 1939 M3型 & M4海军型 (FEB 1942)
        "VIII": ("FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM"), # 1939 M3型 & M4海军型 (FEB 1942)
        "Beta": ("LEYJVCNIXWPBQMDRTAKZGFUHOS", ""), #  1941春 M4 型R2(第二版)
        "Gamma":("FSOKANUERHMBTIYCWLQPZXVGJD", ""), #  1942春 M4型 R2(第二版)
        
        # 反射器
        "A":    ("EJMZALYXVBWFCRQUONTSPIKHGD", ""),
        "B":    ("YRUHQSLDPXNGOKMIEBFZCWVJAT", ""), 
        "C":    ("FVPJIAOYEDRZXWGCTKUQSBNMHL", ""), 
        "B薄": ("ENKQAUYWJICOPBLMDXZVFTHRGS", ""), # 1940 M4 R1 (M3 +薄)型
        "C薄": ("RDOBJNTKVEHMLFCWZAXGYIPSUQ", ""), # 1940 M4 R1 (M3 +薄)型
    }

class 轮:
    # 例子: 轮("B"), 轮("I", 'A', 1). 初始偏移字就是密码. 此偏移相对于固定的输入输出端的起始位'A'
    def __init__(self, 轮名, 偏移字='A', 环位=1):
        self.轮名, (映射表, 缺口集) = 轮名, 轮集[轮名]
        
        self.映射表 = [字转位(字) for 字 in 映射表]  # 转字母映射表为数字映射表
        self.逆射表 = [self.映射表.index(i) for i in range(26)]
        
        self.环位 = 环位 - 1    # 蟒语之列索引号从0开始    
        self.缺口集 = [(缺口 - self.环位) % 26 for 缺口 in map(字转位, 缺口集)]
        self.偏移位 = (字转位(偏移字) - self.环位)%26
       
      
    def 到缺口(self): return (self.偏移位 % 26) in self.缺口集
    
    def 转齿轮(self):  # 从右边看进去,齿轮逆时针转动, 面向德密机,齿轮朝操作员方向转动,轮上跑向操作员的数字递增
        self.偏移位 += 1

    
    def 入(self, 字, 偏移):
        self.入字 = self.映射表[(字 + self.偏移位 - 偏移) % 26]
        return self.入字
    def 出(self, 字, 偏移): 
        self.出字 = self.逆射表[(字 + self.偏移位 - 偏移) % 26]
        return self.出字

class 德密机:
    def __init__(self, 插线板, *轮群):
        self.插线板 = list(range(26))
        for 字对 in 插线板.split():
            a, b = map(字转位, 字对)
            self.插线板[a] = b
            self.插线板[b] = a
        self.轮群 = 轮群 # 面向德密机,轮子排列从左至右依次为:反射轮, 左轮, 中伦, 右轮
        
    def 加解密(self, 消息, 结果=None):
        输出 = ""
        for 字 in 消息:
            if not 列转串(字): # 跳过非A-Z符号, 只加密A-Z字母
                输出 += 字
                continue
            # 转齿 轮群; 只有最右边三个或四个轮可以转动
            左轮, 中轮, 右轮 = self.轮群[-3:]
            if 中轮.到缺口():
                左轮.转齿轮()
                中轮.转齿轮() # 德密机不同于加法进位之处, 也是困惑盟军之处
            elif 右轮.到缺口():
                中轮.转齿轮()
            右轮.转齿轮()
            
            #单字转换
            
            偏移 = 0 # 输入无偏移
            字位 = self.插线板[字转位(字)] # 通过插线板
            for 轮 in self.轮群[::-1]: # 通过轮群: 右轮 至 左轮 再到反射轮
                字位, 偏移 = 轮.入(字位, 偏移), 轮.偏移位
            for 轮 in self.轮群[1:]: # 反向通过 轮群: 左轮 到 右轮
                字位, 偏移 = 轮.出(字位, 偏移), 轮.偏移位          
            字位 = (字位 - 轮.偏移位) % 26 # 
            字位 = self.插线板[字位] # 回到 插线板
            
            输出 += 位转字(字位)
        if 结果: assert 列转串(结果) == 列转串(输出), "\nEXP: %s\nGOT: %s" % (结果, 输出)
        return 输出

def 测试(密码='AAA', 消息='HI'):
    密码=密码.upper()
    消息 = 消息.upper()
    print( 德密机("AP BR CM FZ GJ IL NT OV QS WX", 轮("B"), 轮("I", 密码[0], 10), 轮("II", 密码[1], 14), 轮("III", 密码[2], 21)).\
        加解密(消息))
    
def 测项(密码='AAA'):
    密码=密码.upper()
    消息 =('symmetric cipher', 'RSA is a public cipher', 'hash function', 'digital signature', 'Openssl is great' )
    
    for 条 in 消息:
        条 = 条.upper()
        print( 德密机("AP BR CM FZ GJ IL NT OV QS WX", 轮("B"), 轮("I", 密码[0], 3), 轮("II", 密码[1], 10), 轮("III", 密码[2], 19)).\
        加解密(条))    

def 三轮全测( 密码='XYZ', 消息='Merry New Year!', 插线='AP BR CM FZ GJ IL NT OV QS WX', 环设=(10,14,21)):
    插线=插线.upper()
    密码=密码.upper()
    消息 = 消息.upper()
    print( 德密机(插线, 轮("B"), 轮("I", 密码[0], 环设[0]), 轮("II", 密码[1],  环设[1]), 轮("III", 密码[2],  环设[2])).\
        加解密(消息))   

if __name__ == '__main__':
    # 摘自 http://wiki.franklinheath.co.uk/index.php/Enigma/Paper_Enigma
    print( 德密机("", 轮("B"), 轮("I", 'A', 1), 轮("II", 'B', 1), 轮("III", 'C', 1)).\
        加解密("AEFAE JXXBN XYJTY", "CONGRATULATIONS"))
    
    print( 德密机("", 轮("B"), 轮("I", 'A', 1), 轮("II", 'B', 1), 轮("III", 'C', 1)).\
        加解密("CONGRATULATIONS"))
    print( 德密机("", 轮("B"), 轮("I", 'A', 1), 轮("II", 'B', 1), 轮("III", 'R', 1)).\
        加解密("MABEK GZXSG", "TURN MIDDLE"))
    print( 德密机("", 轮("B"), 轮("I", 'A', 1), 轮("II", 'D', 1), 轮("III", 'S', 1)).\
        加解密("RZFOG FYHPL", "TURNS THREE"))
    print( 德密机("", 轮("B"), 轮("I", 'X', 10), 轮("II", 'Y', 14), 轮("III", 'Z', 21)).\
        加解密("QKTPE BZIUK", "GOOD RESULT"))
    print( 德密机("AP BR CM FZ GJ IL NT OV QS WX", 轮("B"), 轮("I", 'V', 10), 轮("II", 'Q', 14), 轮("III", 'Q', 21)).\
        加解密("HABHV HLYDF NADZY", "THATS IT WELL DONE"))
    
    # 摘自 http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages
    # 德密机指南, 1930
    print( 德密机("AM FI NV PS TU WZ", 轮("A"), 轮("II", 'A', 24), 轮("I", 'B', 13), 轮("III", 'L', 22)).\
        加解密("GCDSE AHUGW TQGRK VLFGX UCALX VYMIG MMNMF DXTGN VHVRM MEVOU YFZSL RHDRR XFJWC FHUHM UNZEF RDISI KBGPM YVXUZ",
                  "FEIND LIQEI NFANT ERIEK OLONN EBEOB AQTET XANFA NGSUE DAUSG ANGBA ERWAL DEXEN DEDRE IKMOS TWAER TSNEU STADT"))
    # Operation Barbarossa, 1941
    print( 德密机("AV BS CG DL FU HZ IN KM OW RX", 轮("B"), 轮("II", 'B', 2), 轮("IV", 'L', 21), 轮("V", 'A', 12)).\
        加解密("EDPUD NRGYS ZRCXN UYTPO MRMBO FKTBZ REZKM LXLVE FGUEY SIOZV EQMIK UBPMM YLKLT TDEIS MDICA GYKUA CTCDO MOHWX MUUIA UBSTS LRNBZ SZWNR FXWFY SSXJZ VIJHI DISHP RKLKA YUPAD TXQSP INQMA TLPIF SVKDA SCTAC DPBOP VHJK-",
                  "AUFKL XABTE ILUNG XVONX KURTI NOWAX KURTI NOWAX NORDW ESTLX SEBEZ XSEBE ZXUAF FLIEG ERSTR ASZER IQTUN GXDUB ROWKI XDUBR OWKIX OPOTS CHKAX OPOTS CHKAX UMXEI NSAQT DREIN ULLXU HRANG ETRET ENXAN GRIFF XINFX RGTX-"))
    print( 德密机("AV BS CG DL FU HZ IN KM OW RX", 轮("B"), 轮("II", 'L', 2), 轮("IV", 'S', 21), 轮("V", 'D', 12)).\
        加解密("SFBWD NJUSE GQOBH KRTAR EEZMW KPPRB XOHDR OEQGB BGTQV PGVKB VVGBI MHUSZ YDAJQ IROAX SSSNR EHYGG RPISE ZBOVM QIEMM ZCYSG QDGRE RVBIL EKXYQ IRGIR QNRDN VRXCY YTNJR",
                  "DREIG EHTLA NGSAM ABERS IQERV ORWAE RTSXE INSSI EBENN ULLSE QSXUH RXROE MXEIN SXINF RGTXD REIXA UFFLI EGERS TRASZ EMITA NFANG XEINS SEQSX KMXKM XOSTW XKAME NECXK"))
    # U-264 (Kapitänleutnant Hartwig Looks), 1942
    print( 德密机("AT BL DF GJ HM NW OP QY RZ VX", 轮("B薄"), 轮("Beta", 'V', 1), 轮("II", 'J', 1), 轮("IV", 'N', 1), 轮("I", 'A', 22)).\
        加解密("NCZW VUSX PNYM INHZ XMQX SFWX WLKJ AHSH NMCO CCAK UQPM KCSM HKSE INJU SBLK IOSX CKUB HMLL XCSJ USRR DVKO HULX WCCB GVLI YXEO AHXR HKKF VDRE WEZL XOBA FGYU JQUK GRTV UKAM EURB VEKS UHHV OYHA BCJW MAKL FKLM YFVN RIZR VVRT KOFD ANJM OLBG FFLE OPRG TFLV RHOW OPBE KVWM UQFM PWPA RMFH AGKX IIBG",
                  "VONV ONJL OOKS JHFF TTTE INSE INSD REIZ WOYY QNNS NEUN INHA LTXX BEIA NGRI FFUN TERW ASSE RGED RUEC KTYW ABOS XLET ZTER GEGN ERST ANDN ULAC HTDR EINU LUHR MARQ UANT ONJO TANE UNAC HTSE YHSD REIY ZWOZ WONU LGRA DYAC HTSM YSTO SSEN ACHX EKNS VIER MBFA ELLT YNNN NNNO OOVI ERYS ICHT EINS NULL"))
    # Scharnhorst (Konteradmiral Erich Bey), 1943
    print( 德密机("AN EZ HK IJ LR MQ OT PV SW UX", 轮("B"), 轮("III", 'U', 1), 轮("VI", 'Z', 8), 轮("VIII", 'V', 13)).\
        加解密("YKAE NZAP MSCH ZBFO CUVM RMDP YCOF HADZ IZME FXTH FLOL PZLF GGBO TGOX GRET DWTJ IQHL MXVJ WKZU ASTR",
                  "STEUE REJTA NAFJO RDJAN STAND ORTQU AAACC CVIER NEUNN EUNZW OFAHR TZWON ULSMX XSCHA RNHOR STHCO"))