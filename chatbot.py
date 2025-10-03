from common import client

class chatbot :

    def  __init__(self, model, system_role, instruction):
        self.context = [{"role" : "system", "content" : system_role}]
        self.model = model
        self.instruction = instruction
        self.max_token_size = 16 * 1024
        self.available_token = 0.9


    def add_user_response(self, user_msg):
        self.context.append({"role" : "user", "content" : user_msg})

    def add_ai_response(self, ai_msg):
        self.context.append({"role" : "assistant", "content" : ai_msg})

    def send_request(self):
        try :
            self.context[-1]['content'] += self.instruction
            response = client.responses.create(
                model=self.model, 
                input=self.context,
                tools=tools,
                
            ).model_dump()
        except Exception as e:
            print(f"Exception 오류({type(e)}) 발생:{e}")

        return response
    
tools = [{
    "type": "function",
    "name": "currency_rate_get",
    "description": "지정된 통화의 원(KRW) 기준의 환율 확인.",
    "parameters": {
        "type": "object",
        "properties": {
            "currency_name": {
                "type": "string",
                "description": "예시로 든 통화에서 한글로 답할것, 응답은 한개만 e.g. 달러, 유로, 엔, 위안"
            },
        },
        "required": ["currency_name"],
        "additionalProperties": False
    },
    "strict": True
}]