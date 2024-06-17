package dataset1123;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class MD5Example3 {
    public static void main (String [] args) throws NoSuchAlgorithmException {
        String name = "abcdef";
        MessageDigest md = MessageDigest.getInstance("MD5");
        md.update(name.getBytes());
        System.out.println(md.digest());
    }
}
