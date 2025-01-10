import os
import json
import csv
import subprocess

# 需要下载的代码合集路径
repo_file = "/home/mylab/dataset/APIdataset/Crawler_Dataset/Py_code/19_1_12_py/code8.txt"
# 下载记录路径
csv_path = "/home/mylab/dataset/APIdataset/Crawler_Dataset/Py_code/19_1_12_py/file_url8.csv"
# 存储路径
download_path = "/home/mylab/dataset/APIdataset/Crawler_Dataset/Py_code/19_1_12_py/data8/"

# 将文件名存入csv
def csv_create(repositories):
    header = ['filename','file_url']
    path = csv_path
    if os.path.exists(path):
        with open(path, 'a', encoding='utf-8', newline='') as file_obj:
            writer = csv.DictWriter(file_obj,fieldnames = header)
            writer.writerows(repositories)
    else:
        with open(path, 'w', encoding='utf-8', newline='') as file_obj:
            writer = csv.DictWriter(file_obj,fieldnames = header)
            writer.writeheader()
            writer.writerows(repositories)

# 获取文件中的仓库
def read_repositories():
    repositories = []
	# 获取文件信息
    with open(repo_file, 'r') as input_file:
        for repo_name in input_file:
            if "," not in repo_name:
                continue
            if "index," in repo_name:
                continue
            index,repository,file_url,commit_count,commit_url = repo_name.split(",") 
            urlname = os.path.basename(file_url)
            filename = commit_count + urlname
            repo_info = {
                "file_url": "https://mirror.ghproxy.com/" + file_url,
                "filename": filename 
            }
            repositories.append(repo_info)
        input_file.close()
    return repositories

# 下载相应代码  
def bash_run(repositories):
    for file in repositories:
        subprocess.run("curl -L -o " + download_path + file["filename"] + " " + file["file_url"], shell=True)


def run():
    #github = login('Summer-Libra',token='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')
    repositories = read_repositories()
    csv_create(repositories)
    bash_run(repositories)
    

run()




