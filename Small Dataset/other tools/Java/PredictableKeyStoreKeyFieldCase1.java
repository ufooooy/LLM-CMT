package dataset;

import java.io.IOException;
import java.net.URL;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;

public class PredictableKeyStoreKeyFieldCase1 {
    CryptoPredictableKeyStorePassword1 crypto;
    public PredictableKeyStoreKeyFieldCase1() throws CertificateException, NoSuchAlgorithmException, KeyStoreException, IOException {
        String key = "changeit";
        crypto = new CryptoPredictableKeyStorePassword1(key);
        crypto.method1("");
    }
}

class CryptoPredictableKeyStorePassword1 {
    String defKey;
    URL cacerts;

    public CryptoPredictableKeyStorePassword1(String key){
        defKey = key;
    }

    public void method1(String passedKey) throws KeyStoreException, IOException, CertificateException, NoSuchAlgorithmException {

        passedKey = defKey;

        String type = "JKS";
        KeyStore ks = KeyStore.getInstance(type);
        cacerts = new URL("https://www.google.com");
        ks.load(cacerts.openStream(), passedKey.toCharArray());
    }
}

