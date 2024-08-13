import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider



endpoint = os.getenv("ENDPOINT_URL", "https://khtml.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt4o_kim")
search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://niauser001.search.windows.net")
search_key = os.getenv("SEARCH_KEY", SEARCH_KEY)
search_index = os.getenv("SEARCH_INDEX_NAME", "workmoneyindex")

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default")
      
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",
)
      
def chatbot_money_input_text(input_text):
  completion = client.chat.completions.create(
      model=deployment,
      messages= [
      {
        "role": "user",
        "content": f"{input_text}"
      }],
      max_tokens=800,
      temperature=0,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None,
      stream=False,
      extra_body={
        "data_sources": [{
            "type": "azure_search",
            "parameters": {
              "endpoint": f"{search_endpoint}",
              "index_name": "workmoneyindex",
              "semantic_configuration": "default",
              "query_type": "vector_simple_hybrid",
              "fields_mapping": {},
              "in_scope": True,
              "role_information": "너는 외국인의 신상 정보를 받고 지원금이 적혀있는 result.txt 파일에 있는 지원금들을 하나씩 확인하여 해당되는 지원금 모두를 외국인에게 알려주는 ai야. 반드시 33개 지원금 중 지원대상에 조금이라도 해당이 되면 모두 출력해줘. 출력 결과는 result.txt 파일에 있는 지원이나 혜택에 해당하는 이름만 작성해줘.  여러가지 지원이나 혜택에 해당될때는, 출력 순서가 제공유형의 현급지급, 현물지급, 감면, 대여, 프로그램/서비스(서비스), 그 외 등등 순서로 구성해줘. 순서 목차도 작성하지 말고 다른말 아무것도 하지말고 지원받을 수 있는 지원이름만 모두 작성해줘.",
              "filter": None,
              "strictness": 3,
              "top_n_documents": 5,
              "authentication": {
                "type": "api_key",
                "key": f"{search_key}"
              },
              "embedding_dependency": {
                "type": "deployment_name",
                "deployment_name": "user01ada002"
              }
            }
          }]
      }
  )
  jsonc = completion.to_json()
  return jsonc