from BeautifulSoup import BeautifulSoup
import urllib2
import re
file = open("links.txt","w")
html_page = urllib2.urlopen("https://db.chgk.info/random/types123/1157999819/limit25")
soup = BeautifulSoup(html_page)
for link in soup.findAll('a', attrs={'href': re.compile("^/tour/")}):
    file.write("https://db.chgk.info%s"%link.get('href'))
    file.write("\n")

file.close()
