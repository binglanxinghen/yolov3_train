import os
import sys
import shutil
import argparse
import xml.etree.ElementTree as ET
import pdb

classes = []
current_path=os.path.split(os.path.realpath(__file__))[0]
default_path=os.path.join(current_path,"../../train_data")
default_train_path=os.path.join(current_path,"../data/dataset/my_train.txt")
default_test_path=os.path.join(current_path,"../data/dataset/my_test.txt")
default_test_path=os.path.join(current_path,"../data/dataset/my_test.txt")
default_name_inside_path=os.path.join(current_path,"../data/classes/my.names")
default_name_outside_path=os.path.join(default_path,"my.names")
if os.path.exists(default_name_outside_path):
    shutil.copy(default_name_outside_path,default_name_inside_path)
    with open(default_name_outside_path) as f:
        classes = f.readlines()
        classes = list(map(lambda x:x.strip("\n"),classes))
        #print(classes)
else:
    print(default_name_outside_path+" is not existed.")
    sys.exit(0) 
#pdb.set_trace()
def convert_voc_annotation(data_path, data_type, anno_path, use_difficult_bbox=True):
    global classes
    img_inds_file = os.path.join(data_path, 'ImageSets', 'Main', data_type + '.txt')
    with open(img_inds_file, 'r') as f:
        txt = f.readlines()
        image_inds = [line.strip() for line in txt]

    with open(anno_path, 'w') as f:
        for image_ind in image_inds:
            image_path = os.path.join(data_path, 'JPEGImages', image_ind + '.jpg')
            annotation = image_path
            label_path = os.path.join(data_path, 'Annotations', image_ind + '.xml')
            root = ET.parse(label_path).getroot()
            objects = root.findall('object')
            for obj in objects:
                difficult = obj.find('difficult').text.strip()
                if (not use_difficult_bbox) and(int(difficult) == 1):
                    continue
                bbox = obj.find('bndbox')
                class_ind = classes.index(obj.find('name').text.lower().strip())
                xmin = bbox.find('xmin').text.strip()
                xmax = bbox.find('xmax').text.strip()
                ymin = bbox.find('ymin').text.strip()
                ymax = bbox.find('ymax').text.strip()
                annotation += ' ' + ','.join([xmin, ymin, xmax, ymax, str(class_ind)])
            print(annotation)
            f.write(annotation + "\n")
    return len(image_inds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default=default_path)
    parser.add_argument("--train_annotation", default=default_train_path)
    parser.add_argument("--test_annotation",  default=default_test_path)
    flags = parser.parse_args()

    if os.path.exists(flags.train_annotation):os.remove(flags.train_annotation)
    if os.path.exists(flags.test_annotation):os.remove(flags.test_annotation)

    num1 = convert_voc_annotation(os.path.join(flags.data_path, 'train/'), 'trainval', flags.train_annotation, False)
    #num2 = convert_voc_annotation(os.path.join(flags.data_path, 'train/VOCdevkit/VOC2012'), 'trainval', flags.train_annotation, False)
    #num3 = convert_voc_annotation(os.path.join(flags.data_path, 'test/VOCdevkit/VOC2007'),  'test', flags.test_annotation, False)
    num2 = convert_voc_annotation(os.path.join(flags.data_path, 'test/'),  'test', flags.test_annotation, False)
    #print('=> The number of image for train is: %d\tThe number of image for test is:%d' %(num1 + num2, num3))
    print('=> The number of image for train is: %d\tThe number of image for test is:%d' %(num1, num2))


