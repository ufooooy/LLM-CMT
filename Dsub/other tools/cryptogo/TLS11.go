package main

import (
	"crypto/tls"
	"fmt"
)

func main() {
	// 创建TLS配置
	tlsConfig := &tls.Config{
		MinVersion: tls.VersionTLS11,
	}

	// 使用TLS配置创建TLS连接
	conn, err := tls.Dial("tcp", "my.host.name:443", tlsConfig)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer conn.Close()

}
