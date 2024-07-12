package CrossFile;

import javax.crypto.NoSuchPaddingException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

public class ECBAESMulCase1Main {
    public static void main (String [] args) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException {
        ECBAESMulCase1 bc = new ECBAESMulCase1();
        String crypto = "AES/ECB/PKCS5Padding";
        bc.go(crypto);
    }
}

