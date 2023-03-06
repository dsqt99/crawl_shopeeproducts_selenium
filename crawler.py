from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import json
import time
import warnings
warnings.filterwarnings("ignore")

def get_product_info(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    print('prepare load web')
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
    driver.get(url)
    print('pass load web')
    driver.implicitly_wait(3)

    # Code to scrape Shopee product information
    product_name_div = driver.find_element(By.CSS_SELECTOR, 'div._44qnta')
    product_name = product_name_div.find_element(By.TAG_NAME, 'span').get_attribute('textContent')

    price = driver.find_element(By.CSS_SELECTOR, 'div.pqTWkA').get_attribute('textContent')

    description = driver.find_element(By.CSS_SELECTOR, 'p.irIKAp').get_attribute('textContent')

    reviandrate = driver.find_elements(By.CSS_SELECTOR, 'div._1k47d8')
    rating = reviandrate[0].get_attribute('textContent')
    reviews = reviandrate[1].get_attribute('textContent')

    type_product = driver.find_elements(By.CSS_SELECTOR, 'a.akCPfg')[-1].get_attribute('textContent')

    try:
        related_products = []
        # while len(driver.find_elements(By.CSS_SELECTOR, 'div.F5GEoY')) == 0:
        #     # scroll to bottom
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     driver.implicitly_wait(1)
        # rps = driver.find_elements(By.CSS_SELECTOR, 'div.F5GEoY')[:5]
        # for rp in rps:
        #     related_product = rp.find_element(By.CSS_SELECTOR, 'div.xu+II7.xIpsKK').get_attribute('textContent')
        #     related_products.append(related_product)
    except:
        pass

    link = url

    sale_quatity = driver.find_element(By.CSS_SELECTOR, 'div.P3CdcB').get_attribute('textContent')

    product = {
        'product_name': product_name,
        'price': price,
        'description': description,
        'reviews': reviews,
        'rating': rating,
        'type_product': type_product,
        'related_products': related_products,
        'link': link,
        'sale_quantity': sale_quatity
    }
    driver.quit()
    return product

def main():
    # read urls from file 
    with open('urls.txt', 'r') as f:
        full_urls = f.read().splitlines()

    idx_continue = 0
    urls = full_urls[idx_continue:]
    print('number of urls: ', len(urls))

    # urls = [
    #     'https://shopee.vn/%C3%81o-thun-tay-l%E1%BB%A1-form-r%E1%BB%99ng-nam-n%E1%BB%AF-ch%E1%BB%AF-ki%E1%BB%83u-SVG-v%E1%BA%A3i-%C4%91%E1%BA%B9p-d%C3%A0y-m%E1%BB%8Bn-i.76875639.4687089413?sp_atk=c5589dcf-a6ed-4575-bb09-91ad8b8bf763&xptdk=c5589dcf-a6ed-4575-bb09-91ad8b8bf763',
    # ]

    # Create a thread pool with 5 threads
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit each URL to the thread pool
        futures = [executor.submit(get_product_info, url) for url in urls]

        with open('products.json', 'a', encoding='utf-8') as f:
            # Wait for all tasks to complete
            for i, future in enumerate(futures):
                print('Scraping product {}/{}'.format(i + idx_continue, len(futures)))
                # result to json
                res = future.result()
                json.dump(res, f, ensure_ascii=False)
                if i % 10 == 0:
                    time.sleep(5)
                f.write('\n')
        f.close()

        print('Done scraping products')

if __name__ == '__main__':
    main()