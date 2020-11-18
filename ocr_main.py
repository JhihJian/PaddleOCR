import tools.infer.predict_system as ocr_system
import tools.infer.utility as utility
import sys
import os
import time
import shutil
import csv

work_dir= "/opt/PaddleOCR" #"K://3-WorkSpace//2-Python-Projects//PaddlePaddle-OCR//PaddleOCR"#"/opt/PaddleOCR"
_config_image_path= work_dir + "/ocr-files/images"
_config_backup_path= work_dir + "/ocr-files/backup"
_config_sleep_time=1 #s
det_model_dir= work_dir + "/inference/det_model/"
rec_model_dir= work_dir + "/inference/rec_model/"
cls_model_dir= work_dir + "/inference/cls_model/"
result_dir = "/opt/PaddleOCR/ocr-files/results/"
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

argv_back=sys.argv.copy()

def createArgs(image_path):
    sys.argv=argv_back.copy()
    sys.argv.append("--use_angle_cls=True")
    sys.argv.append("--use_space_char=True")
    sys.argv.append("--image_dir="+image_path)
    sys.argv.append("--det_model_dir="+det_model_dir)
    sys.argv.append("--rec_model_dir="+rec_model_dir)
    sys.argv.append("--cls_model_dir="+cls_model_dir)

# 输入目录路径，路径内为图片文件，文件名为timestamp
# 输出目标路径，文件名为目录名+.txt，文件内容为 dict转换的json
# dict 结构 timestamp : ocr_text
def ocr_image(file_path):
    if os.path.isdir(file_path):
        createArgs(file_path)
        print(sys.argv)
        result_dict= ocr_system.main(utility.parse_args())
        with open(os.path.join(result_dir,os.path.basename(file_path)+".txt"),'w',encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerows(result_dict.items())
        # os.rmdir(file_path) 只能删除空文件夹
        shutil.rmtree(file_path)
        print(file_path+" finish")



if __name__ == '__main__':
    if not os.path.exists(_config_backup_path):
        os.makedirs(_config_backup_path)
    if not os.path.exists(_config_image_path):
        os.makedirs(_config_image_path)
    while(True):
        for file in os.listdir(_config_image_path):
            ocr_image(os.path.join(_config_image_path, file))
        time.sleep(_config_sleep_time)

