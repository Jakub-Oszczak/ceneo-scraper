import requests
import bs4
from tkinter import *
from selenium import webdriver

DRIVER_PATH = 'ceneo-scraper\chromedriver.exe'
DRIVER = webdriver.Chrome(DRIVER_PATH)

DRIVER.get('https://www.ceneo.pl/Smartfony;szukaj-iphone+11+64gb+czarny')
html = DRIVER.page_source()
print(html)

class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('500x500')
        self.title('Ceneo scraper') 
        self.product_var = StringVar(self)
 
        self.create_widgets()
 
    def make_request(self):
        self.input = self.input_box.get()
        r = requests.get('https://www.ceneo.pl/Smartfony;szukaj-iphone+11+64gb+czarny')
 
    def create_widgets(self):
        self.search_label = Label(self, text = "Search your prodcut:")
        self.search_label.grid(row=0, column=0)
        self.input_box = Entry(self)
        self.input.grid(row=1, column=0)
        self.search_button = Button(self, text='Search', command=self.make_request())
 
if __name__ == '__main__':
    app = App()
    app.mainloop()