import argparse
from urllib.parse import quote

def user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", help="keywords of google images you want")
    args = parser.parse_args()
    return args.keyword

def construct_url(keyword):

    params = '&tbm='

    url = 'https://www.google.com/search?q=' + quote(
                keyword.encode('utf-8')) + '&espv=2&sxsrf=ACYBGNSwqBUElVjmEWOTu3-mXPnReqFoLw:1581376760401&source=lnms' + params + 'isch&sa=X&ved=2ahUKEwiY7bzAj8jnAhUQjq0KHbXwBEYQ_AUoAXoECBMQAw&biw=838&bih=880'

    print(url)
   
def main():
    keyword = user_input()
    construct_url(keyword)

if __name__ == '__main__':
    main()