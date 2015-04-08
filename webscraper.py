import time
import random
import urllib2
import pandas as pd
from bs4 import BeautifulSoup
import os

loc = r"/home/david/Downloads/companylist-3.csv"

import pandas as pd

data_file = pd.read_csv(loc)
Lista = data_file["Symbol"]

paths = link


file_loc = r"/home/david/Documents/stocks_list9.csv"

def craw():
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    x = 0
    y = time.time()
    df = pd.DataFrame(columns = ["Stock",
                                  "Next EPS Date",
                                  "EPS Growth Rate",
                                  "Average EPS % Beat Rate",
                                  "Revenue Growth Rate",
                                  "Average % Move 1-Wk after EPS",
                             "Date",
                             "Qtr",
                             "EPS",
                             "Cons",
                             "Surprise",
                             "Revs",
                             "Cons2"])
    for link in Lista:
        try:
            x += 1

            if x % 50 == 0:
                T = time.time() - y
                print x, link, T

            path = paths + str(link)

            while True:
                try:
                    req = urllib2.Request(path, None, headers)
                    html = urllib2.urlopen(req, timeout = 3.5).read()
                    break
                except Exception as e:
                    print e, link, "...retrying..."
                    time.sleep(random.uniform(1.2,3.6))
                    pass

            newpage = BeautifulSoup(html)

            content = newpage.find("table", {"class":"info-table"})
            content_table = newpage.find("table", {"class": "earning_history"})
            if content and content_table:
                try:
                    L1 = [i.text for i in content.find_all("td") if i.text != "After Close"]
                    L4 = [[i.text for i in j.find_all("td") if i.text != "" and i.text != "Details" ] for j in content_table.find_all("tr")]
                    if len(L4)> 0:
                        del L4[0]
                        if len(L4) == 0 and any(i != "N/A" for i in L1):
                            df = df.append({"Stock": link,
                                            "Next EPS Date": L1[0],
                                            "EPS Growth Rate": L1[1],
                                            "Average EPS % Beat Rate": L1[2],
                                            "Revenue Growth Rate": L1[3],
                                            "Average % Move 1-Wk after EPS": L1[4],
                                            "Date": "N/A",
                                            "Qtr": "N/A",
                                            "EPS": "N/A",
                                            "Cons": "N/A",
                                            "Surprise": "N/A",
                                            "Revs": "N/A",
                                            "Cons2": "N/A"}, ignore_index = True)
                        else:
                            for i in range(len(L4)):
                                df = df.append({"Stock": link,
                                                "Next EPS Date": L1[0],
                                                "EPS Growth Rate": L1[1],
                                                "Average EPS % Beat Rate": L1[2],
                                                "Revenue Growth Rate": L1[3],
                                                "Average % Move 1-Wk after EPS": L1[4],
                                                "Date": L4[i][0],
                                                "Qtr": L4[i][1],
                                                "EPS": L4[i][2],
                                                "Cons": L4[i][3],
                                                "Surprise": L4[i][4],
                                                "Revs": L4[i][5],
                                                "Cons2": L4[i][6]}, ignore_index = True)
                except Exception as e:
                    print "1", e, link
                    pass

            time.sleep(random.uniform(1.1,3.2))
        except Exception as e:
            print "2", e, link
            pass
    df.to_csv(file_loc)
    #return df

craw()

path = r"/home/david/Documents/Odesk/csv"
output = r"/home/david/Documents/Odesk/output.csv"

def merge():
    csv_file = [x for x in os.listdir(path)]
    frame = pd.DataFrame()
    list = []
    for file in csv_file:
        df = pd.read_csv(os.path.join(path,file),index_col=None, header=0)
        list.append(df)
    frame = pd.concat(list, ignore_index=True)
    frame.to_csv(output, index=False)

merge()