from django.db import models
from accounts.models import User
from commons.models import SoftDeleteModel
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class ProductCategoryItem(SoftDeleteModel):
    def __str__(self):
        return f"{self.pk}, {self.name}"

    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    name = models.CharField('이름', max_length=50)


class Product(SoftDeleteModel):
    class Meta:
        ordering = ('-id',)
        verbose_name = '상품'
        verbose_name_plural = '상품들'

    def __str__(self):
        return f"{self.pk}, {self.display_name}"

    cate_item = models.ForeignKey(
        ProductCategoryItem, on_delete=models.DO_NOTHING)

    description = models.TextField('설명')

    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)

    market = models.ForeignKey('markets.Market', on_delete=models.DO_NOTHING)
    manufacturer = models.CharField('제조사', max_length=100)
    name = models.CharField('상품명(내부용)', max_length=100)
    display_name = models.CharField('상품명(노출용)', max_length=100)

    price = models.PositiveIntegerField('판매가')

    hit_count = models.PositiveIntegerField('조회수', default=0)
    review_count = models.PositiveIntegerField('리뷰수', default=0)
    review_point = models.FloatField('리뷰평점', default=0)

    product_picked_users = models.ManyToManyField(User, through='products.ProductPickedUser',
                                                  related_name='picked_products')


class ProductSale(models.Model):
    class VatTypeChoices(models.TextChoices):
        과세 = "과세"
        영세 = "영세"
        면세 = "면세"
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="product_sale")
    not_sale_text = models.CharField(
        '판매불가사유', max_length=100, default="재고가 소진되었습니다.")

    vat_type = models.TextField(
        '과세구분', max_length=20, choices=VatTypeChoices.choices, default=VatTypeChoices.과세)
    vat = models.SmallIntegerField(
        '과세', validators=[MinValueValidator(0), MaxValueValidator(100)], default=10)

    sale_price = models.PositiveIntegerField('실제판매가')
    cash_back = models.PositiveIntegerField('적립금', default=0)

    unit = models.PositiveIntegerField('주문단위', default=1)

    is_adult = models.BooleanField('성인인증여부', default=False)


class ProductDisplay(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="product_display")
    is_main = models.BooleanField('메인표시여부', default=False)
    is_optional = models.BooleanField('옵션전용', default=False)
    # 제품 등록중에는 True, 옵션까지 모두 등록후 True,False선택
    is_hidden = models.BooleanField('숨김여부', default=True)
    is_sold_out = models.BooleanField('품절여부', default=False)


class ProductPickedUser(SoftDeleteModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ProductOptions(models.Model):
    prouct = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="options")
    name = models.CharField("옵션분류", max_length=100, help_text="사이즈-색상")
    unit = models.CharField("옵션단위", max_length=100,
                            help_text="mm-color")


class ProductOptionDetail(models.Model):
    option = models.ForeignKey(
        ProductOptions, on_delete=models.CASCADE, related_name="details")
    name = models.CharField("옵션명(내부용)", max_length=100,
                            help_text="250-red")
    display_name = models.CharField(
        "옵션명(외부용)", max_length=100, help_text="255-빨간색")
    quantity = models.IntegerField("옵션재고")
    extra = models.CharField("추가금", max_length=1000)


"""
프로덕트
    ## 필수옵션
    ㄴ 프로덕트 옵션(OneToOne(프로덕트)),
        #옵션디테일 (ForeignKey(옵션))
        ㄴ 옵션1-1
        ㄴ 옵션1-2
        ㄴ 옵션1-3
        ㄴ 옵션2-1
        ㄴ 옵션2-2
        ㄴ 옵션2-3
        ㄴ 옵션3-1
        ㄴ 옵션3-2
        
옵션 등록페이지 1

옵션리스트1 name=사이즈,unit=mm,pre_fix=False
            [등록이름][표시이름]
    ㄴ 옵션1 = 250 , 250
    ㄴ 옵션2 = 260 , 260
    ㄴ 옵션3 = 270 , 270
옵션리스트2 name=색깔,unit="",pre_fix=False
    ㄴ 옵션1 = 레드 , 빨간색
    ㄴ 옵션2 = 블루 , 푸른색
    ㄴ 옵션3 = 그린 , 초록색
옵션리스트3 name=재질,unit="",pre_fix=False
    ㄴ 옵션1 = 무광 , 무광
    ㄴ 옵션2 = 유광 , 유광

백엔드 api

class OptionDetailForm(Schema):
    name : str
    display_name : str
    
class OptionForm(Schema):
    name : str
    unit : str = ""
    prefix : bool = False
    option_details : List(OptionsDetailForm)

class OptionMakeForm(Schema):
    product_id : int
    option_list : List(OptionForm)

def make_options(request,form:OptionMakeForm):
    return custom(form)#부록

ex)
const response = {
    option:{
        name:"사이즈-색상-재질-종류-신발끈",
        unit:"mm-null-null-null-null"
    },
    options:[
        {name : "280-black-무광-단화-black"},
        {name : "280-black-무광-단화-red"},
        {name : "280-black-무광-단화-white"},
        {name : "280-black-무광-메리제인-black"},
        {name : "280-black-무광-메리제인-red"},
        {name : "280-black-무광-메리제인-white"},
        {name : "280-black-무광-장화-black"},
        {name : "280-black-무광-장화-red"},
        {name : "280-black-무광-장화-white"},
        {name : "280-black-유광-단화-black"},
        {name : "280-black-유광-단화-red"},
        {name : "280-black-유광-단화-white"},
        {name : "280-black-유광-메리제인-black"},
        {name : "280-black-유광-메리제인-red"},
        {name : "280-black-유광-메리제인-white"},
        {name : "280-black-유광-장화-black"},
        {name : "280-black-유광-장화-red"},
        {name : "280-black-유광-장화-white"},
        {name : "280-black-스웨이드-단화-black"},
        {name : "280-black-스웨이드-단화-red"},
        {name : "280-black-스웨이드-단화-white"},
        {name : "280-black-스웨이드-메리제인-black"},
        {name : "280-black-스웨이드-메리제인-red"},
        {name : "280-black-스웨이드-메리제인-white"},
        {name : "280-black-스웨이드-장화-black"},
        {name : "280-black-스웨이드-장화-red"},
        {name : "280-black-스웨이드-장화-white"},
        {name : "280-gray-무광-단화-black"},
        {name : "280-gray-무광-단화-red"},
        {name : "280-gray-무광-단화-white"},
        {name : "280-gray-무광-메리제인-black"},
        {name : "280-gray-무광-메리제인-red"},
        {name : "280-gray-무광-메리제인-white"},
        {name : "280-gray-무광-장화-black"},
        {name : "280-gray-무광-장화-red"},
        {name : "280-gray-무광-장화-white"},
        {name : "280-gray-유광-단화-black"},
        {name : "280-gray-유광-단화-red"},
        {name : "280-gray-유광-단화-white"},
        {name : "280-gray-유광-메리제인-black"},
        {name : "280-gray-유광-메리제인-red"},
        {name : "280-gray-유광-메리제인-white"},
        {name : "280-gray-유광-장화-black"},
        {name : "280-gray-유광-장화-red"},
        {name : "280-gray-유광-장화-white"},
        {name : "280-gray-스웨이드-단화-black"},
        {name : "280-gray-스웨이드-단화-red"},
        {name : "280-gray-스웨이드-단화-white"},
        {name : "280-gray-스웨이드-메리제인-black"},
        {name : "280-gray-스웨이드-메리제인-red"},
        {name : "280-gray-스웨이드-메리제인-white"},
        {name : "280-gray-스웨이드-장화-black"},
        {name : "280-gray-스웨이드-장화-red"},
        {name : "280-gray-스웨이드-장화-white"},
    ]
}
const optionSize =  response.length
const optionName = response.option.name.split("-")
const optionUnit = response.option.unit.split("-")
let optionsMenu = {}
for (let i in optionName){
    optionsMenu[i] = {
        name : optionName[i],
        unit : optionUnit[i],
        details : response.options.map(
            res=>res.name.split("-")[i]
        ).reduce(
            (ac,v)=>ac.includes(v)? ac:[...ac,v],[]
        )
    }    
}
console.log(optionsMenu)
=>[
    {
        name:"size",
        unit:"mm",
        details:["280"],
    },
    {
        name:"color",
        unit:null,
        details:["black","gray"],
    },
    {
        name:"재질",
        unit:null,
        details:["무광","유광","스웨이드"],
    }
]
optionsMenu.map(
    res=>{
        return (
            <div>
                dawdawdwdaawd
            </div>
        )
    }
)

version: "3.7"
services:
  extension:
    healthcheck:
      test: ["CMD","curl","-f", "http://172.17.0.1:3002",]
      interval: 1s
      retries: 30
      start_period: 60s
    build: .
    container_name: ${CONTAINER_NAME}
    user: root
    entrypoint: sh command.sh
    volumes:
      - ./.next:/usr/src/app/.next
      - ./components:/usr/src/app/components
      - ./pages:/usr/src/app/pages
      - ./pulic:/usr/src/app/pulic
      - ./src:/usr/src/app/src
      - ./next.onfig.js:/usr/src/app/next.config.js
      - ./package.json:/usr/src/app/package.json
      - ./command.sh:/usr/src/app/command.sh
      - ./tsconfig.json:/usr/src/app/tsconfig.json
    ports:
      - 3002:3000
    restart: unless-stopped
    # cpus: .10
    # mem_limit: "512M"



FROM node:16
WORKDIR /usr/src/app
COPY ./package.json ./package.json
# COPY ./nginx.conf ./etc/nginx/nginx.conf
# RUN apt-get update -y && apt-get install nginx -y 
# RUN service nginx restart
RUN npm install
EXPOSE 3000
# CMD npm start


npm run dev

CONTAINER_NAME=shoppingmall

# See https://help.github.com/ignore-files/ for more about ignoring files.

# dependencies
/node_modules

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local
/out
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Next.js
/.next

/node_modules

"""
