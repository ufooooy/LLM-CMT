package dataset;

import java.io.IOException;
import java.net.URL;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;

public class PredictableKeyStorePasswordCase1 {

    URL cacerts;
    public static void main(String args[]) throws KeyStoreException, IOException, CertificateException, NoSuchAlgorithmException {
        PredictableKeyStorePasswordCase1 pksp = new PredictableKeyStorePasswordCase1();
        pksp.go();
    }

    public void go() throws KeyStoreException, IOException, CertificateException, NoSuchAlgorithmException {
        String type = "JKS";
        KeyStore ks = KeyStore.getInstance(type);
        cacerts = new URL("https://www.google.com");
        String defaultKey = "changeit";
        ks.load(cacerts.openStream(), defaultKey.toCharArray());
    }


}
