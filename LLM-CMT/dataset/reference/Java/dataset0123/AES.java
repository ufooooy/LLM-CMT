package dataset1123;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

public class AES {
    private static final String ALGORITHM = "AES";
    private static final String TRANSFORMATION = "AES/ECB/PKCS5Padding";
    private static final int KEY_LENGTH = 16;

    public static String encrypt(String key, String plainText) throws Exception {
        SecretKeySpec secretKey = new SecretKeySpec(key.getBytes(), ALGORITHM);
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        byte[] cipherText = cipher.doFinal(plainText.getBytes());
        return Base64.getEncoder().encodeToString(cipherText);
    }

    public static String decrypt(String key, String cipherText) throws Exception {
        SecretKeySpec secretKey = new SecretKeySpec(key.getBytes(), 0, KEY_LENGTH, ALGORITHM);
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        byte[] plainText = cipher.doFinal(Base64.getDecoder().decode(cipherText));
        return new String(plainText);
    }

    public static void main(String[] args) throws Exception {
        String plainText = "Hello, world!";
        String key = "mySecretKey12345"; // 修改密钥长度为16字节
        System.out.println(key.length());
        String cipherText = encrypt(key, plainText);
        String decryptedText = decrypt(key, cipherText);
        System.out.println("Original text: " + plainText);
        System.out.println("Encrypted text: " + cipherText);
        System.out.println("Decrypted text: " + decryptedText);
    }
}