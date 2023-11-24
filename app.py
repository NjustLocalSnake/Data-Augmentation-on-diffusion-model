
import shutil
import time
import subprocess
from PIL import Image
from flask import Flask
from flask import request, render_template
import os
from flask import make_response
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_cors import CORS
import json

#创建了Flask web应用程序的实例。
app = Flask(__name__)


CORS(app, supports_credentials=True)
# UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'videos')
RESULTS_PATH = os.path.join(os.path.dirname(__file__), 'results')
RESULTS_SAMPLES_PATH = os.path.join(RESULTS_PATH, 'samples')
# FINAL_PATH = os.path.join(os.path.dirname(__file__), 'final')

@app.route('/upload', methods=['POST'])
def upload():
    list_file = request.files.get("img")
    time_=str(int(time.time()*1000))
    file_name=time_ + "_" + list_file.filename
    local_path=RESULTS_PATH + "\\" + file_name
    list_file.save(RESULTS_PATH + "\\" + file_name)

# 打开上传的图像文件 改尺寸！！
    img = Image.open(list_file)
    # 调整图像尺寸为 (512, 512)
    img = img.resize((512, 512), Image.ANTIALIAS)
    # 保存调整后的图像
    img.save(local_path)
    # 关闭图像文件
    img.close()

    r = os.popen(fr"python scripts/img2img.py --init-img {local_path} --strength 0.4 --n_iter 3")
    # r = os.popen(fr"python detect.py --save-txt --save-conf --weights runs/train/exp_yolov5s/weights/best.pt --source {local_path} ")
    text = r.read()
    r.close()
    print(text)
    # res_list=" ".join((text.replace(",","").split(" ")[4:][0:-1])).split("Done.")

    #把新生成的从exp里移出来
    root = fr"C:\Users\weikejie\Desktop\stable-diffusion-main\results"
    res_path=""
    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            res_path=os.path.join(dirpath, filepath)
#samples/xx.png

    png_image = Image.open(res_path)
    # 把新产生的图片，命名为上传时的图片的名字
    new_res_path=RESULTS_PATH + "\\" + file_name
    os.remove(root + '\\' + new_res_path.split("\\")[-1])
    png_image.save(new_res_path, 'JPEG')
    # 关闭 PNG 图片
    png_image.close()

    # os.remove(root + '\\' + res_path.split("\\")[-1])
    # os.remove(root+'\\'+new_res_path.split("\\")[-1])                  #把results里原来是上传的原图去掉
    # shutil.move(new_res_path,root+'\\'+new_res_path.split("\\")[-1])  #新产生的图从samples里移到results里

    # file_name=res_path.split("\\")[-2:][0]+"/"+res_path.split("\\")[-2:][1]
    tempFilePaths=[]
    tempFilePaths.append(fr"http://10.24.128.10:5000/results/{file_name}")
    data = {
        "status": "success",
        "result": "6",
        "spent": "6",
        "tempFilePaths": tempFilePaths,

    }

    response = json.dumps(data)  # 将python的字典转换为json字符串
    return response, 200, {"Content-Type": "application/json"}
    # return

# 访问上传的文件
# 浏览器访问：http://127.0.0.1:5000/videos/1.mp4/  就可以查看文件了
@app.route('/results/<filename>/', methods=['GET'])
def get_image(filename):
    return send_from_directory(RESULTS_PATH, filename)



if __name__ == '__main__':
    app.run(host="0.0.0.0")
