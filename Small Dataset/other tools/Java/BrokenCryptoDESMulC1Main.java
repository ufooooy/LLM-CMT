package CrossFile;

import javax.crypto.NoSuchPaddingException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

public class BrokenCryptoDESMulC1Main {
    public static void main (String [] args) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException {
        BrokenCryptoDESMulC1 bc = new BrokenCryptoDESMulC1();
        String crypto = "DES/ECB/PKCS5Padding";
        String cryptokey = "DES";
        bc.go(crypto,cryptokey);
    }
}

