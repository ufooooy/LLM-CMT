package dataset;

import javax.crypto.spec.PBEParameterSpec;

public class StaticSaltsCase2 {

    public static void main(String [] args){
        StaticSaltsCase2 cs = new StaticSaltsCase2();
        byte[] salt = {(byte) 0xa2};
        int count = 1020;
        cs.key2(salt,count);

    }
    public void key2(byte[] salt, int count){
        PBEParameterSpec pbeParamSpec = null;
        pbeParamSpec = new PBEParameterSpec(salt, count);
    }
}
