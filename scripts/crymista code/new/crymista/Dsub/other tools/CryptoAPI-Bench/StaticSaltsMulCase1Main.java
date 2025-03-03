package CrossFile;

public class StaticSaltsMulCase1Main {
    public static void main(String [] args){
        StaticSaltsMulCase1 cs = new StaticSaltsMulCase1();
        byte[] salt = {(byte) 0xa2};
        int count = 1020;
        cs.key2(salt,count);

    }
}

