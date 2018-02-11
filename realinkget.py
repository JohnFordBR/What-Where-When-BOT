from BeautifulSoup import BeautifulSoup
import urllib2
import re
f = open('links.txt', "r")
lines = f.readlines()
f.close()
file = open("realinks.txt","w")
for i in range(len(lines)):
    html_page = urllib2.urlopen(lines[i])
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a', attrs={'href': re.compile("^/question/")}):
        file.write("https://db.chgk.info%s"%link.get('href'))
        file.write("\n")
file.close()
