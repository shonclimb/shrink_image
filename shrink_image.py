from PIL import Image
import os
import glob
import pyheif
import subprocess
import argparse
import random,string
import shutil

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size')# 第一引数：省略名, 第二引数：正式名
    parser.add_argument('-t', '--title')# 第一引数：省略名, 第二引数：正式名
    return parser.parse_args()

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

def main():
    arges = get_args()
    FILESIZE = 2*1000000
    IMAGENAME = randomname(5)

    if arges.size:
        FILESIZE = int(arges.size)*1000000
    if arges.title:
        IMAGENAME = arges.title

    # ディレクトリのファイルリストを取得
    pwd = os.path.dirname(os.path.abspath(__file__))
    print(pwd)
    file_list = glob.glob(pwd + '/*')
    
    for file in file_list:
        # HEICファイルだった場合はjpeg変換
        if 'HEIC' in file:
            command = 'sips --setProperty format jpeg ' + file +  ' --out ' + file.replace('.HEIC','.jpeg')
            subprocess.call(command, shell=True)
            os.remove(file)
        elif 'heic' in file:
            command = 'sips --setProperty format jpeg ' + file +  ' --out ' + file.replace('.heic','.jpeg')
            subprocess.call(command, shell=True)
            os.remove(file)
        

    dst_folder = rf'{pwd}/{IMAGENAME}'
    if not os.path.exists(dst_folder):
        os.mkdir(dst_folder)
    
    file_list = glob.glob(pwd + '/*')
    index = 0
    for file in file_list:
        if any(map(file.__contains__,('PNG', 'JPG', 'jpg', 'jpeg','png'))):
            # 画像サイズを確認
            img = Image.open(file)
            extension = str(file).split(".")[1]
            print('filesize: {}, width: {}, height: {}'.format(os.path.getsize(file)*0.000001,img.width, img.height))

            while os.path.getsize(file) > FILESIZE:
                # 読み込んだ画像の幅、高さを取得し半分に
                (width, height) = (int(img.width*0.9) , int(img.height*0.9))
                # 画像をリサイズする
                img = img.resize((width, height))
                # ファイルを保存
                img.save(file, quality=90)
                print('filesize: {}, width: {}, height: {}'.format(os.path.getsize(file)*0.000001, img.width, img.height))

            dst_file_path = rf'{dst_folder}/{IMAGENAME}_{index}.{extension}'
            while os.path.isfile(dst_file_path):
                index += 1
                dst_file_path = rf'{dst_folder}/{IMAGENAME}_{index}.{extension}'
               
            shutil.copyfile(file, dst_file_path)
            print('copyed')
            os.remove(file)
            index += 1
        else:
            print(rf'{file} is not phto')
            continue

if __name__ == '__main__':
    main()