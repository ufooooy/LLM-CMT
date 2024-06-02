package main

import (
	"fmt"
	"golang.org/x/crypto/cast5"
)

func main() {
	key := []byte("0123456789abcdef") // 16字节密钥
	plaintext := []byte("CroCAST5")

	// 创建一个 CAST5 加密器
	block, err := cast5.NewCipher(key)
	if err != nil {
		fmt.Println("Error creating CAST5 cipher:", err)
		return
	}

	ciphertext := make([]byte, cast5.BlockSize)
	block.Encrypt(ciphertext, plaintext)
	fmt.Printf("Ciphertext: %x\n", ciphertext)

	decrypted := make([]byte, len(plaintext))
	block.Decrypt(decrypted, ciphertext)
	fmt.Println("Decrypted:", string(decrypted))
}
