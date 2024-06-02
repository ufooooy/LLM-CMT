#include <stdio.h>
#include <stdlib.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#pragma warning(disable:4996)

int main() {
    SSL_CTX* ctx;
    SSL* ssl;

    // 初始化 OpenSSL 库
    SSL_library_init();
    ERR_load_BIO_strings();
    OpenSSL_add_all_algorithms();

    // 创建 SSL 上下文对象
    ctx = SSL_CTX_new(TLSv1_2_client_method());
    if (ctx == NULL) {
        printf("Failed to create SSL context.\n");
        ERR_print_errors_fp(stderr);
        return -1;
    }

    // 设置证书校验模式为不进行任何校验
    SSL_CTX_set_verify(ctx, SSL_VERIFY_NONE, NULL);

    // 创建 SSL 对象并与服务器建立连接
    ssl = SSL_new(ctx);
    if (ssl == NULL) {
        printf("Failed to create SSL object.\n");
        return -1;
    }

    // 关闭 SSL 连接
    SSL_free(ssl);
    SSL_CTX_free(ctx);
    EVP_cleanup();
    ERR_free_strings();

    return 0;
}