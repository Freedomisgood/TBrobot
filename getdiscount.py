import time
import requests
import re



headers = {
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vbXNhcGkubWFpc2hvdW1tLmNvbS9hcGkvdjEvQ29kZUxvZ2luIiwiaWF0IjoxNTUzNjQ4OTEyLCJleHAiOjE1NTQyNDg4NTIsIm5iZiI6MTU1MzY0ODkxMiwianRpIjoibXliTzdxbUlPSWFQWWxzdCIsInN1YiI6NjMxMjU1LCJwcnYiOiJjYjc4YjVlMWZmY2UwZjgzMWQwMjMxZGYyYzhiZDdjODA2NDc3NzYyIn0.l6K82JrPT_Lc8OKU3xkM15SEvxVpwJgjfXhnH5JxaLc',
    'Host': 'msapi.maishoumm.com',
    'User-Agent': 'okhttp/3.3.1',
}

params = (
    ('device_id', 'e583e3b824800858'),
    ('version', '28'),
)


class Mama(object):
	"""获得优惠的账号"""
	def __init__(self, user_id):
		super(Mama, self).__init__()
		self.user_id = user_id
		
	@classmethod
	def getKeyWord(cls,msg):
		'''
		从用户发送的淘口令中获得搜索商品的关键字
		:param msg: 淘口令
		:return: 关键字
		'''
		data = {
		  'keyword':msg
		 }

		response = requests.post('http://msapi.maishoumm.com/api/v1/GetTkl', headers=headers, params=params, data=data)
		html = response.json()
		return html.get('data').get('title')


	def searchGoods(self,keyword):
		'''
		通过关键字直接搜索物品
		:param keyword: 从淘口令中提取的关键字
		:return: 符合条件商品的item
		'''

		data = {
		  'user_id': self.user_id,
		  'page': '1',
		  'sort': 'desc',
		  'type': '1',
		  'keyword': keyword,
		  'hascoupon': '0',
		  'timestamp': str(time.time())[:10],
		  'order': ''
		}

		response = requests.post('http://msapi.maishoumm.com/api/v1/search', 
			headers=headers, params=params, data=data)
		datas = response.json().get('data').get('data')
		'''
		0号为推荐
		{'couponmoney': '20',
		  'fqcat': 8,
		  'give_money': 2.46,		最大的分享佣金
		  'id': 16958510,
		  'itemendprice': '9.90',	用券后价格
		  'itemid': '584952027074',	商品ID
		  'itempic': 'https://img.alicdn.com/imgextra/i4/1804785178/O1CN01hWoZdE1o7ZJiIGdx1_!!1804785178.png_300x300.jpg',
		  'itemprice': '29.90',		商品原价
		  'itemsale': 176725,
		  'itemshorttitle': '三七 中药清火牙膏105g*2支',
		  'itemtitle': '三七 中药清火牙膏105g*2支',
		  'pid': 'mm_32490747_43626016_341908488',
		  'quan_id': '1b84cdf00df9413ebc9d8a2170464cf0',
		  'sellernick': '亮丽洁昕贝专卖店',
		  'share_money': 0,
		  'shoptype': 'B',
		  'tkrates': '30.00',
		  'videoid': '0'},

		  1号为淘口令的准确搜索
		  {'couponmoney': '20',
		  'give_money': 2.46,
		  'itemendprice': 9.9,
		  'itemid': 584952027074,
		  'itempic': 'https://img.alicdn.com/bao/uploaded/i4/1834133585/O1CN010adp7p1cLyO7IpJjm_!!0-item_pic.jpg_300x300.jpg',
		  'itemprice': '29.9',
		  'itemsale': '118372',
		  'itemshorttitle': '2支装共210克云南三七牙膏清爽薄荷修护牙龈美白牙齿清新口气',
		  'itemtitle': '2支装共210克云南三七牙膏清爽薄荷修护牙龈美白牙齿清新口气',
		  'lm': 1,
		  'pid': 'mm_32490747_43626016_341908488',
		  'quan_id': '1b84cdf00df9413ebc9d8a2170464cf0',
		  'qwf': 1,							    是否有券
		  'sellernick': '亮丽洁昕贝专卖店',       商家名称
		  'share_money': 0,
		  'shoptype': 'B',
		  'tkrates': 30},
		'''

		
		correctList = []
		for data in datas:
			'''
			两种匹配方式，完全匹配or包含
			'''
			print("itemtitle:",data.get('itemtitle'))
			reResult = re.match(keyword,data.get('itemtitle'))
			if reResult or keyword in data.get('itemtitle'):
				# exact_search=data
				# break
				correctList.append(data)

		if correctList:
			correctList.sort(key=lambda x: float(x.get('itemendprice')))
			exact_search = correctList[0]
			print(exact_search)
			quan_id = exact_search.get('quan_id')
			itemid = exact_search.get('itemid')
			return quan_id , itemid









	def singleGood(self,quan_id,ID):
		'''
		商品详情页,发现用不到
		:param quan_id:
		:param ID:
		:return:
		'''
		data = {
		  'user_id': self.user_id,
		  'quan_id': quan_id,
		  'id': ID
		}

		response = requests.post('http://msapi.maishoumm.com/api/v1/GoodDetail', headers=headers, params=params, data=data)
		print(response.text)





	def shareLink(self,quan_id,Itemid):
		'''
		商品的分享链接
		:param quan_id: 是否有券,可能为None
		:param Itemid: 商品id
		:return: 商品的分享的url
		'''
		data = {
		  'user_id': self.user_id,
		  'quan_id': quan_id,
		  'Itemid': Itemid
		}
		'''
		{
	    "status_code": 200,
	    "message": "请求成功",
	    "data": {
	        "details": {
	            "title": "2支装共210克云南三七牙膏清爽薄荷修护牙龈美白牙齿清新口气",
	            "extension": "2支装共210克云南三七牙膏清爽薄荷修护牙龈美白牙齿清新口气",
	            "itemid": "584952027074",
	            "shop_type": "B",
	            "banner": [
	                "https://img.alicdn.com/bao/uploaded/i4/1834133585/O1CN010adp7p1cLyO7IpJjm_!!0-item_pic.jpg",
	                "https://img.alicdn.com/i1/1834133585/O1CN01Ke7j3w1cLyNtCrQCS_!!1834133585.jpg",
	                "https://img.alicdn.com/i1/1834133585/O1CN01vDaS0I1cLyNq6cbXy_!!1834133585.jpg",
	                "https://img.alicdn.com/i2/1834133585/O1CN01tL8Ytg1cLyOBrt45U_!!1834133585.jpg"
	            ],
	            "itempic": "https://img.alicdn.com/bao/uploaded/i4/1834133585/O1CN010adp7p1cLyO7IpJjm_!!0-item_pic.jpg",
	            "zk_final_price": "29.9",
	            "reserve_price": "49",
	            "volume": "121307",
	            "coupon_price": "20",
	            "endprice": "9.90",
	            "coupon_start_time": "2019-03-27",
	            "coupon_end_time": "2019-03-29",
	            "quan_id": "1b84cdf00df9413ebc9d8a2170464cf0",
	            "tkrates": "30.00",
	            "yongjin": 2.46,
	            "share_yongjin": 0,
	            "uproletype": 1,
	            "uprolename": "买手",
	            "Ewmurl": "http://t.cn/EJ9kF9J",
	            "Tkl": "($Huz8by2FJAl)",
	            "Coupon_rul": "http://t.cn/EJ9kF9J",
	            "shuoming": "{标题}表示商品标题，必填\n{商品原价}表示在售价格，必填\n{券后价}表示券后价格，必填\n{宣传语}表示商品推荐语，可为空\n{下单链接}表示下单链接",
	            "Temp": "【{标题}】\n【在售价】{商品原价}元\n【优惠券金额】{优惠券价格}元\n【券后价】{券后价}元\n【下单链接】{下单链接}\n---------\n copy此条消息，{淘口令}，打开【手机淘宝】即可查看",
	            "Template": "【2支装共210克云南三七牙膏清爽薄荷修护牙龈美白牙齿清新口气】\n【在售价】29.9元\n【优惠券金额】20元\n【券后价】9.90元\n【下单链接】http://t.cn/EJ9kF9J\n---------\n copy此条消息，($Huz8by2FJAl)，打开【手机淘宝】即可查看"
	        }
	    }
	}
		'''

		response = requests.post('http://msapi.maishoumm.com/api/v1/ShareQuan', headers=headers, params=params, data=data)
		json = response.json()
		Template = json.get('data').get('details').get('Template')
		
		share_yongjin = json.get('data').get('details').get('share_yongjin')
		returnYongjin = str(float(share_yongjin)*0.3)[:4]
		# print(returnYongjin)
		return Template + "\n下单成功可获得红包补贴：" + "%.2f"%returnYongjin + "元"


	def getOrder(self,page=1,keyword=None,status=None):
		'''

		:param page: 默认第一页
		:param keyword: 搜索关键字
		:param status: 是否支付完成
		:return:
		'''

		data = {
		  'month': '3',
		  'year': '2019',
		  'user_id': self.user_id,
		  'typeid': '0',
		  'page': page,
		  'type': '',
		  'keyword': ''
		}



		html = requests.post('http://msapi.maishoumm.com/api/v1/OrderDetail'
			, headers=headers, params=params, data=data)
		print(html.json())
		datas = html.json().get('data').get('data')
		for data in datas:
			if keyword in data.get('title') and data.get('orderzt') == status:
				pass
				# TODO: 实现这里的数据库操作
				# shuju += str(float(share_yongjin)*0.3)[:4]





if __name__ == '__main__':
	mama = Mama('631090')
	# mama = Mama('631255')
	msg = '【2支装共210克云南三七牙膏清爽薄荷修护牙龈美白牙齿清新口气】\
	https://m.tb.cn/h.3z3WWAC 点击链接，再选择浏览器咑閞；\
	或復\xB7制这段描述￥4PAFbyb8iru￥后到👉淘♂寳♀👈'

	keyword = Mama.getKeyWord(msg)
	print(keyword)

	quan_id , itemid =  mama.searchGoods(keyword)
	if quan_id and itemid:
		print(mama.shareLink(quan_id,itemid))
	# mama.getOrder()
