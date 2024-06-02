package dataset1123;

import javax.crypto.Cipher;
import javax.crypto.NullCipher;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class NullCipherExample {

    public static void main(String[] args) throws Exception {
        // 输入的明文
        String plainText = "Hello, world!";
        System.out.println("Plain Text: " + plainText);

        // 使用 NullCipher
        Cipher cipher = new NullCipher();

        // 尝试加密明文（实际上不进行加密）
        byte[] encryptedBytes = cipher.doFinal(plainText.getBytes(StandardCharsets.UTF_8));

        // 将加密后的字节数组转换为Base64字符串
        String encryptedBase64 = Base64.getEncoder().encodeToString(encryptedBytes);

        // 输出加密后的结果
        System.out.println("Encrypted Text (Base64): " + encryptedBase64);
    }
}
