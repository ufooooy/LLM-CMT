#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include<openssl/rand.h>
#include <openssl/evp.h>
#pragma warning(disable:4996)

#define ITERATIONS 10000
#define KEY_LENGTH 32
#define SALT_LENGTH 128

int main() {
    const char* password = "mySecretPassword";
    unsigned char salt[SALT_LENGTH] = "123456789abcdef";
    unsigned char key[KEY_LENGTH];

    // Generate Key
    PKCS5_PBKDF2_HMAC(password, strlen(password), salt, sizeof(salt), ITERATIONS, EVP_sha256(), KEY_LENGTH, key);

    printf("Derived Key: ");
    for (int i = 0; i < KEY_LENGTH; i++) {
        printf("%02x", key[i]);
    }
    return 0;
}
