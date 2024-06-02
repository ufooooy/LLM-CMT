package app

import (
	"bookget/config"
	"bookget/lib/gohttp"
	"bookget/lib/util"
	"context"
	"crypto/md5"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http/cookiejar"
	"net/url"
	"regexp"
	"strings"
)

type Ncpssd struct {
	dt *DownloadTask
}

func (p *Ncpssd) Init(iTask int, sUrl string) (msg string, err error) {
	p.dt = new(DownloadTask)
	p.dt.UrlParsed, err = url.Parse(sUrl)
	p.dt.Url = sUrl
	p.dt.Index = iTask
	p.dt.Jar, _ = cookiejar.New(nil)
	return p.download()
}

func (p *Ncpssd) getBookId(sUrl string) (bookId string) {
	m := regexp.MustCompile(`(?i)barcodenum=([A-z0-9_-]+)`).FindStringSubmatch(sUrl)
	if m != nil {
		return m[1]
	}
	m = regexp.MustCompile(`(?i)pdf/([A-z0-9_-]+)\.pdf`).FindStringSubmatch(sUrl)
	if m != nil {
		return m[1]
	}
	return bookId
}

func (p *Ncpssd) download() (msg string, err error) {
	respVolume, err := p.getVolumes(p.dt.Url, p.dt.Jar)
	if p.dt.BookId == "" || err != nil {
		fmt.Println(err)
		return "requested URL was not found.", err
	}
	name := util.GenNumberSorted(p.dt.Index)
	log.Printf("Get %s  %s\n", name, p.dt.Url)
	bookId := p.dt.UrlParsed.Query().Get("type")
	if bookId == "" {
		bookId = "ncpssd"
	}
	p.dt.SavePath = CreateDirectory(p.dt.UrlParsed.Host, bookId, "")
	for i, vol := range respVolume {
		if config.Conf.Volume > 0 && config.Conf.Volume != i+1 {
			continue
		}
		log.Printf(" %d/%d volume, %s \n", i+1, len(respVolume), vol)
		p.do(vol)
		util.PrintSleepTime(config.Conf.Speed)
		fmt.Println()
	}
	return msg, err
}

func (p *Ncpssd) do(pdfUrl string) (msg string, err error) {
	token, _ := p.getToken()
	ext := util.FileExt(pdfUrl)
	dest := p.dt.SavePath + p.dt.BookId + ext
	jar, _ := cookiejar.New(nil)
	ctx := context.Background()
	referer := "https://" + p.dt.UrlParsed.Host
	gohttp.FastGet(ctx, pdfUrl, gohttp.Options{
		DestFile:    dest,
		Overwrite:   false,
		Concurrency: 1,
		CookieJar:   jar,
		CookieFile:  config.Conf.CookieFile,
		Headers: map[string]interface{}{
			"user-agent": config.Conf.UserAgent,
			"Referer":    referer,
			"Origin":     referer,
			"site":       "npssd",
			"sign":       token,
		},
	})
	return "", err
}

func (p *Ncpssd) getVolumes(sUrl string, jar *cookiejar.Jar) (volumes []string, err error) {
	if strings.Contains(sUrl, "fullTextRead?filePath=") {
		dUrl := p.getPdfUrl(sUrl)
		p.dt.BookId = p.getBookId(dUrl)
		volumes = append(volumes, dUrl)
	} else {
		p.dt.BookId = p.getBookId(sUrl)
		name := util.GenNumberSorted(p.dt.Index)
		log.Printf("Get %s  %s\n", name, sUrl)
		dUrl, err := p.getReadUrl(p.dt.BookId)
		if err != nil {
			return nil, err
		}
		volumes = append(volumes, dUrl)
	}
	return volumes, err
}

func (p *Ncpssd) getCanvases(sUrl string, jar *cookiejar.Jar) (canvases []string, err error) {
	//TODO implement me
	panic("implement me")
}

func (p *Ncpssd) getBody(sUrl string, jar *cookiejar.Jar) ([]byte, error) {
	referer := url.QueryEscape(p.dt.Url)
	ctx := context.Background()
	cli := gohttp.NewClient(ctx, gohttp.Options{
		CookieFile: config.Conf.CookieFile,
		CookieJar:  jar,
		Headers: map[string]interface{}{
			"User-Agent":       config.Conf.UserAgent,
			"Referer":          referer,
			"X-Requested-With": "XMLHttpRequest",
			"Content-Type":     "application/json; charset=utf-8",
		},
	})
	resp, err := cli.Get(sUrl)
	if err != nil {
		return nil, err
	}
	bs, _ := resp.GetBody()
	if bs == nil {
		return nil, errors.New(fmt.Sprintf("ErrCode:%d, %s", resp.GetStatusCode(), resp.GetReasonPhrase()))
	}
	return bs, nil
}

func (p *Ncpssd) postBody(sUrl string, d []byte) ([]byte, error) {
	//TODO implement me
	panic("implement me")
}

func (p *Ncpssd) getReadUrl(bookId string) (string, error) {
	apiUrl := fmt.Sprintf("https://%s/Literature/readurl?id=%s&type=3", p.dt.UrlParsed.Host, bookId)
	bs, err := p.getBody(apiUrl, p.dt.Jar)
	if err != nil {
		return "", err
	}
	type ResponseReadUrl struct {
		Url string `json:"url"`
	}
	var respReadUrl ResponseReadUrl
	if err = json.Unmarshal(bs, &respReadUrl); err != nil {
		return "", err
	}
	return respReadUrl.Url, nil
}

func (p *Ncpssd) getPdfUrl(sUrl string) string {
	var pdfUrl string
	m := regexp.MustCompile(`(?i)filePath=(.+)\.pdf`).FindStringSubmatch(sUrl)
	if m != nil {
		s, _ := url.QueryUnescape(m[1])
		pdfUrl = s + ".pdf"
	}
	return pdfUrl
}

func (p *Ncpssd) getToken() (string, error) {
	apiUrl := "https://" + p.dt.UrlParsed.Host + "/get/server/date"
	bs, err := p.getBody(apiUrl, p.dt.Jar)
	if err != nil {
		return "", err
	}
	type ResponseServerDate struct {
		Result bool   `json:"result"`
		Code   int    `json:"code"`
		Data   string `json:"data"`
		Succee bool   `json:"succee"`
	}

	var responseServerDate ResponseServerDate
	if err = json.Unmarshal(bs, &responseServerDate); err != nil {
		return "", err
	}
	h := md5.New()
	h.Write([]byte("L!N45S26y1SGzq9^" + responseServerDate.Data))
	token := fmt.Sprintf("%x", h.Sum(nil))
	return token, nil
}
