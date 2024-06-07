package dataset;

import java.net.URL;

public class HttpPathCase1 {
    public static void main(String[] args) throws Exception {
        int choice = 2;
        String url = "http://www.facebook.com";
        if(choice>3)
            url = "https://www.google.com";
        System.out.println(new URL(url));
    }
}

