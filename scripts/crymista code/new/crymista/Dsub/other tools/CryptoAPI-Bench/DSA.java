package dataset1123;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.SecureRandom;

public class DSA {

    public static void main(String[] args) throws Exception {
        // Create a DSA key pair generator
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("DSA");

        // Insecure way of initializing the key pair generator with a fixed seed
        byte[] insecureSeed = "ThisIsNotASecureSeed".getBytes();
        keyPairGenerator.initialize(1024, new java.security.SecureRandom(insecureSeed));

        // Generate a DSA key pair
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
