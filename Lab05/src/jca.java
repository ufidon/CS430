
/* JCA - Java Cryptographic Architecture
 * */
import java.util.*;
import java.lang.*;
import javax.crypto.*;
import javax.crypto.spec.*;

import java.security.*;
import java.security.spec.*;
import java.nio.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import org.apache.commons.codec.binary.*;
import org.apache.commons.codec.binary.Base64;

public class jca {

	public static void main(String[] args) throws Throwable {
		// ============== text encoding
		String bless = "Happy Christmas!";
		byte[] rawbless = bless.getBytes();
		String rawblesshex = Hex.encodeHexString(rawbless);
		String rawbless64 = Base64.encodeBase64String(rawbless);
		byte[] dBase64 = Base64.decodeBase64(rawbless64);
		String dBase64hex = Hex.encodeHexString(dBase64);
		String dBase64str = new String(dBase64, StandardCharsets.UTF_8);
		String dasciistr = new String(dBase64, StandardCharsets.US_ASCII);
		String utf16str = new String(dBase64, StandardCharsets.UTF_16);
		String utf16lestr = new String(dBase64, StandardCharsets.UTF_16LE);
		String utf16bestr = new String(dBase64, StandardCharsets.UTF_16BE);
		String utf32str = new String(dBase64, StandardCharsets.ISO_8859_1);
		
		System.out.printf("\n\n== Text encoding ==\n");
		System.out.printf("plaintext default encoding: %s\n", bless);
		System.out.printf("in hex: %s\n", rawblesshex);
		System.out.printf("in Base64: %s\n", rawbless64);
		System.out.printf("in hex: %s\n", dBase64hex);
		System.out.printf("plaintext in UTF-8: %s\n", dBase64str);
		System.out.printf("plaintext in ascii: %s\n", dasciistr);
		System.out.printf("plaintext in UTF-16: %s\n", utf16str);
		System.out.printf("plaintext in UTF-16LE: %s\n", utf16lestr);
		System.out.printf("plaintext in UTF-16BE: %s\n", utf16bestr);
		System.out.printf("plaintext in ISO_8859_1: %s\n", utf32str);
		
		// ============== Random number generator
		System.out.printf("\n\n== Random number generator ==\n");
		SecureRandom rng = SecureRandom.getInstanceStrong();

		rng.setSeed(1314);

		// generate 10 random numbers
		System.out.println("Generate 10 random numbers:");
		for (int i = 0; i < 10; ++i) {
			System.out.printf("%3d %06.6f \n", rng.nextInt(256), rng.nextDouble());

		}

		// ============== Message Digest
		System.out.printf("\n\n== Message Digest ==\n");
		String message = "Happy New Year!";
		byte[] data = message.getBytes(StandardCharsets.UTF_8);

		String[] shaalgs = { "SHA-1", "SHA-256", "SHA-384", "SHA-512" };
		MessageDigest dgst;
		byte[] shacode;
		String strshacode;
		for (String shaalg : shaalgs) {
			dgst = MessageDigest.getInstance(shaalg);

			dgst.update(data);
			shacode = dgst.digest();
			strshacode = Hex.encodeHexString(shacode);
			System.out.printf("The %s code of \'%s\' is: %s \n", shaalg, message, strshacode);
		}

		// ============== AES Encryption/Decryption
		System.out.printf("\n\n== AES Encryption/Decryption ==\n");
		// 1.0 generate aes key automatically
		KeyGenerator keygen = KeyGenerator.getInstance("AES");
		SecretKey aesKey = keygen.generateKey();
		String keyhexstr = Hex.encodeHexString(aesKey.getEncoded());
		System.out.printf("Key generated automatically:%s  %d\n", keyhexstr, keyhexstr.length());

		// 1.1 generate aes key manually
		byte[] manualkey = Hex.decodeHex("11223344556677889900112233445566".toCharArray());
		SecretKey aeskeym = new SecretKeySpec(manualkey, "AES");
		keyhexstr = Hex.encodeHexString(aeskeym.getEncoded());
		System.out.printf("Key manually created:%s  %d\n", keyhexstr, keyhexstr.length());

		// 1.2 generate aes key from password
		SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
		String password = "hello", salt = "salty";
		KeySpec spec = new PBEKeySpec(password.toCharArray(), salt.getBytes(), 65536, 256);
		SecretKey aeskeyg = factory.generateSecret(spec);
		keyhexstr = Hex.encodeHexString(aeskeyg.getEncoded());
		System.out.printf("Key PBE generated:%s  %d\n", keyhexstr, keyhexstr.length());

		SecretKey aeskey256 = new SecretKeySpec(aeskeyg.getEncoded(), 0, 32, "AES");
		keyhexstr = Hex.encodeHexString(aeskey256.getEncoded());
		System.out.printf("256bit key:%s  %d\n", keyhexstr, keyhexstr.length());
		SecretKey aeskey192 = new SecretKeySpec(aeskeyg.getEncoded(), 0, 24, "AES");
		keyhexstr = Hex.encodeHexString(aeskey192.getEncoded());
		System.out.printf("192bit key:%s  %d\n", keyhexstr, keyhexstr.length());
		SecretKey aeskey128 = new SecretKeySpec(aeskeyg.getEncoded(), 0, 16, "AES");
		keyhexstr = Hex.encodeHexString(aeskey128.getEncoded());
		System.out.printf("128bit key:%s  %d\n", keyhexstr, keyhexstr.length());

		// 2.0 AES cipher with padding
		System.out.printf("\n\nAES cipher with padding\n");
		Cipher aesCipherpad = Cipher.getInstance("AES/ECB/PKCS5Padding");

		aesCipherpad.init(Cipher.ENCRYPT_MODE, aeskey256);
		// Our cleartext
		String strplain = "This is the end of Fall 2016.";
		byte[] cleartext = strplain.getBytes();
		// Encrypt the cleartext
		byte[] ciphertext = aesCipherpad.doFinal(cleartext);
		String hexciphertext = Hex.encodeHexString(ciphertext);
		System.out.printf("plaintext: %s  %d bytes\n", strplain, strplain.length());
		System.out.printf("ciphertext: %s  %d hex digits\n", hexciphertext, hexciphertext.length());

		// Initialize the same cipher for decryption
		aesCipherpad.init(Cipher.DECRYPT_MODE, aeskey256);
		// Decrypt the ciphertext
		byte[] decryptedtext = aesCipherpad.doFinal(ciphertext);
		String strdecrypted = new String(decryptedtext);
		System.out.printf("decryptedtext: %s  %d bytes\n", strdecrypted, strdecrypted.length());

		aesCipherpad = Cipher.getInstance("AES/ECB/NoPadding");
		aesCipherpad.init(Cipher.DECRYPT_MODE, aeskey256);
		decryptedtext = aesCipherpad.doFinal(ciphertext);
		strdecrypted = new String(decryptedtext);
		String hexdecryptedtext = Hex.encodeHexString(decryptedtext);
		System.out.printf("decryptedtext: %s  %d bytes\n", strdecrypted, strdecrypted.length());
		System.out.printf("decryptedtext: %s  %d hex digits\n", hexdecryptedtext, hexdecryptedtext.length());

		// 2.1 AES cipher without padding
		System.out.printf("\n\nAES cipher without padding\n");
		aesCipherpad.init(Cipher.ENCRYPT_MODE, aeskey256);

		// Encrypt the cleartext
		try {
			ciphertext = aesCipherpad.doFinal(cleartext);
			hexciphertext = Hex.encodeHexString(ciphertext);
			System.out.printf("\nplaintext: %s  %d bytes\n", strplain, strplain.length());
			System.out.printf("ciphertext: %s  %d hex digits\n", hexciphertext, hexciphertext.length());
		} catch (IllegalBlockSizeException e) {
			System.out.println(e.toString());
		}
		strplain = "Happy New Year!!";
		cleartext = strplain.getBytes();
		try {
			ciphertext = aesCipherpad.doFinal(cleartext);
			hexciphertext = Hex.encodeHexString(ciphertext);
			System.out.printf("\nplaintext: %s  %d bytes\n", strplain, strplain.length());
			System.out.printf("ciphertext: %s  %d hex digits\n", hexciphertext, hexciphertext.length());
		} catch (IllegalBlockSizeException e) {
			System.out.println(e.toString());
		}
		aesCipherpad.init(Cipher.DECRYPT_MODE, aeskey256);
		decryptedtext = aesCipherpad.doFinal(ciphertext);
		strdecrypted = new String(decryptedtext);
		hexdecryptedtext = Hex.encodeHexString(decryptedtext);
		System.out.printf("decryptedtext: %s  %d bytes\n", strdecrypted, strdecrypted.length());
		System.out.printf("decryptedtext: %s  %d hex digits\n", hexdecryptedtext, hexdecryptedtext.length());

		// 2.2 AES cipher with initial vector
		System.out.printf("\n\nAES cipher with initial vector\n");
		//aesCipherpad = Cipher.getInstance("AES/OFB/PKCS5Padding");
		aesCipherpad = Cipher.getInstance("AES/OFB/NoPadding");

		byte[] ivraw = Hex.decodeHex("11223344556677889900112233445566".toCharArray());
		IvParameterSpec iv = new IvParameterSpec(ivraw);
		aesCipherpad.init(Cipher.ENCRYPT_MODE, aeskey256, iv);
		// Our cleartext
		strplain = "This is the end of Fall 2016.";
		cleartext = strplain.getBytes();
		// Encrypt the cleartext
		ciphertext = aesCipherpad.doFinal(cleartext);
		hexciphertext = Hex.encodeHexString(ciphertext);
		System.out.printf("plaintext: %s  %d bytes\n", strplain, strplain.length());
		System.out.printf("ciphertext: %s  %d hex digits\n", hexciphertext, hexciphertext.length());

		// Initialize the same cipher for decryption
		aesCipherpad.init(Cipher.DECRYPT_MODE, aeskey256, iv);
		// Decrypt the ciphertext
		decryptedtext = aesCipherpad.doFinal(ciphertext);
		strdecrypted = new String(decryptedtext);
		System.out.printf("decryptedtext: %s  %d bytes\n", strdecrypted, strdecrypted.length());
		
		
		// 3.0 Encrypt/Decrypt during file input/output
		FileInputStream fis;
	    FileOutputStream fos;
	    CipherInputStream cis, cisd;
	    CipherOutputStream cos, cosd;
	    
	    // How about PKCS5Padding? NoPadding
	    Cipher encipher =  Cipher.getInstance("AES/OFB/NoPadding");
	    encipher.init(Cipher.ENCRYPT_MODE, aeskey256, iv);
	    
	    Cipher decipher =  Cipher.getInstance("AES/OFB/NoPadding");
	    decipher.init(Cipher.DECRYPT_MODE, aeskey256, iv);
	    
	    // encrypt during read
	    fis = new FileInputStream("plaintext.txt");
	    cis = new CipherInputStream(fis, encipher);
	    fos = new FileOutputStream("erciphertext.txt");
	    
	    byte[] fdata = new byte[32];
	    int i = cis.read(fdata); // encrypt during read
	    while (i != -1) {
	        fos.write(fdata, 0, i);
	        i = cis.read(fdata);
	    }
	    fos.flush();
	    fos.close();
	    cis.close();
	    fis.close();
	    
	    // encrypt/decrypt during read
	    fis = new FileInputStream("plaintext.txt");
	    cis = new CipherInputStream(fis, encipher);
	    cisd = new CipherInputStream(cis, decipher);
	    fos = new FileOutputStream("erdrplaintext.txt");
	    i = cisd.read(fdata);
	    while(i != -1){
	    	fos.write(fdata,0,i);
	    	i = cisd.read(fdata);
	    }
	    fos.flush();
	    fos.close();
	    cisd.close();
	    
	    // decrypt during read
	    fis = new FileInputStream("ciphertext.txt");
	    cisd = new CipherInputStream(fis, decipher);
	    fos = new FileOutputStream("drplaintext.txt");
	    
	    i = cisd.read(fdata); // encrypt during read
	    while (i != -1) {
	        fos.write(fdata, 0, i);
	        i = cisd.read(fdata);
	    }
	    fos.flush();
	    fos.close();
	    cisd.close();
	    fis.close();
	    
	    // decrypt/encrypt during read
	    fis = new FileInputStream("ciphertext.txt");
	    cisd = new CipherInputStream(fis, decipher);
	    cis = new CipherInputStream(cisd, encipher);
	    fos = new FileOutputStream("drerciphertext.txt");
	    i = cis.read(fdata);
	    while(i != -1){
	    	fos.write(fdata,0,i);
	    	i = cis.read(fdata);
	    }
	    fos.flush();
	    fos.close();
	    cis.close();	    
	    
	    // encrypt during write
	    fis = new FileInputStream("plaintext.txt");
	    fos = new FileOutputStream("ewciphertext.txt");
	    cos = new CipherOutputStream(fos, encipher);
	    i = fis.read(fdata);
	    while(i != -1){
	    	cos.write(fdata,0,i);
	    	i = fis.read(fdata);
	    }
	    cos.flush();
	    cos.close();
	    fis.close();
	    
	    // encrypt/decrypt during write
	    fis = new FileInputStream("plaintext.txt");
	    fos = new FileOutputStream("ewdwplaintext.txt");
	    cos = new CipherOutputStream(fos, encipher);
	    cosd = new CipherOutputStream(cos, decipher);
	    i = fis.read(fdata);
	    while(i != -1){
	    	cosd.write(fdata,0,i);
	    	i = fis.read(fdata);
	    }
	    cosd.flush();
	    cosd.close();
	    fis.close();	    
	    	    
	    
	    // decrypt during write
	    
	    fis = new FileInputStream("ciphertext.txt");
	    fos = new FileOutputStream("drplaintext.txt");
	    cos = new CipherOutputStream(fos, decipher);
	    
	    i = fis.read(fdata); 
	    while (i != -1) {
	        cos.write(fdata, 0, i); // decrypt during write
	        i = fis.read(fdata); 
	    }
	    cos.flush();
	    fos.close();
	    cos.close();
	    fis.close();
	        
	    
	    
		

	}

}
