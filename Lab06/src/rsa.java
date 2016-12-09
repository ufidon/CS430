
/* JCA - Java Cryptographic Architecture
 * */
import java.util.*;
import java.lang.*;
import java.math.BigInteger;

import javax.crypto.*;
import javax.crypto.spec.*;

import java.security.*;
import java.security.interfaces.*;
import java.security.spec.*;
import java.nio.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import org.apache.commons.codec.binary.*;
import org.apache.commons.codec.binary.Base64;

public class rsa {

	public static void main(String[] args) throws Throwable {

	//==== 0.0 HMAC
		// Generate secret key for HMAC-SHA256
		System.out.println("==== HMAC Examples:");
        KeyGenerator kg = KeyGenerator.getInstance("HmacSHA256");
        SecretKey sk = kg.generateKey();
        System.out.println("Key:"+Hex.encodeHexString(sk.getEncoded()));

        // Get instance of Mac object implementing HMAC-SHA256, and
        // initialize it with the above secret key
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(sk);
        byte[] result = mac.doFinal("Happy Christmas!".getBytes());
        System.out.println("HMAC-SHA256:"+Hex.encodeHexString(result));
	    // cs430@cisplayground:~$ echo -n 'Happy Christmas!' | openssl dgst
        //-sha256 -mac hmac -macopt hexkey:35e9c840c57904e4eb0aa3deb234df70
        //ad6b88c733251ea57de01527dfa155a8    
        
        
        
    //==== Signature signing and verification
    //==== 1.0 Generating a pair of keys
        System.out.println("\n\n====RSA Keypair generation:\n");
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
        
        // Algorithm-Independent Initialization
        SecureRandom random = SecureRandom.getInstance("SHA1PRNG", "SUN");
        random.setSeed("Happy Christmas!".getBytes());
        keyGen.initialize(1024, random);
        
        // Algorithm-Specific Initialization
        RSAKeyGenParameterSpec rsaSpec = new RSAKeyGenParameterSpec(1024, RSAKeyGenParameterSpec.F0);

        keyGen.initialize(rsaSpec, random);
        

        
        KeyPair keypair = keyGen.generateKeyPair();
        RSAPublicKey pubkey = (RSAPublicKey) keypair.getPublic();
        RSAPrivateKey prvkey = (RSAPrivateKey) keypair.getPrivate();
        
        
        RSAPrivateKeySpec rsaprvSpec = new RSAPrivateKeySpec(prvkey.getModulus(), prvkey.getPrivateExponent());
        RSAPublicKeySpec rsapubSpec = new RSAPublicKeySpec(pubkey.getModulus(), pubkey.getPublicExponent());
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        PrivateKey privKey = keyFactory.generatePrivate( rsaprvSpec);
        PublicKey publKey = keyFactory.generatePublic( rsapubSpec);
        
        if(privKey.equals(prvkey) || (Arrays.equals(privKey.getEncoded(), prvkey.getEncoded())))
        	System.out.println("private keys equal!");
        if(pubkey.equals(publKey))
        	System.out.println("public keys equal!");
        
        String hexpubex = pubkey.getPublicExponent().toString(16);
        System.out.printf("public exponent: %s  %d hex digits\n", hexpubex, hexpubex.length());
        String hexprvex = prvkey.getPrivateExponent().toString(16);
        System.out.printf("private exponent: %s  %d hex digits\n", hexprvex, hexprvex.length());
        String hexmod = prvkey.getModulus().toString(16);
        if(prvkey.getModulus()==pubkey.getModulus())
        	System.out.printf("RSA modulus: %s  %d hex digits\n", hexmod, hexmod.length());
        
        System.out.println("\n\n====Signature generation and verification:\n");
        
        Signature ds = Signature.getInstance("SHA256withRSA");
        /* Initializing the object with a private key */
        //ds.initSign(prvkey);
        ds.initSign(privKey);
        
        String strdata = "Happy Christmas!";
        byte[] data = strdata.getBytes();
        String hexdata = Hex.encodeHexString(data);
        /* Update and sign the data */
        ds.update(data);
        byte[] sig = ds.sign();
        String hexsig = Hex.encodeHexString(sig);
        System.out.printf("data for signing: %s  %d hex digits\n", hexdata, hexdata.length());
        System.out.printf("signature: %s  %d hex digits\n", hexsig, hexsig.length());
        
        /* Initializing the object with the public key */
        ds.initVerify(pubkey);

        /* Update and verify the data */
        ds.update(data);
        boolean verifies = ds.verify(sig);
        System.out.println("signature verifies: " + verifies);
        
        // Generating/Verifying Signatures Using Key Specifications and KeyFactory
        
        
        
	//==== x.1 Password-based Encryption
        System.out.println("\n\n====PBE Examples:");
        PBEKeySpec pbeKeySpec;
        PBEParameterSpec pbeParamSpec;
        SecretKeyFactory keyFac;

        // Salt
        byte[] salt = SecureRandom.getInstanceStrong().getSeed(8);
        System.out.println("salt:"+Hex.encodeHexString(salt));
        // Iteration count
        int count = 1000;

        // Create PBE parameter set
        pbeParamSpec = new PBEParameterSpec(salt, count);

        // Prompt user for encryption password.
        // Collect user password as char array (using the
        // "readPassword" method from above), and convert
        // it into a SecretKey object, using a PBE key
        // factory.

        String password = "Happy Christmas!";
        pbeKeySpec = new PBEKeySpec(password.toCharArray());
        keyFac = SecretKeyFactory.getInstance("PBEWithHmacSHA256AndAES_128");
        SecretKey pbePass = keyFac.generateSecret(pbeKeySpec);
        String pbeKeyhex = Hex.encodeHexString(pbePass.getEncoded());
        System.out.printf("PBE pass: %s  %d hex digits\n", pbeKeyhex, pbeKeyhex.length());
        // Create PBE Cipher: Note that this algorithm implies CBC as the cipher mode 
        // and PKCS5Padding as the padding scheme 
        
        Cipher pbeCipher = Cipher.getInstance("PBEWithHmacSHA256AndAES_128");


        // Initialize PBE Cipher with key and parameters
        pbeCipher.init(Cipher.ENCRYPT_MODE, pbePass, pbeParamSpec);
        
        try{
        String ivhex = Hex.encodeHexString(pbeCipher.getIV());
        System.out.printf("initial vector: %s  %d hex digits\n", ivhex, ivhex.length());
        }catch(java.lang.NullPointerException e)
        {
        	System.out.println(e.toString());
        }        
        String salthex = Hex.encodeHexString(pbeParamSpec.getSalt());
        System.out.printf("salt: %s  %d hex digits\n", salthex, salthex.length());
        System.out.printf("PBE Algorithm: %s  \n", pbeCipher.getAlgorithm());
        
        // Our cleartext
        String cleartext = "Happy Christmas!";

        // Encrypt the cleartext       
        
        byte[] ciphertext = pbeCipher.doFinal(cleartext.getBytes());
        System.out.println("ciphertext:"+Hex.encodeHexString(ciphertext));
        
        
        // for certificate, refer to 
        // http://www.programcreek.com/java-api-examples/java.security.cert.CertificateFactory

	}

}
