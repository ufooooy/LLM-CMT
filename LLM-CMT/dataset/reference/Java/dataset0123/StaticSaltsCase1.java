package dataset;

import javax.crypto.spec.PBEParameterSpec;

public class StaticSaltsCase1 {
    public static void main (String [] args){
        StaticSaltsCase1 cs = new StaticSaltsCase1();
        cs.key2();
    }

    public void key2(){
        PBEParameterSpec pbeParamSpec = null;
        byte[] salt = {(byte) 0xa2};
        int count = 1020;
        pbeParamSpec = new PBEParameterSpec(salt, count);
    }
}
