# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 20:05:27 2019

@author: Emirhan
"""
import csv
import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time, socks, socket
from stem import Signal
from stem.control import Controller

url='Enter Your URL'
ua = UserAgent()


intab = "şüöİğıçŞÜĞÇÖ"
outtab = "suoIgicSUGCO"
trantab = str.maketrans(intab, outtab)
prov=[]


with Controller.from_port(port = 9051) as controller:
        
    controller.authenticate(password = 'Enter Your Tor Password which you decided while installing')
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket  
    for prov in provinces:
        controller.signal(Signal.NEWNYM)
        if controller.is_newnym_available() == False:
            print("Waitting time for Tor to change IP: "+ str(controller.get_newnym_wait()) +" seconds")
            time.sleep(controller.get_newnym_wait())
            #time.sleep(30)

        url_sub=url+prov #If you have sub url to iterate
        req=None
        while req is  None:
            try:
                table = None
                while table is None:
                    try:

                        controller.signal(Signal.NEWNYM)
                        if controller.is_newnym_available() == False:
                            print("Waitting time for Tor to change IP: "+ str(controller.get_newnym_wait()) +" seconds")
                            time.sleep(controller.get_newnym_wait())
                            #time.sleep(30)

                        req = Request(url_sub)
                        req.add_header('User-Agent', ua.random)
                        req_doc= urlopen(req)#.read().decode('utf8')
                        
                        print(req_doc)
                        soup =BeautifulSoup(req_doc,'html.parser')
                        table=soup.find('table',attrs={'id':'searchResultsTable'})

                        if(str(table)=='None'):
                            print(table)
                            break
                        for counter,tr in enumerate(table.find_all('tr')):
                           if tr.find('a')!=None:
                                link=tr.find('a').get('href')
                                if link[:5]=='/ilan':
                                    url_data=url+link
                                    fiyat=tr.find('td',attrs={'class':'searchResultsPriceValue'}).find('div').text
                                    location=tr.find('td',attrs={'class':'searchResultsLocationValue'}).text
                                    emlak_id=link[-15:-6]
                                    
                                    print(counter,' ',link)
                                    controlbit=0
                                    while controlbit==0:
                                        try:
                                            controller.signal(Signal.NEWNYM)
                                            if controller.is_newnym_available() == False:
                                                print("Waitting time for Tor to change IP: "+ str(controller.get_newnym_wait()) +" seconds")
                                                time.sleep(controller.get_newnym_wait())
                                                #time.sleep(30)

                                            req_data = Request(url_data)
                                            req_data.add_header('User-Agent', ua.random)
                                            req_data_open= urlopen(req_data)
                                            print(req_data)
                                            data_soup =BeautifulSoup(req_data_open,'html.parser')
                                            classified_info=data_soup.find('div',attrs={'class':'classifiedInfo'})
                                            info_ul=classified_info.find('ul',attrs={'class':'classifiedInfoList'})
                                            
                                            controlbit=1
                                            for counter,li in enumerate(info_ul.find_all('li')):
                                                key=str(li.find('strong').text.lower().replace(" ", "_").replace("\t", "").replace("\n", "").replace("²", "2").replace("(", "_").replace(")", "").replace("__", "_").replace("________", "").replace("\xa0", "").replace('\u0307', ""))
                                                key=key.translate(trantab)
                            
                                                value=li.find('span').text.lower().replace("\t", "").replace("\n", "").replace(" ", "").replace("(", "_").replace(")", "").replace("__", "_").replace("\xa0", "").replace('\u0307', "").replace(' TL', "").replace('.', "")
                                                value=value.translate(trantab)
                                                
                                                if ('record_no'== key):
                                                    record_no=value
                                                elif('record_date'==key):
                                                    record_date=value
                                                elif('record_type'==key):
                                                    record_type=value

                                            with open('index_final.csv', 'a', newline='') as csv_file:
                                                writer=csv.writer(csv_file)
                                                writer.writerow([record_no,record_date,record_type])
                                                
                                        except urllib.error.HTTPError as e:
                                            print('0')
                                            controlbit=0
                                            pass
                    except urllib.error.HTTPError as e:
                        print('1')
                        print(e)
                        pass
                    except Exception as e:
                        print('table exception',e)
                        break
            except Exception as e:
                print('2')
                print(e)
                pass
        #time.sleep(30)
            
controller.close()

