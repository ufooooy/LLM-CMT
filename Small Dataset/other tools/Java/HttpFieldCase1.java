package dataset;

import java.net.MalformedURLException;
import java.net.URL;

public class HttpFieldCase1 {
    CryptoHTTP1 crypto;
    public HttpFieldCase1() throws MalformedURLException {
        String url = "http://gmail.com";
        crypto = new CryptoHTTP1(url);
        crypto.method1("");
    }
}

class CryptoHTTP1 {
    String defURL;

    public CryptoHTTP1(String url){
        defURL = url;
    }

    public void method1(String passedURL) throws MalformedURLException {

        if(passedURL.isEmpty()){
            passedURL = defURL;
        }
        System.out.println(new URL(passedURL));
    }
}

