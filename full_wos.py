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
directory_files = 'D:/Users/idelavega/Desktop/Topics_paper'

folder = directory_files
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)
    
total_data = pd.DataFrame(columns = ['PT', 'AU', 'BA', 'BE', 'GP', 'AF', 'BF', 'CA', 'TI', 'SO', 'SE', 'BS',
       'LA', 'DT', 'CT', 'CY', 'CL', 'SP', 'HO', 'DE', 'ID', 'AB', 'C1', 'RP',
       'EM', 'RI', 'OI', 'FU', 'FX', 'CR', 'NR', 'TC', 'Z9', 'U1', 'U2', 'PU',
       'PI', 'PA', 'SN', 'EI', 'BN', 'J9', 'JI', 'PD', 'PY', 'VL', 'IS', 'PN',
       'SU', 'SI', 'MA', 'BP', 'EP', 'AR', 'DI', 'D2', 'EA', 'EY', 'PG', 'WC',
       'SC', 'GA', 'UT', 'PM', 'OA', 'HC', 'HP', 'DA'] )

start = time.time()

start_year = 1990
end_year = 2018


chromedriver = 'D:/Users/idelavega/Desktop/chromedriver.exe'
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
search_criteria.select_by_index(4)

year = driver.find_element_by_id('value(input1)').clear()
year = driver.find_element_by_id('value(input1)')
year.send_keys(str(start_year)+'-'+str(end_year))
        
driver.find_element_by_id('searchCell1').click()
driver.implicitly_wait(time_wait)

Select(driver.find_element_by_id('selectPageSize_bottom')).select_by_index(2)
driver.implicitly_wait(time_wait)

content = BeautifulSoup(driver.page_source,'html.parser')
        
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
    
    if n==1:
        export = driver.find_element_by_id("exportTypeName").click()
        driver.find_elements_by_class_name('subnav-item')[33].click()
    else:
        driver.find_element_by_class_name('selectedExportOption').click()
    
    driver.find_element_by_id('numberOfRecordsRange').click()
    driver.find_element_by_id('markFrom').clear()
    driver.find_element_by_id('markFrom').send_keys(start_number)
    driver.find_element_by_id('markTo').clear()
    driver.find_element_by_id('markTo').send_keys(end_number)
    Select(driver.find_element_by_id('bib_fields')).select_by_index(3)
    Select(driver.find_element_by_id('saveOptions')).select_by_index(4)           
            
    driver.find_element_by_class_name('quickoutput-action').click()
    driver.implicitly_wait(time_wait)
    driver.find_element_by_xpath("//*[@class='flat-button quickoutput-cancel-action']").click() 
    driver.implicitly_wait(time_wait)   
    
    os.chdir(directory_files)
    time.sleep(5)
    data = pd.read_csv('savedrecs.txt',sep='\t', encoding='utf-16',
                               index_col = False)  
    total_data = total_data.append(data)
    
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

driver.find_element_by_class_name('selectedExportOption').click()

driver.find_element_by_id('numberOfRecordsRange').click()
driver.find_element_by_id('markFrom').clear()
driver.find_element_by_id('markFrom').send_keys(start_number)
driver.find_element_by_id('markTo').clear()
driver.find_element_by_id('markTo').send_keys(end_number)
Select(driver.find_element_by_id('bib_fields')).select_by_index(3)
Select(driver.find_element_by_id('saveOptions')).select_by_index(4)           
            
driver.find_element_by_class_name('quickoutput-action').click()
driver.implicitly_wait(time_wait)
driver.find_element_by_xpath("//*[@class='flat-button quickoutput-cancel-action']").click() 
driver.implicitly_wait(time_wait)   
    
os.chdir(directory_files)
time.sleep(5)
data = pd.read_csv('savedrecs.txt',sep='\t', encoding='utf-16',
                               index_col = False)  
total_data = total_data.append(data)
    
folder = directory_files
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)  
    
driver.close()

end = time.time()
print('Elapsed time:',end-start)

total_data.to_csv('total_data.txt', sep='|')























