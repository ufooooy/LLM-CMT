package main

import (
	"crypto/rand"
	"crypto/sha256"
	"fmt"
	"golang.org/x/crypto/pbkdf2"
)

func main() {
	password := []byte("mysecretpassword")
	salt := make([]byte, 16)
	_, err := rand.Read(salt)
	if err != nil {
		fmt.Println("Error generating salt:", err)
		return
	}

	key := pbkdf2.Key(password, salt, 1000, 32, sha256.New)
	fmt.Printf("Derived Key: %x\n", key)
}
