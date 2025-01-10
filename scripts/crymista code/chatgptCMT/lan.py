misuse_key = {'ch': ['摘要', '文件', '详细描述'], 'en': ['abstract', 'files', 'detail']}

wrong_format_warning = {'ch': '检测到gpt没有按指定格式输出，或其判断这批代码的没有密码误用情况。',
                        'en': 'It is detected that GPT does not output in the specified format, or it judges that '
                              'there is no cryptography API misuse in this batch of codes.'}

rejudge_warning = {'ch': '需要给新的prompt，让gpt重新判断。', 'en': 'You need to give a new prompt and let GPT rejudge.'}

missing_warning = {'ch': '检测到gpt漏报了这些代码：', 'en': 'It is detected that GPT missed these codes: '}
stop = {'ch': '。', 'en': '.'}

rejudge_warning2 = {'ch': '这些代码将记录下来，需要新增prompt，让gpt重新判断。',
                    'en': 'These codes will be record and you need to give a '
                          'new prompt and then let GPT '
                          'rejudge.'}

except_warning = {'ch': '第', 'en': 'Round'}
except_warning2 = {'ch': '轮结束，判断失败的代码有：', 'en': 'end, the codes for failed judgment are: '}

resubmit_warning = {'ch': '重新提交失败代码，消除因输出格式错误导致的分类失败。',
                    'en': 'Resubmit failed codes to eliminate identification '
                          'caused by incorrect output '
                          'format.'}

success_hint = {'ch': 'Nice！所有代码均识别完毕。', 'en': 'Nice! All codes have been identified.'}

fail_warning = {'ch': '消除格式错误问题，仍判断失败的代码有：',
                'en': 'To eliminate the format error problem, the codes that still fail '
                      'are: '}

exit_hint = {'ch': '任意键继续或按"q"退出：', 'en': 'Press any key to continue or "q" to exit:'}

exit_warning = {'ch': '你选择了按"q"退出，请查看日志以手动解决具体问题。',
                'en': 'You have pressed "q" to exit. Please check the logs to manually resolve the specific issue.'}

json_error = {'ch': '处理这批代码时抛出json解析异常，已跳过，你最终可能需要手动解决该问题。',
              'en': 'A json parsing exception was thrown while processing this batch of code, which has been skipped. '
                    'You may end up needing to solve the problem manually.'}
