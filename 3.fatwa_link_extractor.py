from core.core import launchBrowser,clickLink
from tqdm import tqdm
from time import sleep
import json 
import os
import pandas as pd 

df=pd.read_csv("all_topic.csv")
driver=launchBrowser(Debug=False)
Footer_item=".//div[@class='footer-item']"

fatwa_data=[]
for idx,row in df.iterrows():
    url=row["link"]
    titile=row["title"]
    path=row["path"]
    total_pages=row["num_pages"]
    #print(f"Processing base: {base} with total pages: {total_pages}")
    for page in tqdm(range(1, total_pages + 1), desc=f"Processing {path}"):
        driver.get(f"{url}/?pageno={page}&order=")
        sleep(2)  # Wait for the page to load
        try:
            elems=driver.find_elements(value=Footer_item,by="xpath")
            for elem in elems:
                link=elem.find_element(value=".//a",by="xpath")
                href=link.get_attribute("href")
                if "https://" in href:
                    fatwa_data.append({"title":titile,"path":path,"page":page,"link":url,"fatwa":href})
        except Exception as e:
            print(f"Error processing page {page} of {path}: {e}")
    fdf=pd.DataFrame(fatwa_data)
    fdf.to_csv("intermediate.csv",index=False)
    print(f"Saved Intermediate Fatwa:{len(fatwa_data)}")

fdf=pd.DataFrame(fatwa_data)
fdf.to_csv("all_fatwa.csv",index=False)
