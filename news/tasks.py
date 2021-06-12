from time import sleep
from celery import shared_task
import smtplib
from email.message import EmailMessage
from datetime import datetime
from bs4 import BeautifulSoup
import requests

from .models import News_Update
from .models import Prefer

@shared_task

def scraping():
    if len(list(News_Update.objects.all())) <= 0:
        News_Update.objects.create(
                newspaper = "Hindu",
                sports = "sports news",
                technology = "edu news",
                business =  "Bus news",
                entertainment = "entertainment"
            )
        News_Update.objects.create(
                newspaper = "Economic",
                sports = "sports news",
                technology = "edu news",
                business =  "Bus news",
                entertainment = "entertainment"
            )
        News_Update.objects.create(
                newspaper = "Deccan",
                sports = "sports news",
                technology = "edu news",
                business =  "Bus news",
                entertainment = "entertainment"
                
            )
        News_Update.objects.create(
                newspaper = "Times",
                sports = "sports news",
                technology = "edu news",
                business =  "Bus news",
                entertainment = "entertainment"
                
            )
    sleep(2)




def updating():
    #sports
    get_sports= requests.get("https://timesofindia.indiatimes.com/sports")
    contents_sports=BeautifulSoup(get_sports.content,'html.parser')
    sports_class=contents_sports.find_all(class_="w_img")
    titles_sports=[sports_class[i]['title'] for i in range(4)]
    links_sports = ["https://timesofindia.indiatimes.com"+sports_class[i]['href'] for i in range(4)]
    #print(links_sports)
    titles_sports.extend(links_sports)
    sports_S =','.join(map(str, titles_sports))

    #Entertainment
    get_enter= requests.get("https://timesofindia.indiatimes.com/etimes")
    contents_enter=BeautifulSoup(get_enter.content,'html.parser')
    enter_class=contents_enter.find(class_="ent_music_listing")
    enter_a = enter_class.find_all('a')
    titles_enter=[enter_a[i]['title'] for i in range(4)]
    links_enter=["https://timesofindia.indiatimes.com"+enter_a[i]['href'] for i in range(4)]
    #print(links_enter)
    titles_enter.extend(links_enter)
    enter_S =','.join(map(str, titles_enter))

    #Business
    get_bus= requests.get("https://timesofindia.indiatimes.com/business")
    contents_bus=BeautifulSoup(get_bus.content,'html.parser')
    bus_div = contents_bus.find(class_="top-newslist")
    ul_div = bus_div.find(class_="cvs_wdt clearfix")
    li_div = ul_div.find_all('li')
    bus_class=[li_div[i].find(class_='w_tle') for i in range(4)]
    bus_a = [bus_class[i].find('a') for i in range(4)]
    titles_bus=[bus_a[i]['title'] for i in range(4)]
    #print(titles_bus)
    links_bus=["https://timesofindia.indiatimes.com"+bus_a[i]['href'] for i in range(4)]
    #print(links_bus)
    titles_bus.extend(links_bus)
    bus_S =','.join(map(str, titles_bus))

    #Technology
    get_tech= requests.get("https://www.gadgetsnow.com/tech-news?utm_source=toiweb&utm_medium=referral&utm_campaign=toiweb_hptopnav")
    contents_tech=BeautifulSoup(get_tech.content,'html.parser')
    bus_divt = contents_tech.find(class_="tech_list ctn_stories")
    ul_divt = bus_divt.find(class_="cvs_wdt")
    li_divt = ul_divt.find_all('li')
    tech_class=[li_divt[i].find(class_='w_tle') for i in range(4)]
    tech_a = [tech_class[i].find('a') for i in range(4)]
    titles_tech=[tech_a[i]['title'] for i in range(4)]
    #print(titles_tech)
    links_tech=["https://www.gadgetsnow.com"+tech_a[i]['href'] for i in range(4)]
    #print(links_tech)
    titles_tech.extend(links_tech)
    tech_S =','.join(map(str, titles_tech))

    up = {
        'sports' : sports_S,
        'entertainment' : enter_S,
        'business' : bus_S,
        'technology' : tech_S,
    }
    News_Update.objects.filter(newspaper = 'Times').update(**up)
    sleep(2)



def send_mail(subject,to):
    msg=EmailMessage()
    msg['subject'] = subject
    msg['to'] = to 
    msg.add_header('Content-Type','text/html')

    user_obj = Prefer.objects.get(email = to)
    if(user_obj.sports !='none'):
        P_news = News_Update.objects.get(newspaper = user_obj.sports)      
        sports_content =  list(P_news.sports.split(","))
    if(user_obj.entertainment !='none'):
        P_news = News_Update.objects.get(newspaper = user_obj.entertainment)
        entertainment_content = list(P_news.entertainment.split(","))
    if(user_obj.technology !='none'):
        P_news = News_Update.objects.get(newspaper = user_obj.technology)
        technology_content = list(P_news.technology.split(","))
    if(user_obj.business !='none'):
        P_news = News_Update.objects.get(newspaper = user_obj.business)
        business_content = list(P_news.business.split(","))

    body=""""""

    if(user_obj.technology !='none'):      
        body1="""
        <html>
        <head>
        <style>
            h2{
            font-family:'Courier New',monospace;  
            }
            a{
                text-decoration:none;
            }
            ol{
                padding-left:2em; 
            }
            li{
                margin-top:5px;
            }
        </style>
        </head>
        <body>
        <h2>Technology</h2>
        <ol type="1">
        <li><b><a href="""+technology_content[4]+""">"""+technology_content[0]+"""</a></b></li>
        <li><b><a href="""+technology_content[5]+""">"""+technology_content[1]+"""</a></b></li>
        <li><b><a href="""+technology_content[6]+""">"""+technology_content[2]+"""</a></b></li>
        <li><b><a href="""+technology_content[7]+""">"""+technology_content[3]+"""</a></b></li>
        </ol>
        </body>
        </html>
        """
        body = body + body1

    if(user_obj.business !='none'):
        body2="""
        <html>
        <head>
        <style>
            h2{
            font-family:'Courier New',monospace;  
            }
            a{
                text-decoration:none;
            }
            ol{
                padding-left:2em; 
            }
            li{
                margin-top:5px;
            }
        </style>
        </head>
        <body>
        <h2>Business</h2>
        <ol type="1">
        <li><b><a href="""+business_content[4]+""">"""+business_content[0]+"""</a></b></li>
        <li><b><a href="""+business_content[5]+""">"""+business_content[1]+"""</a></b></li>
        <li><b><a href="""+business_content[6]+""">"""+business_content[2]+"""</a></b></li>
        <li><b><a href="""+business_content[7]+""">"""+business_content[3]+"""</a></b></li>
        </ol>
        </body>
        </html>
        """
        body = body + body2

    if(user_obj.entertainment !='none'):
        
        body3="""
        <html>
        <head>
        <style>
            h2{
            font-family:'Courier New',monospace;  
            }
            a{
                text-decoration:none;
            }
            ol{
                padding-left:2em; 
            }
            li{
                margin-top:5px;
            }
        </style>
        </head>
        <body>
        <h2>Entertainment</h2>
        <ol type="1">
        <li><b><a href="""+entertainment_content[4]+""">"""+entertainment_content[0]+"""</a></b></li>
        <li><b><a href="""+entertainment_content[5]+""">"""+entertainment_content[1]+"""</a></b></li>
        <li><b><a href="""+entertainment_content[6]+""">"""+entertainment_content[2]+"""</a></b></li>
        <li><b><a href="""+entertainment_content[7]+""">"""+entertainment_content[3]+"""</a></b></li>
        </ol>
        </body>
        </html>
        """
        body = body + body3


    if(user_obj.sports !='none'):
        body4="""
        <html>
        <head>
        <style>
            h2{
            font-family:'Courier New',monospace;  
            }
            a{
                text-decoration:none;
            }
            ol{
                padding-left:2em; 
            }
            li{
                margin-top:5px;
            }
        </style>
        </head>
        <body>
        <h2>Sports</h2>
        <ol type="1">
        <li><b><a href="""+sports_content[4]+""">"""+sports_content[0]+"""</a></b></li>
        <li><b><a href="""+sports_content[5]+""">"""+sports_content[1]+"""</a></b></li>
        <li><b><a href="""+sports_content[6]+""">"""+sports_content[2]+"""</a></b></li>
        <li><b><a href="""+sports_content[7]+""">"""+sports_content[3]+"""</a></b></li>
        </ol>
        </body>
        </html>
        """
        body = body + body4
    

    msg.set_payload(body.encode("utf-8"))
    
    user="p.manikanta681@gmail.com"
    msg['from'] = user
    password="qcjxrxdejbczxscd"  #password got from google.activity.com
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    print("sent")
    server.quit()
 


scraping()
while True:
    updating()
    sleep(2)
    hr = '15'
    m = '08'
    if  datetime.today().strftime("%H")==hr and  m <= datetime.today().strftime("%M") <= str(int(m)+2):
        for user in Prefer.objects.all():
            if user.msg_type == 'sms':
                pass
            else:
                if user.sent == "nsent":
                    send_mail("TODAY'S NEWS",user.email)
                    p ={
                        'sent' : "sent" 
                    }
                    Prefer.objects.filter(email = user.email).update(**p)
    if  datetime.today().strftime("%H")==hr and  datetime.today().strftime("%M")==str(int(m)+4):
        for user in Prefer.objects.all():
            if user.sent == "sent":
                p ={
                    'sent' : "nsent" 
                }
                Prefer.objects.filter(email = user.email).update(**p)
