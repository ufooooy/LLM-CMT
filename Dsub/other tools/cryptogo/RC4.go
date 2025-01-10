package main

import (
	"crypto/rc4"
	"fmt"
)

func RC4Encrypt(key, plaintext []byte) ([]byte, error) {
	block, err := rc4.NewCipher(key)
	if err != nil {
		fmt.Println("Error creating CAST5 cipher:", err)
		return nil, err
	}
	ciphertext := make([]byte, len(plaintext))
	block.XORKeyStream(ciphertext, plaintext)
	return ciphertext, nil
}

func main() {
	key := []byte("0123456789abcdef")
	plaintext := []byte("RC4 Encryption!")

	//Encrypt
	ciphertext, err := RC4Encrypt(key, plaintext)
	fmt.Printf("Ciphertext: %x\n", ciphertext)
	if err != nil {
		fmt.Println("Error decrypting:", err)
		return
	}

	//Decrypt
	decrypted, err := RC4Encrypt(key, ciphertext)
	fmt.Println("Decrypted:", string(decrypted))
	if err != nil {
		fmt.Println("Error decrypting:", err)
		return
	}
}
