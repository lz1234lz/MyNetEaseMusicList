# -*- coding: utf-8 -*-
import scrapy
import requests
from requests_toolbelt import MultipartEncoder
from scrapy.selector import Selector

class NetmusicSpider(scrapy.Spider):
    name = 'netmusic'
    allowed_domains = ['music.163.com']
    start_urls = ['http://music.163.com/']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': r'_iuqxldmzr_=32;_ntes_nnid=2857b411963182f91484ed3f6f630e8e,1553589972142; _ntes_nuid=2857b411963182f91484ed3f6f630e8e; WM_NI=0tmyVrv0P4aYFjPbo4DjP4YBmF9BgLR8Nd5oViBm%2BY6BC0cPkrR60E9EkBmD%2BXosIjp0uGACBA4nCIAkwM7rRCSST6k3T9tc809JvNTLLgXGooruTsTIZeoywtHy%2B10%2FVGY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed1d843ae97fb99d14090ac8ea2d84a878e9ebaf36dfbea99a4ce45a3ade1afe12af0fea7c3b92af4aca39ad57ab6f0a0d5e45386b6a083ee4088b6a0d5dc4aaf9af7a3e64892e88285b86596b78e8eaa53f69e8dd1e25ca9ae9ed7b34ffb9ba5a3f050e988a194cc62b4f0bba8c449829ffc8fc24383b5b9aeb67a929d9db4d73ea9ed9cdaf769fcf0f7abf54698948488db4dadb1be96d77998979686ee73b5ac889aaa3bf4f19aa8dc37e2a3; WM_TID=S9Gf0CtbkslFBAAVAEZ5ls%2FWGaPO9dFp; __remember_me=true; playerid=68300321; JSESSIONID-WYYY=XDIQdmiIN03h%5CkuVtEcXouuop3UHeoj2WhGGqZXwSYXpVc5DbkE7fBFOMlQoyzBfb%2FtAiUtIXZ3NJsTW6wbyasvVGTbDo%2B6FtzV9o%2F1AQ%2F2i4CwPu8eszWSBI%5CBTZVdxr6VGcsE4Cy8%5CxfsRuh3ig2UKfH1Bxu1YYnAmUU5xA%2Fs%2FXab6%3A1553648235498; MUSIC_U=8f6bd1da8ab3ca2b02b67aeb8d5562e887463e52c3bf9b9f669e3b9403f69e7a1a559c902f498f5a7b3e4b90288760fdaf9e62a8590fd08a; __csrf=2a5d7df25633e6fb0bad9a7dc8fbb69c',
        'Host': 'music.163.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            }
    def start_requests(self):
        yield scrapy.Request('https://music.163.com/playlist?id=24399134',headers=self.headers,callback=self.parse)
    def parse(self, response):
        selcetor_item = response.css('li a')
        for item in selcetor_item:
            url = 'https://music.163.com' + item.css('a::attr("href")').extract()[0]
            yield scrapy.Request(url,headers=self.headers,callback=self.parse_detail,meta={'url':url[30:]})
    def parse_detail(self, response):
        music_url = 'http://music.163.com/song/media/outer/url?id=' + response.meta["url"] + '.mp3'
        music_img = response.css('div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cvrwrap.f-cb.f-pr > div.u-cover.u-cover-6.f-fl > img::attr("src")').extract_first()
        music_name = response.css('div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cnt > div.hd > div > em::text').extract_first()
        artist = response.css('div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cnt > p:nth-child(2) > span > a:nth-child(1)::text').extract_first()
        album = response.css('div.g-bd4.f-cb > div.g-mn4 > div > div > div.m-lycifo > div.f-cb > div.cnt > p:nth-child(3) > a::text').extract_first()
        url = 'http://192.168.1.129:8000/api_v1/music/'
        data = {
            'music_url':music_url,
            'music_name':music_name,
            'music_img':music_img,
            'artist':artist,
            'album':album
        }
        m = MultipartEncoder(fields=data)
        headers = {
            'Content-type' : m.content_type
        }
        try:
            r = requests.post(url,data=m,headers = headers,timeout=5)
        except:
            print('*'*10,'save field','*'*10,'\n')