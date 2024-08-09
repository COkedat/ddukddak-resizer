# img_module.py를 불러옴
# 대충 이미지 리사이즈를 하고 저장하는 코드

from tqdm import tqdm
import sys
import configparser
from PIL import Image
import math
import os

class ImageResizer:
    # 생성자
    def __init__(self):
        # 변수와 기본값 설정
        self.resize_all = False
        self.target_area = 1048576
        self.save_folder = 'resized'
        self.save_suffix = '_resized'
        self.save_on_exe_folder = True
        
        # 설정 파일이 없다면 만듦
        if not os.path.exists('config.ini'):
            # 설정 파일 생성
            config = configparser.ConfigParser(interpolation=None)
            
            # 설정 파일에 기본값 입력
            config['DEFAULT'] = {}
            config['DEFAULT']['resize_all'] = 'False'
            config['img_resize'] = {}
            config['img_resize']['target_area'] = '1048576'
            config['img_save'] = {}
            config['img_save']['save_folder'] = 'resized'
            config['img_save']['save_suffix'] = '_resized'
            config['img_save']['save_on_exe_folder'] = 'True'

            # 설정 파일 저장
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        
        # 설정 파일을 불러옴
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.resize_all = config.getboolean('DEFAULT', 'resize_all')
        self.target_area = config.getint('img_resize', 'target_area')
        self.save_folder = config.get('img_save', 'save_folder')
        self.save_suffix = config.get('img_save', 'save_suffix')
        self.save_on_exe_folder = config.getboolean('img_save', 'save_on_exe_folder')
    
    # 이미지 오염 여부 확인 함수
    def is_corrupted(self, img_path):
        try:
            # 이미지를 불러와서 해상도를 확인
            img = Image.open(img_path)
            img.verify()
            return False
        except:
            return True


    # 이미지 리사이즈 함수
    # 기본적인 목표는 이미지의 해상도의 곱이 target_area보다 작아지도록 리사이즈
    def img_resize(self, img_path):
        # 이미지를 불러와서 해상도를 확인
        img = Image.open(img_path)
        width, height = img.size

        # 해상도의 곱이 target_area보다 작다면 이미지를 그대로 반환
        if height * width < self.target_area:
            return img
        # 해상도의 곱이 target_area보다 크다면 이미지를 리사이즈
        else:
            # 이미지의 비율이 1:1이라면 1024X1024로 변경
            if height == width:
                img = img.resize((1024, 1024), Image.Resampling.LANCZOS)

            # 아니면 해상도의 곱이 target_area보다 작아질때까지 비율에 맞춰 줄임
            else:
                # 원본 이미지의 비율
                aspect_ratio = width / height

                # 면적을 기준으로 새로운 높이 계산
                new_height = math.sqrt(self.target_area / aspect_ratio)
                new_height = int(new_height)
                new_width = int(new_height * aspect_ratio)

                # 최종 면적이 target_area을 초과하지 않는지 확인
                if new_width * new_height > self.target_area:
                    new_width -= 1
                    new_height = int(new_width / aspect_ratio)

                # 이미지 리사이즈
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # 리사이즈된 이미지를 반환
                return resized_img
        # 그냥 넣은거임
        return img

    # 이미지 저장 함수
    def img_save(self, img, img_path):
        # save_on_exe_folder가 True일 경우 실행 파일이 있는 폴더에 저장 (기본값, 폴더 생성 O)
        if self.save_on_exe_folder:
            save_path = os.path.join(os.path.dirname(sys.argv[0]), self.save_folder)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            save_path = os.path.join(save_path, os.path.basename(img_path)[:-len(os.path.splitext(img_path)[1])] + self.save_suffix)
            save_path = os.path.join(save_path + os.path.splitext(img_path)[1])

        # save_on_exe_folder가 False일 경우 원본 이미지와 동일한 경로에 저장 (폴더 생성 X)
        else:
            # 파일의 경로, 이름, 확장자 분리
            file_path = os.path.dirname(img_path)
            file_name = os.path.basename(img_path)
            file_ext = os.path.splitext(img_path)[1]

            # 저장할 파일 이름 생성
            file_name = file_name[:-len(file_ext)] + self.save_suffix + file_ext
            save_path = os.path.join(file_path, file_name)

        # 이미지 저장
        img.save(save_path)

def main():
    # 클래스 생성
    resizer = ImageResizer()
    
    # resize_all이 True일 경우 동일 폴더 내 모든 이미지 리사이징
    if resizer.resize_all:
        # 이미지 파일 목록 불러오기
        print("Mode : Resize All")
        img_list = [f for f in os.listdir('.') if 
                    f.endswith('.jpg') or f.endswith('.png') or 
                    f.endswith('.jpeg') or f.endswith('.bmp') or 
                    f.endswith('.gif') or f.endswith('.webp')]
        if len(img_list) == 0:
            print("[Warning] No image files in the folder.")
            print("Usage: Please put image files in the folder.")
            return

    # False일 경우 인수로 들어온 이미지 파일만 리사이징 (기본값)
    else:      
        # 이미지 파일 경로를 입력하지 않았을 경우 사용법 출력
        if len(sys.argv) < 2:
            print("[Warning] No image file path is given.")
            print("Usage: python img_main.py [image_path1] [image_path2] ...")
            print("Or change 'resize_all' to 'True' in config.ini to resize all images in the folder.")
            return
        # 인수들을 이미지 파일 리스트로 저장
        print("Mode : Resize Selected")
        img_list = sys.argv[1:]

    # 이미지 리스트 리사이징 후 저장
    for img_o in tqdm(img_list):
        if resizer.is_corrupted(img_o):
            # 파일명만 출력
            print(f"[Warning] {os.path.basename(img_o)} is corrupted. Skipping...")
            continue
        img = resizer.img_resize(img_o)
        resizer.img_save(img, img_o)
    return
    

if __name__ == '__main__':
    main()
    input("Press Any Key to exit...")