import sqlite3
from pathlib import Path


dir_path = Path(__file__).parent
db_path = dir_path.parent/'LocalSetu.db'
column_list = ['id','url','anti_url','user','date','tag','r18','man','pixiv_id','pixiv_tag','pixiv_tag_t','pixiv_name','pixiv_url','verify','tencent_url']

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute(
    '''create table if not exists LocalSetu(
        id integer primary key not null,
        url TEXT(255) not null,
        anti_url TEXT(255) default '',
        user integer(11) default null,
        date text default null,
        tag TEXT(255) default null,
        r18 integer default 0,
        man integer default 0,
        pixiv_id integer(255) default 0,
        pixiv_tag text(255) default '',
        pixiv_tag_t text(255) default '',
        pixiv_name TEXT(255) default '',
        pixiv_url TEXT(255) default '',
        verify integer default 0,
        tencent_url TEXT(255))''')
conn.commit()

def test_conn():
    try:
        conn.ping()
    except:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
def update_db():
    test_conn()
    cursor.execute('''select count(*) from pragma_table_info('LocalSetu')''')
    column_num = cursor.fetchone()[0]
    msg = ''
    for each in column_list[1:column_num]:
        msg += f"{each},"
    msg = msg.strip(',')
    sql = f"""
    DROP table if exists TempOldTable;
    ALTER TABLE LocalSetu RENAME TO TempOldTable;
    create table if not exists LocalSetu(
        id integer primary key not null,
        url TEXT(255) not null,
        anti_url TEXT(255) default '',
        user integer(11) default null,
        date text default null,
        tag TEXT(255) default null,
        r18 integer default 0,
        man integer default 0,
        pixiv_id integer(255) default 0,
        pixiv_tag text(255) default '',
        pixiv_tag_t text(255) default '',
        pixiv_name TEXT(255) default '',
        pixiv_url TEXT(255) default '',
        verify integer default 0,
        tencent_url TEXT(255));
    INSERT INTO LocalSetu ({msg}) SELECT {msg} FROM TempOldTable;
    DROP TABLE TempOldTable;
    """
    cursor.executescript(sql)
    conn.commit()
        

class getImgDao:
    def __init__(self):
        test_conn()
        
    def get_local_image_random(self, is_man):
        """????????????
        id,url,anti_url,user,date,tag,pixiv_tag_t,pixiv_id,pixiv_url,verify
        """
        sql="SELECT id,url,anti_url,user,date,tag,pixiv_tag_t,pixiv_id,pixiv_url,verify FROM LocalSetu where man = ? AND verify = 0 ORDER BY random() limit 1"
        cursor.execute(sql,(is_man,))
        conn.commit()
        return cursor.fetchone()
    
    def get_local_image_user(self, is_man,user):  
        """????????????????????????
        id,url,anti_url,user,date,tag,pixiv_tag_t,pixiv_id,pixiv_url,verify
        """
        sql="SELECT id,url,anti_url,user,date,tag,pixiv_tag_t,pixiv_id,pixiv_url,verify from LocalSetu where man = ? AND user = ? AND verify = 0 ORDER BY random() limit 1"
        cursor.execute(sql,(is_man,str(user)))
        conn.commit()
        return cursor.fetchone()
    
    def get_local_image_ID(self, is_man,id):
        """??????ID????????????
        id,url,anti_url,user,date,tag,pixiv_tag_t,pixiv_id,pixiv_url,verify
        """
        test_conn()
        sql="SELECT id,url,anti_url,user,date,tag,pixiv_tag_t,pixiv_id,pixiv_url,verify FROM LocalSetu where man = ? AND id = ? ORDER BY random() limit 1"
        cursor.execute(sql,(is_man,id))
        conn.commit()
        return cursor.fetchone()
    
    def get_local_image_tag(self, is_man,tag):
        """??????TAG????????????
        id,url,anti_url,user,date,tag,pixiv_tag_t,pixiv_id,pixiv_url,verify
        """
        test_conn()
        sql="SELECT id,url,anti_url,user,date,tag,pixiv_tag_t,pixiv_id,pixiv_url,verify FROM LocalSetu where man = ? AND (tag like ? OR pixiv_tag like ? OR pixiv_tag_t like ?) AND verify = 0 ORDER BY random() limit 1"
        cursor.execute(sql,(is_man,tag,tag,tag))
        conn.commit()
        return cursor.fetchone()
    
    def get_original_image(self, id):
        """????????????????????????
        pixiv_url,verify,pixiv_name,pixiv_id,url
        """
        test_conn()
        sql="SELECT pixiv_url,verify,pixiv_name,pixiv_id,url FROM LocalSetu where id = ?"
        cursor.execute(sql,(id,))
        conn.commit()
        return cursor.fetchone()
    
    def update_original_image(self,pixiv_id,pixiv_tag,pixiv_tag_t,r18,pixiv_img_url,pixiv_name,id):
        """??????????????????"""
        test_conn()
        sql = "update LocalSetu set pixiv_id = ?,pixiv_tag = ?,pixiv_tag_t = ?,r18 = ?,pixiv_url = ?,pixiv_name = ? where id = ?"
        cursor.execute(sql,(pixiv_id,pixiv_tag,pixiv_tag_t,r18,pixiv_img_url,pixiv_name,id))
        conn.commit()
        
class loadImgDao:
    def __init__(self):
        test_conn()
        
    def load_image(self,url,user,tag,is_man,tencent_url):
        """???????????????????????????"""
        test_conn()
        sql="INSERT OR IGNORE INTO LocalSetu (id,url,user,date,tag,man,tencent_url) VALUES (NULL,?,?,datetime('now','localtime'),?,?,?)"
        cursor.execute(sql,(url,user,tag,is_man,tencent_url))
        id=cursor.lastrowid
        conn.commit()
        return id
    
    #???????????????????????????????????????????????????
    def load_file(self,url,user,tag,is_man):
        """???????????????????????????"""
        sql="INSERT OR IGNORE INTO LocalSetu (id,url,user,date,tag,man) VALUES (NULL,?,?,datetime('now'),?,?)"
        cursor.execute(sql,(url,user,tag,is_man))
        id=cursor.lastrowid
        conn.commit()
        return
    
    def check_url(self,url):
        """??????url????????????"""
        sql="SELECT id FROM LocalSetu where url = ?"
        cursor.execute(sql,(url,))
        conn.commit()
        return cursor.fetchone()
     
        
class deleteDao:
    def __init__(self):
        test_conn()
        
    def get_info(self,id):
        """?????????????????????url"""
        test_conn()
        sql="select url,user from LocalSetu where id = ?"
        cursor.execute(sql,(id,))
        conn.commit()
        return cursor.fetchall()
    
    def apply_for_delete(self,id):
        """??????????????????"""
        test_conn()
        sql="update LocalSetu set verify = 2 where id = ?"
        cursor.execute(sql,(id,))
        conn.commit()
        
    def delete_image(self,id):
        """????????????"""
        test_conn()
        sql="delete from LocalSetu where id = ?"
        cursor.execute(sql,(id,))
        conn.commit()
            
        
class verifyDao:
    def __init__(self):
        test_conn()
        
    def update_verify_stats(self,id:int, data:int):
        """
        ??????????????????
        id: ??????ID
        data: 0:??????, 1:?????????
        """
        try:
            test_conn()
            sql = f"update LocalSetu set verify = {data} where id = ?"
            cursor.execute(sql,(id,))
            conn.commit()
            return data
        except:
            return 1

    def update_verify_info(self,id:int, pixiv_id ,pixiv_tag ,pixiv_tag_t ,r18 ,pixiv_url ):
        """
        ??????????????????
        id: ??????ID
        pixiv_id: P?????????ID
        pixiv_tag?????????TAG
        pixiv_tag_t: ??????TAG
        r18??? ??????R18
        pixiv_url??? P???????????????
        """
        try:
            test_conn()
            sql = "update LocalSetu set pixiv_id = ?,pixiv_tag = ?,pixiv_tag_t = ?,r18 = ?,pixiv_url = ? where id = ?"
            cursor.execute(sql,(pixiv_id,pixiv_tag,pixiv_tag_t,r18,pixiv_url,id))
            conn.commit()
            return 0
        except:
            return 1
        
    def get_verify_info(self,verify):
        """????????????????????????
        url,user,date,id,man
        """
        test_conn()
        sql="select url,user,date,id,man from LocalSetu where verify = ? ORDER BY random() limit 1"
        cursor.execute(sql,(verify,))
        return cursor.fetchone()
    
    def get_verify_list(self,id):
        """?????????ID??????????????????????????????"""
        test_conn()
        sql="SELECT id,url FROM LocalSetu where (pixiv_id = 0 or verify = 1) and id >= ?"
        cursor.execute(sql,(id,))
        return cursor.fetchall()
        

class normalDao:
    def __init__(self):
        test_conn()
        
    def get_all_info(self,id):
        """??????????????????"""
        test_conn()
        sql="SELECT * FROM LocalSetu where id = ?"
        cursor.execute(sql,(id,))
        return cursor.fetchone()
    
    def get_tecent_url_list(self):
        """??????????????????URL???????????????"""
        test_conn()
        sql="SELECT id FROM LocalSetu where tencent_url is not NULL"
        cursor.execute(sql)
        return cursor.fetchall()
        
    def get_tecent_url(self,id):
        """????????????url????????????"""
        test_conn()
        sql="SELECT url,tencent_url FROM LocalSetu where id = ?"
        cursor.execute(sql,(id,))
        return cursor.fetchone()
    
    def update_tag(self,tag,id):
        """??????TAG"""
        test_conn()
        sql="update LocalSetu set tag = ? where id = ?"
        cursor.execute(sql,(tag,id))
        conn.commit()
        
    def get_anti_url(self,id):
        """?????????????????????"""
        test_conn()
        sql="SELECT url,anti_url FROM LocalSetu where id =? ORDER BY random() limit 1"
        cursor.execute(sql,(id,))
        conn.commit()
        return cursor.fetchall()
    
    def update_anti_url(self,anti_url,id):
        """???????????????url"""
        test_conn()
        sql="update LocalSetu set anti_url = ? where id = ?"#????????????????????????
        cursor.execute(sql,(anti_url,id))
        conn.commit()
        
    def get_image_count(self):
        """??????????????????"""
        test_conn()
        sql = "select count(*) as sumnumber from LocalSetu"
        cursor.execute(sql)
        conn.commit()
        return cursor.fetchone()
        
    def get_image_upload_rank(self):
        """??????????????????"""
        test_conn()
        sql = "select user,count(user) as number from LocalSetu GROUP BY user ORDER BY number desc limit 10"
        cursor.execute(sql)
        conn.commit()
        return cursor.fetchall()