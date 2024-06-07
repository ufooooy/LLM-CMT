package dataset;

import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.PBEParameterSpec;
import java.security.SecureRandom;
import java.util.HashMap;
import java.util.Map;

public class PredictablePBEKeyPositiveCase2 {
    private PBEKeySpec pbeKeySpec = null;
    private PBEParameterSpec pbeParamSpec = null;

    public static void main(String [] args){
        PredictablePBEKeyPositiveCase2 ckp = new PredictablePBEKeyPositiveCase2();
        Map<String,String> hm = new HashMap<String, String>();
        hm.put("aaa", "afix");
        hm.put("bbb", "bfix");
        hm.put("ccc", "cfix");
        hm.put("ddd", "dfix");

        String key = hm.get("aaa");
        ckp.key(key);
    }
    public void key(String key) {
        byte [] salt = new byte[16];
        SecureRandom sr = new SecureRandom();
        sr.nextBytes(salt);
        int iterationCount = 11010;
        int keyLength = 16;
        pbeKeySpec = new PBEKeySpec(key.toCharArray(),salt,iterationCount,keyLength);
    }
}

