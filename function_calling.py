import requests, logging
from flask import Flask
import json, os


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

BOK_KEY = os.getenv("BANK_OF_KOREA")

class functionCalling :

    def currency_rate_get(self, **info) :
        curr_name = info["currency_name"]

        app.logger.info(curr_name)
        
        url = f"https://ecos.bok.or.kr/api/KeyStatisticList/{BOK_KEY}/json/kr/1/5"
        res = requests.get(url)

        data = res.json()
        items = data.get("KeyStatisticList", {}).get("row", [])
        
        """
        1. 위안, 달러, 엔 이면 
        2. CLASS_NAME"이 환율 이면서
        3. "KEYSTAT_NAME"에 들어온 값(위안, 달러, 엔)이 포함되어 있으면 
        4. DATA_VALUE"랑 "CYCLE 뽑기
        """
        
        for item in items:
            class_name = item.get("CLASS_NAME")
            keystat_name = item.get("KEYSTAT_NAME")

            if(class_name == "환율" and curr_name in keystat_name) :
                return item.get("DATA_VALUE"), item.get("CYCLE")
        
        return "환율 정보가 존재하지 않습니다.", "NULL"