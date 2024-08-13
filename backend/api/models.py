from django.db import models
from db_connect import db

# Create your models here.
govern_db = db['govern']  # 행정절차
info_db = db['info'] # 문서 분석 정보
caution_db = db['caution_db'] # 주의 사항