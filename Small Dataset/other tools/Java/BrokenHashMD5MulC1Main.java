package CrossFile;

import java.security.NoSuchAlgorithmException;

public class BrokenHashMD5MulC1Main {
    public static void main (String [] args) throws NoSuchAlgorithmException {
        BrokenHashMulC1 bh = new BrokenHashMulC1();
        String str = "abcdef";
        String crypto = "MD5";
        bh.go(str,crypto);
    }
}

