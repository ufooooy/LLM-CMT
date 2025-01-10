#include<iostream>
#pragma warning(disable:4996)
#include<openssl/des.h>   
using namespace std;
int main(int argc, char* argv[])
{
	unsigned char data[] = "DES TEST";  
	unsigned char out[1024] = { 0 };    
	unsigned char out2[1024] = { 0 };   
	//1.…Ë÷√√‹‘ø
	const_DES_cblock key = "1234567";  
	DES_key_schedule key_sch;         
	DES_set_key(&key, &key_sch);

	DES_ecb_encrypt((const_DES_cblock*)data, (DES_cblock*)out, &key_sch, 1);
	for (int i = 0; i < 8; i++) {
		printf("%02X", out[i]);
	}
	cout << endl;
	DES_ecb_encrypt((const_DES_cblock*)out, (DES_cblock*)out2, &key_sch, 0);
	cout << out2 << endl;

	return 0;
}
