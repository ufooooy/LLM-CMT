package dataset1123;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.DESedeKeySpec;

public class TripleDES {
    private static final String ALGORITHM = "DESede";

    public static byte[] encrypt(byte[] key, byte[] data) throws Exception {
        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance(ALGORITHM);
        SecretKey secretKey = keyFactory.generateSecret(new DESedeKeySpec(key));
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        return cipher.doFinal(data);
    }

    public static byte[] decrypt(byte[] key, byte[] data) throws Exception {
        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance(ALGORITHM);
        SecretKey secretKey = keyFactory.generateSecret(new DESedeKeySpec(key));
        Cipher cipher = Cipher.getInstance(ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        return cipher.doFinal(data);
    }

    public static void main(String[] args) throws Exception {
        byte[] key = "mySecretKey12345".getBytes();
        // Pad the key to 24 bytes
        byte[] paddedKey = new byte[24];
        System.arraycopy(key, 0, paddedKey, 0, key.length);
        byte[] data = "Hello, world!".getBytes();
        byte[] encryptedData = encrypt(paddedKey, data);
        byte[] decryptedData = decrypt(paddedKey, encryptedData);
        System.out.println(new String(decryptedData));
    }
}