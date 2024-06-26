package dataset;

import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.PBEParameterSpec;
import java.security.SecureRandom;

public class PredictablePBEKeyFieldCase1 {
    CryptoPredictablePBE crypto;
    public PredictablePBEKeyFieldCase1(){
        String password = "sagar";
        crypto = new CryptoPredictablePBE(password);
        crypto.method1("");
    }
}


class CryptoPredictablePBE {
    String defPassword;
    private PBEKeySpec pbeKeySpec = null;
    private PBEParameterSpec pbeParamSpec = null;

    public CryptoPredictablePBE(String password){

        defPassword = password;
    }

    public void method1(String passedPassword) {

        if(passedPassword.isEmpty()){
            passedPassword = defPassword;
        }
        byte [] salt = new byte[16];
        SecureRandom sr = new SecureRandom();
        sr.nextBytes(salt);
        int iterationCount = 11010;
        int keyLength = 16;
        pbeKeySpec = new PBEKeySpec(passedPassword.toCharArray(),salt,iterationCount,keyLength);
    }
}

