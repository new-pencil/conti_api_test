import yaml


def handle_yaml_file(file_path):
    """
    读取yaml文件
    :param file_path: 文件路径
    :return: 全部文件数据
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data
