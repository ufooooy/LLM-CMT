package CrossFile;

import javax.crypto.NoSuchPaddingException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

public class BrokenCryptoRC4MulC1Main {
    public static void main (String [] args) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException {
        BrokenCryptoRC4MulC1 bc = new BrokenCryptoRC4MulC1();
        String crypto = "RC4";
        bc.go(crypto);
    }
}

