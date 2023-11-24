from PIL import Image
import os

# 指定文件夹路径和新的图片尺寸，这里用的是绝对路径，可以自行修改
folder_path = "C:\\Users\\weikejie\\Desktop\\stable-diffusion-main\\img"
new_size = (512, 512)
count=0;
# 遍历文件夹中的所有图片文件
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # 打开图片并调整大小
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)
        image = image.resize(new_size)
        new_filename = "{:05d}".format(count) + os.path.splitext(filename)[1]
        # 生成新的文件名并保存图片
        count+=1
        new_image_path = os.path.join(folder_path, new_filename)
        image.save(new_image_path)
