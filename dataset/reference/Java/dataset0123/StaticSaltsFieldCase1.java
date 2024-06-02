package dataset;

import javax.crypto.spec.PBEParameterSpec;

public class StaticSaltsFieldCase1 {
    CryptoStaticSalt1 crypto;
    public StaticSaltsFieldCase1() {
        byte[] salt = {(byte) 0xa2};
        crypto = new CryptoStaticSalt1(salt);
        crypto.method1(null);
    }
}


class CryptoStaticSalt1 {
    byte[] defSalt;

    public CryptoStaticSalt1(byte [] salt) {
        defSalt = salt;
    }

    public void method1(byte[] passedSalt)  {

        passedSalt = defSalt;
        int count = 1020;
        PBEParameterSpec pbeParamSpec = null;
        pbeParamSpec = new PBEParameterSpec(passedSalt, count);

    }
}


