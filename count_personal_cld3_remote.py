import re
import os
import json
import emoji
import string
import nltk
import time
#import langid
#from google.cloud import translate
from multiprocessing import Process
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from gensim.summarization import keywords
#import pycld2 as cld2
# import cld3
import remoteCld3

#nltk.download('stopwords')
#nltk.download('punkt')



'''
@lang id api
只做語系偵測
不做關鍵字
 
'''

def parallel_request(buckets, filename, outputfile):
    procs = []
    for i in range(len(buckets)):
        #print(buckets[i])
        p = Process(target = count_p, args=(buckets[i], filename, outputfile))
        procs.append(p)
        p.start()
    for p in procs:
        p.join()
    print ("Personal Done")

def count_p(bucket, filename, outfile):
    cld=remoteCld3.cld3()
    cld.establishConn("140.112.26.127",8886)
    load_f = open(filename, 'r', encoding="utf-8")
    lines = []
    for line in load_f.readlines():
        lines.append(line)
        
    page_name_lang_dict = {}
    
    for i in bucket:
        user = json.loads(lines[i])
        print(user['user_link'])
        #---------------
        #place

        place_type = []
        place_name = []
        for i in range(len(user['place_visited'])):
            if user['place_visited'] == "None":
                pass
            else:
                place_type.append(user['place_visited'][i]['place_type'])
                place_name.append(user['place_visited'][i]['place_name'])

        zip_place = zip(place_type, place_name)
        zip_place = list(zip_place)

        place_name_count = {}
        for item in zip_place:
            place_name_count[item] = zip_place.count(item)

        #分開紀錄place_name的類型與數量
        pname_count = list(place_name_count.values())
        pname_type = list(place_name_count.keys())

        place_name_tmp = []
        for i in range(len(pname_type)):
            d = {"place_name": pname_type[i][1], "place_type": pname_type[i][0], "place_name_count": pname_count[i]}
            place_name_tmp.append(d)


        #---------------
        #pages

        page_type = []
        page_name = []
        pname_lang = []
        for i in range(len(user['pages_liked'])):
            if user['pages_liked'] == "None":
                pass
            else:
                page_type.append(user['pages_liked'][i]['page_type'])
                page_name.append(user['pages_liked'][i]['page_name'])

                pname = user['pages_liked'][i]['page_name']
                # print("A - "+pname)
                pname = pname.replace("更多", "")
                pname = pname.replace("翻譯年糕", "")


                sub_pname = give_emoji_free_text(pname)
                if sub_pname not in page_name_lang_dict:       
                    try:
                        if sub_pname == "None"  or len(sub_pname)==0:
                            continue
                        else:
                            # print(sub_pname)
                            name_lang = cld.getLang(sub_pname)
                            name_lang=name_lang[name_lang.find("'")+1:name_lang.rfind("'")]
                            pname_lang.append(name_lang)
                            page_name_lang_dict[sub_pname] = name_lang
                    except Exception as e:
                        print(str(e))
                        continue
                else:
                    pname_lang.append(page_name_lang_dict[sub_pname])

        zip_page = zip(page_type, page_name)
        zip_page = list(zip_page)

        page_type_count = {}
        for item in page_type:
            page_type_count[item] = page_type.count(item)

        page_name_count = {}
        for item in zip_page:
            page_name_count[item] = zip_page.count(item)

        #分開紀錄page_name的類型與數量
        name_count = list(page_name_count.values())
        name_type = list(page_name_count.keys())


        page_name_tmp = []
        for i in range(len(name_type)):
            d = {"page_name": name_type[i][1], "page_type": name_type[i][0], "page_name_count": name_count[i]}
            page_name_tmp.append(d)


        #---------------
        #story lang

        if 'stories_by' in user:
            #紀錄stories_by的語系
            story_by_lang  = []
            for i in range(len(user['stories_by'])):
                if user['stories_by'] == "None":
                    pass
                else:
                    story = user['stories_by'][i]['story']
                    # print("B - "+story)
                    story = handle_story(story)
                    
                    sub_story = give_emoji_free_text(story)        
                    try:
                        if sub_story == "None" or len(sub_story)==0:
                            continue
                        else:
                            # print(sub_story)
                            story_lang = cld.getLang(sub_story)
                            story_lang=story_lang[story_lang.find("'")+1:story_lang.rfind("'")]
                            story_by_lang.append(story_lang)
                    except Exception as e:
                        print(str(e))
                        continue

        else:
            story_by_lang  = []

        if 'stories_liked' in user:
            story_like_lang = []
            for i in range(len(user['stories_liked'])):
                if user['stories_liked'] == "None":
                    pass
                else:
                    story = user['stories_liked'][i]['story']
                    #print("C - "+story)
                    story = handle_story(story)
 
                    sub_story = give_emoji_free_text(story)        
                    try:
                        if sub_story == "None" or len(sub_story)==0:
                            continue
                        else:
                            # print(sub_story)
                            story_lang = cld.getLang(sub_story)
                            story_lang=story_lang[story_lang.find("'")+1:story_lang.rfind("'")]
                            story_like_lang.append(story_lang)
                    except Exception as e:
                        print(str(e))
                        continue
        else:
            story_like_lang = []

        
        all_story_lang = story_by_lang + story_like_lang

        story_lang_count = {}
        for item in all_story_lang:
            story_lang_count[item] = all_story_lang.count(item)

        story_lang_count = sorted(story_lang_count.items(), key = lambda kv: kv[1], reverse = True)

        lang_tmp = []
        for i in range(len(story_lang_count)):
            d = {"stories_lang": story_lang_count[i][0], "percentage": round(story_lang_count[i][1]/len(all_story_lang), 2)}
            lang_tmp.append(d)

        #---------------
        #page_lang

        page_lang_count = {}
        for item in pname_lang:
            page_lang_count[item] = pname_lang.count(item)

        page_lang_count = sorted(page_lang_count.items(), key = lambda kv: kv[1], reverse = True)

        sum_lang = 0
        for i in range(len(page_lang_count)):
            sum_lang += page_lang_count[i][1]

        plang_tmp = []
        for i in range(len(page_lang_count)):
            d = {"pages_lang": page_lang_count[i][0], "percentage": round(page_lang_count[i][1]/sum_lang, 2)}
            plang_tmp.append(d)

        d = {"user_link":user["user_link"], "user_profile":user["user_profile"], "place":place_name_tmp, "pages":page_name_tmp, "story_language":lang_tmp, "pages_language":plang_tmp}

        d = json.dumps(d, ensure_ascii=False)


        with open(outfile, "a+", encoding="utf-8") as f:
            f.write(d)
            f.write('\n')
            print("Write Finish...")
        time.sleep(1)
    cld.closeConn()
    return outfile

def give_emoji_free_text(text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
    return clean_text

def handle_story(story):
    story = story.replace("更多", "")
    story = story.replace("翻譯年糕", "")
    story = story.replace("繼續閱讀", "")
    story = re.sub("(http|https)://[\w\-]+(\.[\w\-]+)+\S*", " ", story)

    table = str.maketrans({key: None for key in string.punctuation})
    story = story.translate(table) 

    emoji_list = re.findall(r'[^\w\s,]', story)
    emoji_list = [s.replace('！', '') for s in emoji_list]
    if '！' in emoji_list:
        emoji_list = [s.replace('！', '') for s in emoji_list]
    if '。' in emoji_list:
        emoji_list = [s.replace('。', '') for s in emoji_list]
    str_emoji = ''.join(emoji_list)

    for char in str_emoji:
        story = story.replace(char," ")
    
    return story

if __name__ == '__main__':

    # cld=remoteCld3.cld3()
    # cld.establishConn("140.112.26.127",8886)
    # a="https://twitter.com/imVkohli/status/720200559412842496?s=09"
    # a=handle_story(a)
    # a=give_emoji_free_text(a)
    # print(a)
    # res=cld.getLang(a)
    # print(res)
    # cld.closeConn()


    filename = './1649381645318723_output_file.txt'
    out_final = './personal_1649381645318723_cld3_remote.txt'
    
    # Multi-Processing

    NUM_WORKERS = 1

    load_f = open(filename, 'r', encoding="utf-8")

    lines = []
    for line in load_f.readlines():
        lines.append(line)
    buckets = [[] for i in range(NUM_WORKERS)]
    for i in range(len(lines)):
        remainder = int(i) % NUM_WORKERS
        buckets[remainder].append(i) 

    parallel_request(buckets, filename, out_final)
