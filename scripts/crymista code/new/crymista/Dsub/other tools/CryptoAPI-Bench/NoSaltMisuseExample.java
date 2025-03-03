package dataset1123;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class NoSaltMisuseExample {

    public static void main(String[] args) throws NoSuchAlgorithmException {
        String password = "myPassword123";
        String hashedPassword = hashPassword(password);

        System.out.println("Hashed password: " + hashedPassword);
    }

    public static String hashPassword(String password) throws NoSuchAlgorithmException {
        // Hash the password without using a salt (incorrect usage)
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] hashedPassword = md.digest(password.getBytes());

        return bytesToHex(hashedPassword);
    }

    private static String bytesToHex(byte[] bytes) {
        StringBuilder result = new StringBuilder();
        for (byte b : bytes) {
            result.append(String.format("%02x", b));
        }
        return result.toString();
    }
}
