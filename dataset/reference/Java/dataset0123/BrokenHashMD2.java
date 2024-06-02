package dataset;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class BrokenHashMD2 {
    public static void main (String [] args) throws NoSuchAlgorithmException {
        String name = "abcdef";
        MessageDigest md = MessageDigest.getInstance("MD2");
        md.update(name.getBytes());
        System.out.println(md.digest());
    }
}
