package dataset;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

public class StaticVectorAESCBCFieldCase1 {
    CryptoStaticIV1 crypto;
    public StaticVectorAESCBCFieldCase1() throws InvalidKeyException, NoSuchAlgorithmException, NoSuchPaddingException, InvalidAlgorithmParameterException {
        byte [] bytes = "abcde".getBytes();

        crypto = new CryptoStaticIV1(bytes);
        crypto.method1(null);
    }
}

class CryptoStaticIV1 {
    byte [] defIV;

    public CryptoStaticIV1(byte[] bytes) {
        defIV = bytes;
    }

    public void method1(byte[] passedIV) throws NoSuchAlgorithmException, NoSuchPaddingException, InvalidKeyException, InvalidAlgorithmParameterException {

        passedIV = defIV;
        IvParameterSpec ivSpec = new IvParameterSpec(passedIV);
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        SecretKey key = keyGen.generateKey();
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE,key,ivSpec);

    }
}

