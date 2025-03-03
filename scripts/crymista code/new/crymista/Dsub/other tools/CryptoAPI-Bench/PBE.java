package dataset1123;

import javax.crypto.spec.PBEParameterSpec;
import java.security.SecureRandom;

public class PBE {
    public static final String DEFAULT_COUNT = "20";
    private static char[] COUNT;
    private static char[] count;
    
    public PBE() {
        go2();
        go3();
    }
    
    private static void go2(){
        COUNT = DEFAULT_COUNT.toCharArray();
    }
    
    private static void go3(){
        count = COUNT;
    }
    
    public void key2(){
        SecureRandom random = new SecureRandom();
        byte[] salt = new byte[32];
        random.nextBytes(salt);

        PBEParameterSpec pbeParamSpec = new PBEParameterSpec(salt, Integer.parseInt(String.valueOf(count)));
    }

    public static void main(String[] args) {
        PBE pbe = new PBE();
        pbe.key2();
    }
}