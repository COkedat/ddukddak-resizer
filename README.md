# 뚝딱 리사이저
## Ddukddak Resizer
### 한국어
대충 NAI Anlas 낭비를 막기위한 리사이징 코드뭉치

리사이징하면 1024*1024 = 1048576 범위 안에 들어가도록 리사이징해줌

생성되는 컨픽 설명
```
[DEFAULT]
resize_all - 이미지 리스트를 어떻게 모을지 여부
 - True  >> 실행 파일과 동일 폴더내 모든 이미지들로 리스트 작성
 - False >> 드래그 앤 드롭이나 인수로 이미지 리스트 작성 (기본값)

[img_resize]
target_area - 가로*세로의 최대 크기
 - 1048576 (기본값)

[img_save]
use_folder - output 폴더 생성 여부 (기본값 True)
save_folder - 저장 폴더 명 (기본값은 resized)
save_suffix - 저장 접미사 명 (기본값은 _resized)
save_on_exe_folder - 실행 파일과 동일 경로에 저장할지 여부
 - True  >> 실행 파일과 동일 경로에 저장, 폴더 생성함 (기본값)
 - False >> 원본 이미지 경로와 동일한 경로에 저장, 폴더를 생성하지 않음

[img_path]
is_path_override - 저장 경로 오버라이드 여부 (기본값 False)
path_override - 저장 경로
정보) 오버라이드는 use_folder, save_folder, save_on_exe_folder를 무시함
```

빌드 하는 법
'pyinstaller -F ddukddak_resizer_main.py'






### English
Resizing code to prevent NAI Anlas waste

Resizing to fall within the range of 1048576 (1024*1024)

Config desc
```
[DEFAULT]
resize_all - How to create the image list
 - True  >> Create a list of all images in the same folder as the executable file
 - False >> Create an image list with drag-and-drop or argument (Default)

[img_resize]
target_area - Maximum Size of Width * Length
 - 1048576 (Default)

[img_save]
use_folder - Determines creating output folder (Default is True)
save_folder - Save folder name (Default is 'resized')
save_suffix - Save suffix name (Default is '_resized')
save_on_exe_folder - Whether to save to the same path as the executable file
 - True  >> Save to the same path as the executable, creates a folder (Default)
 - False >> Save to the same path as the source image path, does not create a folder

[img_path]
is_path_override - Determines Overriding output path (Default is False)
path_override - Output path
정보) If Override option is true, It ignores [use_folder, save_folder, save_on_exe_folder]
```


How to build 
'pyinstaller -F ddukddak_resizer_main.py'
