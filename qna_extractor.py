from core.core import launchBrowser,clickLink
from tqdm import tqdm
from time import sleep
import json 
import os
import arabic_reshaper
import json

with open("islamweb_fatawa.json", "r", encoding="utf-8") as f:
    data = json.load(f)

driver=launchBrowser(Debug=False)


question_item=".//div[@class='mainitem quest-fatwa']"
answer_item=".//div[@itemprop='acceptedAnswer']"

for topic in data:
    print(f"Topic: {topic}")
    print(f"URL: {data[topic]['url']}")
    print(f"Total Pages: {data[topic]['total_pages']}")
    print(f"Links: {len(data[topic]['links'])} links found")
    json_data=[]
    for link in tqdm(data[topic]['links']):
        driver.get(link)
        question= driver.find_element(value=question_item, by="xpath")
        question=question.find_element(value=".//div[@itemprop='text']", by="xpath")
        question_text = question.text.replace("السؤال","").strip()
        question_text = arabic_reshaper.reshape(question_text)
        #print(f"Question: {question_text}")
        answer= driver.find_element(value=answer_item, by="xpath")
        answer=answer.find_element(value=".//div[@itemprop='text']", by="xpath")
        answer_text = answer.text.replace("الإجابــة","").strip()
        answer_text = arabic_reshaper.reshape(answer_text)
        
        #print(f"Answer: {answer_text}")
        json_data.append({
            "سؤال": question_text,
            "إجابة": answer_text
        })
       
    print("\n")  # Add a newline for better readability
    with open(f"{topic}.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    print(f"Data for topic '{topic}' saved to {topic}.json")