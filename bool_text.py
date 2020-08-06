import re
# 데이터 전처리
def preprocessing(text):
    # 개행문자 제거
    text = re.sub('\\\\n', ' ', text)
    # 특수문자,자음 제거
    text = re.sub('[.,;:\)*?!~`’^\-_+<>@\#$%&=#}※ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㅠㅜ]', '', text)
    # 중복 생성 공백값
    text = re.sub(' +', ' ', text)
    return text
# 불용어 제거
def remove_stopwords(text):
    tokens = text.split(' ')
    stops = ['수', '현', '있는', '있습니다', '그', '년도', '합니다', '하는', '쟂','띨','사진','삭제된 메시지입니다','샵검색',
             '및', '제', '할', '하고', '더', '한', '그리고', '월', 'ㅎㅎㅎ','ㅎㅎ','ㅋㅋ','근데','진짜','너무','아니','다시',
             '내가','김준',
             '저는', '없는', '입니다', '등', '일', '많은', '이런', '것은', 'ㅋ','ㅎㅎ','ㅎ','ㅋㅋㅋ','ㅋㅋ','ㅠㅠㅠㅠ','ㅠㅠ']
    meaningful_words = [w for w in tokens if not w in stops]
    return ' '.join(meaningful_words)

def delete_emoji(text):
    only_BMP_pattern = re.compile("["
                                  u"\U00010000-\U0010FFFF"
                                  "]+", flags=re.UNICODE)
    only_text = only_BMP_pattern.sub(r'', text)
    return only_text
