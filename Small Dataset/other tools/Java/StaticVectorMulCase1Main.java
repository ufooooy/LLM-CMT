package CrossFile;

import javax.crypto.NoSuchPaddingException;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

public class StaticVectorMulCase1Main {
    public static void main (String [] args) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, InvalidAlgorithmParameterException {
        StaticVectorMulCase1 siv = new StaticVectorMulCase1();
        byte [] bytes = "abcde".getBytes();

        siv.go(bytes);
    }
}
