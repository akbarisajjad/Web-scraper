import os
import requests
import threading
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

BASE_URL = "https://example.com"
OUTPUT_DIR = "scraped_site"
CRAWL_DEPTH = 2  # عمق خزش

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

def download_file(url, folder):
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            filename = sanitize_filename(os.path.basename(urlparse(url).path))
            filepath = os.path.join(folder, filename)
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return filename
    except:
        pass
    return None

def extract_metadata(soup, page_folder):
    metadata = {
        "title": soup.title.string if soup.title else "No Title",
        "description": "",
        "keywords": ""
    }
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        metadata["description"] = meta_desc["content"]
    
    meta_keywords = soup.find("meta", attrs={"name": "keywords"})
    if meta_keywords:
        metadata["keywords"] = meta_keywords["content"]
    
    meta_path = os.path.join(page_folder, "metadata.txt")
    with open(meta_path, "w", encoding="utf-8") as meta_file:
        for key, value in metadata.items():
            meta_file.write(f"{key}: {value}\n")
    
    print("✅ متا دیتا ذخیره شد:", meta_path)

def extract_text_content(soup, page_folder):
    for tag in soup(["script", "style"]):  
        tag.decompose()  
    text_content = soup.get_text(separator="\n", strip=True)  

    text_path = os.path.join(page_folder, "content.txt")
    with open(text_path, "w", encoding="utf-8") as text_file:
        text_file.write(text_content)
    
    print("✅ متن صفحه ذخیره شد:", text_path)

def extract_and_save_css(soup, page_folder):
    styles = soup.find_all("style")
    global_css = ""

    for i, style in enumerate(styles):
        global_css += f"/* Style Block {i+1} */\n{style.string}\n"
        style.decompose()  

    if global_css:
        css_filename = os.path.join(page_folder, "global.css")
        with open(css_filename, "w", encoding="utf-8") as css_file:
            css_file.write(global_css)
        print("✅ استایل‌های کلی ذخیره شد.")

def scrape_page(url, depth=0):
    if depth > CRAWL_DEPTH:
        return

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    page_folder = os.path.join(OUTPUT_DIR, sanitize_filename(urlparse(url).path.lstrip('/')))
    os.makedirs(page_folder, exist_ok=True)

    extract_metadata(soup, page_folder)
    extract_and_save_css(soup, page_folder)
    extract_text_content(soup, page_folder)

    images = soup.find_all("img")
    threads = []
    for img in tqdm(images, desc="Downloading Images"):
        img_url = urljoin(url, img.get("src"))
        t = threading.Thread(target=download_file, args=(img_url, page_folder))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    html_path = os.path.join(page_folder, "index.html")
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(str(soup.prettify()))

    print(f"✅ صفحه ذخیره شد: {html_path}")

    for a in soup.find_all("a", href=True):
        link = urljoin(url, a["href"])
        scrape_page(link, depth+1)

def zip_output():
    zip_filename = f"{OUTPUT_DIR}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(OUTPUT_DIR):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), OUTPUT_DIR))
    print(f"✅ فایل ZIP ایجاد شد: {zip_filename}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    scrape_page(BASE_URL)
    zip_output()
    driver.quit()
