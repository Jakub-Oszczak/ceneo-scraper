from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import ImageTk, Image
from urllib.request import urlopen
from io import BytesIO

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

'''
class Popup(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.center_window()
        self.title('Wait') 
        self.style = ttk.Style(self)
        self.style.theme_use('vista')
        self.progress = ttk.Progressbar(self, length=100)
        self.progress.pack()
    
    def center_window(self, width=200, height=75):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (2*height)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def start_progress_bar(self, bool):
        if bool:
            self.progress.start()
        else:
            self.progress.stop()
'''

class App(Tk):
    def __init__(self):
        super().__init__()
        self.first_search = True 
        self.center_window()
        self.title('Ceneo scraper') 
        self.product_var = StringVar(self)
        self.style = ttk.Style(self)
        self.style.theme_use('vista')
        self.create_widgets()

    def get_products(self):
        try:
            driver.get('https://www.ceneo.pl')
            input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'form-head-search-q'))
            )
            input.send_keys(self.input)
            input.submit()
            main = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'category-list-body.js_category-list-body.js_search-results.js_products-list-main'))
            )
            self.products = main.find_elements(By.CLASS_NAME, 'cat-prod-row__body')
        except TimeoutError:
            print('Timed out')
            self.quit()

    def make_request(self):
        self.product_list = []

        self.input = self.input_box.get()
        if self.input == '':
            warning = messagebox.showerror('Empty input', 'Please enter product name')
            return
        
        self.destroy_widgets()
        self.please_wait()

        try:
            driver.get('https://www.ceneo.pl')
            input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'form-head-search-q'))
            )
            input.send_keys(self.input)
            input.submit()
            try:
                main = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'category-list-body.js_category-list-body.js_search-results.js_products-list-main'))
                )
            except TimeoutException:
                warning = messagebox.showerror('Error', 'Product not found')
                self.cancle_wait()
                return

            self.products = main.find_elements(By.CLASS_NAME, 'cat-prod-row__body')
            for product in self.products:
                product_name = product.find_element(By.CSS_SELECTOR, 'span')
                self.product_list.append(product_name.text)
            
            self.cancle_wait()
            self.geometry('250x150')
            self.frame = ttk.LabelFrame(self, text='Choose product:')
            self.frame.place(x=20, y=80)
            self.product_var.set(self.product_list[0])
            self.product_menu = ttk.OptionMenu(self.frame, self.product_var, self.product_list[0], *self.product_list, command=self.show_product)
            self.product_menu.pack()
            self.update_idletasks()
            width1 = self.frame.winfo_x() + self.frame.winfo_width()
            width2 = self.search_button.winfo_x() + self.search_button.winfo_width()
            if (width1) > (width2):
                width = width1
            else:
                width = width2
            self.geometry(f'{width+25}x150')
# DODAJ SKLAOWANIE ZDJ BO CZASEM SĄ OGROMNE
# DODAJ MOŻLIWOŚĆ ZMIANY PRZEDMIOTU PO WYŚWIETLENIU WYBRANEGO PRZEDMIOTU ORAZ WYSZUKANIA NOWEGO PRZEDMIOTU
        except TimeoutError:
            print('Timed out')
            self.quit()

    def please_wait(self):
        self.update_idletasks()
        win_width = self.winfo_width()
        win_height = self.winfo_height()
        padx = (win_width - 150)//2
        pady = (win_height//5)
        self.wait_frame = ttk.LabelFrame(self, width=win_width, height=win_height, padding=(padx, pady))
        self.wait_frame.place(x=0, y=0)
        self.search_button['state'] = DISABLED
        self.progress = ttk.Progressbar(self.wait_frame, length=150, value=75)
        self.progress.pack()
        self.wait_label = Label(self.wait_frame, text='Please wait...')
        self.wait_label.pack()
        self.update_idletasks()
    
    def cancle_wait(self):
        self.search_button['state'] = ACTIVE
        self.wait_frame.destroy()
        self.update_idletasks()

    def create_widgets(self):
        self.search_label = ttk.Label(self, text = "Search your prodcut:")
        self.search_label.place(x=20, y=20)
        self.input_box = ttk.Entry(self)
        self.input_box.place(x=20, y=45)
        self.search_button = ttk.Button(self, text='Search', command=self.make_request)
        self.search_button.place(x=150, y=43)
    
    def find_price(self, product):
        price = product.find_element(By.CLASS_NAME, 'cat-prod-row__price')
        price = price.find_element(By.CLASS_NAME, 'btn-compare-outer')
        try:
            self.title = price.find_element(By.CLASS_NAME, 'js_seoUrl.go-to-product.button.button-primary.js_force-conv.js_clickHash')
        except NoSuchElementException:
            self.title = price.find_element(By.CLASS_NAME, 'js_seoUrl.go-to-shop.button.button-primary.js_force-conv.js_clickHash')
        
        self.title = self.title.text
        if self.title == 'IDŹ DO SKLEPU':
            price_value = product.find_element(By.CLASS_NAME, 'price-format.nowrap')
            price_value = price_value.text
            return price_value
        price = price.click()
        price = driver.find_element(By.CLASS_NAME, 'product-offers__list.js_product-offers')
        price_value = price.find_element(By.CLASS_NAME, 'price-format.nowrap')
        price_value = price_value.text
        return price_value

    def find_shop_link(self, product):
        if self.title == 'IDŹ DO SKLEPU':
            shop_link = product.find_element(By.CLASS_NAME, 'js_seoUrl.go-to-shop.button.button-primary.js_force-conv.js_clickHash')
            shop_link = shop_link.get_attribute('href')
            return shop_link
        shop_link = driver.find_element(By.CLASS_NAME, 'product-offers__list.js_product-offers')
        shop_link = shop_link.find_element(By.CLASS_NAME, 'button.button--primary.button--flex.go-to-shop')
        shop_link = shop_link.get_attribute('href')
        return shop_link

    def find_product_picture(self, product):
        if self.title == 'IDŹ DO SKLEPU':
            product_picture = product.find_element(By.TAG_NAME, 'img')
            product_picture = product_picture.get_attribute('src')
            print(product_picture)
            return product_picture
        product_picture = driver.find_element(By.CLASS_NAME, 'js_gallery-anchor.js_image-preview')
        product_picture.click()
        product_picture = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-picture-large.opaque')))
        product_picture = product_picture.get_attribute('src')
        product_picture_close = driver.find_element(By.CLASS_NAME, 'popup__exit')
        product_picture_close.click()
        return product_picture

    def find_logo_picture(self):
        logo_picture = driver.find_element(By.CLASS_NAME, 'lazyloaded')
        logo_picture = logo_picture.get_attribute('src')
        return logo_picture

    def display_product_img(self, product_picture):
        product_image_data = urlopen(product_picture).read()
        product_image = Image.open(BytesIO(product_image_data))
        product_image = ImageTk.PhotoImage(product_image)
        self.product_img_label = Label(self, image=product_image, relief = 'sunken', bd=7)
        self.update_idletasks()
        frame_width = self.frame.winfo_width()
        self.product_img_label.place(x=frame_width + 50, y=20)
        self.product_img_label.image = product_image

    def display_logo_img(self, logo_picture):
        logo_image_data = urlopen(logo_picture).read()
        logo_image = Image.open(BytesIO(logo_image_data))
        logo_image = ImageTk.PhotoImage(logo_image)
        self.logo_img_label = Label(self, image=logo_image, relief = 'sunken', bd=7)
        self.update_idletasks()
        height = self.product_img_label.winfo_height()
        img_x = self.product_img_label.winfo_x()
        self.logo_img_label.place(x=img_x, y=height+90)
        self.logo_img_label.image = logo_image

    def display_product_info(self, price_value, shop_name):
        self.price_label = Label(self, text='Best price:  ' + price_value, font=('Helvetica', 15))
        self.seller_label = Label(self, text='Seller:  ' + shop_name, font=('Helvetica', 15))
        self.update_idletasks()
        height = self.product_img_label.winfo_height()
        img_x = self.product_img_label.winfo_x()
        self.price_label.place(x=img_x, y=height+30)
        self.seller_label.place(x=img_x, y=height+60)

    def find_shop_name(self, shop_link):
        driver.get(shop_link)
        time.sleep(2)
        shop_name = driver.current_url
        shop_name = shop_name.split('/')
        return shop_name[2]

    def destroy_widgets(self):
        try:
            self.product_img_label.destroy()
            self.price_label.destroy()
            self.seller_label.destroy()
            self.logo_img_label.destroy()
            self.geometry('250x100')
        except:
            self.geometry('250x100')
            pass
    
    def show_product(self, *args):
        if not self.first_search:
            self.destroy_widgets()
            self.please_wait()
            self.get_products()
        else:
            self.geometry('250x100')
            self.please_wait()

        try:
            cookie_close = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'cookie-close-button.js_cookie-monster-close-accept.js_gtm_button')))
            cookie_close.click()
            pop_up_close = driver.find_element(By.CLASS_NAME, 'js_widget-close.widget-close')
            pop_up_close.click()
        except TimeoutException:
            pass
        
        for product in self.products:
            product_name = product.find_element(By.CSS_SELECTOR, 'span')
            if product_name.text in args:
                price_value = self.find_price(product)
                shop_link = self.find_shop_link(product)
                product_picture = self.find_product_picture(product)
                if self.title != 'IDŹ DO SKLEPU':
                    logo_picture = self.find_logo_picture()
                shop_name = self.find_shop_name(shop_link)
                self.cancle_wait()
                self.display_product_img(product_picture)
                if self.title != 'IDŹ DO SKLEPU':
                    self.display_logo_img(logo_picture)
                self.display_product_info(price_value, shop_name)
                self.update_idletasks()
                win_width = self.product_img_label.winfo_x() + self.product_img_label.winfo_width() + 30
                if self.title != 'IDŹ DO SKLEPU':
                    win_height = self.logo_img_label.winfo_y() + self.logo_img_label.winfo_height() + 30
                else:
                    win_height = self.seller_label.winfo_y() + self.seller_label.winfo_height() + 30
                self.geometry(f'{win_width}x{win_height}+500+100')
                break
        self.first_search = False
    
    def center_window(self, width=250, height=100):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (2*height)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == '__main__':
    app = App()
    app.mainloop()