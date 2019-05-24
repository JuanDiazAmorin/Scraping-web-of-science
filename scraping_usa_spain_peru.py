

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
path_data = 'D:/Users/idelavega/Desktop/Papers/USA_SPAIN_PERU/data'


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
       'SC', 'GA', 'UT', 'PM', 'OA', 'HC', 'HP', 'DA','COUNTRY', 'YEAR',
       'JOURNAL'] )
error = []
error_journal = []
    
start = time.time()



countries = ('PERU','SPAIN','USA')
start_year = 1990
end_year = 1995

for z in range(0, len(countries)):
    os.chdir(path_data)
    journals = pd.read_excel('journals_list.xlsx', sheet_name=countries[z])
    
    for year in range(start_year, end_year+1):
              
        for j in range(0, len(journals)):
            
            print(journals['journal'][j])
            journal = journals['journal'][j]
            
            chromedriver = 'D:/Users/idelavega/Desktop/chromedriver'
            options = webdriver.ChromeOptions()
            prefs = {"download.default_directory": directory_files} 
            options.add_experimental_option("prefs", prefs)
        
            driver = webdriver.Chrome(chromedriver,options=options)
            driver.get('https://www.webofknowledge.com')
            driver.implicitly_wait(time_wait)
        
            driver.find_element_by_link_text('Búsqueda avanzada').click()
        
        
            driver.find_element_by_id('selectallBtm').click()
            driver.find_element_by_id('deleteBtm').click()
        
            driver.find_element_by_id('value(input1)').clear()
            driver.find_element_by_id('value(input1)').send_keys('CU='+str(countries[z])+ ' AND '+ 'PY='+str(year)+' AND '+'SO='+journal)                    
            Select(driver.find_element_by_id('value(input2)')).deselect_all()
            Select(driver.find_element_by_id('value(input2)')).select_by_visible_text('All languages')
            Select(driver.find_element_by_id('value(input3)')).deselect_all()
            Select(driver.find_element_by_id('value(input3)')).select_by_visible_text('Article')
            Select(driver.find_element_by_name('range')).select_by_index(6)
        
            Select(driver.find_element_by_name('startYear')).select_by_visible_text(str(start_year))
            Select(driver.find_element_by_name('endYear')).select_by_visible_text(str(end_year))
        
        
            driver.find_element_by_id('settings-arrow').click()
        
            driver.find_element_by_id('editionitemBSCI').click()
            driver.find_element_by_id('editionitemBHCI').click()
            driver.find_element_by_id('editionitemESCI').click()
            
            driver.find_element_by_id('searchButton').click()
            driver.implicitly_wait(time_wait)
            
            result = BeautifulSoup(driver.page_source,'html.parser')
            number_paper = int(result.find(class_='historyResults').get_text().replace(' ',''))
            
            if number_paper==0:
                pass
                error_journal.append('CU='+str(countries[z])+ ' AND '+ 'PY='+str(year)+' AND '+'SO='+journal)
                driver.close()
            else:           
                driver.find_element_by_id('set_1_div').click()
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
                                          
                if quotient>0:
                    for n in range(1, len(spaces)):
                        try:
                            start_number = (n-1)*500 + 1
                            end_number   = n*500
                            print(start_number)
                            print(end_number)
                                
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
                            
                            time.sleep(6)
                            os.chdir(directory_files) 
                            data = pd.read_csv('savedrecs.txt',sep='\t', encoding='utf-16',
                                               index_col = False)
        
                            data['COUNTRY'] = str(countries[z])
                            data['YEAR'] = year
                            data['JOURNAL'] = journal
                            total_data = total_data.append(data)
                        
                            folder = directory_files
                            for the_file in os.listdir(folder):
                                file_path = os.path.join(folder, the_file)
                                try:
                                    if os.path.isfile(file_path):
                                        os.unlink(file_path)
                                except Exception as e:
                                    print(e)
                        except:
                            pass
                            error.append('CU='+str(countries[z])+ ' AND '+ 'PY='+str(year)+' AND '+'SO='+journal+' ;start:'+str(start_number)+' ;end:'+str(end_number))
                else:
                    n=0
                 
                folder = directory_files
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(e)
                try:
                    start_number = n*500 + 1
                    end_number =  n*500 + remainder
                         
                    driver.find_element_by_class_name('goToPageNumber-input').clear()
                    driver.find_element_by_class_name('goToPageNumber-input').send_keys(1)
                            
                    driver.find_element_by_class_name('goToPageNumber-input').send_keys(Keys.ENTER)
                    driver.implicitly_wait(time_wait)            
                    
                    if n==0:
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
                    
                    os.chdir(directory_files) 
                        
                    driver.find_element_by_class_name('quickoutput-action').click()
                    driver.implicitly_wait(time_wait)
                    driver.find_element_by_xpath("//*[@class='flat-button quickoutput-cancel-action']").click() 
                    driver.implicitly_wait(time_wait)   
                    
                    time.sleep(6)
                    data = pd.read_csv('savedrecs.txt',sep='\t', encoding='utf-16',
                                               index_col = False)  
                    data['COUNTRY'] = str(countries[z])
                    data['YEAR'] = year
                    data['JOURNAL'] = journal
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
                except:
                    pass
                    error.append('CU='+str(countries[z])+ ' AND '+ 'PY='+str(year)+' AND '+'SO='+journal+' ;start:'+str(start_number)+' ;end:'+str(end_number))
       
          