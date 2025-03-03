package main

import (
	"fmt"
	"net/url"
)

func main() {
	urlString := "http://www.baidu.com"
	parsedURL, err := url.Parse(urlString)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// 输出解析后的 URL 信息
	fmt.Printf("Host: %s\n", parsedURL.Host)
}
