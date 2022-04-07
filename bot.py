from pydoc import doc
from tkinter import N
from turtle import position
from bs4 import BeautifulSoup
import requests
import csv
from urllib.request import Request, urlopen
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans 
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


url = "https://euw.op.gg/summoners/euw/TheDaeye/champions"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(url,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page,features="html.parser")
table = soup.find("table")
name = []
played = []
kda = []
wr = []

for tr in table.find_all('tr') :
    p = 0
    for td in tr.find_all('td') :
        x = td.find("a")
        z = td.find('span')
        y = td.find('div', {"class": "css-f6o7zg e16vpksz1"})
        y2 = td.find('div', {"class": "css-1v4s0wd e16vpksz1"})
        y3 = td.find('div', {"class": "css-19qjrqp e16vpksz1"})
        y4 = td.find('div', {"class": "css-1pmizq3 e16vpksz1"})
        w = td.find('div', {"class": "winratio-graph__text left"})
        l = td.find('div', {"class": "winratio-graph__text right"})
        if y is not None :
            y = y.text
            y = y.replace(":1","")
            kda.append(float(y))
        if y2 is not None :
            y2 = y2.text
            y2 = y2.replace(":1","")
            kda.append(float(y2))
        if y3 is not None :
            y3 = y3.text
            y3 = y3.replace(":1","")
            kda.append(float(y3))
        if y4 is not None :
            y4 = y4.text
            y4 = y4.replace(":1","")
            kda.append(float(y4))
        if z is not None:
            z = z.text
            z = z.replace("%","")
            wr.append(int(z))
        if x is not None :
            x = x.text.strip()
            if x != "":
                name.append(x)
        if w is not None :
            w = w.text
            w = w.replace("W","")
            p += int(w)
        if l is not None :
            l = l.text
            l = l.replace("L","")
            p += int(l)
    played.append(int(p))
played.pop(0)

url = "https://www.leagueofgraphs.com/summoner/euw/TheDaeye"
req = Request(url,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page,features="html.parser")
tier = soup.find(class_ = "leagueTier").text.strip()
stripped = tier.split(' ', 1)[0]
RankTier = []
RankTier.append(stripped)

wrs = []
ratios = []
names = []
rank = []
for i in range(7):
    with open('sample'+str(i)+'.html', 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        for tr in soup.find_all('tr') :
            c = 0
            for td in tr.find_all('td') :
                n = td.find("a")
                p = td.find('span', {"class": "value"})
                r = td.find('span', {"class": "ratio"})
                if n is not None:
                    if c == 1:
                        names.append(n.text.strip())
                        if i == 0:
                            rank.append("Iron")
                        if i == 1:
                            rank.append("Bronze")
                        if i == 2:
                            rank.append("Silver")
                        if i == 3:
                            rank.append("Gold")
                        if i == 4:
                            rank.append("Platinum")
                        if i == 5:
                            rank.append("Diamond")
                        if i == 6:
                            rank.append("Master")
                    else:
                        c += 1
                if p is not None :
                    p = p.text
                    if p[-1] == "%" :
                        p = p.replace("%","")
                        wrs.append(float(p))
                if r is not None :
                    r = r.text
                    ratios.append(float(r))

with open("data_stats.csv", "w" , newline='') as new_file:
    writer = csv.writer(new_file)
    writer.writerow(["Name","Winrate", "KDA", "Rank"])
    for i in range(len(wrs)):
        writer.writerow([names[i],wrs[i],ratios[i],rank[i]])
    

#print(name)
#print(played)
#print(kda)
#print(wr)

with open("data_test.csv", "w" , newline='') as new_file:
    writer = csv.writer(new_file)
    writer.writerow(["Played", "Winrate"])
    for i in range(len(name)):
        writer.writerow([played[i],wr[i]])

data = pd.read_csv("data_test.csv")
Played = data['Played']
Wr = data['Winrate']
kmeans = KMeans(n_clusters=4,init='random',n_init=10, max_iter=100, random_state=0)
kmeans.fit_predict(data)

position = []
if(len(kmeans.labels_)) >= 6 :
    comp = kmeans.labels_[0]
    count = 0
    other = []
    for i in range(6):
        if kmeans.labels_[i] == comp :
            count += 1
        else :
            other.append(kmeans.labels_[i])
    if count != 6 :
        with open("data2.csv", "w" , newline='') as new_file:
            writer = csv.writer(new_file)
            writer.writerow(["Winrate", "KDA"])
            for i in range(len(name)) :
                if played[i] >= 10 and kmeans.labels_[i] == other[0] or kmeans.labels_[i] == comp:
                    position.append(i)
                    writer.writerow([wr[i],kda[i]])
    else :
        with open("data2.csv", "w" , newline='') as new_file:
            writer = csv.writer(new_file)
            writer.writerow(["Winrate", "KDA"])
            for i in range(len(name)) :
                if played[i] >= 10 and kmeans.labels_[i] == comp:
                    position.append(i)
                    writer.writerow([wr[i],kda[i]])

data2 = pd.read_csv("data2.csv")
Win = data2['Winrate']
Kda = data2['KDA']
clust = 3
kmeans2 = KMeans(n_clusters=clust,init='random',n_init=10, max_iter=100, random_state=0)
kmeans2.fit_predict(data2)
#print(kmeans2.cluster_centers_)
#print(kmeans2.labels_)
#plt.title('Champion Winrate')
#plt.xlabel('Winrate')
#plt.ylabel('KDA')
#plt.scatter(Win,Kda, c=kmeans2.labels_, cmap='rainbow')
#plt.scatter(kmeans2.cluster_centers_[:,0] ,kmeans2.cluster_centers_[:,1], color='black')
#plt.tight_layout()
#plt.show()

#print(position)
lab = []
for i in range(clust):
    lab.append(i)

def bubble_sort(arr,lab):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                lab[j], lab[j+1] = lab[j+1], lab[j]
    return arr

bubble_sort(kmeans2.cluster_centers_[:,1],lab)
#print(lab)

Best = []
Worst = []
Worstp = []
Bestp = []
val = 0

for i in range(len(kmeans2.labels_)):
    if kmeans2.labels_[i] == lab[clust-1]:
        val += 1

for i in range(len(kmeans2.labels_)):
    if val < 3 :
        if kmeans2.labels_[i] == lab[clust-1] or kmeans2.labels_[i] == lab[1] :
            p = position[i]
            Bestp.append(p)
            Best.append(kda[p])
    else :
        if kmeans2.labels_[i] == lab[clust-1]:
            p = position[i]
            Bestp.append(p)
            Best.append(kda[p])
    if kmeans2.labels_[i] == lab[0]:
        p = position[i]
        Worstp.append(p)
        Worst.append(kda[p])

bubble_sort(Worst,Worstp)
bubble_sort(Best,Bestp)
Worst.reverse()
Worstp.reverse()
Best.reverse()
Bestp.reverse()
#print(Worstp)
#print(Worst)
#print(Bestp)
#print(Best)

longueur = []
largeur = []
maxi = clust
print("Vos meilleur champions sont : ")
if len(Bestp) < clust :
    clust = len(Bestp)
    maxi = clust

for i in range(clust):
    print(name[Bestp[i]])
    longueur.append(wr[Bestp[i]])
    largeur.append(kda[Bestp[i]])

clust = 3
if len(Worstp) < clust :
    clust = len(Worstp)
maxi += clust
print("Vos pires champions sont : ")
for i in range(clust):
    print(name[Worstp[i]])

df = pd.read_csv('data_stats.csv')
a = df.loc[:,"Winrate"]
b = df.loc[:,"KDA"]
x = list(zip(a, b))
y = df.loc[:,"Rank"]
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
knn = KNeighborsClassifier(n_neighbors = 159)
knn.fit(x_train, y_train)

predict = []
for i in range(len(longueur)):
    prediction = knn.predict([[longueur[i], largeur[i]]])
    predict.append(str(prediction[0]))

def points(list):
    result = 0
    for i in range(len(list)):
        if list[i] == 'Iron':
            result += 0
        if list[i] == 'Bronze':
            result += 400
        if list[i] == 'Silver':
            result += 800
        if list[i] == 'Gold':
            result += 1200
        if list[i] == 'Platinum':
            result += 1600
        if list[i] == 'Diamond':
            result += 2000
        if list[i] == 'Master':
            result += 2400
    return result

def calcul(predict):
    result = points(predict)
    d = result/len(predict)
    ranking = points(RankTier)
    d = (d+ranking)/2
    if d > 2400 :
        d = 'Master'
    elif d > 2000:
        d = 'Diamond'
    elif d > 1600:
        d = 'Platinum'
    elif d > 1200:
        d = 'Gold'
    elif d > 800:
        d = 'Silver'
    elif d > 400:
        d = 'Bronze'
    elif d > -1:
        d = 'Iron'
    return d

print("Votre MMR sur vos meilleur champion à un niveau : " + calcul(predict))

