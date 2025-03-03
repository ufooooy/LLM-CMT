package dataset1123;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocketFactory;

public class WeakTLSExample {

    public static void main(String[] args) throws Exception {
        String url = "https://example.com";

        // 创建SSL上下文，强制使用TLSv1.1
        SSLContext sslContext = SSLContext.getInstance("TLSv1.1");
        sslContext.init(null, null, null);
        SSLSocketFactory sslSocketFactory = sslContext.getSocketFactory();

        // 打开连接
        URL targetUrl = new URL(url);
        HttpURLConnection connection = (HttpURLConnection) targetUrl.openConnection();
        if (connection instanceof HttpsURLConnection) {
            // 设置SSL Socket Factory
            ((HttpsURLConnection) connection).setSSLSocketFactory(sslSocketFactory);
        }

        // 发起请求
        BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String line;
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }
        reader.close();

        // 关闭连接
        connection.disconnect();
    }
}
