package dataset1123;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import javax.crypto.Cipher;

public class RSA {
    private static final String ALGORITHM = "RSA";
    private static final int KEY_SIZE = 1024;

    public static byte[] encrypt(byte[] data, PublicKey publicKey) throws Exception {
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        return cipher.doFinal(data);
    }

    public static byte[] decrypt(byte[] data, PrivateKey privateKey) throws Exception {
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, privateKey);
        return cipher.doFinal(data);
    }

    public static KeyPair generateKeyPair() throws NoSuchAlgorithmException {
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance(ALGORITHM);
        keyPairGenerator.initialize(KEY_SIZE);
        return keyPairGenerator.generateKeyPair();
    }

    public static void main(String[] args) throws Exception {
        KeyPair keyPair = generateKeyPair();
        PublicKey publicKey = keyPair.getPublic();
        PrivateKey privateKey = keyPair.getPrivate();
        String message = "Hello, world!";
        byte[] encryptedMessage = encrypt(message.getBytes(), publicKey);
        byte[] decryptedMessage = decrypt(encryptedMessage, privateKey);
        System.out.println(new String(decryptedMessage));
    }
}
