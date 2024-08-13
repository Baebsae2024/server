from django.shortcuts import render
from .myAI import learningAI
from .myAI import learningAIcopy
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from db_connect import db
from .models import *
from bson.json_util import dumps
import gridfs
import json
import base64
import pymongo
from PIL import Image
import os
from io import BytesIO

# Create your views here.
def main(request):
    return HttpResponse("<h1>Hello~</h1>")

class GovernAPI(APIView):
    def get(self, request):
        title = request.GET.get('title')
        if not title:
            return JsonResponse({'error': 'Title parameter is required.'}, status=400)

        try:
            # MongoDB에서 데이터 찾기
            data = govern_db.find({'title': title})
            data_list = []
        
            for item in data:
                
                data_list.append(item)
        
            json_data = dumps(data_list)
            result = json.loads(json_data)
            return JsonResponse(result, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class ImageAPI(APIView):
    def post(self, request):
        if 'file' in request.FILES:
            file = request.FILES['file']
            # GridFS 인스턴스 가져오기
            fs = gridfs.GridFS(db)
            # GridFS에 파일 저장
            file_id = fs.put(file.read(), filename=file.name)
            file_data = fs.get(file_id).read()

            # 파일 데이터를 이미지로 변환
            image = Image.open(BytesIO(file_data))

            # 이미지를 바이트 객체로 변환
            buffered = BytesIO()
            image.save(buffered, format=image.format)
            img_str = base64.b64encode(buffered.getvalue()).decode('ascii')

            info = learningAI.chatbot_image_explain_question(img_str, isImage=True)
            dict_info = {'content':info}
            info_db.insert_one(dict_info)

            return JsonResponse(dict_info, safe=False, status=200)
        else:
            return JsonResponse({'error': 'No file provided.'}, status=400)



        
class CautionAPI(APIView):
    def get(self, request):
        cursor = caution_db.find()
    
        #커서를 리스트로 변환
        documents = list(cursor)
    
        # MongoDB 문서의 ObjectId는 JSON으로 직렬화되지 않으므로 문자열로 변환
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        return JsonResponse(documents, safe=False, status=200)
    
    # def info(request):
    #     title = request.GET.get('title')
    #     if not title:
    #         return JsonResponse({'error': 'Name parameter is required.'}, status=400)

    #     try:
    #         # MongoDB에서 데이터 찾기
    #         data = db['caution_db'].find({'title': title})
    #         data_list = []
        
    #         for item in data:
                
    #             data_list.append(item)
        
    #         json_data = dumps(data_list)
    #         result = json.loads(json_data)
    #         return JsonResponse(result, safe=False, status=200)
    #     except Exception as e:
    #         return JsonResponse({'error': str(e)}, status=500)

        
class CompanyAPI(APIView):
    def get(self, request):
        data = learningAIcopy.chatbot_money_input_text(request)
        # Return all data if no name parameter is provided
        return JsonResponse({'data': data}, status=200)