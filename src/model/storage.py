import io
import os
import requests
import zipfile

from src.model.sync import Sync


class Storage:

    def __init__(self, app):
        self.app = app
        self.storage_books = {}
        self.timeout = 3
        self.verify = False
        self.headers = {
            "User-Agent":
                r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) " +
                "Gecko/20100101 Firefox/96.0",
            "Content-type": "application/x-www-form-urlencoded"
        }

    def list(self):
        self.storage_list()
        for i in os.listdir("data"):
            if os.path.isfile("data/" + i) and (i[-4:] == ".jpg"):
                cover = f"data/{i}"
                self.storage_books[cover] = f"data/{i[:-4]}/"
                self.app.syncs[self.storage_books[cover]] = \
                    Sync(app=self.app, current_path=self.storage_books[cover])

    def storage_list(self):
        self.app.log.debug("Enter to function storage_list()")
        try:
            direct_link = self.app.conf.LIST_URL
            self.app.log.debug(f"Update {direct_link}")
            resp = requests.get(direct_link,
                                timeout=self.timeout,
                                verify=self.verify,
                                headers=self.headers)
            if resp.status_code == 200:
                self.app.log.debug(f"Unzip list.zip")
                z = zipfile.ZipFile(io.BytesIO(resp.content))
                z.extractall("data")
                z.close()
            else:
                raise Exception(f"resp.StatusCode={resp.status_code}")
        except Exception as e:
            self.app.log.debug("ERROR: " + e.__str__())

    def storage_book(self, book):
        self.app.log.debug(f"Enter to function storage_book(book='{book}')")
        try:
            direct_link = self.app.conf.UPDATE_URL + book
            resp = requests.get(direct_link,
                                timeout=self.timeout,
                                verify=self.verify,
                                headers=self.headers)
            if resp.status_code == 200:
                z = zipfile.ZipFile(io.BytesIO(resp.content))
                output_dir = "data/" + book[:-4]
                if not os.path.exists(output_dir):
                    os.mkdir(output_dir)
                z.extractall(output_dir)
                z.close()
            else:
                raise Exception(f"resp.StatusCode={resp.status_code}")
        except Exception as e:
            self.app.log.debug("ERROR: " + e.__str__())
