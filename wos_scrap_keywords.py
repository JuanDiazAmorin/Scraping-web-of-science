##
#
#   SCRPAING KEYWORD
#

# THIS SCRIPT SCRAPS ALL JOURNALS (FROM SCIMAJO) BASED ON ARTIFICIAL INTELLIGENCE:
import os
import math
#import goslate
import numpy as np
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


time_wait = 100
directory_files = 'C:/Users/idelavega/Desktop/Download_WOS'

folder = directory_files
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)
 

start = time.time()

#chromedriver = 'C:/Users/Usuario/Desktop/chromedriver'
chromedriver = 'C:/Users/idelavega/Desktop/chromedriver'
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": directory_files} 
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chromedriver,options=options)
driver.get('https://www.scimagojr.com/journalrank.php?category=1702&type=j&wos=true')

content = BeautifulSoup(driver.page_source,'html.parser')

journals_number = content.find(class_='pagination').get_text()
journals_number = float(journals_number.split()[-1])
pages = math.ceil(journals_number/50)

journals = []

table = content.find_all(class_='tit')

for i in range(1,len(table)):
    journals.append(table[i].get_text())

for k in range(2,pages+1):
    driver.find_element_by_xpath('//a[contains(@href,"journalrank.php?category=1702&wos=true&type=j&page='+str(k)+'&total_size=127")]').click()
    content = BeautifulSoup(driver.page_source,'html.parser')
    table = content.find_all(class_='tit')
    for i in range(1,len(table)):
        journals.append(table[i].get_text())


driver.close()

TI = []
AB = []
DE = []
ID = []


# 04-03-19: JOURNALS: 0-10

for i in range(0, len(journals)):
    print(journals[i])
    
    time.sleep(2)
    folder = directory_files
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)      
    try:
        chromedriver = 'C:/Users/idelavega/Desktop/chromedriver'
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": directory_files} 
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(chromedriver,options=options)
        driver.get('https://www.webofknowledge.com')
        driver.implicitly_wait(time_wait)
        driver.find_element_by_id('settings-arrow').click()

        driver.find_element_by_id('editionitemBSCI').click()
        driver.find_element_by_id('editionitemBHCI').click()
        driver.find_element_by_id('editionitemESCI').click()
        
        search_criteria = Select(driver.find_element_by_id('select1'))
        search_criteria.select_by_index(3)
        
        journal_title = driver.find_element_by_id('value(input1)').clear()
        journal_title = driver.find_element_by_id('value(input1)')
        journal_title.send_keys(journals[i])
        
        
        driver.find_element_by_id('searchCell1').click()
        driver.implicitly_wait(time_wait)
        
          
        Select(driver.find_element_by_id('selectPageSize_bottom')).select_by_index(2)
        driver.implicitly_wait(time_wait)
        
        content = BeautifulSoup(driver.page_source,'html.parser')
        #number_pages = int(content.find(id='pageCount.top').get_text())
        
        number_papers = int(content.find(id='hitCount.top').get_text().replace('.',''))
        print('Number of papers:', number_papers)
        
        quotient = math.floor(number_papers/500)
        remainder = number_papers%500
        
        spaces = np.linspace(0,quotient*500,quotient+1)
        spaces = [int(x) for x in spaces]
        
        print('Processing ...')
        
        for n in range(1, len(spaces)):
            start_number = (n-1)*500 + 1
            end_number   = n*500
            
            driver.find_element_by_class_name('goToPageNumber-input').clear()
            driver.find_element_by_class_name('goToPageNumber-input').send_keys(1)
            
            driver.find_element_by_class_name('goToPageNumber-input').send_keys(Keys.ENTER)
            driver.implicitly_wait(time_wait)            
            
            
            Select(driver.find_element_by_id('saveToMenu')).select_by_index(5)
            driver.find_element_by_id('numberOfRecordsRange').click()
            driver.find_element_by_id('markFrom').send_keys(start_number)
            driver.find_element_by_id('markTo').send_keys(end_number)
            Select(driver.find_element_by_id('bib_fields')).select_by_index(2)
            Select(driver.find_element_by_id('saveOptions')).select_by_index(4)           
            
            driver.find_element_by_class_name('quickoutput-action').click()
            driver.implicitly_wait(time_wait)
            driver.find_element_by_class_name('quickoutput-cancel-action').click()
            driver.implicitly_wait(time_wait)           

            os.chdir(directory_files)
            time.sleep(5)
            data = pd.read_csv('savedrecs.txt',sep='\t', encoding='utf-16',
                               index_col = False)
            #data = data.dropna(axis=1, how='all')
            
            title = pd.DataFrame(data['TI'])
            abstract = pd.DataFrame(data['AB'])
            keywords = pd.DataFrame(data['DE'])
            keywords_plus = pd.DataFrame(data['ID'])
            
            for m in range(0, len(data)):
                TI.append(data['TI'].iloc[m])
                AB.append(data['AB'].iloc[m])
                DE.append(data['DE'].iloc[m])
                ID.append(data['ID'].iloc[m])
            
            folder = directory_files
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e) 
          
        start_number = n*500 + 1
        end_number =  n*500 + remainder
         
        driver.find_element_by_class_name('goToPageNumber-input').clear()
        driver.find_element_by_class_name('goToPageNumber-input').send_keys(1)
            
        driver.find_element_by_class_name('goToPageNumber-input').send_keys(Keys.ENTER)
        driver.implicitly_wait(time_wait)            
            
            
        Select(driver.find_element_by_id('saveToMenu')).select_by_index(5)
        driver.find_element_by_id('numberOfRecordsRange').click()
        driver.find_element_by_id('markFrom').send_keys(start_number)
        driver.find_element_by_id('markTo').send_keys(end_number)
        Select(driver.find_element_by_id('bib_fields')).select_by_index(2)
        Select(driver.find_element_by_id('saveOptions')).select_by_index(4)           
            
        driver.find_element_by_class_name('quickoutput-action').click()
        driver.implicitly_wait(time_wait)
        driver.find_element_by_class_name('quickoutput-cancel-action').click()
        driver.implicitly_wait(time_wait)           

        os.chdir(directory_files)
        time.sleep(5)
        data = pd.read_csv('savedrecs.txt',sep='\t', encoding='utf-16',
                               index_col = False)
            #data = data.dropna(axis=1, how='all')
            
        title = pd.DataFrame(data['TI'])
        abstract = pd.DataFrame(data['AB'])
        keywords = pd.DataFrame(data['DE'])
        keywords_plus = pd.DataFrame(data['ID']) 

        for m in range(0, len(data)):
            TI.append(data['TI'].iloc[m])
            AB.append(data['AB'].iloc[m])
            DE.append(data['DE'].iloc[m])
            ID.append(data['ID'].iloc[m])
            
        folder = directory_files
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)            
            
    except Exception:
        pass
    
        driver.close()
    
data = {'TI':TI, 'AB':AB, 'DE':DE, 'ID':ID}
data = pd.DataFrame(data=data)
end = time.time()
print('Elapsed time:',end-start)
    
       
data.to_csv('data.txt',sep='\t')        
















        
        
        
