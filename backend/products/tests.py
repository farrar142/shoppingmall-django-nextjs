from django.test import TestCase

# Create your tests here.
from pprint import pprint
form = {
    "product_id": 1,
    "option_list": [
        {
            "name": "size",
            "unit": "mm",
            "prefix": False,
            "option_details": [
                {
                    "name": "245",
                    "display_name": "245"
                },
                {
                    "name": "240",
                    "display_name": "240"
                },
                {
                    "name": "250",
                    "display_name": "250"
                },
                {
                    "name": "255",
                    "display_name": "255"
                },
                {
                    "name": "260",
                    "display_name": "260"
                },
                {
                    "name": "265",
                    "display_name": "265"
                },
                {
                    "name": "270",
                    "display_name": "270"
                },
                {
                    "name": "275",
                    "display_name": "275"
                },
                {
                    "name": "280",
                    "display_name": "280"
                },
            ]
        },
        {
            "name": "color",
            "unit": "null",
            "prefix": False,
            "option_details": [
                {
                    "name": "red",
                    "display_name": "빨간색"
                },
                {
                    "name": "blue",
                    "display_name": "푸른색"
                },
                {
                    "name": "green",
                    "display_name": "초록색"
                },
                {
                    "name": "white",
                    "display_name": "하얀색"
                },
                {
                    "name": "black",
                    "display_name": "검은색"
                },
                {
                    "name": "gray",
                    "display_name": "회색"
                },
            ]
        },
        {
            "name": "재질",
            "unit": "null",
            "prefix": False,
            "option_details": [
                {
                    "name": "무광",
                    "display_name": "안반딱여요"
                },
                {
                    "name": "유광",
                    "display_name": "반딱해요"
                },
                {
                    "name": "스웨이드",
                    "display_name": "부드러워요"
                },
            ]
        },
        {
            "name": "종류",
            "unit": "null",
            "prefix": False,
            "option_details": [
                {
                    "name": "단화",
                    "display_name": "짧아요"
                },
                {
                    "name": "메리제인",
                    "display_name": "시원해요"
                },
                {
                    "name": "장화",
                    "display_name": "워커만해요"
                },
            ]
        },
        {
            "name": "신발끈",
            "unit": "pcs",
            "prefix": False,
            "option_details": [
                {
                    "name": "black",
                    "display_name": "검은줄"
                },
                {
                    "name": "red",
                    "display_name": "빨간줄"
                },
                {
                    "name": "white",
                    "display_name": "하얀줄"
                },
            ]
        },
    ]
}


class ProductOption:
    my_options = []

    def __init__(self, product_id, name, unit, prefix):
        self.product_id = product_id
        self.name = name
        self.unit = unit
        self.prefix = prefix

    def __str__(self):
        return self.name + self.unit + self.prefix

    def add_options(self, options):
        self.my_options.append(options)

    def get_options(self):
        for i in self.my_options:
            print(i)
        return self.my_options


class OptionDetail:
    def __init__(self, option, name, dname):
        self.option = option
        self.name = name
        self.dname = dname
        self.option.add_options(self)
        self.quantity = 0

    def __str__(self):
        return "{"+"name : "+'"'+self.name+'"'+",display_name : "+'"'+self.dname+'"},'


callstack = 0


def make_option_details(product_option, options, length=0, options_name: list = [], options_display_name: list = [], start=0, names=[], dnames=[]):
    global callstack
    callstack += 1
    if start >= length:
        # 엔드포인트
        # OptionDetail.objects.create(...)
        OptionDetail(product_option, "-".join(options_name),
                     "-".join(options_display_name))
        return options_name, options_display_name
    res = options[start]['option_details']
    if start <= length:
        for i in res:
            _options_name = [*options_name, i['name']]
            _options_display_name = [*options_display_name, i['display_name']]
            _name, _dname = make_option_details(product_option,
                                                options, length, _options_name, _options_display_name, start+1)
            if _name:
                # 리커시브 제외
                names.append(_name)
                dnames.append(_dname)
    if start == 0:
        # 메인 리턴
        return names, dnames
    # 리커시브 제외
    return None, None


def make_options(form):
    product_id = form["product_id"]
    option_list = form["option_list"]
    _option_names = []
    _option_unit = []
    _option_prefix = []
    for _option in option_list:
        _option_names.append(_option["name"])
        _option_unit.append(_option["unit"])
        _option_prefix.append(_option["prefix"])
    _option_names = f'{product_id}_{"-".join(_option_names)}'
    _option_unit = f'{product_id}_{"-".join(_option_unit)}'
    _option_prefix = f'{product_id}_{"-".join(str(_option_prefix))}'
    product_option = ProductOption(
        product_id, _option_names, _option_unit, _option_prefix)
    opt_len = len(option_list)
    options_name = []
    make_option_details(
        product_option, option_list, opt_len, options_name)
    return product_option.get_options()  # ProductOptions.optionsdetails.all()


print(len(make_options(form)))
print(callstack)
