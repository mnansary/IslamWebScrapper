import pandas as pd 
import os 
from core.core import launchBrowser,clickLink
from tqdm import tqdm
from time import sleep
import json 
import os
import arabic_reshaper
import json

save_dir="./data"
question_item=".//div[@class='mainitem quest-fatwa']"
answer_item=".//div[@itemprop='acceptedAnswer']"


df=pd.read_csv("data/all_fatwa.csv")
df["topic"]=df["path"].apply(lambda x: x.split("#")[0])


driver=launchBrowser(Debug=False)



for topic,_df in df.groupby("topic"): 
    json_data=[]
    os.makedirs(os.path.join(save_dir,topic),exist_ok=True)
    for subject,_sdf in _df.groupby("path"):
        if os.path.exists(os.path.join(save_dir,topic,f"{subject}.json")):
            continue
        print(f"Topic:{topic} Subject:{subject} fatwas:{len(_sdf)}")
        links=_sdf.fatwa.tolist()
        for link in tqdm(links):
            try:
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
            except Exception as e: 
                print()
                print(e)
                print(link)
                print()

        with open(os.path.join(save_dir,topic,f"{subject}.json") , "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
       

        
    