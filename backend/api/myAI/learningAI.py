import requests
from openai import AzureOpenAI
import json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from db_connect import db



class chatbot:
    def __init__(self, payload):
        self.api_key = API_KEY
        self.endpoint = ENDPOINT
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        self.payload = payload
    
    def payload_append(self, input_text, isImage):
        temp1 = self.payload
        temp2 = {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": input_text
                    }
                ]
        }
        if isImage:
            temp2 = {
                    "role": "user",
                    "content": [
                        {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{input_text}"
                        }
                        }
                    ]
                    }
        temp1["messages"].append(temp2)
        return temp1
    
    def question(self, input_text, isImage=False):
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=self.payload_append(input_text, isImage))
            response.raise_for_status()
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")
        response_json = response.json()

        return response_json['choices'][0]['message']['content']


chatbot_image_explain = chatbot(payload={
                                    "messages": [{
                                    "role": "system",
                                    "content": [
                                        {
                                        "type": "text",
                                        "text": "너는 외국인이 한국에 왔을 때, 잘 모르는 문서를 해석해주는 역할이야. 사진을 입력받으면, 사진에 있는 문서 내용을 외국인들이 알기 쉽게 설명해줘. 이때, 간단한 항목 설명이나 문서 설명과 함께, 설명하면서 각각의 작성 예시도 작성해주면 좋겠어. 전체 작성 예시는 작성하지 않아도 돼. 문서를 작성할 때 꼼꼼히 봐야할 점이나 주의사항을 설명해줘. 외국인에게 어려운 말을 쓰지 말아줘."
                                        }
                                    ]
                                    }],
                                    "temperature": 0.5,
                                    "top_p": 0.95,
                                    "max_tokens": 800
                                })

chatbot_warning_title = chatbot(payload={
                                    "messages": [{
                                    "role": "system",
                                    "content": [
                                        {
                                        "type": "text",
                                        "text": """너는 입력을 읽은 뒤, 한국으로 들어온 외국인 노동자들이 빠른 정착을 위해서 낯선 서류들과 법률들 그리고 문화 차이에 대해 제목으로 만드는 역할을 할거야. 제목은 최대한 간결하게 해주고 내용의 핵심 단어들을 위주로 만들어줘. 제목은 한국어로 작성해주고 한 문장으로 끝나게 해줘. 예시와 비슷하게 만들어줘.

                                                ---
                                                <예시>
                                                1. 근로계약서 이건 확인하셨나요?
                                                2. 한국에서의 첫걸음 이건 알아야해요
                                                3. 한국 최저시급에 대한 정보
                                                4. 한국에서 오해하기 쉬운 것들
                                                5. 용인에서 일자리 구하는 방법
                                                6. 한국은 '이런'사람들을 좋아한다
                                                7. 외국인 세금 관련 사항들
                                                ---"""
                                        }
                                    ]
                                    }],
                                    "temperature": 0.5,
                                    "top_p": 0.95,
                                    "max_tokens": 800
                                })


chatbot_warning_content = chatbot(payload={
                                    "messages": [{
                                    "role": "system",
                                    "content": [
                                        {
                                        "type": "text",
                                        "text": "너는 입력으로 제목을 입력받으면, 제목에 맞게 글을 작성하면 돼. 제목에 맞는 내용을 5~8줄정도로 작성해. 이때, 글은 구어체로 작성해줘. 한국으로 들어온 이민자들을 대상으로 하기 때문에 최대한 쉬운 단어로 해줘."
                                        }
                                    ]
                                    }],
                                    "temperature": 0.5,
                                    "top_p": 0.95,
                                    "max_tokens": 800
                                })

chatbot_govern = chatbot(payload={
                                    "messages": [{
                                    "role": "system",
                                    "content": [
                                        {
                                        "type": "text",
                                        "text": "행정 절차와 관련된 내용이야. 제목과 함께 결과를 외국인 노동자가 쉽게 볼 수 있도록 최대한 쉬운 단어로 해줘. 내용을 5~8줄정도로 작성해."
                                        }
                                    ]
                                    }],
                                    "temperature": 0.5,
                                    "top_p": 0.95,
                                    "max_tokens": 800
                                })


imagebot = AzureOpenAI(
    api_version="2024-05-01-preview",
    azure_endpoint="https://khtml.openai.azure.com/",
    api_key=API_KEY_IMAGE,
)


def chatbot_image_explain_question(input_text, isImage):
    return chatbot_image_explain.question(input_text, isImage)

def chatbot_warning_title_question(input_text):
    return chatbot_warning_title.question(input_text)

def chatbot_warning_content_question(input_text):
    return chatbot_warning_content.question(input_text)

def chatbot_payload_question(input_text):
    return chatbot_warning_content.question(input_text)

def chatbot_govern_question(input_text):
    return chatbot_govern.question(input_text)

def imagebot_question(input_text):
    result = imagebot.images.generate(
        model="dalle3", # the name of your DALL-E 3 deployment
        prompt=input_text,
        n=1
    )

    image_url = json.loads(result.model_dump_json())['data'][0]['url']

    return image_url



import threading

def warning_database():
    temp_title = chatbot_warning_title_question("주제 제목하나 정해줘.")
    temp_content = chatbot_warning_content_question(temp_title)
    image = imagebot_question(temp_title+temp_content)

    document = {
        'content':temp_content,
        'title': temp_title,
        'image':image
    }
    db['caution_db'].insert_one(document)
    print(temp_title)
    print(temp_content)
    print(image)

warning_database()