import urllib2
import urllib



url_format = "http://www.bing.com/search?q={query}&intlF=1&first={first}"
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Cookie": "DUP=Q=w1gVFoaPs7cXRpMcrGY5Dg2&T=291736828&A=1&IG=F8DD6C28E36B4A6FB992D1B9E92EF8E9; MUID=2B3C2945C772653D18392379C3726608; SRCHD=AF=NOFORM; SRCHUSR=DOB=20170330; _FP=hta=on; ipv6=hit=1; MUID=2B3C2945C772653D18392379C3726608; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=E9D3307B041B43BF97C1A4DFC4053E01; SRCHUSR=DOB=20170330; MUIDB=2B3C2945C772653D18392379C3726608; _FP=hta=on; ipv6=hit=1; _EDGE_S=mkt=zh-cn&SID=0673D959656A6B2C0A2DD30C64CB6A51; SRCHHPGUSR=CW=1905&CH=1006&DPR=1&UTC=480; _SS=SID=0673D959656A6B2C0A2DD30C64CB6A51&bIm=073872&HV=1490879494; WLS=TS=63626476291; SNRHOP=I=&TS=; _FS=intlF=1; SRCHHPGUSR=CW=1905&CH=788&DPR=1&UTC=480; _EDGE_S=mkt=zh-cn&SID=0673D959656A6B2C0A2DD30C64CB6A51&SID=0673D959656A6B2C0A2DD30C64CB6A51&SID=0673D959656A6B2C0A2DD30C64CB6A51&SID=0673D959656A6B2C0A2DD30C64CB6A51&SID=0673D959656A6B2C0A2DD30C64CB6A51&SID=0673D959656A6B2C0A2DD30C64CB6A51; _SS=SID=0673D959656A6B2C0A2DD30C64CB6A51&bIm=073872&HV=1490882429; WLS=TS=63626479228; SNRHOP=I=&TS=; _FS=intlF=1"
}

def call(query, first = 1):
    global url_format, headers
    while True:
        try:
            query = urllib.quote(query)
            url = url_format.format(query = query, first = first)
            request = urllib2.Request(url, None, headers)
            response = urllib2.urlopen(request)
            return response.read()
        except Exception, e:
            print e
    
if __name__ == "__main__":
    query = 'cock'
    first = 50
    print call(query, 50)


