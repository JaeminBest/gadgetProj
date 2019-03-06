import numpy as np
import csv
import random
import shutil
import os
from os.path import isfile, join

root = '/home/di_lab/skt_data/'
datalist_dir = '/home/di_lab/skt_data/data_list/'

def parse_f(name):
    return str(name).split(' ')[1].split('_')[1]

def train_num(data_dir, data_list):
    f_idx = []
    for i, f in enumerate(data_list):
        img_dir = data_dir + f
        if isfile(img_dir):
            f_idx.append(i)
    return len(data_list) - len(f_idx)

def set_list (num):
    list_dir = datalist_dir
    with open(list_dir+str(num)+'.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(csv_reader):
            if len(row) != 0:
                if row[0] == 'ok':
                    ok_list = row[1:]
                elif row[0] == 'defects':
                    de_list = row[1:]
    return ok_list, de_list

def set_type (num_p, num_t):
    parts = 'L'+str(num_p)
    f = root+'defects/20171127_20171220_defect_CAM1_'+parts+'_polaroid.txt'

    def_list = []
    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(csv_reader):
            def_list.append(row[0].split(' '))
        def_list = np.array(def_list).T

    return def_list[0][def_list[1] == 'defect0'+str(num_t)]

root = '/home/di_lab/skt_data/'
img_db = './patterns_db/'

# NEED to be changed depend on each local's setting!
random_img_dir = img_db+'random_images/'
marked_img_dir = img_db+'marked_images/'
pattern_dir = img_db+'patterns/'

def image_selection(num_to_select = 50, directory = random_img_dir, num_t = 3, num_p = 3):
    n = 0
    directory = directory+'defect0'+str(num_t)+'/'
    ok_list = []
    de_list = []

    parts = 'L'+str(num_p)
    ok_dir = root+'ok/20171127_20171220_ok_CAM1_'+parts+'_polaroid/'
    de_dir = root+'defects/20171127_20171220_defect_CAM1_'+parts+'_polaroid/'

    for i in range(8):
        a, b = set_list(i+1)
        ok_list = ok_list + a
        de_list = de_list + b

    random_defects = random.sample(de_list, num_to_select)
    random_defects = np.intersect1d(random_defects, set_type(num_p, num_t))

    for i, f in enumerate(random_defects):
        img_dir = de_dir+f
        if isfile(img_dir):
            continue
        for j, img_name in enumerate(os.listdir(img_dir)):
            try:
                if not(os.path.isdir(directory)):
                    os.makedirs(os.path.join(directory))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print("Failed to create directory!")
                    raise

            tmp = img_name.split('.')
            if tmp[-1]=='png' and tmp[0].split('_')[-1] != 'CAM1' and tmp[0].split('_')[2] == '1':
                n += 1

                print(img_dir+'/'+img_name)
                ## copy image of img_dir/img_name to random image directory
                shutil.copy(img_dir+'/'+img_name, directory)

                os.rename(directory+img_name, directory+'defect0'+str(num_t)+'_'+str(n)+'.png')



def find_end_points(img): # This function is available for only scratch defect
    minLineLength = 10
    maxLineGap = 10
    lines = cv2.HoughLinesP(img,1,np.pi/180,100,minLineLength,maxLineGap)

    x1, x2, y1, y2 = [], [], [], []
    for i in range(len(lines)):
        x1 = x1+[lines[i][0][0]]
        y1 = y1+[lines[i][0][1]]
        x2 = x2+[lines[i][0][2]]
        y2 = y2+[lines[i][0][3]]

    return (min(x1+x2), min(y1+y2), max(x1+x2), max(y1+y2))

def extract_pattern(n = 0, original_dir = random_img_dir, marked_dir = marked_img_dir, defect_type = 'defect03'):
#     if folder[-1] != '/':
#         folder = folder + '/'
#     print('folder : '+folder)

    mark_folder = marked_dir+defect_type+'/'
    original_folder = random_img_dir+defect_type+'/'
    save_folder = pattern_dir+defect_type+'/'

    for i in range(n):

        candidate = cv2.imread(mark_folder+defect_type+'_mark'+str(i+1)+'.jpg')
        original = cv2.imread(original_folder+defect_type+'_'+str(i+1)+'.png')

        ## test code
        #print(str(i+1)+"th iteration")
        #print(mark_folder+defect_type+'_mark'+str(i+1)+'.jpg')
        #print("cv2.imread call is failed : "+str(candidate==None))

        height, width = original.shape[:2]

        # Extract the red marks. Get the end points of the line
        hsv = cv2.cvtColor(candidate, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0,200,200]) #example value
        upper_red = np.array([10,255,255]) #example value
        mask = cv2.inRange(hsv, lower_red, upper_red)

        #(min_x, min_y, max_x, max_y) = find_end_points(mask)
        max_y, min_y, max_x, min_x = max(np.where(mask>0)[0]), min(np.where(mask>0)[0]), max(np.where(mask>0)[1]), min(np.where(mask>0)[1])

        # Get a rectangle box which contains the line by using the end points
        min_x = max(0, min_x-10)
        max_x = min(width, max_x+10)
        min_y = max(0, min_y-10)
        max_y = min(height, max_y+10)

        crop_img = original[min_y:max_y, min_x:max_x]

        # Save the rectangle boxes from original scratch files. These boxes will be considered as candidate features.
        try:
            if not(os.path.isdir(save_folder)):
                os.makedirs(os.path.join(save_folder))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory!")
                raise

        cv2.imwrite(save_folder+'pattern'+str(i+1)+'.jpg', crop_img)

        print(i+1)
