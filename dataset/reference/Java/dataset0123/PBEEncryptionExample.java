package dataset1123;

import javax.crypto.*;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.PBEParameterSpec;
import java.security.spec.AlgorithmParameterSpec;
import java.security.spec.KeySpec;
import java.util.Base64;

public class PBEEncryptionExample {

    public static void main(String[] args) throws Exception {
        String plainText = "Hello, world!";
        String password = "MyPassword";

        // 加密
        String encryptedText = encrypt(plainText, password);
        System.out.println("Encrypted Text: " + encryptedText);

        // 解密
        String decryptedText = decrypt(encryptedText, password);
        System.out.println("Decrypted Text: " + decryptedText);
    }

    public static String encrypt(String plainText, String password) throws Exception {
        byte[] salt = { 1, 2, 3, 4, 5, 6, 7, 8 }; // 8-byte salt
        int iterationCount = 1000; // Number of iterations

        KeySpec keySpec = new PBEKeySpec(password.toCharArray(), salt, iterationCount);
        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("PBEWithMD5AndDES");
        SecretKey key = keyFactory.generateSecret(keySpec);

        Cipher cipher = Cipher.getInstance("PBEWithMD5AndDES");
        AlgorithmParameterSpec paramSpec = new PBEParameterSpec(salt, iterationCount);
        cipher.init(Cipher.ENCRYPT_MODE, key, paramSpec);

        byte[] encryptedBytes = cipher.doFinal(plainText.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }

    public static String decrypt(String encryptedText, String password) throws Exception {
        byte[] salt = { 1, 2, 3, 4, 5, 6, 7, 8 }; // 8-byte salt
        int iterationCount = 1000; // Number of iterations

        KeySpec keySpec = new PBEKeySpec(password.toCharArray(), salt, iterationCount);
        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("PBEWithMD5AndDES");
        SecretKey key = keyFactory.generateSecret(keySpec);

        Cipher cipher = Cipher.getInstance("PBEWithMD5AndDES");
        AlgorithmParameterSpec paramSpec = new PBEParameterSpec(salt, iterationCount);
        cipher.init(Cipher.DECRYPT_MODE, key, paramSpec);

        byte[] encryptedBytes = Base64.getDecoder().decode(encryptedText);
        byte[] decryptedBytes = cipher.doFinal(encryptedBytes);
        return new String(decryptedBytes);
    }
}
