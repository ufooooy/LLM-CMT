package CrossFile;

import javax.crypto.NoSuchPaddingException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

public class BrokenCryptoBlowfishMulC1Main {
    public static void main (String [] args) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException {
        BrokenCryptoBlowfishMulC1 bc = new BrokenCryptoBlowfishMulC1();
        String crypto = "Blowfish";
        bc.go(crypto);
    }
}

