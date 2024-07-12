package main

import (
	"fmt"
	"golang.org/x/crypto/xtea"
)

func main() {
	key := []byte("0123456789abcdef") // 16字节密钥
	plaintext := []byte("Hello, XTEA!")

	block, err := xtea.NewCipher(key)
	if err != nil {
		fmt.Println("Error creating CAST5 cipher:", err)
		return
	}

	ciphertext := make([]byte, len(plaintext))
	block.Encrypt(ciphertext, plaintext)
	fmt.Printf("Ciphertext: %x\n", ciphertext)

	decrypted := make([]byte, len(ciphertext))
	block.Decrypt(decrypted, ciphertext)
	fmt.Println("Decrypted:", string(decrypted))
}
