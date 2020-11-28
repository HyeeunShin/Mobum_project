from typing import List, Any
from urllib.request import urlopen
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

class Url:

    def __init__(self):
        self.mobum = ('http://openapi.sb.go.kr:8088/584d49536d61733232364570647146/xml/SbModelRestaurantDesignate/1/')
        self.cancel = ('http://openapi.sb.go.kr:8088/716f776d576173323738506a6e6c62/xml/SbModelRestaurantCancel/1/')
        self.name_lst = []
        self.address_lst = []
        self.ifm_lst = []
        self.mb_nm_lst = []
        self.mb_addr_lst = []
        self.mbTel_lst = []
        self.cc_nm_lst = []
        self.cc_addr_lst = []
        self.ccWhy_lst = []

    def get_link(self, how):

        if how == 'mobum':
            url = self.mobum
            last = 200
        else:
            url = self.cancel
            last = 311

        store_url = url + str(last) + '/'  # url 자료 개수 지정
        store_html = urlopen(store_url)
        html = BeautifulSoup(store_html, 'html.parser')     # 깔끔한 url

        self.storeName = html.find_all('upso_nm')
        self.address = html.find_all('site_addr_rd')
        if url == self.mobum:
            self.ifm = html.find_all('upso_site_telno')
        else:
            self.ifm = html.find_all('asgn_cancel_why')
            self.tp = 1

        for i in range(0, last - 1):
            self.name_lst.append(self.storeName[i].text)
            self.address_lst.append(self.address[i].text)
            self.ifm_lst.append(self.ifm[i].text)


        return self.name_lst, self.ifm_lst, self.address_lst

    def get_data(self, name):
        self.mb_nm_lst, self.mbTel_lst , self.mb_addr_lst= self.get_link('mobum')

        if name in self.mb_nm_lst:
            idx = self.mb_nm_lst.index(name)
            mbData = ['모범음식점 업소', 'Tel : ' + self.mbTel_lst[idx], self.mb_addr_lst[idx]]

        else:
            return self.get_cancel_data(name)
        return mbData

    def get_cancel_data(self, name):
        self.cc_nm_lst, self.ccWhy_lst, self.cc_addr_lst= self.get_link('cancel')
        if name in self.cc_nm_lst:
            idx = self.cc_nm_lst.index(name)
            ccData = ['모범음식점 취소 업소', '사유 : ' + self.ccWhy_lst[idx], self.cc_addr_lst[idx]]
        else:
            return False
        return ccData


if __name__ == '__main__':
    u = Url()
    b = u.get_data('낙지사랑')
    a = u.get_data('갈비둥지 어해랑')
    print(b)
    print(a)
