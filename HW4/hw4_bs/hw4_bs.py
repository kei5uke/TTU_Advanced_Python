import json
import requests
from bs4 import BeautifulSoup


def get_product_list(url):
    # Get page content
    page = requests.get(url, timeout=5)
    # Load it into soup
    soup = BeautifulSoup(page.content, "lxml")
    # find <li> tags where they store products info
    products = soup.find_all("li", {"class": "item"})
    product_list = []
    for product in products:
        # Get product name
        product_names = product.h2.get_text()
        # Get product price
        product_price = product.find("span", {"class":"price"}).get_text()
        # Get product image href
        product_img = product.img.get("src")
        print(product_names,product_price,product_img)
        # Store them as a dict
        product_dict = {"Product name": product_names,
                            "Product price": product_price,
                            "Product image": product_img}
        product_list.append(product_dict)

    try:
        # Get the next page content
        next_page_url = soup.find("a", {"class":"next"})["href"]
        # If the next page exist
        if next_page_url:
            # Recursion: get product list from next page
            tmp = get_product_list(next_page_url)
            # Extend to the current list
            product_list.extend(tmp)
            return product_list
    # If not exist
    except:
        print("Next page does not exists.")
        return product_list

    
    
def main():
    product_list = get_product_list(url = "https://ordi.eu/sulearvutid?___store=en&___from_store=et")
    with open('hw4_bs.json', 'w') as jf:
        json.dump(product_list, jf, indent=4)

if __name__ == "__main__":
    main()