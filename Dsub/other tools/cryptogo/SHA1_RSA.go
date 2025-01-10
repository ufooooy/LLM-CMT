package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha1"
	"encoding/hex"
	"fmt"
)

func main() {
	// 生成私钥
	k, err := rsa.GenerateKey(rand.Reader, 2048)
	CheckErr_SHA1_RSA(err)
	raw := "Hello RSA!"

	OAEP_SHA1(raw, k)

}

func OAEP_SHA1(raw string, k *rsa.PrivateKey) {
	// 加密数据
	encData, err := rsa.EncryptOAEP(sha1.New(), rand.Reader, &k.PublicKey, []byte(raw), nil)
	CheckErr_SHA1_RSA(err)

	// 将加密信息转换为16进制
	fmt.Println(hex.EncodeToString(encData))

	// 解密数据
	decData, err := rsa.DecryptOAEP(sha1.New(), rand.Reader, k, encData, nil)
	CheckErr_SHA1_RSA(err)

	fmt.Println(string(decData))
}

func CheckErr_SHA1_RSA(err error) {
	if err != nil {
		panic(err)
	}
}
