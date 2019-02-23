### 마르코프 체인을 이용하여 문장생성
마르코프 체인을 이용을 이용하면 확률기반으로 문장을 생성
[마르코프 체인을 이용하여 문장생성](http://blog.naver.com/PostView.nhn?blogId=pjt3591oo&logNo=221101060940&parentCategoryNo=&categoryNo=106&viewDate=&isShowPopularPosts=false&from=postView)


### 문장 생성 과정
<pre>
1. 문장을 형태소로 분할
2. 단어의 전후를 딕셔너리 등록
3. 딕셔너리를 이용하여 임의의 문장생성
1, 2번은 학습단계, 3번은 실제 문장을 만드는 것으로 이해하면 됩니다.
</pre>

### ● 1 단계 : 문장을 형태소로 분할
<pre>
# pip install konlpy
# https://aka.ms/vs/15/release/vs_buildtools.exe
# https://www.scivision.co/python-windows-visual-c++-14-required/
# https://download.oracle.com/otn-pub/java/jdk/8u201-b09/42970487e3af4f5aa5bca3f542482c60/jdk-8u201-windows-x64.exe

from konlpy.tag import Twitter

sentence = """안녕하세요. 저는 멍개라고 합니다. 오늘 날씨가 정말로 좋은것 같아요."""

twitter = Twitter()
malist = twitter.pos(sentence, norm=True)
words = []
words = []

for word in malist:
    if not word[1] in ["Punctuation"]:
        words.append(word[0])
    if word[0] == '.':
        words.append(word[0])

print(words)

# 결과
# ['안녕하세', '요', '.', '저', '는', '멍', '개', '라고', '합', '니다', '.', '오늘', '날씨', '가', '정말로', '좋', '은', '것', '같아', '요', '.']
# 여기서 중요한 점은 하나의 문장을 꼭 마침표(.)를 찍어서 끝을내야 합니다.

</pre>

### ● 2단계 : 단어의 전후 딕셔너리 등록
<pre>
# 마르코프 체인 딕셔너리 만들기
def make_dic(words):
    tmp = ["@"]
    dic = {}

    for word in words:
        tmp.append(word)

        if len(tmp) < 3: continue
        if len(tmp) > 3: tmp = tmp[1:]

        set_word3(dic, tmp)

        if word == ".":
            tmp = ["@"]
            continue

    return dic

# 딕셔너리에 데이터 등록하기
def set_word3(dic, s3):
    w1, w2, w3 = s3

    if not w1 in dic: dic[w1] = {}
    if not w2 in dic[w1]: dic[w1][w2] = {}
    if not w3 in dic[w1][w2]: dic[w1][w2][w3] = 0

    dic[w1][w2][w3] += 1

print(make_dic(1단계에서 생성된 형태소 분할))
</pre>

### ● 3단계 : 문장 만들기
<pre>
# 문장 만들기
def make_sentence(dic):
    ret = []
    if not '@' in dic: return "no dic"
    top = dic['@']

    w1 = word_choice(top)
    w2 = word_choice(top[w1])

    ret.append(w1)
    ret.append(w2)

    while True:
        w3 = word_choice(dic[w1][w2])
        ret.append(w3)
        if w3 == ".": break
        w1, w2 = w2, w3

    ret = "".join(ret)
    
    return ret


def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))

new_sentence = make_sentence(dic)
print(new_sentence)
</pre>

### ● 챗봇 응답기
<pre>
import urllib.request
from konlpy.tag import Twitter
import os, re, json, random

dict_file = "chatbot-data.json"
dic = {}
twitter = Twitter()

# 업데이트
def register_dic(words):
    global dic
    if len(words) == 0: return
    tmp = ["@"]
    for i in words:
        word = i[0]
        if word == "" or word == "\r\n" or word == "\n": continue
        tmp.append(word)
        if len(tmp) < 3: continue
        if len(tmp) > 3: tmp = tmp[1:]
        set_word3(dic, tmp)
        if word == "." or word == "?":
            tmp = ["@"]
            continue
    # 딕셔너리가 변경될 때마다 저장하기
    json.dump(dic, open(dict_file,"w", encoding="utf-8"))

def make_sentence(head):
    if not head in dic: return ""
    ret = []

    if head != "@": ret.append(head)        
    top = dic[head]

    w1 = word_choice(top)
    w2 = word_choice(top[w1])

    ret.append(w1)
    ret.append(w2)

    while True:
        if w1 in dic and w2 in dic[w1]:
            w3 = word_choice(dic[w1][w2])
        else:
            w3 = ""
        ret.append(w3)
        if w3 == "." or w3 == "？ " or w3 == "": break
        w1, w2 = w2, w3
    ret = "".join(ret)
  
    return ret

def make_reply(text):
    # 단어 학습 시키기
    if not text[-1] in [".", "?"]: text += "."
    words = twitter.pos(text)
    register_dic(words)
    # 사전에 단어가 있다면 그것을 기반으로 문장 만들기
    for word in words:
        face = word[0]
        if face in dic: return make_sentence(face)
        
    return make_sentence("@")

if os.path.exists(dict_file):
    dic = json.load(open(dict_file, "r"))

if __name__ == "__main__":
    message = "치킨이 먹고싶다"
    new_message = make_reply(message)
    print("%s : %s" %(message, new_message))
</pre>
