package dataset1123;

import javax.crypto.spec.PBEParameterSpec;
import java.security.SecureRandom;

public class LessThan1000IterationPBEABICase {

    public static void main(String[] args){
        LessThan1000IterationPBEABICase lt = new LessThan1000IterationPBEABICase();
        int count = 20;
        lt.go(count);
    }
    public void go(int count){
        SecureRandom random = new SecureRandom();
        PBEParameterSpec pbeParamSpec = null;
        byte[] salt = new byte[32];
        random.nextBytes(salt);

        pbeParamSpec = new PBEParameterSpec(salt, count);
    }
}
