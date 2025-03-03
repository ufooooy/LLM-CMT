package dataset;

import java.security.SecureRandom;

public class PredictableSeedsPathCase1 {
    public static void main (String [] args){
        SecureRandom sr = new SecureRandom();
        int choice=2;
        byte [] bytes = {(byte) 100, (byte) 200};
        if(choice>1)
            sr.nextBytes(bytes);

        sr.setSeed(bytes);
        int v = sr.nextInt();
        System.out.println(v);
    }
}

