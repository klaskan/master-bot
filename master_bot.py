from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep    
import numpy as np
import random

class MasterBot():
    """
    Remeber to download selenium webdriver to make it work.
    https://chromedriver.chromium.org/downloads
    """
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.listUrls = []
        self.username = ''
        self.password = ''

    def loginToPage(self):
        self.driver.get('https://eksperiment-uib.herokuapp.com/accounts/login/?next=/sessions/')
        user_field = self.driver.find_element_by_xpath('//*[@id="id_username"]')
        pass_field = self.driver.find_element_by_xpath('//*[@id="id_password"]')
        login_button = self.driver.find_element_by_xpath('//*[@id="btn-login"]')
        #login in with username and password
        user_field.send_keys(self.username)
        pass_field.send_keys(self.password)
        login_button.click()
    
    #creates a new session and adds all the links for the participants in self.listUrls
    def createSessionForEight(self):
        session_button = self.driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[2]/a')
        session_button.click()
        #next page
        creat_new_session_button = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/form[1]/div/button[1]')
        creat_new_session_button.click() 
        #next page
        #select session1
        drop_down_option_two = self.driver.find_element_by_xpath('//*[@id="id_session_config"]/option[2]')
        drop_down_option_two.click()
        #user 8 players
        number_of_players = self.driver.find_element_by_xpath('//*[@id="id_num_participants"]')
        number_of_players.send_keys('8')
        create_button = self.driver.find_element_by_xpath('//*[@id="btn-create-session"]')
        create_button.click()
        #next page
        #save table of links
        sleep(7)
        table_links = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/table/tbody')
        for tr in table_links.find_elements_by_xpath('/html/body/div[1]/div[2]/table/tbody/tr/td/a'):
            self.listUrls.append(tr.text)
    
    #Opens all participants in different tabs
    def openLinks(self):
        for link in self.listUrls:
            #execute javascript in console.
            self.driver.execute_script("window.open('{}');".format(link))
    
    def quize(self):
        for window in range(1,9):
            self.driver.switch_to.window(self.driver.window_handles[window])
            intro_next =  self.driver.find_element_by_xpath('//*[@id="form"]/div/p/button')
            intro_next.click()
        
        for window in range(1,9):
            self.driver.switch_to.window(self.driver.window_handles[window])
            question1 = self.driver.find_element_by_xpath('//*[@id="id_s1_2"]')
            question2 = self.driver.find_element_by_xpath('//*[@id="id_s2_1"]')
            question3 = self.driver.find_element_by_xpath('//*[@id="id_s3_0"]')
            question4 = self.driver.find_element_by_xpath('//*[@id="id_s4_0"]')
            questions_next_button = self.driver.find_element_by_xpath('//*[@id="form"]/div/p[3]/button')
            
            question1.click()
            question2.click()
            question3.click()
            question4.click()
            questions_next_button.click()

    def playGame(self):    
        #New page (Deklarer inntekt)
        for window in range(1,9):
            self.driver.switch_to.window(self.driver.window_handles[window])
            utbetalt = self.driver.find_element_by_xpath('//*[@id="form"]/div/ul/li[2]/h6/b')
            utbetalt = list(utbetalt.text[1:len(utbetalt.text)])
            utbetalt[1] = '.'
            utbetalt = float(''.join(utbetalt))
            
            
            deklarert = self.driver.find_element_by_xpath('//*[@id="id_deklarert"]')
            deklarert.clear()
            random_number = round(np.random.uniform(0, utbetalt), 2)
            deklarert.send_keys(str(random_number))
            
            next_button_deklarert = self.driver.find_element_by_xpath('//*[@id="form"]/div/p[1]/button')
            next_button_deklarert.click()
            
        sleep(1)
        #New page (statistikk)
        for window in range(1,9):
            self.driver.switch_to.window(self.driver.window_handles[window])
            statistikk_next = self.driver.find_element_by_xpath('//*[@id="form"]/div/p/button')
            sleep(1)
            statistikk_next.click()
    

    def optimalStrat(self):
        pass


    def main(self):
        #login
        self.loginToPage()
        #create session
        self.createSessionForEight()
        #open all participants
        self.openLinks()
        #quize
        self.quize()
        #play the game
        try:
            i = 0
            while(i < 24):
                self.playGame()
                sleep(1)
                i = i + 1
            self.driver.quit()
        except:
            self.driver.quit()


#It's showtime                         
if __name__== "__main__":
    bot = MasterBot()
    for i in range(2):
        bot.main()
        sleep(5)
            

