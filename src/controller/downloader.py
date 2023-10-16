import io
import os
import requests
import re
import zipfile


class Downloader:

    def __init__(self, app):
        self.app = app
        self.headers = {
            "User-Agent":
                r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) " +
                "Gecko/20100101 Firefox/96.0",
            "Content-type": "application/x-www-form-urlencoded"
        }

    def update_list(self):
        self.app.log("Enter to function update_list()")
        direct_link = self.cm_get_direct_link(self.app.LIST_URL, self.app.LIST_FILE)
        self.app.log(f"{direct_link}")
        resp = requests.get(direct_link, verify=False, headers=self.headers)
        self.app.log(f"Unzip list.zip")
        z = zipfile.ZipFile(io.BytesIO(resp.content))
        z.extractall("data")
        z.close()

    def download_book(self, book):
        self.app.log("Enter to function download_book()")
        direct_link = self.cm_get_direct_link(self.app.UPDATE_URL + book, book)
        resp = requests.get(direct_link, verify=False, headers=self.headers)
        z = zipfile.ZipFile(io.BytesIO(resp.content))
        output_dir = "data/" + book[:-4]
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        z.extractall(output_dir)
        z.close()

    def cm_get_direct_link(self, url, file_zip):
        self.app.log("Enter to function cm_get_direct_link()")
        data = requests.get(url, verify=False, headers=self.headers).text
        self.app.log("Regex data")
        result1 = re.findall(r'weblink_get.+?"url":"(https:.+?)"',
                             data, flags=re.UNICODE)
        print(result1)
        result2 = re.findall(r'weblink":"(.+?' + file_zip.replace(".", r"\.") + r')"',
                             data, flags=re.UNICODE)
        print(result2)
        return "/".join([result1[0], result2[0]])
