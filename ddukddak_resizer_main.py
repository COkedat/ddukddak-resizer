# img_module.py를 불러옴
# 대충 이미지 리사이즈를 하고 저장하는 코드

from tqdm import tqdm
import sys
import configparser
from PIL import Image
import math
import os
from glob import glob
from tkinter import filedialog

class ImageResizer:
    # 생성자
    def __init__(self):
        # 설정 파일 경로 설정
        base_path = os.path.dirname(sys.argv[0])
        config_path = os.path.join(base_path, 'config.ini')

        # 설정 파일이 없다면 만듦
        if not os.path.exists(config_path):
            # 설정 파일 생성
            self.makeConfig(config_path)
        
        # 설정 파일을 불러옴
        config = configparser.ConfigParser(interpolation=None)
        config.read(config_path)
        
        # img_load 섹션
        self.is_folder_mode = config.getboolean('img_load', 'is_folder_mode') \
            if (config.getboolean('img_load', 'is_folder_mode') is not None) else False
        self.is_folder_mode_recursive = config.getboolean('img_load', 'is_folder_mode_recursive') \
            if (config.getboolean('img_load', 'is_folder_mode_recursive') is not None) else False
        
        # img_resize 섹션
        self.target_area = config.getint('img_resize', 'target_area') \
            if (config.getint('img_resize', 'target_area') is not None) else 1048576
        
        # img_save 섹션
        self.use_folder = config.getboolean('img_save', 'use_folder') \
            if (config.getboolean('img_save', 'use_folder') is not None) else True
        self.save_folder = config.get('img_save', 'save_folder') \
            if (config.get('img_save', 'save_folder') is not None) else 'resized'
        self.save_suffix = config.get('img_save', 'save_suffix') \
            if (config.get('img_save', 'save_suffix') is not None) else '_resized'
        self.save_on_exe_folder = config.getboolean('img_save', 'save_on_exe_folder') \
            if (config.getboolean('img_save', 'save_on_exe_folder') is not None) else True
        
        # img_path 섹션
        self.is_path_override = config.getboolean('img_path', 'is_path_override') \
            if (config.getboolean('img_path', 'is_path_override') is not None) else False
        self.path_override = config.get('img_path', 'path_override') \
            if (config.get('img_path', 'path_override') is not None) else 'C:\\Users\\Administrator\\Desktop'
                
    
    # 이미지 오염 여부 확인 함수
    def is_corrupted(self, img_path):
        try:
            # 이미지를 불러와서 해상도를 확인
            img = Image.open(img_path)
            img.verify()
            return False
        except:
            return True

    # 설정 파일 생성 함수
    def makeConfig(self, config_path):
        # 설정 파일 생성
        config = configparser.ConfigParser(interpolation=None)
        
        # 설정 파일에 기본값 입력
        config['img_load'] = {}
        config['img_load']['is_folder_mode'] = 'False'
        config['img_load']['is_folder_mode_recursive'] = 'False'
        config['img_resize'] = {}
        config['img_resize']['target_area'] = '1048576'
        config['img_save'] = {}
        config['img_save']['use_folder'] = 'True'
        config['img_save']['save_folder'] = 'resized'
        config['img_save']['save_suffix'] = '_resized'
        config['img_save']['save_on_exe_folder'] = 'True'
        config['img_path'] = {}
        config['img_path']['is_path_override'] = 'False'
        config['img_path']['path_override'] = 'C:\\Users\\Administrator\\Desktop'

        # 설정 파일 저장
        with open(config_path, 'w') as configfile:
            config.write(configfile)

    # 이미지 리사이즈 함수
    # 기본적인 목표는 이미지의 해상도의 곱이 target_area보다 작아지도록 리사이즈
    def img_resize(self, img_path):
        # 이미지를 불러와서 해상도를 확인
        img = Image.open(img_path)
        width, height = img.size

        # 해상도의 곱이 target_area보다 같거나 작다면 이미지를 그대로 반환
        if height * width <= self.target_area:
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
        # is_path_override가 True일 경우 path_override로 저장 (가장 우선됨, 폴더 생성 X)
        if self.is_path_override:
            save_path = self.path_override
            save_path = os.path.join(save_path, os.path.basename(img_path)[:-len(os.path.splitext(img_path)[1])] 
                                     + self.save_suffix + os.path.splitext(img_path)[1])
        # save_on_exe_folder가 True일 경우 실행 파일이 있는 폴더에 저장 (기본값, 폴더 생성 O)
        elif self.save_on_exe_folder:
            save_path = os.path.dirname(sys.argv[0])
            # use_folder가 True일 경우 하위 폴더를 생성
            if self.use_folder:
                save_path = os.path.join(save_path, self.save_folder)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                save_path = os.path.join(save_path, os.path.basename(img_path)[:-len(os.path.splitext(img_path)[1])]
                                         + self.save_suffix+ os.path.splitext(img_path)[1])
            # False일 경우 하위 폴더를 생성하지 않음
            else:
                save_path = os.path.join(save_path, os.path.basename(img_path)[:-len(os.path.splitext(img_path)[1])] 
                                         + self.save_suffix + os.path.splitext(img_path)[1])

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

    # 이미지 파일 경로를 입력하지 않았을 경우 사용법 출력
    if len(sys.argv) < 2:
        # 기초 경로 설정
        base_path = os.path.dirname(sys.argv[0])

        # 폴더 모드일 경우 폴더 선택
        if resizer.is_folder_mode:
            # 폴더 선택
            directory = filedialog.askdirectory(initialdir=base_path, title="Select Folder")
            glob_pattern = ("*.jpg", "*.png","*.jpeg","*.bmp","*.gif","*.webp")

            # 폴더 내 이미지 파일 리스트 불러오기 (재귀 O)
            if ((directory is not None or directory != '') and resizer.is_folder_mode_recursive):
                img_list = []
                for imgs in glob_pattern:
                    img_list.extend(glob(directory + "/**/" + imgs, recursive=True))

            # 폴더 내 이미지 파일 리스트 불러오기 (재귀 X)
            elif((directory is not None or directory != '') and not resizer.is_folder_mode_recursive):
                img_list = []
                for imgs in glob_pattern:
                    img_list.extend(glob(directory + "/" + imgs))

            # 폴더 선택하지 않았을 경우
            else: 
                img_list = None
            
        # 폴더 모드가 아닐 경우 이미지 파일 선택
        else:
            img_list = filedialog.askopenfilenames(initialdir=base_path, title="Select Image Files", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg;*.bmp;*.gif;*.webp")])

        # 이미지 파일이 없거나 선택하지 않았을 경우
        if (img_list is None or len(img_list) == 0):
            print("[Warning] No image files or No folder selected. Exiting...")
            input("Press Any Key to exit...")
            return
    else:
        # 인수들을 이미지 파일 리스트로 저장
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