#include<iostream>
#include<openssl/rc4.h>
using namespace std;
#pragma warning(disable:4996)

int main()
{
    unsigned char* key = (unsigned char*)"0123456789abcdef";

    std::string mes = "Hello,RC4!";
    RC4_KEY enkey, dekey;
    RC4_set_key(&enkey, 128, key);
    RC4_set_key(&dekey, 128, key);

    unsigned char c_text[30];
    unsigned char p_text[30];
    RC4(&enkey,mes.size(), reinterpret_cast<const unsigned char*>(mes.c_str()), c_text);
    c_text[mes.size()] = '\0';
    cout <<c_text << endl;
    RC4(&dekey, mes.size(), c_text, p_text);
    p_text[mes.size()] = '\0';
    cout << p_text << endl;
    return 0;
}
