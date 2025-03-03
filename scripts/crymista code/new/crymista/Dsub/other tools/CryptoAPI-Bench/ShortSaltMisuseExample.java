import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;

public class ShortSaltMisuseExample {

    public static void main(String[] args) throws NoSuchAlgorithmException {
        String password = "myPassword123";
        String hashedPassword = hashPassword(password);

        System.out.println("Hashed password: " + hashedPassword);
    }

    public static String hashPassword(String password) throws NoSuchAlgorithmException {
        // Generate a short salt (incorrect usage)
        SecureRandom random = new SecureRandom();
        byte[] salt = new byte[8];  // 8 bits = 1 byte
        random.nextBytes(salt);

        // Hash the password with the short salt (incorrect usage)
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        md.update(salt);
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
