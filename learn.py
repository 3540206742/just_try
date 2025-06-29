import requests
import parsel
import csv
f = open('data.csv',mode='w',encoding='utf-8',newline='')
csv_writer=csv.DictWriter(f,fieldnames=[
    "户型",
    "信息",
    "房名",
    "地址",
    "描述",
])
csv_writer.writeheader()
#发送请求
for page in range(1,11):
    print(f"正在采集第{page}页的数据内容")
    url = f"https://www.anjuke.com/sale/p{page}/?pi=bing-cpc-dc-ty2&kwid=%7Bkeywordid%7D&msclkid=73f710266c2b19fcd0237846d9eead45"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
    }
    response = requests.get(url=url, headers=headers)
    # 获取数据
    html = response.text
    #print(html)

    # 解析数据
    selector = parsel.Selector(html)
    divs = selector.css('.property-content')
    for div in divs:
        title = div.css('.property-content-title-name::text').get()
        housetype = ''.join(div.css('.property-content-info-attribute span::text').getall())
        houseinfo = div.css('.property-content-info-text::text').getall()
        houseinfo = [i.strip() for i in houseinfo if i != ' ']
        housename = div.css('.property-content-info-comm-name::text').get()
        houseaddress = ''.join(div.css('.property-content-info-comm-address span::text').getall())
        housedescrip = div.css('.property-content-info-tag::text').getall()
        dic = {
            "户型": housetype,
            "信息": houseinfo,
            "房名": housename,
            "地址": houseaddress,
            "描述": housedescrip,
        }
        print(dic)
        csv_writer.writerow(dic)
#保存数据
