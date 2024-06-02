#include <stdio.h>
#include <stdlib.h>
#include <openssl/dsa.h>
#include <openssl/err.h>
#include<cstring>
#pragma warning(disable:4996)

int main() {
    DSA* dsa = NULL;
    int ret;
    const char* message = "Hello, DSA!";

    dsa = DSA_new();

    //DSA Key
    dsa = DSA_generate_parameters(1024, NULL, 0, NULL, NULL, NULL, NULL);
    DSA_generate_key(dsa);

    // Signature
    unsigned char signature[1024];
    unsigned int sig_len = 0;
    ret = DSA_sign(0, (unsigned char*)message, strlen(message), signature, &sig_len, dsa);

    // Verify Signature
    ret = DSA_verify(0, (const unsigned char*)message, strlen(message), signature, sig_len, dsa);
    if (ret != 1) {
        printf("Failed!\n");
    }
    else {
        printf("Succeeded!\n");
    }

    // free
    DSA_free(dsa);

    return 0;
}
