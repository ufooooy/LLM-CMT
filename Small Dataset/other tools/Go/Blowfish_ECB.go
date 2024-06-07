package main

import (
	"golang.org/x/crypto/blowfish"

	"github.com/andreburgaud/crypt2go/ecb"

	"github.com/andreburgaud/crypt2go/padding"

	"fmt"

	"encoding/base64"
)

func TestEncrypt() {

	bytes := []byte("cap")

	key := []byte("1c157d26e2db9a96a556e7614e1fbe36")

	encByte := encrypt(bytes, key)

	enc := base64.StdEncoding.EncodeToString(encByte)

	fmt.Printf("ENC - %s\n", enc)

}

func encrypt(pt, key []byte) []byte {

	block, err := blowfish.NewCipher(key)

	if err != nil {

		panic(err.Error())

	}

	mode := ecb.NewECBEncrypter(block)

	padder := padding.NewPkcs5Padding()

	pt, err = padder.Pad(pt) // padd last block of plaintext if block size less than block cipher size

	if err != nil {

		panic(err.Error())

	}

	ct := make([]byte, len(pt))

	mode.CryptBlocks(ct, pt)

	return ct

}

func main() {
	TestEncrypt()
}
