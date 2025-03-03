package dataset;

import javax.crypto.spec.PBEParameterSpec;

public class StaticSaltsInFieldCase1 {
    public static final String DEFAULT_SALT = "12345";
    private static char[] SALT;
    private static char[] salt;
    public static void main(String [] args){
        StaticSaltsInFieldCase1 cs = new StaticSaltsInFieldCase1();
        int count = 1020;
        go2();
        go3();
        cs.key2(count);

    }

    private static void go2(){
        SALT = DEFAULT_SALT.toCharArray();
    }
    private static void go3(){
        salt = SALT;
    }

    public void key2(int count){
        PBEParameterSpec pbeParamSpec = null;
        pbeParamSpec = new PBEParameterSpec(new byte[]{Byte.parseByte(salt.toString())}, count);
    }
}

