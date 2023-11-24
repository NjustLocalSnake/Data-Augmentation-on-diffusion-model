### 图像分析与处理大作业
# 基于Diffusion model的数据增强微信小程序



## 使用说明


### 安装
```shell
conda env create -f environment.yaml
conda activate ldm
```

### 更改为您自己的ip
更改`app.py`中的 ` fr"http://ip:5000/results/{file_name}" ` 的 ip 为您自己的ipv4地址
<br/>
更改`index.js`中的 ` url: 'http://ip:5000/upload" ` 的 ip 为您自己的ipv4地址  


### 下载权重文件

After [obtaining the `stable-diffusion-v1-*-original` weights](#weights), link them
```
mkdir -p models/ldm/stable-diffusion-v1/
ln -s <path/to/model.ckpt> models/ldm/stable-diffusion-v1/model.ckpt 
```

