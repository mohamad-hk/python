import requests
import re
from bs4 import BeautifulSoup
from sklearn import tree
import mysql.connector

data = []
x = []
y = []
price = []
output = []
name = []
color = []
release_date = []
# connect to database
cnx = mysql.connector.connect(user='root', password='mhk11379',
                              host='127.0.0.1',
                              database='learn')
cursor = cnx.cursor()
# web scraping
fixed = 'https://bama.ir/car/all-brands/all-models/all-trims?hasprice=true&page=1'
for p in range(1, 20):
    fixed1 = fixed.replace(fixed[-1], p.__str__())
    print(fixed1)
    print('Extracting')
    r = requests.get(fixed1)
    soup = BeautifulSoup(r.text, 'html.parser')
    # tag price
    res1 = soup.find_all('span', attrs={'itemprop': 'price'})
    # tag nae
    res2 = soup.find_all('p', attrs={'class': 'price hidden-xs'})
    # tag output
    res3 = soup.find_all('h2', attrs={'class': 'persianOrder'})
    # tag color
    res4 = soup.find_all('span', attrs={'id': 'ex-color', 'class': 'visible-xs'})
    # tag release_date
    res5 = soup.find_all('span', attrs={'class': 'year-label visible-xs', 'itemprop': 'releaseDate'})

    for i in range(0, len(res2)):

        textfi2 = re.sub(r'\s+', ' ', res5[i].text)

        textfi1 = re.sub(r'\s+', ' ', res4[i].text)

        textfi = re.sub(r'\s+', ' ', res3[i].text)

        text = re.sub(r'\s+', ' ', res2[i].text)

        opt2 = re.sub(r'کارکرد+', ' ', text)

        opt = re.sub(r'\s+', ' ', res1[i].text)
        opt1 = opt.replace('در توضیحات', 'y')

        if opt1.split()[0] != 'y':
            opt11 = opt1.replace(',', '')
            opt22 = opt2.replace(',', '')
            opt33 = opt22.replace('صفر', '0')

            price.append(int(opt11.strip()))

            output.append(int(opt33.strip()))

            name.append(textfi)

            color.append(textfi1)

            release_date.append(textfi2)

# paste in database
for k in range(0, len(price)):
    cursor.execute("INSERT INTO bama7 (price, output,name,color,release_date) VALUES(%s,%s,%s,%s,%s)",
                   (price[k], output[k], name[k], color[k], release_date[k]))
    cnx.commit()
# cursor.execute("delete from bama4")

print('Enter price')

in1 = int(input())

print('Enter output')

in2 = int(input())

cursor.execute("select*from bama7")

myresult = cursor.fetchall()
# alghorithm machine learning
for data in myresult:
    x.append(data[0:2])
    y.append(data[2])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

new_data = [[in1, in2]]
answer = clf.predict(new_data)

print(answer[0])
