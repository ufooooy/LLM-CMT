package dataset;

import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.PBEParameterSpec;
import java.security.SecureRandom;

public class PredictablePBEKeyInFieldCase1 {
    private PBEKeySpec pbeKeySpec = null;
    private PBEParameterSpec pbeParamSpec = null;
    public static String KEY = "sagar";
    public static char [] DEFAULT_ENCRYPT_KEY = KEY.toCharArray();
    private static char[] ENCRYPT_KEY;
    private static char[] encryptKey;

    public static void main(String [] args) {
        PredictablePBEKeyInFieldCase1 pksp = new PredictablePBEKeyInFieldCase1();
        go2();
        go3();
        pksp.go();
    }

    private static void go2(){
        ENCRYPT_KEY = DEFAULT_ENCRYPT_KEY;
    }
    private static void go3(){
        encryptKey = ENCRYPT_KEY;
    }

    private void go() {
        SecureRandom sr = new SecureRandom();
        byte [] salt = new byte[16];
        sr.nextBytes(salt);
        pbeKeySpec = new PBEKeySpec(encryptKey,salt,10000,16);
    }
}
