from github3 import login
import re

START_MONTH='10'
END_MONTH='11'
DAY='01'
YEAR=2019
BASE_QUERY='in:file language:python stars:>100'
#in:description: 这个部分指定了搜索的范围，即搜索项目的描述部分。in:file: 这部分指定了搜索的文件内容范围，但在这个查询中没有指定具体的文件。通常，你可以指定文件类型或搜索特定文件中的内容。
SORT='stars'
ORDER='desc'
INDEX=0

repository_path ='/home/mylab/dataset/APIdataset/Crawler_Dataset/Go_code/23_1_12_go/repositories100.txt'

def filter_private_repos(repository_search_res):
	return not repository_search_res.repository.private

def filter_android_repos(repo_info):
	repo_name = repo_info["repo_name"]
	pattern1 = r'android'
	pattern2 = r'ios'
	filter_res1 = re.search(pattern1,repo_name,re.I)
	filter_res2 = re.search(pattern2,repo_name,re.I)
	if(filter_res1 or filter_res2):
		return 0
	else:
		return 1
	


def get_repo_info(repository_search_res):
	commit_info = get_commit_info(repository_search_res.repository)
	return	{
			"repo_name" : repository_search_res.repository.full_name,
			"commit_count" : commit_info["count"],
			"commit_url" : commit_info["last_commit_url"],
			"forks_count" : repository_search_res.forks_count,
			"stargazers_count" : repository_search_res.stargazers_count}
		

def get_commit_info(repository):
	for commit in repository.commits(): #returns ShortCommit (this is to get the latest commit of the rep)
		break
	latest_commit_url=commit.html_url
	commit_count = 0
	for comm in repository.commits(): #returns ShortCommit (this is to get the total commit count of the rep)
		commit_count = commit_count + 1
	return	{
			"last_commit_url" : latest_commit_url,
			"count" : commit_count}

def get_filtered_repo(repo_info):
    if repo_info["commit_count"] > 100:
        print(repo_info["repo_name"])
    return repo_info["commit_count"] > 100 #filtering repositories with number of commits greater than 100

def get_result(filtered_repo_info):
	global INDEX
	INDEX = INDEX + 1
	return str(INDEX) + ";" + str(filtered_repo_info["repo_name"]) + ";" + str(filtered_repo_info["commit_count"]) + ";" + str(filtered_repo_info["commit_url"])+ ";" + str(filtered_repo_info["forks_count"])+ ";" + str(filtered_repo_info["stargazers_count"])

def get_single_year_data(base_query, year, start_month, day, end_month, sort, order, github):
	query = base_query
	query += ' created:"' + str(year) + '-' + start_month + '-' + day + ' .. ' + str(year) + '-' + end_month + '-' + day + '"'
	print (query)
	query_results = filter(filter_private_repos, github.search_repositories(query, sort, order)) # returns Repository sorted by stars in desc order
	return map(get_repo_info, query_results)


def run():
    #github = login('Summer-Libra',token='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')
    github = login('Summer-Libra',token='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')
    repo_infos = get_single_year_data(BASE_QUERY, YEAR, START_MONTH, DAY, END_MONTH, SORT, ORDER, github)
    filtered_repo_infos = filter(get_filtered_repo, repo_infos)
    filtered_repo_system = filter(filter_android_repos, filtered_repo_infos)

	# repository_path = repository_path = 'repositories' + '_' + YEAR + '_' + START_MONTH + '_' + END_MONTH + '_' LANGUAGE + '.txt'
    with open(repository_path, 'w') as output_file:
	    output_file.write('\n'.join(map(get_result, filtered_repo_system)))
	

run()
