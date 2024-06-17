#include <iostream>
#include <string>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#pragma warning(disable:4996)

int main()
{
    // Generate the RSA key pair
    RSA* keypair = RSA_generate_key(1024, RSA_F4, NULL, NULL);

    // Extract the public key from the key pair
    const BIGNUM* n, * e,*d;
    RSA* pubkey = RSA_new();
    RSA_get0_key(keypair, &n, &e, NULL);
    RSA_set0_key(pubkey, BN_dup(n), BN_dup(e), NULL);

    RSA* prikey = RSA_new();
    RSA_get0_key(keypair, &n, &e, &d);
    RSA_set0_key(prikey, BN_dup(n), BN_dup(e), BN_dup(d));

    // Get the message to be encrypted
    std::string message = "Hello, RSA!";

    // Allocate memory for the encrypted message
    unsigned char* encrypted_message = new unsigned char[RSA_size(pubkey)];

    // Encrypt the message
    int result = RSA_public_encrypt(message.size(), (const unsigned char*)message.c_str(), encrypted_message, pubkey, RSA_PKCS1_OAEP_PADDING);

    // Print the encrypted message
    std::cout << "Encrypted message: ";
    for (int i = 0; i < result; i++)
        std::cout << std::hex << (encrypted_message[i] & 0xff) << " ";
    std::cout << std::endl;

    // Clean up
    RSA_free(keypair);
    RSA_free(pubkey);
    delete[] encrypted_message;

    return 0;
}