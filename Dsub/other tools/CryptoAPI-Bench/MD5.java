package dataset1123;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class MD5 {
    public static void main (String [] args) throws NoSuchAlgorithmException {
        String str = "abcdef";
        String crypto = "MD5";
        go(str,crypto);
    }
    public static void go (String str, String crypto) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance(crypto);
        md.update(str.getBytes());
        byte[] digest = md.digest();
        StringBuilder sb = new StringBuilder();
        for (byte b : digest) {
            sb.append(String.format("%02x", b & 0xff));
        }
        System.out.println(sb.toString());
    }
}
