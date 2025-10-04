from flask import Flask, request
from chatbot import chatbot
from characters import system_role, instruction
from function_calling import functionCalling
import logging, json

# Flask 앱 객체 생성
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

question_helper = chatbot(
    model = "gpt-5-nano",
    system_role = system_role,
    instruction = instruction
    
)

FC = functionCalling()
answer = ""

def format_response(resp):
    data = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": resp
                }
            }
        ]
    }
}
    return data


# 라우트(Route): URL 경로와 함수를 연결
@app.route("/chatbot_kakao", methods=["POST"])
def kakao_con():
    app.logger.info(request.json)  # 받은 요청 로그 찍기
    request_message = request.json['userRequest']['utterance'] # 받은 요청 request_message에 저장하기
    app.logger.info(request_message)
    # request_message user 메시지에 추가하기
    question_helper.add_user_response(request_message)
    # 메시지 보내기
    res = question_helper.send_request()

    data = res["output"][1]
    app.logger.info(data)

    respon_message = ""

    def_name = data["type"] # 타입으로 구별하기 message, function_call로 들어옴.
    app.logger.info(def_name)

    # function calling 필요없으면.
    if def_name == "message" :
        text = data["content"]
        statement = text[0]
        respon_message = statement["text"]
        app.logger.info(respon_message)
        question_helper.add_ai_response(respon_message)
    
    # function calling 필요있으면
    else :
        args = data["arguments"]
        info = json.loads(args)
        rate, date = FC.currency_rate_get(**info)
        app.logger.info(rate, date)

        if(date == "NULL"):
            respon_message = "환율 정보가 존재하지 않습니다. (시스템 오류) : 다시 질문해주세요."
    
        else :
            app.logger.info("펑션 들어옴")
            question = "{} 날의 현재 환율은 {} 라는 정보를 줄게 답장 줘.".format(date, rate)
            app.logger.info(question)
            question_helper.add_user_response(question)
            answer = question_helper.send_request()
            app.logger.info(type(answer))
            h = answer["output"][1]
            app.logger.info(h)
            b = h["content"]
            app.logger.info(b[0])
            j = b[0]
            k = j["text"]
            app.logger.info(k)
            question_helper.add_ai_response(k)
            respon_message = k

            # 나중에 data만 빼내는 거 함수로 만들기
      

    return format_response(respon_message) # 카카오 포맷에 맞춰 응답 보내기


@app.route("/")
def hello():
    return "Hello"

# 서버 실행
if __name__ == "__main__":
    app.run(debug=False)

