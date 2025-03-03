#include <iostream>
#include <string>
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <openssl/pem.h>
#pragma warning(disable:4996)

int main() {
	const EC_POINT* pub_key = NULL;
	const BIGNUM* priv_key = NULL;

	EC_KEY* key = EC_KEY_new_by_curve_name(NID_X9_62_prime192v1);
	EC_KEY_generate_key(key);
	pub_key = EC_KEY_get0_public_key(key);
	priv_key = EC_KEY_get0_private_key(key);
	pub_key = EC_KEY_get0_public_key(key);

	EC_KEY_free(key);
	return 0;
}