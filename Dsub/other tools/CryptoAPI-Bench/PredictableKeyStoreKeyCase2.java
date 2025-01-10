package dataset;

import java.io.IOException;
import java.net.URL;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;

public class PredictableKeyStoreKeyCase2 {
    URL cacerts;
    public static void main(String args[]) throws KeyStoreException, IOException, CertificateException, NoSuchAlgorithmException {
        PredictableKeyStoreKeyCase2 pkspac = new PredictableKeyStoreKeyCase2();
        String key = "changeit";
        pkspac.method1(key);
    }

    public void method1(String k) throws KeyStoreException, IOException, CertificateException, NoSuchAlgorithmException {
        String key2 = k;
        method2(key2);
    }

    public void method2(String key) throws KeyStoreException, IOException, CertificateException, NoSuchAlgorithmException {
        String type = "JKS";
        KeyStore ks = KeyStore.getInstance(type);
        cacerts = new URL("https://www.google.com");
        ks.load(cacerts.openStream(), key.toCharArray());
    }
}

