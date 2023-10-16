import io
import json
import os
import urllib.request
import re
import zipfile


class Downloader:

    def __init__(self, app):
        self.app = app
        self.headers = {
            "User-Agent":
                r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) " +
                "Gecko/20100101 Firefox/96.0"
        }

    def update_list(self):
        self.app.log("Enter to function update_list()")
        direct_link = self.cm_get_direct_link(self.app.LIST_URL, self.app.LIST_FILE)
        self.app.log(f"{direct_link}")
        resp = urllib.request.urlopen(
            urllib.request.Request(direct_link, headers=self.headers)).read()
        self.app.log(f"Unzip list.zip")
        z = zipfile.ZipFile(io.BytesIO(resp))
        z.extractall("data")
        z.close()

    def download_book(self, book):
        self.app.log("Enter to function download_book()")
        direct_link = self.cm_get_direct_link(self.app.UPDATE_URL + book, book)
        resp = urllib.request.urlopen(
            urllib.request.Request(direct_link, headers=self.headers)).read()
        z = zipfile.ZipFile(io.BytesIO(resp))
        output_dir = "data/" + book[:-4]
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        z.extractall(output_dir)
        z.close()

    def cm_get_info(self, url):
        resp = urllib.request.urlopen(
            urllib.request.Request(url, headers=self.headers)).read().decode("UTF-8")
        return resp

    def cm_get_direct_link(self, url, file_zip):
        data = self.cm_get_info(url)
        result1 = re.findall(r'weblink_get.+?"url":"(https:.+?)"',
                             data, flags=re.UNICODE)
        print(result1)
        result2 = re.findall(r'weblink":"(.+?' + file_zip.replace(".", r"\.") + r')"',
                             data, flags=re.UNICODE)
        print(result2)
        return "/".join([result1[0], result2[0]])
