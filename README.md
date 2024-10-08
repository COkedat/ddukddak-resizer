# 뚝딱 리사이저
## Ddukddak Resizer
### 한국어
대충 NAI Anlas 낭비를 막기위한 리사이징 코드뭉치 (내가 쓸려고 만듦)

리사이징하면 1024*1024 = 1048576 범위 안에 들어가도록 리사이징해줌

기본적으로 exe나 py에 이미지를 드래그 앤 드롭해 실행하면 됨

생성되는 컨픽 설명
```
[img_load]
is_folder_mode - 그냥 실행시 폴더 선택으로 바꿀지 여부
 - True  >> 폴더 선택
 - False >> 파일 선택 (기본값)
is_folder_mode_recursive - 폴더 선택일 경우 재귀로 불러오는지 여부
 - True  >> 재귀로 내부 폴더까지 불러옴
 - False >> 해당 폴더에서만 불러옴 (기본값)


[img_resize]
target_size - 가로 세로 최대 크기
 - 1024 (기본값)

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
```
정보) 오버라이드는 use_folder, save_folder, save_on_exe_folder를 무시함

빌드 하는 법
'pyinstaller -F ddukddak_resizer_main.py'       




#

### English
Resizing code to prevent NAI Anlas waste

Resizing to fall within the range of 1048576 (1024*1024)

Basically you can drag and drop images on exe or py file

Config desc
```
[img_load]
is_folder_mode - Folder Selction if you start with no arguments
 - True  >> Folder Selction
 - False >> File Selction (Default)
is_folder_mode_recursive - Recursively load image files on Folder Selection Mode
 - True  >> Recursively load image files on Folder Selection Mode
 - False >> Only load image files on selected folder (Default)


[img_resize]
target_area - Maximum Size of Width or Length
 - 1024 (Default)

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
```
Info) If Override option is true, It ignores [use_folder, save_folder, save_on_exe_folder]    

How to build 
'pyinstaller -F ddukddak_resizer_main.py'
