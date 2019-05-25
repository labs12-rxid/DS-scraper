from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bs4 import BeautifulSoup
import io
import pandas as pd
import numpy as np
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import re
import numpy as np
import os
import glob
import shutil
import json
import html
from string import punctuation
from collections import deque
from config import chromedriver_path, max_output_drugs
from color_shape import color_array, shape_array
import traceback
        

debug = False
max_output_drugs = int(max_output_drugs)


# headless = (os.getenv('headless') == 'False')
headless = True
print('headless', headless)

print('chromedriver_path', chromedriver_path)
print('max output drugs', max_output_drugs)
print('are changes getting through?')


class ititle_contains(object):
    """ An expectation for checking that the title contains a case-insensitive
    substring. title is the fragment of title expected
    returns True when the title matches, False otherwise
    """

    def __init__(self, title):
        self.title = title

    def __call__(self, driver):
        return self.title.lower() in html.unescape(driver.title).lower()


class drugscom:
    def __init__(self):
        print('drugscom __init__ start')
        self.debug = False
        self.first = True
        if debug:
            self.nonmatch_unique_file = open('nonmatch_unique.txt', 'wt')
        else:
            self.nonmatch_unique_file = None
        self.wurl = 'https://www.drugs.com/pill_identification.html'
        self.base = "https://www.drugs.com"
        # self.caps = DesiredCapabilities().CHROME
        # self.caps["pageLoadStrategy"] = "normal"  
        print('before chrome options')
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--timeout:5000')
        if headless:
            self.chrome_options.add_argument('--headless')
        self.driver = webdriver.chrome.webdriver.WebDriver(
            chromedriver_path, options=self.chrome_options) #, desired_capabilities=self.caps)
        self.ddriver = webdriver.chrome.webdriver.WebDriver(
            chromedriver_path, options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 5)
        self.dwait = WebDriverWait(self.ddriver, 5)
        self.driver.set_window_size(850, 1600)
        self.results = []
        self.potential_matches = []
        self.actions = ActionChains(self.driver)
        print('after chrome options')


        self.shape_codes = [
            {"id": -1, "name": 'unspecified', 'code': -1},
            {"id": 0, "name": 'Round', 'code': 24},
            {"id": 1, "name": 'Capsule', 'code': 5},
            {"id": 2, "name": 'Oval', "code": 20},
            {"id": 3, "name": 'Egg', "code":  9},
            {"id": 4, "name": 'Barrel', "code": 1},
            {"id": 5, "name": 'Rectangle', "code": 23},
            {"id": 6, "name": '3 Sided', "code": 32},
            {"id": 7, "name": '4 Sided', "code": 14},
            {"id": 8, "name": '5 Sided', "code": 13},
            {"id": 9, "name": '6 Sided', "code": 27},
            {"id": 10, "name": '7 sided', "code": 25},
            {"id": 11, "name": '8 sided', "code": 10},
            {"id": 12, "name": 'U Shaped', "code": 33},
            {"id": 13, "name": 'Figure 8', "code": 12},
            {"id": 14, "name": 'Heart', "code": 16},
            {"id": 15, "name": 'Kidney', "code": 18},
            {"id": 16, "name": 'Gear', "code": 15},
            {"id": 17, "name": 'Character', "code": 6}
            # {"id": 18, "name": 'Diamand', "code": 7}, # these were removed by drugs.com
            # {"id": 19, "name": 'Square', "code": 28},
        ]
        self.color_codes = [
            {'id': 0, 'name': 'Beige', 'code': 14},
            {'id': 1, 'name': 'Black', 'code': 73},
            {'id': 2, 'name': 'Blue', 'code': 1},
            {'id': 3, 'name': 'Brown', 'code': 2},
            {'id': 4, 'name': 'Clear', 'code': 3},
            {'id': 5, 'name': 'Gold', 'code': 4},
            {'id': 6, 'name': 'Gray', 'code': 5},
            {'id': 7, 'name': 'Green', 'code': 6},
            {'id': 8, 'name': 'Maroon', 'code': 44},
            {'id': 9, 'name': 'Orange', 'code': 7},
            {'id': 10, 'name': 'Peach', 'code': 74},
            {'id': 11, 'name': 'Pink', 'code': 8},
            {'id': 12, 'name': 'Purple', 'code': 9},
            {'id': 13, 'name': 'Red', 'code': 10},
            {'id': 14, 'name': 'Tan', 'code': 11},
            {'id': 15, 'name': 'White', 'code': 12},
            {'id': 16, 'name': 'Yellow', 'code': 13},            
            {'id': 0, 'name': 'Beige & Beige', 'code': 14},
            {'id': 1, 'name': 'Black & Black', 'code': 73},
            {'id': 2, 'name': 'Blue & Blue', 'code': 1},
            {'id': 3, 'name': 'Brown & Brown', 'code': 2},
            {'id': 4, 'name': 'Clear & Clear', 'code': 3},
            {'id': 5, 'name': 'Gold & Gold', 'code': 4},
            {'id': 6, 'name': 'Gray & Gray', 'code': 5},
            {'id': 7, 'name': 'Green & Green', 'code': 6},
            {'id': 8, 'name': 'Maroon & Maroon', 'code': 44},
            {'id': 9, 'name': 'Orange & Orange', 'code': 7},
            {'id': 10, 'name': 'Peach & Peach', 'code': 74},
            {'id': 11, 'name': 'Pink & Pink', 'code': 8},
            {'id': 12, 'name': 'Purple & Purple', 'code': 9},
            {'id': 13, 'name': 'Red & Red', 'code': 10},
            {'id': 14, 'name': 'Tan & Tan', 'code': 11},
            {'id': 15, 'name': 'White & White', 'code': 12},
            {'id': 16, 'name': 'Yellow & Yellow', 'code': 13},
            {'id': 17, 'name': 'Beige & Red', 'code': 69},
            {'id': 18, 'name': 'Black & Green', 'code': 55},
            {'id': 19, 'name': 'Black & Teal', 'code': 70},
            {'id': 20, 'name': 'Black & Yellow', 'code': 48},
            {'id': 21, 'name': 'Blue & Brown', 'code': 52},
            {'id': 22, 'name': 'Blue & Grey', 'code': 45},
            {'id': 23, 'name': 'Blue & Orange', 'code': 71},
            {'id': 24, 'name': 'Blue & Peach', 'code': 53},
            {'id': 25, 'name': 'Blue & Pink', 'code': 34},
            {'id': 26, 'name': 'Blue & White', 'code': 19},
            {'id': 27, 'name': 'Blue & White Specks', 'code': 26},
            {'id': 28, 'name': 'Blue & Yellow', 'code': 21},
            {'id': 29, 'name': 'Brown & Clear', 'code': 47},
            {'id': 30, 'name': 'Brown & Orange', 'code': 54},
            {'id': 31, 'name': 'Brown & Peach', 'code': 28},
            {'id': 32, 'name': 'Brown & Red', 'code': 16},
            {'id': 33, 'name': 'Brown & White', 'code': 57},
            {'id': 34, 'name': 'Brown & Yellow', 'code': 27}, 
            {'id': 35, 'name': 'Clear & Green', 'code': 49},
            {'id': 36, 'name': 'Dark & Light Green', 'code': 46},
            {'id': 37, 'name': 'Gold & White', 'code': 51},
            {'id': 38, 'name': 'Grey & Peach', 'code': 63},
            {'id': 39, 'name': 'Grey & Pink', 'code': 39},
            {'id': 40, 'name': 'Grey & Red', 'code':58},
            {'id': 41, 'name': 'Grey & White', 'code': 51},
            {'id': 42, 'name': 'Grey & Yellow', 'code': 68},
            {'id': 43, 'name': 'Green & Orange', 'code': 65},
            {'id': 44, 'name': 'Green & Peach', 'code': 63},
            {'id': 45, 'name': 'Green & Pink', 'code': 56},
            {'id': 46, 'name': 'Green & Purple', 'code': 43},
            {'id': 47, 'name': 'Green & Turquoise', 'code': 62},
            {'id': 48, 'name': 'Green & White', 'code': 30},
            {'id': 49, 'name': 'Green & Yellow', 'code': 22},
            {'id': 50, 'name': 'Lavender & White', 'code': 42},
            {'id': 51, 'name': 'Maroon & Pink', 'code': 40},
            {'id': 52, 'name': 'Orange & Turquoise', 'code': 50},
            {'id': 53, 'name': 'Orange & White', 'code': 64},
            {'id': 54, 'name': 'Orange & Yellow', 'code': 23},
            {'id': 55, 'name': 'Peach & Purple', 'code': 60},
            {'id': 56, 'name': 'Peach & Red', 'code': 66},
            {'id': 57, 'name': 'Peach & White', 'code': 18},
            {'id': 58, 'name': 'Pink & Purple', 'code': 15},
            {'id': 59, 'name': 'Pink & Red Specks', 'code': 37},
            {'id': 60, 'name': 'Pink & Turquoise', 'code': 29},
            {'id': 61, 'name': 'Pink & White', 'code': 25},
            {'id': 62, 'name': 'Pink & Yellow', 'code': 72},
            {'id': 63, 'name': 'Red & Turquoise', 'code': 17},
            {'id': 64, 'name': 'Red & White', 'code': 35},
            {'id': 65, 'name': 'Red & Yellow', 'code': 20},
            {'id': 66, 'name': 'Tan & White', 'code': 33},
            {'id': 67, 'name': 'Turquoise & White', 'code': 59},
            {'id': 68, 'name': 'Turquuise & Yellow', 'code': 24},
            {'id': 69, 'name': 'White & Blue Specks', 'code': 32},
            {'id': 70, 'name': 'White & Red Specks', 'code': 41},
            {'id': 71, 'name': 'White & Yellow', 'code': 38},
            {'id': 72, 'name': 'Yellow & Grey', 'code': 31},
            {'id': 73, 'name': 'Yellow & White', 'code': 36}]

        self.color_table = \
            """
                Beige	#F5F5DC	(245,245,220)
                Black	#000000	(0,0,0)
                Blue	#0000FF	(0,0,255)
                Brown	#A52A2A	(165,42,42)
                Gold	#FFD700	(255,215,0)
                Gray 	#808080	(128,128,128)
                Green	#008000	(0,128,0)
                Maroon	#800000	(128,0,0)
                Orange	#FFA500	(255,165,0)
                Peach	#FFDAB9	(255,218,185)
                Pink	#FFC0CB	(255,192,203)
                Purple	#800080	(12,0,128)
                Red     #FF0000	(255,0,0)
                Tan     #D2B48C	(210,180,140)
                White	#FFFFFF	(255,255,255)
                Yellow	#FFFF00	(255,255,0)
                """
        self.color_map = {
            'beige': ['white', 'brown', 'gray', 'tan'],
            'brown': ['beige'],
            'gray': ['beige', 'white'],
            'maroon': ['red', 'purple'],
            'peach': ['pink'],
            'pink': ['peach'],
            'purple': ['maroon'],
            'red': ['maroon'],
            'tan': ['beige'],
            'white': ['beige', 'tan', 'yellow', 'gray'],
            'yellow': ['white']
        }
        self.shape_map = {
            'oval': ['egg-shape', 'egg', 'elliptical / oval'],
            'egg': ['egg-shape','oval',' elliptical / oval'],
            'capsule': ['capsule-shape'],
            'square': ['four-sided', 'rectangle'],
            'rectangle': ['four-sided'],
            'four-sided': ['rectangle'],
            'diamand': ['four-sided']
            }
    def get_color_code(self, id):
        for d in self.color_codes:
            if d['id'] == id:
                return d
        print(f'unknown color id {id} ')
        return 12  # white

    def get_shape_code(self, id):
        for d in self.shape_codes:
            if d['id'] == id:
                return d
        print(f'unknown shape id {id} ')
        return 0  # round

    def color_shape_match(self, color_target, color, shape_target, shape):
        color = color.lower()
        shape = shape.lower()
        #color_target: yellow  color: yellow shape_target: oval  shape: elliptical / oval
        print(f"color_target: {color_target}  color: {color} shape_target: {shape_target}  shape: {shape}")
        if color_target != color:
            Match = False
            if color_target in self.color_map:
                for color_ in self.color_map[color_target]:
                    if color == color_:
                        Match = True
                        break
            if not Match:
                return False
        if shape_target == "unspecified":
            return True
        if shape_target != shape:
            Match = False
            if shape_target in self.shape_map:
                for shape_ in self.shape_map[shape_target]:
                    # print(f'|{shape_}|  |{shape}|')
                    if shape == shape_:
                        Match = True
                        # print('shape match  is True')
                        break
            if not Match:
                return False
        return True       

    def mprint_is_equal(self, m1, m2, target_color, color, target_shape, shape):  # m1 is drugs.com mprint, m2 is DB mprint
#       mprint_is_equal 
        mcs = self.color_shape_match(target_color,color,target_shape, shape)
        if len(m1) == 0:
            return mcs        

        rv = 0
        m1l = m1.lower()
        m2l = m2.lower()
        if m1l == m2l: 
            return True if mcs else 3

        print(f'mprint_is_equal |{m1}| |{m2}|')



        m1l = ''.join(c for c in m1l if c not in punctuation)
        m2l = ''.join(c for c in m2l if c not in punctuation)
        if m1l == m2l:
            return True if mcs else 3
    #         print('no match yet', m1l, m2l)

                        

        for i in range(3): # 0 no change, 1 dup first word, 2 dup entire imprint
            m1s = m1l.split()
            m2s = m2l.split()
            if i == 1:
                m2s.insert(0, m2s[0])  # dup first word (usually company name)
            elif i == 2:
                print('m2s before extend', m2s)
                m2s.extend(m2s)  # dup MPRINTS on each side
                print('extended m2s', m2s)

            for j in range(2): # 0 no change,1 perpend'LOGO'

                # print('m1s', m1s,'i',i,'j',j)
                # print('m2s', m2s)
                if "".join(m1s) == "".join(m2s):
                    return True

          # test every possible starting word (don't know where left/right break is)
                m2sq = deque(m2s)
                m1ss = "".join(m1s)
                for _ in range(len(m2s)):
                    l = m2sq.popleft()
                    m2sq.append(l)
                    if j == 1:
                        m2sq.insert(0, 'logo')
                    # print('rotate',m1ss,m2sq)
                    m2qs = "".join(m2sq)
                    # if j == 1:
                        #  print(f'testing for eq for m1ss: |{m1ss}| m2qs: |{m2qs}| mcs: {mcs}')
                    eq = (m1ss == m2qs)
                    if eq:
                        if mcs:
                            if j == 1:
                                print('returning true for logo match')
                            return True
                        else:
                            return 3 # potential match - nonmatching color/shape
                    peq = (m1ss.find(m2qs) >= 0) 
                    if peq and mcs:
                        # print(f'setting 4 for m1ss: |{m1ss}| m2qs: |{m2qs}|')
                        rv = 4 # potential match - partial
                    if j == 1:
                        m2sq.popleft()  # remove 'logo'
        if rv > 0:
            return rv
        print('returning False from mprint_is_equal')
        return False

    def select_50(self):
        fifty_elem = self.driver.find_element(
            By.CSS_SELECTOR, "select[name='maxrows']")
        print('fifty_elem', fifty_elem)
        fifty = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='maxrows']")))
        # time.sleep(1)
        fifty.send_keys(Keys.RETURN)
        # color.click()
        print('fifty sent RETURN')
        target_fifty_elem = fifty_elem.find_element(
            By.XPATH, f"//option[@value=50]")
        self.driver.execute_script(
            "arguments[0].click();", target_fifty_elem)
        # time.sleep(2.5)
        print('50 click complete')        

    def select_color(self, color_code):
        color_elem = self.driver.find_element(
             By.CSS_SELECTOR, "select[id='color-select']")
        print('color_elem', color_elem)
        color = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select[id='color-select']")))
        # time.sleep(1)
        color.send_keys(Keys.RETURN)
        # color.click()
        print('color.click')

        # self.wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, "//input[@type='submit']")))
        target_color_elem = color_elem.find_element(
            By.XPATH, f"option[@value={color_code}]")
        print('target_color_elem found', target_color_elem.text)
        # self.driver.execute_script(
        #     "arguments[0].scrollIntoView();", target_color_elem)
        # # target_color_elem = color_elem.find_element(
        # #     By.XPATH, f"//option[@value={color_code}]")
        # print('target_color_elem after scroll\n', target_color_elem)
        # print('scroll complete')
        # self.driver.execute_script(
        #     "arguments[0].click();", target_color_elem)
        target_color_elem.click()
        # time.sleep(2.5)
        print('color click complete')

    def select_shape(self, shape_code):
#<select id="shape-select" name="shape" class="input-list">        
        shape_elem = self.driver.find_element(
            By.CSS_SELECTOR, "select[id='shape-select']")
        print('shape_elem', shape_elem.get_attribute("name")," | ", shape_elem.get_attribute("class"))
        shape = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select[id='shape-select']")))
        # time.sleep(1)
        shape.send_keys(Keys.RETURN)
        target_shape_elem = shape_elem.find_element(
            By.XPATH, f"option[@value={shape_code}]")
        print('target_shape_elem found', target_shape_elem.text)
        # self.driver.execute_script(
        #     "arguments[0].scrollIntoView();", target_shape_elem)
        # target_shape_elem = shape_elem.find_element(
        #     By.XPATH, f"//option[@value={shape_code}]")
        # print('target_shape_elem after scroll\n', target_shape_elem)
        # print('shape scroll complete')
        # self.driver.execute_script(
        #     "arguments[0].click();", target_shape_elem)
        target_shape_elem.click()
        # time.sleep(2.5)
        print('shape click complete')

    def make_mark_down(self, isoup) -> str:
        try:
            for a in isoup.select('a'):
                # insert sup tag after the span
                # span = isoup.new_tag('span')
                # span.string = a.text.replace('\n', '')
                # a.insert_after(span)
                # replace the a tag with it's contents
                a.unwrap()
            for div in isoup.find_all('div', {'class': 'contentAd'}):
                print('removing contentAd div')
                div.decompose()
            for ins in isoup.find_all('ins', {'class': 'display-ad' }):
                print('removing ins')
                ins.decompose()
            return str(isoup).replace('\n','')
        except Exception as e:
            print('error making markdown', repr(e))
            print(f'Make Markdown Error on line {sys.exc_info()[-1].tb_lineno}')
            return None

                 
    def get_data(self, ijo):
        print('in get_data')
        print('ijo',ijo)
        pmprint = ijo['imprint']
        color_row = self.get_color_code(ijo['color'])
        shape_row = self.get_shape_code(ijo['shape'])
        print(f'color_row: {color_row}  shape_row: {shape_row} ijo: {ijo}')
        target_color = color_row['name'].lower()
        target_shape = shape_row['name'].lower()
        color_code = color_row['code']
        shape_code = shape_row['code']
        self.potential_matches = []
        i = 0
        gds = []
        gds0 = []
        print('starting get_data', pmprint, color_code, target_color, shape_code, target_shape)

        #         self.driver.get(self.wurl)
        #         WebDriverWait(self.driver, 100).until(EC.title_contains(
        #             "Pill Identifier (Pill Finder) - Drugs.com"))
        #         try:
        #             elem = self.wait.until(
        #                 EC.element_to_be_clickable((By.LINK_TEXT, 'Accept' if len(self.results) == 0 else 'Search Again')))
        #         except:
        if self.first:
            self.driver.get(self.wurl)
            WebDriverWait(self.driver, 100).until(EC.title_contains(
                "Pill Identifier (Pill Finder) - Drugs.com"))
            if self.debug:
                print('started')
                time.sleep(3)
                self.driver.refresh()
            else:
                elem = self.wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, 'Accept')))
                elem.click()
                print('accept clicked')
            self.first = False

        mprint = pmprint
#         elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/imprints.php']")))
        elem = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#livesearch-imprint")))
        elem.click()
        elem.clear()
        elem.send_keys(mprint)
        # elem.send_keys(Keys.RETURN)

        # color may be covered with a drugs.com pulldown without this
        side_target = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "img[src='/img/pillid/example.png']")))
        side_target.click()

        print('send enter for submit skipped')
        submit = self.driver.find_element(
            By.XPATH, "//input[@type='submit']")
        print('submit found')

        self.select_color(color_code)
        if shape_code >= 0:
            self.select_shape(shape_code)


        # if the python way of clicking submit works use it, otherwise use the JavaScript way
        # try:
        #     elem = self.wait.until(EC.element_to_be_clickable(
        #         (By.XPATH, "//input[@type='submit']")))
        #     elem.send_keys(Keys.RETURN)
        #     print('send enter for submit succeeded')
        # except:
        time.sleep(1.5)
        # self.driver.execute_script(
        #     """
        #     const ke = new KeyboardEvent("keydown", {
        #         bubbles: true, cancelable: true, keyCode: 13
        #     });
        #     arguments[0].dispatchEvent(ke);

        #     setTimeout(function () {
        #         const ku = new KeyboardEvent("keyup", {
        #             bubbles: true, cancelable: true, keyCode: 13
        #         });
        #         arguments[0].dispatchEvent(ku);      
        #     }, 25);           
        #     """
        #     , submit)
        for i in range(3):
            try:
                print('waiting for submit clickable')
                elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
                print("waiting for submit click")
                elem.click()
                # elem.send_keys(Keys.RETURN)
                print('submit click done')
                break
            except:
                time.sleep(1)            
                try:
                    print('using javascript click')
                    self.driver.refresh()
                    self.driver.execute_script("arguments[0].click();", submit)
                    break
                except:
                    print('click timout', i)
                    time.sleep(1)

            # print('submit input not clickable')
        # self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Search Again')))
        # print('before submit driver.refresh')
        # self.driver.refresh()
        # # print('after submit driver.refresh done', len(self.driver.page_source))
        # with open(f"{mprint}.html", "wt") as File:
        #     File.write(self.driver.page_source)
        # print(f"{mprint}.html written")
        time.sleep(1.5)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        title = soup.find('h1')
        print('title',title)
        text = title.text
        try:
            f = text[0]
            L = 0
            h = None
            if f == 'I':
                h = 'Image Results for "'
            elif f == 'R':
                h = 'Results for "'
            elif f == 'N':
                h = 'No Results for "'
            else:
                print('test aborted, unknown text:', text)
            if h != None:
                L = len(h)
            if L > 0 and text[0:L] == h:
                print(text[L:L+len(mprint)],mprint) 
                assert text[L:L+len(mprint)] == mprint, "h1 doesn't have mprint"
                m = re.match(r"([\w-]+) And ([\w-]+)", text[L+len(mprint) + 1:] )
                print(f're text|{text[L+len(mprint) +1:]}|')
                print('m',m)
                print('color groups(0)[0]|', m.groups(0)[0])
                print('shape groups(0)[1]|', m.groups(0)[1])

                print('mprint', mprint)
                assert m.groups(0)[1] == shape_array[shape_code], 'correct shape not selected'
                assert m.groups(0)[0] == color_array[color_code], 'correct color not selected'
        except Exception as e:
            print('target shape',shape_array[shape_code] )
            print('target color',color_array[color_code] )
            print('error', repr(e))
            print(f'h1 verify Error {sys.exc_info()[-1].tb_lineno}') 
            print('restarting')
            return self.get_data(ijo)
            # throw('h1 verify error')
    



        # if title == None:
        #     return self.get_data(self, ijo)
        # try:
        #     title = title[len('Image Results for "'):]

        # # <h1>Image Results for "C 10 Yellow And Egg-shape"</h1>
        # h1r = r"Image Results for \"([\w\d]+?)\")    
        a = None
        mprint = None
        # with open('soup.html',"wt") as File:
        #     File.write(soup.prettify())
        # allimgs = soup.find_all(By.CSS_SELECTOR, 'img')
        # print('allimgs len', len(allimgs))
        np = soup.find('a', {'aria-label': 'Next page'})
        if np != None:
            print('selecting 50')
            self.select_50()
            self.driver.refresh()
        else:
            print('single 10 page')
        for pgno in range(1,2): # only doing max of 50 
            imgs = soup.findAll(
                lambda tag: tag.name == "img" and
                len(tag.attrs) >= 1 and
                tag["src"][0:14] == '/images/pills/')
            print('len imgs', len(imgs), 'pgno', pgno)
            mpr = 0
            for img in imgs:
                #             s = img['src']
                #                       print('s',s)
                print('type!!', type(img.parent.parent))
                a = img.parent.parent('span', text='Pill Imprint:')[
                                    0].next_sibling.next_sibling
                print('a',a,'type(a)', type(a))                             
                print('mprint', a.text, 'href', a.href, 'img', img)
                color = img.parent.parent('span', text='Color:')[
                                        0].next_sibling.strip().lower()
                print('color', color)
                shape = img.parent.parent('span', text='Shape:')[
                                        0].next_sibling.strip().lower()
    #             print('a', a, type(a), a.text)
                mprint = a.text
                dmprint = a.text
                # remove repeated internal spaces
                mprint = ' '.join(mprint.split())
                print('mprint', mprint)
                mpr = int(self.mprint_is_equal(mprint, pmprint, target_color, color, target_shape, shape))
                print('mpr', mpr)
                if mpr == 1: # True, match made
                    break
                if mpr > 0:
                    print('a',a,'type(a)', type(a))    
                    gds.append({"a": a, "mpr": mpr, "mprint": mprint, "dmprint": dmprint})
                    #self.get_details(a, mpr, mprint, dmprint)
                if mpr == 0:
                    gds0.append({"a": a, "mpr": mpr, "mprint": mprint, "dmprint": dmprint})

                    #                     print('not equal',mprint,pmprint)
                # if len(imgs) == 1:  # unique image result from drugs.com
                #     if debug:
                #         self.nonmatch_unique_file.write(
                #             f"mprint {mprint} pmprint {pmprint}")
                #     print('a is none only 1 image',a == None)
                #     mpr = 4 if a == None else 1
                #     break
#                 print(f"nonmatch continue mprint {mprint} pmprint {pmprint}")
                a = None
                mprint = None
                continue
    #             print('soup breaking out of imgs loop')
            if mpr == 1:
                assert a != None, 'mpr 1 None a'
                break # breaking out of pgno looop
            # np = soup.find('a', {'aria-label': 'Next page'})
            # print('np', np)
            # if np == None:
            #     print('np == None')
            #     break
            # # elem = self.wait.until(
            # #     EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next Page']")))
            # elem = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Next')))
            #                    # By.XPATH, "//input[@type='submit']")
            # print('Next Page elem', elem)
            # elem.click()   
            # try: 
            #     WebDriverWait(self.driver, 50).until(EC.title_contains(f"(Page {pgno + 1})"))        
            # except: 
            #     print('bad title:', self.driver.title) 
            # soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                


        try:
            elem = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Search Again')))
            elem.click()
            if headless == False:
                self.select_color(color_code)  # for testing color select
                self.select_shape(shape_code)  # for testing shape select
        except:
            pass
        if a == None and len(gds) == 0 and len(gds0) == 0:
            print('null a')
            return json.dumps(self.results, indent=4)
        if mpr == 1:
            assert a != None, "None a for mpr == 1"
            self.get_details(a, mpr, mprint, dmprint)
            #             a = elem.parent.find_next('a')
            #             print(f"img: {a['href']} MPRINT: {a.text}")
            #             mprint = a.text
            #             mprint = ' '.join(mprint.split()) # remove repeated internal spaces
            #             if not self.mprint_is_equal(mprint,pmprint):
            #                 continue

#             if self.mprint_is_equal(mprint,pmprint) & appended: # works because drugs.com puts matching mprint first
#                 break
#             print( mprint.lower(), pmprint.lower())
        else:
            try:
                if len(gds) > 0:
                    print('extending gds', len(gds))
                    if len(gds) > max_output_drugs:
                        gds = gds[0:max_output_drugs]
                    for gd in gds:
                        a = gd['a']
                        mpr = gd['mpr']
                        mprint = gd['mprint']
                        dmprint = gd['dmprint']
                        print('a',a,'type(a)', type(a))
                        self.get_details(a, mpr, mprint, dmprint)
                    self.results.extend(self.potential_matches)
                elif len(gds0) > 0:
                    print('extending gds0', len(gds))
                    if len(gds0) > max_output_drugs:
                        gds0 = gds0[0:max_output_drugs]                    
                    for gd in gds0:
                        a = gd['a']
                        mpr = gd['mpr']
                        mprint = gd['mprint']
                        dmprint = gd['dmprint']
                        self.get_details(a, mpr, mprint, dmprint)
                    self.results.extend(self.potential_matches) 
            except Exception as e:   
                print('error', repr(e))
                print(f'__gd__ Error  {traceback.print_tb(sys.exc_info()[2])}')                

        try:
            print('returning')
            if len(self.results) > max_output_drugs:
                self.results = self.results[0:max_output_drugs]  
            rv = json.dumps(self.results, indent=4)
            self.reset()
            return rv
        except Exception as e:   
            print('error', repr(e))
            print(f'__results__ Error {traceback.print_tb(sys.exc_info()[2])}')               
            return None    




    def get_details(self, a, mpr, mprint, dmprint):
        time.sleep(0.5)
        print("ddriver getting details page a['href']", a['href'])
        try:
            self.ddriver = webdriver.chrome.webdriver.WebDriver(
                chromedriver_path, options=self.chrome_options)
        except Exception as e:
            print('error on ddriver.reset', repr(e))
            # print(f'Error on line {sys.exc_info()[-1].tb_lineno}')
        for i in range(0,3):
            try:
                self.ddriver.get(self.base + a['href'])
                break
            except:
                if i == 2:
                    print("can't get details page")
                    raise Exception(f"getting details page {a['href']} failed")
                time.sleep(1)
        print(f'waiting for mprint {mprint}')
        WebDriverWait(self.ddriver, 100).until(ititle_contains(mprint))
#             print(a.text, ' title')
        isoup = BeautifulSoup(self.ddriver.page_source, 'html.parser')
        div = isoup.find_all('div', {'class': 'contentBox'})[0]
        brand = div.h1.text
        brand = brand[brand.index('(') + 1:-1]
        generic = None
        f_generic = None
        try:
            f_generic = isoup.find_all(
                'p', {'class': 'drug-subtitle'})[0].text
            generic = f_generic[14:]
            print('generic', generic)
        except:
            print('generic error, full generic', f_generic)
            if f_generic == None:
                generic = brand
                brand = ""
        # <dt class="pid-item-title pid-item-inline">Color:</dt>
        colors = isoup.find_all('dt', string='Color:')
        print('colors', colors)
        shapes = isoup.find_all('dt', string='Shape:')
        print('shapes', shapes)
#             imgs = isoup.find_all('img')
#             print('imgs len',len(imgs))
        imgs = isoup.findAll(
            lambda tag: tag.name == "img" and
            len(tag.attrs) >= 1 and
            tag["src"][0:14] == '/images/pills/')
        print('imgs length', len(imgs))
#             print('brand', brand, 'generic', generic, mprint, )
        # assert len(imgs) == 1, 'more than one or 0 images in detail page'
        # taking 1st img only
        for img in imgs:
            #                   print('img', img)
            try:
                s = img['src']
                a = isoup.find_all('a', string='Side Effects')[0]
                # ul = isoup.find_all('ul', {'class': ['more-resources-list', 'more-resources-list-general']})
                # print('len ul',len(ul))
                # if len(ul) > 0:
                #     li = ul[0].find('li')
                #     if li != None:
                #         print('li text', li.text)

                # with open('isoup.html',"wt") as File:
                #     File.write(isoup.prettify())

                print('side effects a href', a['href'])
                self.ddriver.get(self.base + a['href'])
                print('side effects page title', self.ddriver.title)
                WebDriverWait(self.ddriver, 10).until(
                    ititle_contains('Side Effects'))
                side_effects_html = self.ddriver.page_source
                h2ftc = '<h2>For the Consumer</h2>'
                ftc = side_effects_html.find(h2ftc)
                fhp = side_effects_html.find('<h2 id="for-professionals">')
                assert ftc > 0  and fhp > 0, 'h2 not found'
                print('ftc',ftc,'fhp', fhp)
                if ftc == -1:
                    ftc = 0
                else:
                    ftc += len(h2ftc)
                if fhp == -1:
                    fhp = len(side_effects_html)                                                
                isoup = BeautifulSoup(side_effects_html[ftc:fhp], 'html.parser')
                if debug:
                    with open('./html/' + generic + '.html',"wt") as File:
                        File.write(isoup.prettify())
                mark_down = self.make_mark_down(isoup)
                if debug:
                    if mark_down != None:
                        with open('./html/' + generic + '.result.html',"wt") as File:
                            File.write(mark_down)                    
                print('mark_down i:', i)
                # print(colors[i].next_sibling.text)
                # print(shapes[i].next_sibling.text)

                # #                       print('s',s)
                #                     if s[0:14] == '/images/pills/':
                #                          print('found img', s, ' mprint ', mprint)ls
                #         
                #                 self.img = base + s
                ar = self.results if mpr == 1 else self.potential_matches
                ar.append(
                    {'brand': brand, 'generic': generic, 'dmprint': dmprint, 'img': self.base + s,
                        'color': colors[i].next_sibling.text, 'shape': shapes[i].next_sibling.text,
                        'side_effects': mark_down
                        })
                print(f'appending {brand} {s} {len(self.results)} results')
                break
            except Exception as e:
                print('error appending', repr(e))
                print(f'get_details error {sys.exc_info()[-2]}')
                break

    def reset(self):
        del self.results
        self.results = []

    def close(self):
        self.driver.quit()
        self.ddriver.quit()
        if self.nonmatch_unique_file != None:
            self.nonmatch_unique_file.close()
        del self.results

#            <option value="1">Blue</option>
#            <option value="2">Brown</option>
