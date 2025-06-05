from core.core import launchBrowser,clickLink
from tqdm import tqdm
from time import sleep
import json 
import os
import pandas as pd 

df=pd.read_csv("all_topic.csv")
driver=launchBrowser(Debug=False)
Footer_item=".//div[@class='footer-item']"
Pagination_item=".//*[@class='pagination']"

num_pages=[]
for url in df.link.tolist():
    driver.get(url)
    try:
        try:
            elem=driver.find_element(value=Pagination_item,by="xpath")
        except Exception as e:
            num_pages.append(1)
            print(f"EXCEPTION: {url}")
            continue
        elems=elem.find_elements(value=".//li",by="xpath")
        total_pages = 0
        
        for elem in elems:total_pages=max(total_pages, int(elem.text)) if elem.text.isdigit() else total_pages
        print(f"{url} Total pages found: {total_pages}")
        num_pages.append(total_pages) 
    except Exception as e:
        print(f"Error finding pagination: {e}")
df["num_pages"]=num_pages
df.to_csv("all_topic.csv",index=False)       
    