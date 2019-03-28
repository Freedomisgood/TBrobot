import itchat
from getdiscount import *

if __name__ == '__main__':
	user_id = '*'
	itchat.auto_login(enableCmdQR=2)

	mama = Mama(user_id)

	@itchat.msg_register(itchat.content.TEXT)
	def receiveMSG(msg):
		'''
		如果是发送淘宝链接的，则返回优惠链接
		:param msg: VX发送人发送的信息
		:return: 优惠链接
		'''
		# TODO: 根据发送人的userid暂存商品信息，如果监测到下单则数据库积累金额增加
		if '淘♂寳♀' in msg['Text']:
			keyword = Mama.getKeyWord(msg['Text'])
			# print(keyword)
			quan_id , itemid = mama.searchGoods(keyword)
			if itemid:
				return mama.shareLink(quan_id,itemid)
			else:
				return "返利失败！该商品没有优惠"

	itchat.run()
