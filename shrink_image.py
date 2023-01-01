from PIL import Image
import os
import glob
import pyheif
import subprocess

FILESIZE = 2000000
# ディレクトリのファイルリストを取得
pwd = '/Users/mac/blog_temp/'
file_list = glob.glob(pwd + '/*')

for filename in file_list:
    # 画像ファイルかチェック
    if 'HEIC' in filename:
        command = 'sips --setProperty format jpeg ' + filename +  ' --out ' + filename.replace('.HEIC','.jpeg')
        subprocess.call(command, shell=True)
        
for file in file_list:
    if any(map(file.__contains__,('PNG', 'JPG', 'jpg', 'jpeg'))):
        # 画像サイズを確認
        img = Image.open(file)
        print('filesize: {}, width: {}, height: {}'.format(os.path.getsize(file)*0.000001,img.width, img.height))
        while os.path.getsize(file) > FILESIZE:
            # 読み込んだ画像の幅、高さを取得し半分に
            (width, height) = (int(img.width*0.9) , int(img.height*0.9))
            # 画像をリサイズする
            img = img.resize((width, height))
            # ファイルを保存
            img.save(file, quality=90)
            print('filesize: {}, width: {}, height: {}'.format(os.path.getsize(file)*0.000001, img.width, img.height))
    else:
        print(rf'{file} is not phto')
        continue

