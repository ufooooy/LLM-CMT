package dataset;

import java.security.SecureRandom;

public class PredictableSeedsCase4 {
    public static void main (String [] args){
        byte seed = 100;
        go(seed);
    }

    private static void go(byte seed) {
        SecureRandom sr = new SecureRandom(new byte[]{seed});
        int v = sr.nextInt();
        System.out.println(v);
    }
}
