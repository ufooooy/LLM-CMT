package dataset1123;

import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocketFactory;

public class DefaultHostnameVerifierMisuseExample {

    public static void main(String[] args) throws Exception {
        String url = "https://example.com";
        // 创建URL对象
        URL targetUrl = new URL(url);

        // 获取SSL上下文
        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(null, null, null);
        SSLSocketFactory socketFactory = sslContext.getSocketFactory();

        // 打开连接
        HttpURLConnection connection = (HttpURLConnection) targetUrl.openConnection();
        if (connection instanceof HttpsURLConnection) {
            // 设置SSL Socket Factory，可能使用了默认的主机名验证器
            ((HttpsURLConnection) connection).setSSLSocketFactory(socketFactory);
        }

        // 发起请求
        InputStream input = connection.getInputStream();
        // 读取响应...

        // 关闭连接
        input.close();
    }
}
