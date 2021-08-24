from typing import AsyncIterable
from pixivpy3 import *
from pixivpy_async import *
from PicImageSearch import SauceNAO
import os
import json
import time
import requests
import pymysql
import time
import aiohttp
from loguru import logger
from PicImageSearch import AsyncSauceNAO, NetWork
import asyncio

with open('C:/Users/Administrator/Desktop/hoshino_xcw/XCW/HoShino/hoshino/modules/setu/config.json') as json_data_file:
    config = json.load(json_data_file)

host = config['mysql']['host']
user=config['mysql']['user']
password=config['mysql']['password']
database=config['mysql']['database']
api_key=config['api']['sauceNAO']
refresh_token=config['api']['refresh_token']

aapi = AppPixivAPI()
aapi.login(refresh_token=refresh_token)
t = time.time()

setu_folder = "C:/Users/Administrator/Desktop/hoshino_xcw/XCW/res/img/setu"
conn = pymysql.connect(host=host,user=user,password=password,database=database)
cursor = conn.cursor()
async def get_pixiv_id(url):
    pixiv_id = 0
    async with NetWork(proxy='http://127.0.0.1:7890') as client:
        saucenao = AsyncSauceNAO(client=client,db = 5,api_key=api_key)
        res = await saucenao.search(url)
        pixiv_id = res.raw[0].pixiv_id
        print("已获取到pixiv_id"+str(pixiv_id))
        #await asyncio.sleep(1)
        pixiv_tag,pixiv_tag_t,r18=await get_pixiv_tag(pixiv_id)
        print("已获取到pixiv_tag"+pixiv_tag_t)
        if res.raw[0].similarity < 60 or pixiv_id == '' or not pixiv_id:
            print(res.raw[0].similarity)
            pixiv_id = 0
        return pixiv_id


async def get_pixiv_tag(pixiv_id):
    from pixivpy_async import PixivClient
    from pixivpy_async import AppPixivAPI as apapi
    from pixivpy_async import PixivAPI as ppapi
    try:
        async with PixivClient(proxy="http://127.0.0.1:7890") as client:
            aapid = AppPixivAPI(client=client,proxy="http://127.0.0.1:7890")
            #aapid.set_accept_language('zh-cn')
            await aapid.login(refresh_token=refresh_token)
# get origin url
            json_result = await aapid.illust_detail(pixiv_id)
            illust = json_result.illust.tags
            r18 = 0
            pixiv_tag = ''
            pixiv_tag_t = ''
            if illust[0]['name'] == 'R-18':
                r18 = 1
            for i in illust:
                pixiv_tag = pixiv_tag.strip()+ " "+ str(i['name']).strip('R-18').replace("'","\\'")
                pixiv_tag_t = pixiv_tag_t.strip() + " "+ str(i['translated_name']).strip('None').replace("'","\\'") #拼接字符串 处理带引号sql
            pixiv_tag = pixiv_tag.strip()
            pixiv_tag_t = pixiv_tag_t.strip()
            return pixiv_tag,pixiv_tag_t,r18
    except Exception as e:
        print("yichang1",e)
        return '','',0

async def main():
    #sql="SELECT id,url FROM bot.localsetu where pixiv_id is NULL limit 10"
    sql="SELECT id,url FROM bot.localsetu where id = 759 or id =760 or id=761 ORDER BY id limit 1000"
    cursor.execute(sql)
    results = cursor.fetchall()
    url=''
    id = 0
    tasks1=[]
    tasks2=[]
    start = time.time()
    for row in results:
        id = row[0] #参数初始化
        #url= setu_folder+'/'+row[1]
        url = "https://pixiv.cat/77702503-1.jpg"
        pixiv_tag=''
        pixiv_tag_t=''
        r18=0
        pixiv_id = tasks1.append(get_pixiv_id(url))
        print(id)#这里对应之后的sql
    await asyncio.gather(*tasks1)
    print("usetime:%f s"%(time.time()-start))
    
    
'''            print(pixiv_id)
            try:
                pixiv_tag,pixiv_tag_t,r18=get_pixiv_tag(pixiv_id)
            except Exception as e:
                print("yichang2",e)
                continue
            pixiv_tag_t = pixiv_tag_t.strip('None')
            print(pixiv_tag)
            print(pixiv_tag_t)
        except Exception as e:
            print("yichang3",e)
            continue
        sql="update localsetu set pixiv_id = %s , pixiv_tag = \'%s\' , pixiv_tag_t = \'%s\' , r18 = %s where id = %s"%(pixiv_id,pixiv_tag,pixiv_tag_t,r18,id)
        cursor.execute(sql)
        conn.commit()'''

if __name__ == "__main__":
    asyncio.run(main())
