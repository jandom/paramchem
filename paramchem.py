from bs4 import BeautifulSoup
from xml.dom import minidom
import mechanize
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username")
parser.add_argument("-p", "--password")
parser.add_argument("-c", "--conf")
args = parser.parse_args()

# initialize the browser
br = mechanize.Browser()
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Firefox.')]
br.set_handle_redirect(mechanize.HTTPRedirectHandler)

# login fill-in form and submit
url = "https://cgenff.paramchem.org/userAccount/userLogin.php"
response = br.open(url)
br.form = list(br.forms())[0] 
usrName = br.form.find_control("usrName")
curPwd = br.form.find_control("curPwd")
usrName.value = args.username
curPwd.value = args.password
response = br.submit()
#print response.read() 

# upload the file to parametrize, parse xml output
filename = args.conf
br.form = list(br.forms())[0] 
br.form.add_file(open(filename), 'text/plain', filename)
response = br.submit()
xml = response.read().strip()
print xml
dom = minidom.parseString(xml)
path = dom.getElementsByTagName('path')[0]
inputf = dom.getElementsByTagName('mol2')[0]
outputf = dom.getElementsByTagName('output')[0]

# save input
url = "https://cgenff.paramchem.org/initguess/filedownload.php?file={}/{}".format(path.firstChild.data, inputf.firstChild.data )
print url
response = br.open(url)
topology = response.read()
open(inputf.firstChild.data , "w").writelines(topology)

# save output
url = "https://cgenff.paramchem.org/initguess/filedownload.php?file={}/{}".format(path.firstChild.data, outputf.firstChild.data )
print url
response = br.open(url)
topology = response.read()
open(outputf.firstChild.data , "w").writelines(topology)
