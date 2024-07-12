package CrossFile;

import javax.crypto.NoSuchPaddingException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

public class BrokenCryptoRC2MulC1Main {
    public static void main (String [] args) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException {
        BrokenCryptoRC2MulC1 bc = new BrokenCryptoRC2MulC1();
        String crypto = "RC2";
        bc.go(crypto);
    }
}

