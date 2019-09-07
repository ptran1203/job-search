from nltk.corpus import stopwords
from unidecode import unidecode

vietnamese_raw_stopwords = "có,sử,dụng,racác,những,và,xin,giới,thiệu,chào,ưu,nhược,ơi,ấy,tạm,biệt,nhiều,lại,ngoài"

vietnamese_stopwords = unidecode(vietnamese_raw_stopwords).split(',')

STOPWORDS = set(stopwords.words('english') + vietnamese_stopwords)