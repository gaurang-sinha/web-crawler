import requests
from bs4 import BeautifulSoup
import xmltodict,json,asyncio
import lxml
import time
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Gori@1234",
  database="BrainlyCrawler"
)

mycursor = mydb.cursor()

async def main():
    try:
        res= requests.get('https://brainly.com/sitemap_task_0.xml') 
        data=xmltodict.parse(res.text)
        total_urls=len(data['urlset']['url'])
        for i in range(total_urls):
            try:
                print(i)
                url = data['urlset']['url'][i]['loc']
                await asyncio.wait([saveQues(url)])
            except Exception as e:
                print('error in parsing'+e)
                continue
    except Exception as e:
        print(e)


async def saveQues(url):
    c=requests.get(url)
    soup=BeautifulSoup(c.text,'lxml')
    question_string = soup.select('.sg-text--regular')
    await asyncio.sleep(0.01)
    sql = "INSERT INTO Questions (url, question) VALUES (%s, %s)"
    val = (url, question_string[0].text)
    mycursor.execute(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "record inserted.")
    
 
loop=asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
    



