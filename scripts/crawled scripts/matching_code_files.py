import json
from github3 import login
import getpass
import csv
import argparse

QUERY_SIZE = 20
# base_query = '"#include <openssl/" language:c extension:c'
base_query = '"crypto/" language:go extension:go'
# base_query = '"from Crypto" language:python extension:py'
# base_query = '"javax.crypto" language:java extension:java'

repo_file = "/home/mylab/dataset/APIdataset/Crawler_Dataset/Go_code/23_1_12_go/repositories1_2.txt"
output_file = "/home/mylab/dataset/APIdataset/Crawler_Dataset/Go_code/23_1_12_go/code1.txt"

# 获取文件中的仓库
def read_repositories():
    repositories = []
    with open(repo_file, 'r') as input_file:
        for repo_name in input_file:
            index,name,commit_count,commit_url, forks_count, stargazers_count = repo_name.split(";") #each item in repositories.txt file is "repo_name;lastcommitURL"
            repo_info = {"index": index,
            "name": name.rstrip('\n'),
            "commit_count": commit_count,
            "commit_url": commit_url}
            #repositories.append(name.rstrip('\n'))
            repositories.append(repo_info)
        input_file.close()
    return list(repositories)


# 创建表标题
def create_csv_file():
    csvfile = open(output_file, 'w')
    fieldnames = ['index','repository', 'file_url','commit_count','commit_url']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    return writer


# 爬取库中符合条件的代码
def search_code_in_repos(repos,github):
    query = base_query
    for repo in repos:
        query += " repo:" + repo["name"]
    print("query:",query)
    query_code_results = github.search_code(query)
    return query_code_results

def write_code_results(writer, code_results, repos_to_query):
    for code_result in code_results:
        commit_count=0
        commit_url=''
        index=0
        for repo in repos_to_query:
            if str(repo["name"]) == str(code_result.repository):
                commit_count = repo["commit_count"]
                index = repo["index"]
                commit_url = repo["commit_url"]
        writer.writerow({'index' : index,
            'repository' : code_result.repository,
            'file_url' : code_result.html_url,
            'commit_count' : commit_count,
            'commit_url' : commit_url})


# 将爬取的代码写入csv
def search_code(repositories, writer, start_index, end_index, github):
    repos_to_query = repositories[start_index:end_index]
    code_results = search_code_in_repos(repos_to_query, github)
    write_code_results(writer, code_results, repos_to_query)


def run():
    #github = login('Summer-Libra',token='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')
    github = login('Summer-Libra',token='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')
    repositories = read_repositories() 
    writer = create_csv_file()
    num_of_repos =  len(repositories)
    print('num of repos', num_of_repos) 
    start_index = 0
    end_index = start_index + QUERY_SIZE - 1
    if end_index > num_of_repos:
        end_index = num_of_repos - 1

    while end_index < num_of_repos:
        search_code(repositories, writer, start_index, end_index, github)
        start_index += QUERY_SIZE
        end_index = start_index + QUERY_SIZE - 1

    if (end_index != num_of_repos - 1 and start_index < num_of_repos):
        end_index = num_of_repos
        # print(end_index)
        search_code(repositories, writer, start_index, end_index, github)

run()
