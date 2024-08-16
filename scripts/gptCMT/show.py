import re
import textwrap
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def parse_taxonomy(file_path):
    # 打开文件并逐行读取内容
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    # 创建一个嵌套的字典数据结构来存储解析后的分类信息
    taxonomy = defaultdict(lambda: defaultdict(lambda: {'title': '', 'items': []}))

    current_section = None
    current_subsection = None

    # 遍历文件中的每一行，解析分类信息并存储到taxonomy中
    for line in lines:
        section_match = re.match(r'^### (\d+)\. (.+)$', line)
        subsection_match = re.match(r'^#### (\d+\.\d+) (.+)$', line)
        leaf_match = re.match(r'^- \*\*(.+?)\*\*.*$', line)

        # 当匹配到节信息时，更新当前节的信息，并重置当前子节
        if section_match:
            current_section = section_match.group(1)
            section_title = section_match.group(2)
            taxonomy[current_section]['title'] = section_title
            current_subsection = None  # 当遇到新的节时，重置当前子节为None
        # 当匹配到子节信息时，更新当前子节的信息
        elif subsection_match:
            current_subsection = subsection_match.group(1)
            subsection_title = subsection_match.group(2)
            taxonomy[current_section][current_subsection]['title'] = subsection_title
        # 当匹配到叶子节点信息时，根据当前是否存在子节来存储到相应的位置
        elif leaf_match:
            leaf_title = leaf_match.group(1)
            if current_subsection:
                taxonomy[current_section][current_subsection]['items'].append(leaf_title)
            else:
                if not isinstance(taxonomy[current_section]['items'], list):
                    taxonomy[current_section]['items'] = []
                taxonomy[current_section]['items'].append(leaf_title)

    return taxonomy


def merge_taxonomy(taxonomy1, taxonomy2):
    # 定义一个合并两个分类系统的函数
    # 创建一个默认字典作为存储合并结果的数据结构
    merged_taxonomy = defaultdict(lambda: defaultdict(lambda: {'title': '', 'items': []}))
    # 遍历第一个分类系统的内容
    for section, content in taxonomy1.items():
        for subsection, details in content.items():
            # 检查子节是否存在并且其值是字典类型
            if subsection != 'title' and isinstance(details, dict):
                # 更新合并结果字典的值
                if section not in merged_taxonomy:
                    merged_taxonomy[section]['title'] = content['title']
                if subsection not in merged_taxonomy[section]:
                    merged_taxonomy[section][subsection]['title'] = details['title']
                merged_taxonomy[section][subsection]['items'] = list(
                    set(merged_taxonomy[section][subsection]['items'] + details['items']))
    # 复制第二个分类系统，防止修改原始数据
    temp_taxonomy2 = {k: v.copy() for k, v in taxonomy2.items()}
    # 遍历第二个分类系统的内容
    for section, content in temp_taxonomy2.items():
        for subsection, details in content.items():
            # 检查子节是否存在并且其值是字典类型
            if subsection != 'title' and isinstance(details, dict):
                # 如果节和子节在合并字典中已存在，则更新对应的项列表
                if section in merged_taxonomy and subsection in merged_taxonomy[section]:
                    merged_taxonomy[section][subsection]['items'] = list(
                        set(merged_taxonomy[section][subsection]['items'] + details['items']))
                # 如果节或子节在合并字典中不存在，则添加新的项到合并字典中
                else:
                    if section not in merged_taxonomy:
                        merged_taxonomy[section]['title'] = content['title']
                    if subsection not in merged_taxonomy[section]:
                        merged_taxonomy[section][subsection]['title'] = details['title']
                    merged_taxonomy[section][subsection]['items'] = details['items']

    return merged_taxonomy  # 返回合并后的分类系统结果


def print_taxonomy(taxonomy):
    # 打印分类信息
    for section, content in taxonomy.items():  # 遍历分类字典
        print(f"{section} {content['title']}")  # 打印分类标题
        if content['items'] and isinstance(content['items'], list) and len(content['items']) > 0:  # 判断是否存在条目
            for item in content['items']:  # 遍历条目列表
                print(f"    - {item}")  # 打印条目
        for subsection, details in content.items():  # 遍历分类内容
            if subsection != 'title' and subsection != 'items' and isinstance(details, dict):  # 排除标题和条目
                print(f"  {subsection} {details['title']}")  # 打印子分类标题
                for item in details['items']:  # 遍历子分类的条目列表
                    print(f"    - {item}")  # 打印子分类条目


def trans_taxonomy(taxonomy):
    tax_str = ''
    for section, content in taxonomy.items():
        # print(f"{section} {content['title']}")
        tax_str += f"### {section}. {content['title']}\n"
        if content['items'] and isinstance(content['items'], list) and len(content['items']) > 0:
            for item in content['items']:
                # print(f"    - {item}")
                tax_str += f"- **{item}\n"
        for subsection, details in content.items():
            if subsection != 'title' and subsection != 'items' and isinstance(details, dict):
                # print(f"  {subsection} {details['title']} {type(details)}")
                tax_str += f"#### {subsection} {details['title']}\n"
                for item in details['items']:
                    # print(f"    - {item}")
                    tax_str += f"- **{item}**\n"
    return tax_str


def generate_subsection_color_dict(aux_taxonomy):
    color_dict = {}
    # 使用科研学术论文常用的配色方案
    color_palette = plt.get_cmap('tab10')  # 'tab10' is a good qualitative colormap for plots

    color_index = 0
    unique_subsections = list(set(aux_taxonomy.values()))
    for subsection in unique_subsections:
        # 使用模运算符来确保color_index不会超出color_palette的大小
        color_dict[subsection] = color_palette(color_index % 10)  # 'tab10' has 10 unique colors
        color_index += 1
    # print(color_dict)
    return color_dict


def generate_subsection_superscript_dict(properties):
    superscript_dict = {}
    subsection_sizes = {}

    # Calculate the size of each subsection
    for section, content in properties.items():
        for subsection, details in content.items():
            if subsection not in ['title', 'items'] and isinstance(details, dict):
                subsection_sizes[subsection] = len(details['items'])

    # Sort subsections by size in ascending order
    sorted_subsections = sorted(subsection_sizes, key=lambda k: (int(k.split('.')[0]), int(k.split('.')[1])))

    # Assign superscript index based on sorted subsection sizes
    superscript_index = 1
    for subsection in sorted_subsections:
        superscript_dict[subsection] = superscript_index
        superscript_index += 1

    return superscript_dict


def get_subsection_mapping(taxonomy):
    subsection_mapping = {}
    for section, content in taxonomy.items():
        for subsection, details in content.items():
            # print(subsection, details)
            if subsection != 'title' and subsection != 'items' and isinstance(details, dict):
                for item in details['items']:
                    subsection_mapping[item] = subsection
            if subsection == 'items' and isinstance(details, list):
                for item in details:
                    subsection_mapping[item] = section
    return subsection_mapping


def get_subsection_title_mapping(taxonomy):
    subsection_title_mapping = {}
    for section, content in taxonomy.items():
        for subsection, details in content.items():
            # print(subsection, details)
            if subsection != 'title' and subsection != 'items' and isinstance(details, dict):
                subsection_title_mapping[subsection] = details['title']
            if subsection == 'title':
                subsection_title_mapping[section] = details

    return subsection_title_mapping


# 定义一个函数用于绘制分类图
def plot_taxonomies(main_taxonomy, aux_taxonomy, properties, filename, log=16, width=40):
    # 创建一个图形和坐标轴来展示分类图
    fig, ax = plt.subplots(figsize=(log, width))
    ax.axis('off')

    y = 0  # 设置初始y坐标值
    spacing = 1  # 设置文本之间的垂直间距
    wrap_width = 120  # 设置每行文本的字符数限制

    # 生成从item到它所在的aux_taxonomy二级标题的映射
    aux_subsection_mapping = get_subsection_mapping(aux_taxonomy)
    property_subsection_mapping = get_subsection_mapping(properties)

    # 生成辅助分类的颜色字典
    colors = generate_subsection_color_dict(aux_subsection_mapping)
    # 生成属性上标的字典
    superscripts = generate_subsection_superscript_dict(properties)

    # 获取排序后的辅助分类及其颜色
    sorted_subsections = sorted(list(set(aux_subsection_mapping.values())))
    sorted_colors = {subsection: colors[subsection] for subsection in sorted_subsections}

    # 在图中添加辅助分类的颜色图例
    legend_x = 8
    legend_y = 0
    legend_spacing = 1

    # 在颜色图例上面添加“Taxonomy2”的标注
    ax.text(legend_x + 0.5, legend_y + 1, "Subcategories of Taxonomy2", fontsize=8)

    aux_titles = get_subsection_title_mapping(aux_taxonomy)
    for subsection, color in sorted_colors.items():
        # 获取辅助分类的标题并在图例中绘制颜色块和标题
        subsection_title = aux_titles.get(subsection, '')
        ax.add_patch(patches.Rectangle((legend_x, legend_y), 0.2, 0.2, color=color))
        ax.text(legend_x + 0.25, legend_y, f"{subsection} {subsection_title}", fontsize=8, verticalalignment='center')
        legend_y -= legend_spacing

    # 在图中添加属性上标的图例
    superscript_legend_x = 8
    superscript_legend_y = legend_y - 2
    superscript_legend_spacing = 1

    # 在图例上面添加“Taxonomy3”的标注
    ax.text(superscript_legend_x + 0.5, superscript_legend_y + 1, "Subcategories of Taxonomy3", fontsize=8)

    property_titles = get_subsection_title_mapping(properties)
    for subsection, superscript in superscripts.items():
        # 获取属性的标题并在图例中绘制上标和标题
        subsection_title = property_titles.get(subsection, '')
        ax.text(superscript_legend_x, superscript_legend_y, f"$^{superscript}$: {subsection} {subsection_title}",
                fontsize=8, verticalalignment='center')
        superscript_legend_y -= superscript_legend_spacing

    # 绘制主要内容
    for section, content in main_taxonomy.items():
        section_title = textwrap.fill(f"{section} {content['title']}", wrap_width)
        ax.text(0, y, section_title, fontsize=12, weight='bold')
        y -= spacing
        if content['items'] and isinstance(content['items'], list) and len(content['items']) > 0:
            for item in content['items']:
                wrapped_item = textwrap.fill(f"- {item}", wrap_width)
                color = colors.get(aux_subsection_mapping.get(item, None), 'black')
                superscript = superscripts.get(property_subsection_mapping.get(item, None), '')
                if superscript:
                    ax.text(2, y, wrapped_item + f"$^{superscript}$", fontsize=8, color=color)
                else:
                    ax.text(2, y, wrapped_item, fontsize=8, color=color)
                y -= spacing
        for subsection, details in content.items():
            if subsection != 'title' and subsection != 'items' and isinstance(details, dict):
                subsection_title = textwrap.fill(f"{subsection} {details['title']}", wrap_width)
                ax.text(1, y, subsection_title, fontsize=10, weight='bold')
                y -= spacing
                for item in details['items']:
                    wrapped_item = textwrap.fill(f"- {item}", wrap_width)
                    color = colors.get(aux_subsection_mapping.get(item, None), 'black')
                    superscript = superscripts.get(property_subsection_mapping.get(item, None), '')
                    if superscript:
                        ax.text(2, y, wrapped_item + f"$^{superscript}$", fontsize=8, color=color)
                    else:
                        ax.text(2, y, wrapped_item, fontsize=8, color=color)
                    y -= spacing

    # 设置图形的x和y坐标范围
    plt.xlim(0, 10)
    plt.ylim(y - 1, 1)
    plt.savefig(filename)  # 保存图形
    plt.show()  # 显示图形


def plot_taxonomy(taxonomy, filename):
    # 定义一个函数用来绘制层级分类图，根据给定的taxonomy字典和文件名filename
    fig, ax = plt.subplots(figsize=(16, 8))  # 创建一个图形和轴对象
    ax.axis('off')  # 关闭坐标轴显示

    y = 0  # 初始化y坐标
    spacing = 1  # 设置行间距为1

    for section, content in taxonomy.items():  # 遍历分类字典
        ax.text(0, y, f"{section} {content['title']}", fontsize=12, weight='bold')  # 在指定位置添加文本
        y -= spacing  # 更新y坐标，用于下一个部分的位置调整
        if content['items'] and isinstance(content['items'], list) and len(content['items']) > 0:  # 检查是否存在子项
            for item in content['items']:  # 遍历子项
                ax.text(2, y, f"- {item}", fontsize=8)  # 在指定位置添加子项文本
                y -= spacing  # 更新y坐标，用于下一个子项的位置调整
        for subsection, details in content.items():  # 遍历子分类和详情
            if subsection != 'title' and subsection != 'items' and isinstance(details, dict):  # 检查是否为有效的子分类
                ax.text(1, y, f"{subsection} {details['title']}", fontsize=10, weight='bold')  # 在指定位置添加子分类标题
                y -= spacing  # 更新y坐标，用于子分类的位置调整
                for item in details['items']:  # 遍历子分类的子项
                    ax.text(2, y, f"- {item}", fontsize=8)  # 在指定位置添加子项文本
                    y -= spacing  # 更新y坐标，用于下一个子项的位置调整

    plt.xlim(0, 10)  # 设置x轴范围
    plt.ylim(y - 1, 1)  # 设置y轴范围
    plt.savefig(filename)  # 在指定路径保存图形
    plt.show()  # 显示图形
    

if __name__ == '__main__':
    my_taxonomy0 = parse_taxonomy('base/append-0-op.txt')
    my_taxonomy1 = parse_taxonomy('base/append-1-op.txt')
    my_taxonomy2 = parse_taxonomy('base/append-2-op.txt')
    # get_subsection_mapping(my_taxonomy1)
    # print_taxonomy(my_taxonomy0)
    # print_taxonomy(my_taxonomy1)
    # print_taxonomy(my_taxonomy2)
    plot_taxonomy(my_taxonomy1, 'base_taxonomy_1.jpg')
    plot_taxonomy(my_taxonomy2, 'base_taxonomy_2.jpg')
    plot_taxonomies(my_taxonomy0, my_taxonomy1, my_taxonomy2, 'base_final_taxonomy.jpg', log=16, width=8)

    # my_taxonomy00 = parse_taxonomy('java/data9_11/4/add/append-0-op.txt')
    # my_taxonomy11 = parse_taxonomy('java/data9_11/4/add/append-1-op.txt')
    # my_taxonomy22 = parse_taxonomy('java/data9_11/4/add/append-2-op.txt')
    # print_taxonomy(my_taxonomy00)
    # print_taxonomy(my_taxonomy11)
    # print_taxonomy(my_taxonomy22)
    # plot_taxonomy(my_taxonomy11, 'taxonomy_11.jpg')
    # plot_taxonomy(my_taxonomy22, 'taxonomy_22.jpg')
    # plot_taxonomies(my_taxonomy00, my_taxonomy11, my_taxonomy22, 'final_taxonomy.jpg')
    #

