from core.core import launchBrowser
from tqdm import tqdm
from time import sleep
import json 
import os

Footer_item=".//div[@class='footer-item']"
Pagination_item=".//*[@class='pagination']"

BASES = {
    "العقيدة-الإسلامية": {
        "url": "https://www.islamweb.net/ar/fatawa/4/العقيدة-الإسلامية",
    },
    "القرآن-الكريم": {
        "url": "https://www.islamweb.net/ar/fatawa/350/القرآن-الكريم",
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


if __name__ == "__main__":
    driver=launchBrowser(Debug=False)


    for base in BASES:
        topic=base 
        url=BASES[base]["url"]
        print(f"Processing topic: {topic} {url}")
        driver.get(url)
        try:
            try:
                elem=driver.find_element(value=Pagination_item,by="xpath")
            except Exception as e:
                BASES[base]["total_pages"] = 1
                print(f"Pagination not found for {base}, setting total_pages to 1")
                continue
            elems=elem.find_elements(value=".//li",by="xpath")
            total_pages = 0
            print(len(elems), "pagination items found")
            for elem in elems:total_pages=max(total_pages, int(elem.text)) if elem.text.isdigit() else total_pages
            print(f"Total pages found: {total_pages}")
            BASES[base]["total_pages"] = total_pages
        except Exception as e:
            print(f"Error finding pagination: {e}")
    
    for base in BASES:
        BASES[base]["links"] = []
        url=BASES[base]["url"]
        total_pages=BASES[base]["total_pages"]
        print(f"Processing base: {base} with total pages: {total_pages}")
        for page in tqdm(range(1, total_pages + 1), desc=f"Processing {base}"):
            driver.get(f"{url}/?pageno={page}&order=")
            sleep(2)  # Wait for the page to load
            try:
                elems=driver.find_elements(value=Footer_item,by="xpath")
                for elem in elems:
                    link=elem.find_element(value=".//a",by="xpath")
                    href=link.get_attribute("href")
                    if "https://" in href:
                        BASES[base]["links"].append(href)
            except Exception as e:
                print(f"Error processing page {page} of {base}: {e}")
    
    
    with open("islamweb_fatawa.json", "w", encoding="utf-8") as f:
        json.dump(BASES, f, ensure_ascii=False, indent=4)
    print("Data saved to islamweb_fatawa.json")
    driver.quit()    