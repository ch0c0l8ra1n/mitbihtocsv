from multiprocessing.pool import ThreadPool as Pool
import wget
from urllib.error import *

def download(rec):
    URL = "https://physionet.org/physiobank/database/mitdb/{}"
    exts = ["dat","atr","hea"]
    for ext in exts:
        fileName = "{}.{}".format(rec,ext)
        while True:
            try:
                wget.download(URL.format(fileName),out="data")
                break
            except URLError as e:
                pass
        print("Downloaded {}".format(fileName))

recs = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219, 220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

pool = Pool(10)
pool.map(download,recs)
pool.close()
