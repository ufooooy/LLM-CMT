package CrossFile;

import java.security.SecureRandom;

public class CredentialInStringMulCase1Main {
    public static void main(String [] args){
        CredentialInStringMulCase1 pc = new CredentialInStringMulCase1();
        SecureRandom random = new SecureRandom();
        String key = String.valueOf(random.ints());
        pc.go(key);
    }
}

