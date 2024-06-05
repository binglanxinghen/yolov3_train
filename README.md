# yolov3_train   

## 简介
该代码是训练的代码，可以任意拷贝到任何机器，只需要对应机器有安装git，git clone 这个仓库即可，运行代码需要额外的python包，需要pip install如下：

1.opencv-python  
2.tensorflow==1.14.0  
3.pillow  
4.flask  
5.flask_paginate  
6.flask_sqlalchemy  
7.python-docx  
8.easydict  
其中如果涉及到动态库未安装，在例如libSM.so.6,centos机器可以yum whatprovides libSM.so.6，然后用yum install安装，例
如yum install libSM-1.2.2-2.el7.x86_64 --setopt=protected_multilib=false，如果ubuntu系统，有类似动态库未安装，这里提供一个命令，一键安装所有库，apt-get install -y libsm6 libxext6 libxrender-dev libglib2.0-0
## 训练步骤(**重要)
### 数据预处理

简介：通常数据使用Lableme或者Lableimg等数据集标注工具来构造数据集。此时数据集尚未分割成训练，验证，预测三个部分的数据集，通常比例是8:1:1,因此此步是为了将数据集分割成训练，验证，预测三个部分。  
准备工作：
  1.Lableme或者Lableimg标注后的数据集总文件夹。  
  2.记录着类别名称的文件，比如my.names的文件(一行就是一个类别名)。  

准备工作第一点，假设通过Lablelme或者Labelimg工具标注后的数据集文件夹如下结构：  

-pdata  
  -A_pic(A类花朵图片文件夹)   
  -A_xml(A类花朵xml文件夹)  
  -B_pic(B类花朵图片文件夹)  
  -B_xml(B类花朵Xml文件夹)  
  -C_pic(C类花朵图片文件夹)  
  -C_xml(C类花朵xml文件夹)  
假设存放在/home/test/pdata路径下  
其实文件夹的目录结构无所谓，因为脚本deal_data会根据my.names的类别名称深入检测每一个文件夹的子文件夹，递归的查找每一朵花和每一朵花的xml。但是要注意两点：  
1.这里总目录名和总文件夹下面的子文件夹目录名字必须是英文！！！不是英文名的文件夹先改为英文名的目录名。比如示例是pdata，和A_pic..都是  
2.my.names里面的名称别写错了，因为是根据里面名称查找文件的，假设my.names里面写下A,B,D，错将C写成D，那么生成结果会少掉C的数据。  
准备工作第二点，my.names文件内容示例：  
my.names  
  A  
  B  
  C  
执行脚本：  
  python deal_data -d deal_data -f 

脚本deal_data检测后会构成字典结构：{A类花朵图片1路径：A类花朵1的xml路径，A类花朵图片2路径：A类花朵2的xml路径,...,C类花朵n的路径：C类花朵n的xml路径}最终并根据这个字典结构，以每种花训练，验证，预测的8:1:1的比例构造新的文件夹data，结构如下：
-data  
  -train  
    -Annotations(A,B,C百分之80的xml)  
    -JPEGImages(A,B,C百分之80的图片)  
  -test  
    -Annotations(A,B,C百分之10的xml)   
    -JPEGImages(A,B,C百分之10的xml)   
  -predict  
    -Annotations(A,B,C百分之10的xml)   
    -JPEGImages(A,B,C百分之10的xml)   


### 数据准备
简介：yolov3训练和验证用的数据集放置于目录train_data里面，其中
训练集目录是train_data/train,验证集目录train_data/test，目录下都有Annotations,ImageSets,JPEGImages,SegmentationClass,SegmentationObject，其中只需要关注Annotations,ImageSets,JPEGImages这三个目录，其中ImageSets目录的Main的trainval.txt和test.txt里面写着是训练图片/xml去掉后缀的名字，程序只会训练定义在这两个文件中数据。  
1.把xml数据放置于Annotations目录,jpg图片放置于JPEGImages目录。  
2.运行脚本pre_data.py第一步放置的训练集写在trainval.txt或者test.txt里面.脚本命令为：  
python pre_data.py -t true -e true -l  
具体的参数意思python pre_data.py -h有描述。  
3.最后一步将此次训练集的类别名称写在my.names里面，比如此次训练集包含车，人，鸟，就依次一行一个类别写下cat，human，bird  
### 开始训练
1.进入train_code目录里面，运行python scripts/voc_annotation.py将数据集转换成yolov3的格式  
2.运行python train.py开始训练，等待训练结束  
3.训练结束运行python evaluate.py开始验证  
4.进入mAP目录，cd mAP  
5.python main.py -na获取验证集map的值
## 上传到github
本地代码改完如果需要上传到github上，需要检查一下第一条规则，不要把checkpoint里面的目录上次到github，因为模型太大了。 不熟悉git 命令需要去学，或者linux的vim编辑命令不熟，需要学习。  
简单介绍一下git的流程。git分为本地仓库，暂存仓，远程仓库。  
1.本地仓就是当前我们编辑代码的环境，当我们把git clone xxx 到某台电脑时候，那台电脑就是本地仓。  
2.当我们改完代码时候，可以使用git diff 或者git diff HEAD，皆可以显示刚才更改了那些地方。  
3.当我们本地全部代码编辑完，可以使用git add XXX，把文件提交到暂存仓(一键提交所有的改动是git add -A)，这时候如果add 错了文件，可以用git reset HEAD xxx把这个文件从暂存仓删除(也可以全部一键从暂存仓删除，git reset HEAD .，注意HEAD后面有个点)。  
4.提交到暂存仓后可以git status看一下刚才提交了哪些文件，检测一下时候提交了模型！！！，不要提交模型。  
5.使用git commit，是讲暂存仓库提交到本地仓，这时候会进入到vim模式让你编辑这次代码改动的log，比如这次做了一个新功能，那么这个信息记录到log里面，保存退出即可，:wq（vim的保存退出）。  
6.最后提交到远程仓库，git push -u origin master。  
7.把github账号密码一填即可。  
