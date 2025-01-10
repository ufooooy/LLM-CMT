import ast

# 示例代码
code = """

import os
from cryptoadvance.specter.managers.otp_manager import OtpManager
import time


def test_OtpManager(empty_data_folder):
    # A OtpManager manages Otp, one-time-passwords
    # via json-files in an empty data folder
    otpm = OtpManager(data_folder=empty_data_folder)
    assert os.path.isfile(os.path.join(empty_data_folder, "otps.json"))
    # initialization will load from the folder but it's empty at first
    assert otpm.data == {}  # but you shouldn't access data directly anyway
    # an otp looks like this:
    an_otp = {
        "otp": "aOxO42IeM-aRB4WjBIAQRA",
        "created_at": 1618491877.546648,
        "expiry": 1617495477.546648,
    }
    otpm.add_new_user_otp(an_otp)
    yet_another_otp = {
        "otp": "nPfouONJmUgS642MitqPkg",
        "created_at": time.time(),
        "expiry": time.time() + 60 * 60,  # plus 1 h
    }
    assert otpm.validate_new_user_otp(an_otp["otp"]) == False
    otpm.add_new_user_otp(yet_another_otp)
    assert otpm.validate_new_user_otp(an_otp["otp"]) == False
    assert otpm.validate_new_user_otp(yet_another_otp["otp"]) == True
    otpm.remove_new_user_otp(an_otp["otp"])
    # If it doesn't exist, False as well
    assert otpm.validate_new_user_otp(an_otp["otp"]) == False
    # anything gets you False
    assert otpm.validate_new_user_otp("anything") == False

"""

# 解析代码
parsed_code = ast.parse(code)
# 提取定义的字典
defined_dicts = [node for node in ast.walk(parsed_code) if isinstance(node, ast.Dict)]
# 检查字典是否是otp格式
otp_dict = []
for dict_node in defined_dicts:
    # for key in dict_node.keys:
        # print(key.value, type(key))
    if all(key.value in ["otp", "created_at", "expiry"] for key in dict_node.keys):
        otp_dict.append(dict_node)

# 修改过期时间检查逻辑
overdue_dict = []
for dict_node in otp_dict:
    for key, value in zip(dict_node.keys, dict_node.values):
        if key.value == "expiry":
            # 这里我们检查value类型，决定如何获取其数值
            if isinstance(value, ast.Constant):  # 对应直接的值
                expiry_value = value.value
            elif isinstance(value, ast.BinOp):  # 对应表达式
                # 这里我们只是简单地提示，具体的处理会根据您的需要而定
                print("Expiry value is a calculated expression, not a direct value.")
                continue  # 如果您不处理表达式，则可能想要跳过这个节点

            # 执行时间比较，确认是否过期（这里应有代码处理expiry_value，但因为上方continue，此处可能不会执行）
            print(f"Expiry value: {expiry_value}, Type: {type(expiry_value)}")
            # 根据实际逻辑处理过期情况，例如添加至overdue_dict等
            overdue_dict.append(dict_node)


# 获得otp_dict中的每个字典的变量名
variable_names = []
for dict_node in overdue_dict:
    for parent in ast.walk(parsed_code):
        if isinstance(parent, ast.Assign) and isinstance(parent.value, ast.Dict) and dict_node == parent.value:
            for target in parent.targets:
                if isinstance(target, ast.Name):
                    variable_names.append(target.id)
                    break
            break
print(variable_names)
# 检查variable_names是否在otpm.add_new_user_otp中被使用
# for node in ast.walk(parsed_code):
#     if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_new_user_otp":
#         for arg in node.args:
#             if isinstance(arg, ast.Name) and arg.id in variable_names:
#                 print(f"Variable {arg.id} is used in otpm.add_new_user_otp.")

# 记录使用了 variable_names 的调用
used_variable_names_in_calls = []  # 记录所有调用中使用的variable_names

for node in ast.walk(parsed_code):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_new_user_otp":
        for arg in node.args:
            if isinstance(arg, ast.Name):
                used_variable_names_in_calls.append(arg.id)
print(used_variable_names_in_calls)

# 检查最后一次调用是否使用不合法的 variable_names
if used_variable_names_in_calls:
    last_used_variable = used_variable_names_in_calls[-1]  # 获取最后一个使用的变量名
    if last_used_variable in variable_names:
        print(f"Last call to otpm.add_new_user_otp uses an expired OTP variable: {last_used_variable}")
    else:
        print("Last call to otpm.add_new_user_otp does not use an expired OTP variable.")
else:
    print("There are no calls to otpm.add_new_user_otp with variable names from variable_names.")