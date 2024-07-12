package main

import (
	"crypto/tls"
	"fmt"
)

func main() {

	// 创建 TLS 配置
	tlsConfig := &tls.Config{
		InsecureSkipVerify: false,
		ClientAuth:         tls.NoClientCert,
	}

	// 使用 TLS 配置创建 TLS 连接
	conn, err := tls.Dial("tcp", "my.host.name:443", tlsConfig)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer conn.Close()

	// 这时 conn 就是一个已经建立好 TLS 连接的 net.Conn
	fmt.Println("Connected to", conn.RemoteAddr())
}
