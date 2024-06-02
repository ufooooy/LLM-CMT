package dataset1123;

import javax.crypto.KeyAgreement;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.*;
import java.util.Base64;

public class KeyExchangeWithoutEntityAuthentication {

    public static void main(String[] args) {
        try {
            // Alice and Bob generate their own key pairs
            KeyPair aliceKeyPair = generateKeyPair();
            KeyPair bobKeyPair = generateKeyPair();

            // Alice and Bob exchange their public keys (this step simulates the key exchange)
            PublicKey alicePublicKey = aliceKeyPair.getPublic();
            PublicKey bobPublicKey = bobKeyPair.getPublic();

            // Alice computes the shared secret using her private key and Bob's public key
            SecretKey aliceSharedSecret = computeSharedSecret(aliceKeyPair.getPrivate(), bobPublicKey);

            // Bob computes the shared secret using his private key and Alice's public key
            SecretKey bobSharedSecret = computeSharedSecret(bobKeyPair.getPrivate(), alicePublicKey);

            // Display the shared secrets (in real-world usage, these would be used for encryption)
            System.out.println("Alice's shared secret: " + bytesToHex(aliceSharedSecret.getEncoded()));
            System.out.println("Bob's shared secret: " + bytesToHex(bobSharedSecret.getEncoded()));

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static KeyPair generateKeyPair() throws NoSuchAlgorithmException {
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("DH");
        keyPairGenerator.initialize(2048);  // Key size
        return keyPairGenerator.generateKeyPair();
    }

    private static SecretKey computeSharedSecret(PrivateKey privateKey, PublicKey publicKey) throws NoSuchAlgorithmException, InvalidKeyException {
        KeyAgreement keyAgreement = KeyAgreement.getInstance("DH");
        keyAgreement.init(privateKey);
        keyAgreement.doPhase(publicKey, true);
        return keyAgreement.generateSecret("AES");
    }

    private static String bytesToHex(byte[] bytes) {
        return Base64.getEncoder().encodeToString(bytes);
    }
}
