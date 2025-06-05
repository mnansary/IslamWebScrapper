from core.core import launchBrowser,clickLink
from tqdm import tqdm
from time import sleep
import json 
import os
import pandas as pd
driver=launchBrowser(Debug=False)

BASES = {
    "القرآن-الكريم": {
        "url": "https://www.islamweb.net/ar/fatawa/350/القرآن-الكريم",
    },
    "العقيدة-الإسلامية": {
        "url": "https://www.islamweb.net/ar/fatawa/4/العقيدة-الإسلامية",
    },
    "الحديث-الشريف": {
        "url": "https://www.islamweb.net/ar/fatawa/456/الحديث-الشريف",
    },
    "السيرة-النبوية": {
        "url": "https://www.islamweb.net/ar/fatawa/588/السيرة-النبوية",
    },
    "الدعوة-ووسائلها": {
        "url": "https://www.islamweb.net/ar/fatawa/850/الدعوة-ووسائلها",
    },
    "طب-وإعلام-وقضايا-معاصرة": {
        "url": "https://www.islamweb.net/ar/fatawa/876/طب-وإعلام-وقضايا-معاصرة",
    },
    "فكر-وسياسة-وفن": {
        "url": "https://www.islamweb.net/ar/fatawa/946/فكر-وسياسة-وفن",
    },
    "الفضائل-والتراجم": {
        "url": "https://www.islamweb.net/ar/fatawa/1024/الفضائل-والتراجم",
    },
    "الآداب-والأخلاق-والرقائق": {
        "url": "https://www.islamweb.net/ar/fatawa/1112/الآداب-والأخلاق-والرقائق",
    },
    "الأذكار-والأدعية": {
        "url": "https://www.islamweb.net/ar/fatawa/1156/الأذكار-والأدعية",
    },
    "فقه-العبادات": {
        "url": "https://www.islamweb.net/ar/fatawa/1202/فقه-العبادات",
    },
    "فقه-المعاملات": {
        "url": "https://www.islamweb.net/ar/fatawa/1930/فقه-المعاملات",
    },
    "فقه-الأسرة-المسلمة": {
        "url": "https://www.islamweb.net/ar/fatawa/2198/فقه-الأسرة-المسلمة",
    },
    "فقه-المواريث": {
        "url": "https://www.islamweb.net/ar/fatawa/2420/فقه-المواريث",
    },
    "فقه-الجنايات": {
        "url": "https://www.islamweb.net/ar/fatawa/2440/فقه-الجنايات",
    },
    "الحدود-والتعزيرات": {
        "url": "https://www.islamweb.net/ar/fatawa/2474/الحدود-والتعزيرات",
    },
    "الأطعمة-والأشربة-والصيد": {
        "url": "https://www.islamweb.net/ar/fatawa/2514/الأطعمة-والأشربة-والصيد",
    },
    "الأقضية-والشهادات": {
        "url": "https://www.islamweb.net/ar/fatawa/2546/الأقضية-والشهادات",
    },
    "الأيمان-والنذور": {
        "url": "https://www.islamweb.net/ar/fatawa/2584/الأيمان-والنذور",
    },
    "اللباس-والزينة": {
        "url": "https://www.islamweb.net/ar/fatawa/2602/اللباس-والزينة",
    },
    "أخبار": {
        "url": "https://www.islamweb.net/ar/fatawa/2646/أخبار",
    },
    "تراجم-وشخصيات": {
        "url": "https://www.islamweb.net/ar/fatawa/2756/تراجم-وشخصيات",
    },
    "أصول-الفقه-وقواعده": {
        "url": "https://www.islamweb.net/ar/fatawa/2884/أصول-الفقه-وقواعده",
    },
    "مصادر-الفقه-الإسلامي": {
        "url": "https://www.islamweb.net/ar/fatawa/2888/مصادر-الفقه-الإسلامي",
    }
}

# xpaths
Struct_item=".//ul[@class='tree']"
folder_item=".//div[@class='tree_label']"
doc_item=".//span[@class='tree_label']/a"

all_data_urls=[]
for base in BASES:
    cur_cat_urls=[]
    topic=base 
    url=BASES[base]["url"]
    all_data_urls.append({"title":topic,"link":url,"path":topic})
    print(f"Processing topic: {topic} {url}")
    cur_cat_urls=[url]
    cur_cat_path=[topic]
    while cur_cat_urls:
        #print(cur_cat_urls)
        for gurl,gtopic in zip(cur_cat_urls,cur_cat_path):
            driver.get(gurl)
            elem=driver.find_element(value=Struct_item,by="xpath")
            cats=elem.find_elements(value=folder_item,by="xpath")
            for cat in cats:
                title=cat.text
                link=cat.find_element(by="xpath",value=".//a[@target='_blank']").get_attribute("href")
                all_data_urls.append({"title":title,"link":link,"path":f"{gtopic}#{title}"})
                cur_cat_urls.append(link)
                cur_cat_path.append(f"{gtopic}#{title}")

            # get docs
            docs=elem.find_elements(value=doc_item,by="xpath")
            for doc in docs:
                title=doc.text
                link=doc.get_attribute("href")
                all_data_urls.append({"title":title,"link":link,"path":f"{gtopic}#{title}"})
            cur_cat_urls.remove(gurl)
            cur_cat_path.remove(gtopic)
            print("Remaining:",len(cur_cat_urls),"Extracted:",len(all_data_urls),"current:",gurl)

df=pd.DataFrame(all_data_urls)
df.to_csv("all_topic.csv",index=False)