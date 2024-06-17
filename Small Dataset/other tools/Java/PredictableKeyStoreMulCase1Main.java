package CrossFile;

import java.io.IOException;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;

public class PredictableKeyStoreMulCase1Main {
    public static void main(String args[]) throws KeyStoreException, IOException, CertificateException, NoSuchAlgorithmException {
        PredictableKeyStoreMulCase1 pksp = new PredictableKeyStoreMulCase1();
        String key = "changeit";
        pksp.go(key);
    }
}

