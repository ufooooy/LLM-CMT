package main

import (
	"crypto/rand"
	"crypto/rsa"
	"encoding/hex"
	"fmt"
)

func main() {
	k, err := rsa.GenerateKey(rand.Reader, 1024)
	CheckErr(err)
	raw := "Hello RSA!"

	PKCS1v15(raw, k)
}

func PKCS1v15(raw string, k *rsa.PrivateKey) {
	// 加密数据
	encData, err := rsa.EncryptPKCS1v15(rand.Reader, &k.PublicKey, []byte(raw))
	CheckErr(err)

	// 将加密信息转换为16进制
	fmt.Println(hex.EncodeToString(encData))

	// 解密数据
	decData, err := rsa.DecryptPKCS1v15(rand.Reader, k, encData)
	CheckErr(err)

	fmt.Println(string(decData))
}

func CheckErr(err error) {
	if err != nil {
		panic(err)
	}
}
