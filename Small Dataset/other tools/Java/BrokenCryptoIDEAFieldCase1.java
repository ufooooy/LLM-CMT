package dataset;

import javax.crypto.*;
import java.io.UnsupportedEncodingException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

public class BrokenCryptoIDEAFieldCase1 {
    CryptoIDEA crypto;
    public BrokenCryptoIDEAFieldCase1() throws NoSuchAlgorithmException, NoSuchPaddingException, IllegalBlockSizeException, BadPaddingException, InvalidKeyException, UnsupportedEncodingException {
        crypto = new CryptoIDEA("IDEA");
        crypto.encrypt("abc","");
    }
}

class CryptoIDEA {
    Cipher cipher;
    String defaultAlgo;
    public CryptoIDEA(String defAlgo) throws NoSuchPaddingException, NoSuchAlgorithmException {
        defaultAlgo = defAlgo;
    }

    public byte[] encrypt(String txt, String passedAlgo) throws UnsupportedEncodingException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException, NoSuchAlgorithmException, NoSuchPaddingException {
        if(passedAlgo.isEmpty()){
            passedAlgo = defaultAlgo;
        }

        KeyGenerator keyGen = KeyGenerator.getInstance(defaultAlgo);
        SecretKey key = keyGen.generateKey();
        Cipher cipher = Cipher.getInstance(defaultAlgo);
        cipher.init(Cipher.ENCRYPT_MODE, key);

        byte [] txtBytes = txt.getBytes();
        return cipher.doFinal(txtBytes);
    }
}

