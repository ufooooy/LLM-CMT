package main

import (
	"encoding/hex"
	"fmt"
	"golang.org/x/crypto/md4"
	"strings"
)

func Encode_md4(data string) string {
	h := md4.New()
	h.Write([]byte(data))
	return hex.EncodeToString(h.Sum(nil))
}

func main() {
	strTest := "I love this beautiful world!"
	strEncrypted := "d335a35b61846b9d62f1add8982868f0"
	fmt.Println(strings.EqualFold(Encode_md4(strTest), strEncrypted))
}
