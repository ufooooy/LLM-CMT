import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.SecureRandom;

public class DSAExample {

    public static void main(String[] args) throws Exception {
        // Generate a DSA key pair
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("DSA");
        keyPairGenerator.initialize(1024); // Key length of 1024 bits
        KeyPair keyPair = keyPairGenerator.generateKeyPair();

        // Generate a message to sign
        byte[] message = "Hello, DSA!".getBytes();

        // Create a signature instance using DSA
        Signature signature = Signature.getInstance("DSA");
        signature.initSign(keyPair.getPrivate(), new SecureRandom());

        // Update the signature object with the data to be signed
        signature.update(message);

        // Generate the signature
        byte[] digitalSignature = signature.sign();

        // Verify the signature
        signature.initVerify(keyPair.getPublic());
        signature.update(message);
        boolean verified = signature.verify(digitalSignature);

        System.out.println("Signature verified: " + verified);
    }
}
