
# coding: utf-8

# In[1]:

from bottlenose import api

from bs4 import BeautifulSoup

import urllib.request, urllib.error


import time


import random


from janome.tokenizer import Tokenizer

from requests_oauthlib import OAuth1Session

CK=os.environ["CONSUMER_KEY"]
CS=os.environ["CONSUMER_SECRET"]
AT=os.environ["ACCESS_TOKEN"]
AS=os.environ["ACCESS_TOKEN_SECRET"]
Amazon_access_key_Id=os.environ["AMAZON_ACCESS_KEY"]
Amazon_secret_key_Id=os.environ["AMAZON_SECRET_KEY"]
Amazon_assoc_tag=os.environ["AMAZON_ASSOC_TAG"]


#urllib2になってるからエラー吐くかもしれない
def error_handler(err):
    ex = err['exception']
    if isinstance(ex, urllib2.HTTPError) and ex.code == 503:
        time.sleep(1.5)
        return True
    else:
        return false

#クエリ＝売れ筋カテゴリ（kindle）
def item_search(item_page, amazon, search_index="Books", response_group="SalesRank,Small", browse_node="2275256051"):    
    response = amazon.ItemSearch(
        SearchIndex=search_index, 
        BrowseNode=browse_node, 
        ItemPage=item_page, 
        ResponseGroup=response_group
        )

    time.sleep(1.5)

    return response.findAll('item')

#結果からタイトルだけ取得、リストにいれてランダムで選ぶ
def do_it():
    
    amazon = api.Amazon(Amazon_access_key_Id, Amazon_secret_key, Amazon_assocc_tag, Region="JP",
        Parser=lambda text: BeautifulSoup(text,'lxml'), ErrorHandler=error_handler
    )

    item_list = ([item_search(1, amazon)])

# 出力する
    test = random.choice(item_list)
    
    #creating empty lists
    title_list=[]
    url_list = []
    
    #searching for tings
    for item in test:
        try: title_list.append(item.find('title').text)
        except : continue
        try: url_list.append(item.find('detailpageurl').text)
        except : continue
    
    #creating random number
    randnum = random.randint(1,9)
    
    #making a pair about random ting
    For_printing_title = title_list[randnum]
    For_printing_url = url_list[randnum]
    return For_printing_title, For_printing_url

#じゃのめ用前処理
def wakati(text):
    text = text.replace('\n','') 
    text = text.replace('\r','') 
    t = Tokenizer()
    result =t.tokenize(text, wakati=True)
    return result
 
#文章作成　test.txtは要改変
def generate_text(num_sentence=2):
    filename = "test.txt"
    src = open(filename, "r").read()
    wordlist = wakati(src)
  
    #マルコフ連鎖用のテーブルを作成
    markov = {}
    w1 = ""
    w2 = ""
    for word in wordlist:
        if w1 and w2:
            if (w1, w2) not in markov:
                markov[(w1, w2)] = []
            markov[(w1, w2)].append(word)
        w1, w2 = w2, word
  
    #文章の自動生成　句点の数は変えてもいいかもしれない
    count_kuten = 0 
    num_sentence= num_sentence
    sentence = ""
    title2 =""
    w1, w2  = random.choice(list(markov.keys()))
    while count_kuten < num_sentence:
        tmp = random.choice(markov[(w1, w2)])
        sentence += tmp
        if(tmp=='。'):
            count_kuten += 1
            sentence += '\n' #1文ごとに改行
        w1, w2 = w2, tmp
    title2, url2 = do_it()
    sentence_done = title2+url2+""+sentence
    
    print(sentence_done)
    
    return sentence_done

def tweeting():
# ツイート投稿用のURL
    url = "https://api.twitter.com/1.1/statuses/update.json"

# ツイート本文
    tweet = generate_text()
    params = {"status": tweet}

# OAuth認証で POST method で投稿
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(url, params = params)

# レスポンスを確認
    if req.status_code == 200:
        print ("OK")
    else:
        print ("Error: %d" % req.status_code)




if __name__ == '__main__':
    tweeting()


# In[ ]:



