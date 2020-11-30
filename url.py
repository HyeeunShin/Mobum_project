from typing import List, Any
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas import DataFrame


class Url:

    def __init__(self):
        self.mobum = ('http://openapi.sb.go.kr:8088/584d49536d61733232364570647146/xml/SbModelRestaurantDesignate/1/200')
        self.cancel = ('http://openapi.sb.go.kr:8088/716f776d576173323738506a6e6c62/xml/SbModelRestaurantCancel/1/311')
        self.name_lst = []
        self.address_lst = []
        self.ifm_lst = []
        self.strInfor = {}
        self.label_lst = []

    def get_link(self):
        self.storeType = [self.mobum, self.cancel]
        for tp in self.storeType:
            store_url = tp
            store_html = urlopen(store_url)
            html = BeautifulSoup(store_html, 'html.parser')     # 깔끔한 url

            self.storeName = html.find_all('upso_nm')
            self.address = html.find_all('site_addr_rd')
            if tp == self.mobum:
                self.ifm = html.find_all('upso_site_telno')
                lenNum = 200
                label = '모범음식점'
            else:
                self.ifm = html.find_all('asgn_cancel_why')
                lenNum = 311
                label = '모범음식점 취소업소'


            for i in range(0, lenNum - 1):
                self.name_lst.append(self.storeName[i].text)
                self.ifm_lst.append(self.ifm[i].text)
                self.address_lst.append(self.address[i].text)
                self.label_lst.append(label)

            self.strInfor['모범음식점 여부'] = self.label_lst
            self.strInfor["Name"] = self.name_lst
            self.strInfor["Information"] = self.ifm_lst
            self.strInfor["Address"] = self.address_lst

        df = DataFrame(self.strInfor)
        print(type(df))
        return df

    def get_data(self, name):
        strFrame = self.get_link()
        data_lst = strFrame[strFrame['Name'] == name]

        return data_lst


if __name__ == '__main__':
    u = Url()
    a = u.get_data('갈비둥지 어해랑')
    b = u.get_data('낙지사랑')
    print(a)
    print(b)
    print(type(b))

