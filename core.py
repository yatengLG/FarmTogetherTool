import gzip
import re
from collections import namedtuple

Span = namedtuple('Span', ['start', 'end'])


class FarmTogetherCore:
    def __init__(self, farm_data_file):
        self.farm_data_file = farm_data_file

        self.Money = {
            'Coins': '金币', 'Bills': '钻石', 'Medals': '奖章', 'Tickets': '红票'
        }
        self.Resources = {
            'Resource_2': '蔬菜',    'Resource_1': '水果',    'Resource_5': '小麦',    'Resource_3': '葡萄',
            'Resource_14': '蘑菇',   'Resource_6': '肉类',    'Resource_7': '乳类',    'Resource_8': '蛋类',
            'Resource_9': '鱼类',    'Resource_11': '毛线',   'Resource_4': '花朵',    'Resource_16': '香料',
            'Resource_10': '蜂蜜',   'Resource_13': '果酱',   'Resource_12': '乳酪',   'Resource_15': '金块',
        }
        with open(self.farm_data_file, 'rb') as f:
            self.data = gzip.decompress(f.read())

    def get_farm_level(self):
        result = {}
        pattern = b'Experience:[^}]*}'
        experience = re.search(pattern, self.data)
        if experience is not None:
            level = re.search(b'Level:[0-9]*', experience.group())
            if level is not None:
                result['Level'] = int(experience.group()[level.start() + len('Level:'):level.end()])
        return result

    def get_farm_level_span(self):
        pattern = b'Experience:[^}]*}'
        experience = re.search(pattern, self.data)
        if experience is not None:
            level = re.search(b'Level:[0-9]*', experience.group())
            if level is not None:
                span = Span(level.start() + experience.start() + len('Level:'), level.end() + experience.start())
                return span
        return None

    def set_farm_level(self, leval_value: dict):
        for key, value in leval_value.items():
            if key == 'Level':
                try:
                    span = self.get_farm_level_span()
                    if span is not None:
                        self.data = self.data[:span.start] + str(value).encode('utf-8') + self.data[span.end:]
                except Exception as e:
                    print(e)
        return True

    def get_money(self, money_keys: list[str] = None):
        result = {}
        if money_keys is not None:
            keys = [t for t in money_keys if t in self.Money]
        else:
            keys = [t for t in self.Money.keys()]
        for key in keys:
            pattern = bytes(key.encode('utf-8')) + b':[0-9]*'
            money = re.search(pattern, self.data)
            if money is not None:
                result[key] = int(money.group()[len(key)+1:])
        return result

    def get_money_span(self, money_key:str):
        pattern = bytes(money_key.encode('utf-8')) + b':[0-9]*'
        money = re.search(pattern, self.data)
        if money is not None:
            return Span(money.start()+len(money_key)+1, money.end())
        else:
            return None

    def set_money(self, money_value: dict):
        for k, v in money_value.items():
            if k in self.Money:
                try:
                    span = self.get_money_span(k)
                    if span is not None:
                        self.data = self.data[:span.start] + str(v).encode('utf-8') + self.data[span.end:]
                except Exception as e:
                    print(e)
        return True

    def get_resource(self, resource_keys: list[str] = None):
        result = {}
        if resource_keys is not None:
            keys = [k for k in resource_keys if k in self.Resources]
        else:
            keys = [k for k in self.Resources.keys()]
        for key in keys:
            index = key.split('_')[-1]
            pattern = bytes('Resource:{},'.format(index).encode('utf-8')) + b'[^}]*'
            resource_info = re.search(pattern, self.data)
            if resource_info is None:
                return result
            amount = re.search(b'Amount:[0-9]*', resource_info.group())
            amount = amount.group()[len('amount:'):] if amount is not None else 0
            max = re.search(b'Max:[0-9]*', resource_info.group())
            max = max.group()[len('Max:'):] if max is not None else 0
            result['Resource_{}'.format(index)] = {'Amount': int(amount), 'Max': int(max), 'Cn': self.Resources[key]}
        return result

    def get_resource_amount_span(self, resource_key: str):
        index = resource_key.split('_')[-1]
        pattern = bytes('Resource:{},'.format(index).encode('utf-8')) + b'[^}]*'
        resource_info = re.search(pattern, self.data)
        if resource_info is None:
            return None
        amount = re.search(b'Amount:[0-9]*', resource_info.group())
        if amount is not None:
            return Span(resource_info.start() + amount.start() + len('Amount:'), resource_info.start() + amount.end())
        else:
            return None

    def get_resource_max_span(self, resource_key: str):
        index = resource_key.split('_')[-1]
        pattern = bytes('Resource:{},'.format(index).encode('utf-8')) + b'[^}]*'
        resource_info = re.search(pattern, self.data)
        if resource_info is None:
            return None
        max = re.search(b'Max:[0-9]*', resource_info.group())
        if max is not None:
            return Span(resource_info.start() + max.start() + len('Max:'), resource_info.start() + max.end())
        else:
            return None

    def set_resource_amount(self, resource_key_amount:dict):
        for k, v in resource_key_amount.items():
            if k in self.Resources:
                try:
                    span = self.get_resource_amount_span(k)
                    if span is not None:
                        self.data = self.data[:span.start] + str(v).encode('utf-8') + self.data[span.end:]
                except Exception as e:
                    print(e)
        return True

    def set_resource_max(self, resource_max: dict):
        for k, v in resource_max.items():
            if k in self.Resources:
                try:
                    span = self.get_resource_max_span(k)
                    if span is not None:
                        self.data = self.data[:span.start] + str(v).encode('utf-8') + self.data[span.end:]
                except Exception as e:
                    print(e)
        return True

    def save(self, save_file: str = None):
        if save_file is None:
            save_file = self.farm_data_file
        try:
            with open(save_file, 'wb') as f:
                f.write(gzip.compress(self.data))
        except Exception as e:
            print(e)
        return True


if __name__ == '__main__':
    tool = FarmTogetherCore('farm_0.data')
    print(tool.data[:5000])
    print(tool.get_farm_level())
    print(tool.get_money())
    print(tool.get_resource())
    tool.set_farm_level({'Level': 200})
    tool.set_money({'Coins': 100, 'Bills': 200, 'Medals': 300, 'Tickets': 400})
    tool.set_resource_amount({'Resource_1': 1000, 'Resource_2':2000, 'Resource_3':3000})
    tool.set_resource_max({'Resource_1': 100000, 'Resource_2':200000, 'Resource_3':300000})

    tool.save('farm_1.data')
    tool = FarmTogetherCore('farm_1.data')
    print(tool.data[:5000])
    print(tool.get_farm_level())
    print(tool.get_money())
    print(tool.get_resource())
