package dataset;

import javax.crypto.spec.PBEKeySpec;
        import javax.crypto.spec.PBEParameterSpec;
        import java.security.SecureRandom;

public class PredictablePBEPasswordCase2 {
    private PBEKeySpec pbeKeySpec = null;
    private PBEParameterSpec pbeParamSpec = null;

    public static void main(String [] args){
        PredictablePBEPasswordCase2 ckp = new PredictablePBEPasswordCase2();
        ckp.key();
    }
    public void key() {
        char [] defaultKey = {'s'};
        byte [] salt = new byte[16];
        SecureRandom sr = new SecureRandom();
        sr.nextBytes(salt);
        int iterationCount = 11010;
        int keyLength = 16;
        pbeKeySpec = new PBEKeySpec(defaultKey,salt,iterationCount,keyLength);
    }
}
