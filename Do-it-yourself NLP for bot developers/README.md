### Do-it-yourself NLP for bot developers
[원본](https://medium.com/rasa-blog/do-it-yourself-nlp-for-bot-developers-2e2da2817f3d)


### word embeddings: GloVe/word2vec

* 단어 임베딩(Word Embedding)이란 텍스트를 구성하는 하나의 단어를 수치화하는 방법의 일종

* one-hot encoding
<pre>
#
일반적인 자연어 처리에서 단어를 의미나 발음을 무시하고 각각을 개별적인 기호로 취급
단어를 벡터로 나타낼 때는 총 단어 수만큼의 길이의 벡터에서 다른 모든 값은 0으로 하고 단어 번호에 해당하는 원소만 1로 표시
예를 들어 '학교', '컴퓨터', '집' 3단어만 있고 순서대로 1번, 2번, 3번이라면 학교(1,0,0), 컴퓨터(0,1,0), 집(0,0,1) 표현
단어의 의미를 전혀 고려하지 않음

#
문서를 나타내는 벡터는 그 문서를 이루는 단어 벡터들을 모두 더한 것과 같다.
</pre>

* 단어 임베딩
<pre>
단어의 의미를 고려
one-hot encoding 보다 조밀한 벡터로 단어를 표현
대량의 데이터로 단어 임베딩을 미리 학습시켜 두면, 
문서 분류와 같은 과제에서 더 적은 데이터로도 학습된 임베딩을 사용하여 높은 성능을 낼 수 있음

단어 임베딩의 종류에는 LSA, Word2Vec, GloVe, FastText 등이 있음.
</pre>


* Word2Vec

![](https://raw.githubusercontent.com/rohan-varma/paper-analysis/master/word2vec-papers/models.png)

<pre>
Word2Vec에는 CBOW(continuous bag-of-words)와 Skip-Gram 두 가지 방식이 있음

예를 들어 "나는 매일 파이썬을 공부한다"라는 문장에서 '파이썬'를 대상 단어로 하자. 
여기에 윈도(window)를 좌우 2단어라고 하면 주변 단어는 "는", "매일", "을", "공부"가 될 것이다. 
CBOW는 주변단어의 임베딩을 더해서 대상단어를 예측하고, Skip-Gram은 대상 단어의 임베딩으로 주변단어를 예측한다.

CBOW(특정 단어를 예측), Skip-Gram(특정 단어 주변의 단어를 예측)
</pre>





