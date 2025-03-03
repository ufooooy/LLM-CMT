package CrossFile;

import javax.crypto.NoSuchPaddingException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

public class BrokenCryptoIDEAMulC1Main {
    public static void main (String [] args) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException {
        BrokenCryptoIDEAMulC1 bc = new BrokenCryptoIDEAMulC1();
        String crypto = "IDEA";
        bc.go(crypto);
    }
}

