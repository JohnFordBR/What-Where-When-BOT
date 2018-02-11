#!/usr/bin/env python

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


display = Display(visible=0, size=(1920, 1154))
display.start()

binary = FirefoxBinary('/root/Desktop/firefox/firefox')
browser = webdriver.Firefox(firefox_binary=binary)
browser.set_window_size(1920, 1154)



f = open('realinks.txt', "r")
lines = f.readlines()
f.close()
for i in range(len(lines)):
     browser.get(lines[i])
     browser.save_screenshot('raw_material/question%i.png'%i)


browser.quit()
display.stop()
