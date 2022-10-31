import csv

def parser(path):
    with open(path, "r", encoding="utf8") as f:
        data = list(csv.DictReader(f))
    return data

def converter(data, filename):
    keys = data[0].keys()
    with open(f'{filename}.csv', 'a', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
