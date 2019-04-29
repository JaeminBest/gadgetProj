from sqlalchemy.sql import text
from models import *
from pattern_extractor import *
from app import db_session, engine

def init_db():
    Base.metadata.create_all(bind=engine)

def remove_all():
    init_db()
    sql1 = """DROP TABLE marks"""
    engine.execute(text(sql1))
    sql2 = """DROP TABLE originals"""
    engine.execute(text(sql2))
    sql3 = """DROP TABLE users"""
    engine.execute(text(sql3))

# n corresponding to table number
# n=1 user, n=2 edit, n=3 original, n=4 select
# n=0 all

root = '/home/di_lab/skt_data/'
img_db = './patterns_db/'
mark_root = '/home/jaemin/mark_image/defects/'

# NEED to be changed depend on each local's setting!
random_img_dir = img_db+'random_images/'
marked_img_dir = img_db+'marked_images/'
pattern_dir = img_db+'patterns/'

# for each part update original table
def update_p(num_p,cnt):
    n = 0
    ok_list = []
    de_list = []

    parts = 'L'+str(num_p)
    ok_dir = root+'ok/20171127_20171220_ok_CAM1_'+parts+'_polaroid/'
    de_dir = root+'defects/20171127_20171220_defect_CAM1_'+parts+'_polaroid/'
    marked_dir = mark_root+parts+'/'

    for i in range(8):
        a, b = set_list(i+1)
        ok_list = ok_list + a
        de_list = de_list + b

    for i, f in enumerate(de_list):
        img_dir = de_dir+f
        if isfile(img_dir):
            continue
        for j, img_name in enumerate(os.listdir(img_dir)):
            tmp = img_name.split('.')
            if tmp[-1] =='csv':
                break
            if tmp[-1]=='png' and tmp[0].split('_')[-1] != 'CAM1':
                part_num = tmp[0].split('_')[2]
                image_id = f
                path = img_dir+'/'+img_name
                #print("Original row setting")
                tmp = Original(image_code=image_id, part_num=part_num, label_num=parts)
                print(f"'{path}'")
                #print("Original photo blob setting")
                tmp.set_photo(path)
                db_session.add(tmp)
                db_session.commit()
        cnt = cnt+1
        print(f"'{cnt}'th parts insert done")


# updating gadget_db.Original tables into existing original image
def update():
    cnt=0
    for i in range(6):
        print(f"========== L'{i}' directory update start ==========")
        update_p(i,cnt)
        print(f"========== L'{i}' directory update done ==========")
