import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

public class DES {
    public void go(String crypto, String keyAlgo) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException {
        KeyGenerator keyGen = KeyGenerator.getInstance(keyAlgo);
        SecretKey key = keyGen.generateKey();
        Cipher cipher = Cipher.getInstance(crypto);
        cipher.init(Cipher.ENCRYPT_MODE, key);
    }

    public static void main (String [] args) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException {
        DES bc = new DES();
        String crypto = "DES/ECB/PKCS5Padding";
        String keyAlgo = "DES";
        bc.go(crypto,keyAlgo);
    }
}
