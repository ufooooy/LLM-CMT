#include<openssl/hmac.h>
#include<openssl/sha.h>
#include<iostream>
#pragma warning(disable:4996)
using namespace std;
int main()
{
    char key[] = "ad12ni12";
    char data[] = "hello world how are you";
    unsigned char digest[SHA_DIGEST_LENGTH] = { 0 };
    char mdbuf[2 * SHA_DIGEST_LENGTH + 1] = { 0 };
    unsigned int len = 0;
   
    SHA1((const unsigned char*)data, strlen(data), digest);
    for (int i = 0; i < SHA_DIGEST_LENGTH; i++)
    {
        sprintf(&mdbuf[2 * i], "%02x", digest[i]);
    }
    cout << "Result£º" << mdbuf << endl;

}