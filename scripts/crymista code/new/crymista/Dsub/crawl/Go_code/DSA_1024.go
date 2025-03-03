package main

import (
	"crypto/dsa"
	"crypto/rand"
	"fmt"
	"log"
	"math/big"
)

func main() {
	var params dsa.Parameters
	// 设置DSA参数
	if err := dsa.GenerateParameters(&params, rand.Reader, dsa.L1024N160); err != nil {
		log.Fatalf("Failed to generate parameters: %v", err)
	}

	var privateKey dsa.PrivateKey
	privateKey.PublicKey.Parameters = params
	// 生成私钥
	dsa.GenerateKey(&privateKey, rand.Reader)

	fmt.Println("Private Key: ", privateKey)

	//Signature
	message := []byte("Hello, DSA!")
	r, s, err := dsa.Sign(rand.Reader, &privateKey, message)
	if err != nil {
		panic(err)
	}

	signature := r.Bytes()
	signature = append(signature, s.Bytes()...)

	//Signature Verify
	r = big.NewInt(0).SetBytes(signature[:20])
	s = big.NewInt(0).SetBytes(signature[20:])
	fmt.Println(dsa.Verify(&privateKey.PublicKey, message, r, s))

}
