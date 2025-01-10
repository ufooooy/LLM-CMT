import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class RC4 {
    public static void main(String[] args) throws Exception {
        String key = "1234567890123456";
        String plaintext = "Hello, world!";
        byte[] ciphertext = encrypt(key.getBytes(), plaintext.getBytes());
        System.out.println(new String(ciphertext));
        byte[] decrypted = decrypt(key.getBytes(), ciphertext);
        System.out.println(new String(decrypted));
    }

    public static byte[] encrypt(byte[] key, byte[] plaintext) throws Exception {
        SecretKeySpec keySpec = new SecretKeySpec(key, "RC4");
        Cipher cipher = Cipher.getInstance("RC4");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);
        return cipher.doFinal(plaintext);
    }

    public static byte[] decrypt(byte[] key, byte[] ciphertext) throws Exception {
        SecretKeySpec keySpec = new SecretKeySpec(key, "RC4");
        Cipher cipher = Cipher.getInstance("RC4");
        cipher.init(Cipher.DECRYPT_MODE, keySpec);
        return cipher.doFinal(ciphertext);
    }
}
