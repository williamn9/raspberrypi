import schedule
import bs4 as bs
import urllib.request
import time
import datetime

from time import sleep
from datetime import date
from sense_hat import SenseHat
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

sense = SenseHat()
stock_code=[]
old_stock_code=[]
trade_date=[]
matrix=[]
show=False
today_new=0



#today=datetime.datetime(2020, 12, 8)
today=date.today()
tomorrow=today + datetime.timedelta(days=1)



# Define some colours
g = (0, 55, 0) # Green
b = (0, 0, 0) # Black
o = (100,55,0)
r = (100,0,0)
u = (0, 0, 100) #blue
w = (100,100,100)

def refresh_list():


    global today_new
    
    old_stock_code=stock_code.copy()
    stock_code.clear()
    trade_date.clear()
    source = urllib.request.urlopen('http://www.aastocks.com/tc/stocks/market/ipo/upcomingipo/company-summary').read()
    #source = urllib.request.urlopen('file:///home/pi/Desktop/data.html').read()
    soup = bs.BeautifulSoup(source,'lxml')
    results=soup.find(id='tblUpcoming')
    ipos= results.find_all('tr')
    
    for ipo in ipos:
        children=ipo.findChildren("td", recursive=False)
        if children[1].text != "代號▼":
            if children[1].text not in old_stock_code:
                today_new=today_new+1
                #sense.show_message("New IPO added! New IPO added! New IPO added!", scroll_speed=0.05, text_colour=w)
            stock_code.append(children[1].text)
            trade_date.append(children[8].text)

                


def construct_matrix():

    #today=datetime.datetime(2020, 12, 8)
    today=date.today()
    tomorrow=today + datetime.timedelta(days=1)
    matrix.clear()   
    ipo_total=len(stock_code)
    mark_new=today_new
    
    
    for x in range(ipo_total):

        trade_date_obj=datetime.datetime.strptime(trade_date[x],'%Y/%m/%d').date()


        
        if mark_new+x==ipo_total:
            matrix.append(g)
            mark_new=mark_new-1
        
        elif trade_date_obj==today:
            matrix.append(o)
            
        elif trade_date_obj==tomorrow:
            matrix.append(r)
            
        else:
            matrix.append(u)
    
    #fill in the rest of the matrix
    remainder=64-len(stock_code)
    for x in range(remainder):
        matrix.append(b)
    
        
def job():
    refresh_list()
    construct_matrix()
    #sense.show_message("Refreshing", scroll_speed=0.05, text_colour=w)
    sense.clear()
    sense.set_pixels(matrix)

def next_day():
    global today_new
    today_new=0
    sense.show_message("Next Day", scroll_speed=0.05, text_colour=w)


schedule.every().hour.do(job)
#schedule.every(5).seconds.do(job)
schedule.every().day.at("00:01").do(next_day)
#schedule.every(30).seconds.do(next_day)

job()
today_new=0
job()

while True:
#    for event in sense.stick.get_events():

#        if event.action == "pressed":
#            if event.direction == "middle":
#                show= not show
#                if show:
#                    sense.set_pixels(matrix)
#                else:
#                    sense.clear()


    schedule.run_pending()
    time.sleep(1)
    












