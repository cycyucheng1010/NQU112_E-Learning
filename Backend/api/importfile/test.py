import os

file_path = "C:\\Users\\user\\Desktop\\apple.m4a"

if os.path.exists(file_path):
    print(f"文件 {file_path} 存在.")
else:
    print(f"文件 {file_path} 不存在.")
