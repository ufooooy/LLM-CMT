package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha1"
	"encoding/hex"
	"fmt"
)

func main() {
	k, err := rsa.GenerateKey(rand.Reader, 1024)
	CheckErr2(err)
	raw := "Hello RSA!"

	OAEP(raw, k)

}

func OAEP(raw string, k *rsa.PrivateKey) {
	// 加密数据
	encData, err := rsa.EncryptOAEP(sha1.New(), rand.Reader, &k.PublicKey, []byte(raw), nil)
	CheckErr2(err)

	// 将加密信息转换为16进制
	fmt.Println(hex.EncodeToString(encData))

	// 解密数据
	decData, err := rsa.DecryptOAEP(sha1.New(), rand.Reader, k, encData, nil)
	CheckErr2(err)

	fmt.Println(string(decData))
}

func CheckErr2(err error) {
	if err != nil {
		panic(err)
	}
}
