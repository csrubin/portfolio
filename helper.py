import toml


def get_text_from_file(file_path: str, as_list: bool = False) -> str:
    with open(file_path, 'r') as pyf:
        if as_list:
            text_list = pyf.readlines()
            text = ', '.join([i.strip() for i in text_list])
        else:
            text = pyf.read()
    return text


def get_experience(file_path: str) -> list[dict]:
    with open(file_path, 'r') as tomlfile:
        data = toml.load(tomlfile)

    data_list = []
    for _, exp in data.items():
        data_list.append(exp)

    sorted_list = sorted(data_list, key=lambda d: d['end'], reverse=True)
    return sorted_list

