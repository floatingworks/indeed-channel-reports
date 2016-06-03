import pycurl, re, time, urllib, csv, getpass

from StringIO import StringIO
from bs4 import BeautifulSoup

# config vars
email = raw_input('username: ')
password = getpass.getpass('password: ')

# login to get cookie
c = pycurl.Curl()
c.setopt(c.URL, 'https://secure.indeed.com/account/login')
c.setopt(pycurl.POSTFIELDS, 'email=' + email + '&password=' + password)
c.setopt(pycurl.COOKIEJAR, 'indeedcookie.txt')
c.perform()
c.close()

buffer = StringIO()

# use cookie from indeedcookie.txt
d = pycurl.Curl()
d.setopt(d.URL, 'https://ads.indeed.com/jobroll/traffic')
d.setopt(pycurl.COOKIEFILE, 'indeedcookie.txt')
d.setopt(d.WRITEDATA, buffer)
d.perform()
d.close()
  
body = buffer.getvalue()

soup = BeautifulSoup(body)
# channel values
dropdown = soup.find(id='channel_selector')
channels = dropdown.findAll('option')
#month values
month_dropdown = soup.find(id='month')
months = month_dropdown.findAll('option')
# year values
year_dropdown = soup.find(id='year')
years = year_dropdown.findAll('option')
results = {}

for channel in channels:
  params = {'channel': channel['value'],'month': 'December','year': '2014'}
  buffer = StringIO()

  # a new request method to iterate over all the channels called e
  e = pycurl.Curl()
  e.setopt(d.URL, 'https://ads.indeed.com/jobroll/traffic' + '?' + urllib.urlencode(params))
  e.setopt(pycurl.COOKIEFILE, 'indeedcookie.txt')
  e.setopt(d.WRITEDATA, buffer)
  e.perform()
  e.close()

  channelbody = buffer.getvalue()
  channelsoup = BeautifulSoup(channelbody)

  td = channelsoup.find("td", {"class": "total"})
# if there is data then return it
  if td is not None:
 
    children = td.parent.findChildren()

    # we need the 6th element after the .total class

    for child in children:
      if child == children[5]:
        total = child.text
  else:
    total = ''

  results[channel['value']] = total

#write the data to file. 2 columns, feed name, then total
with open('indeedreport.csv', 'w') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerows(results.items())
