package dataset1123;

import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidKeySpecException;
import java.util.Arrays;

public class PBKDFUsingMD5Example {

    public static void main(String[] args) throws NoSuchAlgorithmException, InvalidKeySpecException {
        String password = "myPassword123";
        String salt = "randomSalt";
        int iterations = 1000;
        int keyLength = 256; // in bits

        byte[] derivedKey = deriveKeyUsingMD5(password, salt, iterations, keyLength);
        System.out.println("Derived key using MD5: " + Arrays.toString(derivedKey));
    }

    public static byte[] deriveKeyUsingMD5(String password, String salt, int iterations, int keyLength)
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        char[] passwordChars = password.toCharArray();
        byte[] saltBytes = salt.getBytes();

        PBEKeySpec spec = new PBEKeySpec(passwordChars, saltBytes, iterations, keyLength);
        SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacMD5");
        return skf.generateSecret(spec).getEncoded();
    }
}
