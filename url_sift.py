import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re
import sqlite3 as lite
import sys

def store_url(soup,cur):
    for link in soup.find_all('a'):
        link_str = link.__str__()
        root = re.search('http://www.nfldraftscout.com/ratings/dsprofile.php\?pyid?\=\d+', link_str)
        draft_branch = re.search('draftyear\=\d+', link_str)
        pos_branch = re.search('genpos\=\w+', link_str)
        if root and draft_branch and pos_branch:
            url = root.group(0) + "&" + draft_branch.group(0) + "&" + pos_branch.group(0)
            print("Adding url: " + url)
            cur.execute("INSERT INTO URL VALUES('%s')"%url)

def get_url(cur):
    for year in range(0,22):
        urls = []
        for listing in range(65,90):
            page = requests.get("http://www.nfldraftscout.com/searchcollege.php?draftyear=" + str(1999 + year) + "&colabbr=" + chr(listing))
            soup = BeautifulSoup(page.content, 'html.parser')
            store_url(soup,cur)

def attempt_connection():
    try:
        con = lite.connect('user.db')
        return con
    except Error as e:
        print(e)

def create_table(cur):
    cur.execute("CREATE TABLE URL(URL TEXT)")

def main():
    url_list = []
    con = attempt_connection()
    with con:
        cur = con.cursor()
    create_table(cur)
    get_url(cur)
    con.commit()
    con.close()
    return 0;

if __name__ == "__main__":
    main()
