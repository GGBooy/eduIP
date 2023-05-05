## get the web content from https://ispip.clang.cn/cernet_cidr.html

import requests
import json


def getContent(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    json_response = response.content.decode()
    return json_response


# regular expression to match ip address, e.g. 127.0.0.1/32, return a list
def getIpCidr(content):
    import re
    pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d+')
    ipCidr = pattern.findall(content)
    return ipCidr

# use the IP list to create a yaml file with the format like:
# rules:
#   - IP-CIDR,202.114.0.250/16,HUST,no-resolve
#   - IP-CIDR,222.20.96.0/24,HUST,no-resolve

def createYaml(ipCidr):
    ip = ['IP-CIDR,'+item+',HUST,no-resolve' for item in ipCidr]
    import yaml
    # 带有两个空格的缩进
    yaml_content = yaml.dump({'prepend-rules': ip}, indent=2)
    with open('hust.yaml', 'w') as f:
        f.write(yaml_content)
    




if __name__ == '__main__':
    url = 'https://ispip.clang.cn/cernet_cidr.html'
    content = getContent(url)
    ipCidr = getIpCidr(content)
    print(ipCidr)
    createYaml(ipCidr)



