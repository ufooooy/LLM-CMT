package main

import (
	"crypto/sha256"
	"fmt"
	"golang.org/x/crypto/pbkdf2"
)

func main() {
	password := []byte("mysecretpassword")
	salt := make([]byte, 16)
	key := pbkdf2.Key(password, salt, 10000, 32, sha256.New)
	fmt.Printf("Derived Key: %x\n", key)
}
