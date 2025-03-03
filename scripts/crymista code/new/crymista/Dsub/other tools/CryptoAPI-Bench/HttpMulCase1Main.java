package CrossFile;

import java.net.MalformedURLException;

public class HttpMulCase1Main {
    public static void main(String [] args) throws MalformedURLException {
        HttpMulCase1 hp = new HttpMulCase1();
        String url = "http://www.google.com";
        hp.go(url);

    }
}

