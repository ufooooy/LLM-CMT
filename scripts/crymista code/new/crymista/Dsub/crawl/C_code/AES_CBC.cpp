#include<openssl/aes.h>
#include<iostream>
#pragma warning(disable:4996)
using namespace std;

const char* aesKey = "0123456789abcdef";
const char* mystr = "This is AES!";

void decrypto(const  char* ciphertext, const unsigned char* key, unsigned char* iv, unsigned char** outText)
{
    AES_KEY aes;
    AES_set_decrypt_key(key, 128, &aes);
    int datalen = strlen(mystr) + 1;

    unsigned char* decrypt = (unsigned char*)calloc(datalen, 1);
    AES_cbc_encrypt((unsigned char*)ciphertext, decrypt, datalen, &aes, iv, AES_DECRYPT);

    *outText = decrypt;
}
void encryptoText(const char* plainText, const unsigned char* key, unsigned char* iv, unsigned char** outText)
{
    AES_KEY aes;
    AES_set_encrypt_key(key, 128, &aes); 

    int datalen;
    if ((strlen(plainText) + 1) % 16 == 0)
    {
        datalen = strlen(plainText) + 1;
    }
    else
    {
        datalen = ((strlen(plainText) + 1) / 16 + 1) * 16;
    }
    unsigned char* cipherText = (unsigned char*)calloc(datalen, 1);

    AES_cbc_encrypt((unsigned char*)plainText, cipherText, datalen, &aes, iv, AES_ENCRYPT);

    *outText = cipherText;

}

int main()
{

    unsigned char iv[16];
    memset(iv, 'a', sizeof(iv));
    unsigned char* cipher = NULL;
    unsigned char* text = NULL;
    
    encryptoText(mystr, (unsigned char*)aesKey, iv, &cipher);
    cout << "Encrypted£º";
    for (int i = 0; i < sizeof(cipher); i++) {
        printf("%02X", cipher[i]);
    }
    memset(iv, 'a', sizeof(iv));
    decrypto((char*)cipher, (unsigned char*)aesKey, iv, &text);
    cout << endl << "Decrypted£º" << text << endl;
    free(cipher);
    free(text);
}