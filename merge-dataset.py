import glob
import os
import xml.etree.cElementTree as ET
import shutil
from tqdm import tqdm
import argparse

def merge(path_data, save_dir):
    images = glob.glob(path_data + '/**/**.jpg')
    max_img = len(images)
    # prefix_img = 'uit_'

    # save_dir = 'uit-drone-dataset-22-04-2021'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    if not os.path.exists(os.path.join(save_dir, 'images')):
        os.mkdir(os.path.join(save_dir, 'images'))

    if not os.path.exists(os.path.join(save_dir, 'annotations')):
        os.mkdir(os.path.join(save_dir, 'annotations'))

    def solve_xml(xml_path, name_img, save_path):
        tree = ET.parse(xml_path)
        root_xml = tree.getroot()

        for folder in root_xml.findall('filename'):
            folder.text = name_img
        
        tree.write(save_path)

    for i in tqdm(range(0, max_img)):
        img = images[i]
        root_path = os.path.split(img)[0]
        filename = os.path.splitext(os.path.split(img)[-1])[0]
        # filename_new = prefix_img + str(i)
        filename_new = os.path.split(root_path)[-1] + '_' + filename
        xml_file = os.path.join(root_path, filename + '.xml')
        solve_xml(xml_file, filename_new + '.jpg', os.path.join(save_dir, 'annotations', filename_new + '.xml'))
        shutil.copyfile(img, os.path.join(save_dir, 'images', filename_new + '.jpg'))

def get_args():
    parser = argparse.ArgumentParser('Train')
    parser.add_argument('--data_dir', type=str, default='./',
                        help='Data dir', dest='data_dir')
    parser.add_argument('--save_dir', type=str, default='./',
                        help='Save dir', dest='save_dir')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = get_args()
    merge(args.data_dir, args.save_dir)
