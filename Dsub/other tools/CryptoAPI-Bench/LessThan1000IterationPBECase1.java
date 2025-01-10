package dataset;

import javax.crypto.spec.PBEParameterSpec;
import java.security.SecureRandom;

public class LessThan1000IterationPBECase1 {
    public static void main(){
        LessThan1000IterationPBECase1 lt = new LessThan1000IterationPBECase1();
        lt.key2();
    }
    public void key2(){
        SecureRandom random = new SecureRandom();
        PBEParameterSpec pbeParamSpec = null;
        byte[] salt = new byte[32];
        random.nextBytes(salt);
        int count = 20;
        pbeParamSpec = new PBEParameterSpec(salt, count);
    }
}
