from lxml import html
import requests

def main():
    # page = requests.get('https://www.google.com/search?q=donkeys&espv=2&sxsrf=ACYBGNSwqBUElVjmEWOTu3-mXPnReqFoLw:1581376760401&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiY7bzAj8jnAhUQjq0KHbXwBEYQ_AUoAXoECBMQAw&biw=838&bih=880#imgrc=rgr8UZ_nc6G_HM')
    page = requests.get('https://www.google.com/imgres?imgurl=https%3A%2F%2Fcdn.mos.cms.futurecdn.net%2F6h8C6ygTdR2jyyUxkALwsc-320-80.jpg&imgrefurl=https%3A%2F%2Fwww.livescience.com%2F54258-donkeys.html&tbnid=rgr8UZ_nc6G_HM&vet=12ahUKEwiBlJbVkP_nAhVd_6wKHRJ8DkkQMygAegUIARCKAg..i&docid=NvtDSdTmwQ5hWM&w=320&h=213&q=donkeys&ved=2ahUKEwiBlJbVkP_nAhVd_6wKHRJ8DkkQMygAegUIARCKAg')
    tree = html.fromstring(page.content)
    #This will create a list of buyers:
    # image_html = tree.xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img/@src')
    image_html = tree.xpath('/html/head/title/text()')
    # image_html = tree.xpath('//div[@title="buyer-name"]/text()')
    #This will create a list of prices
    # prices = tree.xpath('//span[@class="item-price"]/text()')
    # print('Buyers: ', buyers)
    # print('Prices: ', prices)
    print(image_html)


    #try a differe XML parser thing maybe, this one can't find it

if __name__ == '__main__':
    main()