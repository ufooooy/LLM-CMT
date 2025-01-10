#include <stdio.h>
#include <stdlib.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#pragma warning(disable:4996)

int main() {
    SSL_CTX* ctx;
    SSL* ssl;

    // ��ʼ�� OpenSSL ��
    SSL_library_init();
    ERR_load_BIO_strings();
    OpenSSL_add_all_algorithms();

    // ���� SSL �����Ķ���
    ctx = SSL_CTX_new(TLSv1_2_client_method());
    if (ctx == NULL) {
        printf("Failed to create SSL context.\n");
        ERR_print_errors_fp(stderr);
        return -1;
    }

    // ����֤��У��ģʽΪ�������κ�У��
    SSL_CTX_set_verify(ctx, SSL_VERIFY_NONE, NULL);

    // ���� SSL �������������������
    ssl = SSL_new(ctx);
    if (ssl == NULL) {
        printf("Failed to create SSL object.\n");
        return -1;
    }

    // �ر� SSL ����
    SSL_free(ssl);
    SSL_CTX_free(ctx);
    EVP_cleanup();
    ERR_free_strings();

    return 0;
}