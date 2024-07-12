package CrossFile;

public class PredictSeedsMulC1Main {
    public static void main (String [] args){
        //long seed = 456789L;
        PredictSeedsMulC1 ps = new PredictSeedsMulC1();
        byte [] seed = {(byte) 100, (byte) 200};
        ps.go(seed);
    }
}
