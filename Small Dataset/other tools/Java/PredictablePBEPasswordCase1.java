package dataset;

import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.PBEParameterSpec;
import java.security.SecureRandom;

public class PredictablePBEPasswordCase1 {
    private PBEKeySpec pbeKeySpec = null;
    private PBEParameterSpec pbeParamSpec = null;

    public static void main(String [] args){
        PredictablePBEPasswordCase1 ckp = new PredictablePBEPasswordCase1();
        ckp.key();
    }
    public void key() {
        String defaultKey = "saagar";
        byte [] salt = new byte[16];
        SecureRandom sr = new SecureRandom();
        sr.nextBytes(salt);
        int iterationCount = 11010;
        int keyLength = 16;
        pbeKeySpec = new PBEKeySpec(defaultKey.toCharArray(),salt,iterationCount,keyLength);
    }

}
