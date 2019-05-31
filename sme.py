import random, string, csv, time
from selenium import webdriver
import time
import urllib3
import time

# 1. Identify most common elements in registration forms
# 2. Confirmation email -> proceeed 
# 3. Keep track // save login details to a SQL 

class User:
    
    ''' Use classes since most of the registraction forms will be the same ''' 
    
    def __init__(self, usr, passwd, email, *args, **kwargs):
        if usr not in args:
            self.usr = self.usr_gen()
        else:
            self.usr = usr
        if passwd not in args:
            self.passwd = self.pass_gen(20)
        else:
            self.passwd = passwd
        if email not in args:
            self.email = self.name+"-"+self.surname+"@horna-dolna.sk"
        else:
            self.email = email
    
    @classmethod
    def usr_gen(self):
        file = open('/home/projects/test/unit_test/names.csv')
        self.name=random.choice([i[1] for i in csv.reader(file, delimiter=',')])
        file = open('/home/projects/test/surnames.csv')
        self.surname=random.choice([string.capwords(j) for j in [i[0] for i in csv.reader(file, delimiter=',')]])
        self.usr=self.name+self.surname
        return (self.usr, self.name, self.surname)

    @classmethod
    def pass_gen(self, length):
        letters = string.hexdigits
        self.passwd = ''.join(random.choice(letters) for i in range(length))
        return self.passwd
    
    # countes the numbers of names ***a 2 HOUR TRIVIA ***
    def count(self):
        file = open('/home/projects/test/unit_test/surnames.csv')
        for i in csv.reader(file, delimiter=','):
             if i[2].isnumeric():
                     j = j + int(i[2])
             else:
                     pass
        return j

class Domain(User):

    ''' Can there be a domain w/o a user? No. Can there be a user w/o a domain? Yes
    It's a many to many relationship, no class inheritance '''

    def __init__(self, usr=None, passwd=None, email=None, domain=None, **kwargs):
        self.domain = domain
        self.driver = webdriver.Firefox()
        if isinstance(usr, User):
            self.usr = usr
            self.passwd = passwd
            self.email = email
        else:
            super().__init__(usr, passwd, email)


    def login(self, **kwargs):
        self.driver.get(self.domain)
        time.sleep(5)
        username = self.driver.find_element_by_id('SMELoginBoxInput_user_identifier-js')
        username.send_keys(self.usr[0])
        password = self.driver.find_element_by_id('SMELoginBoxInput_password-js')
        password.send_keys(self.passwd)
        submit = self.driver.find_element_by_name('login_button')
        submit.click()
        time.sleep(5)
        if self.driver.current_url == "https://prihlasenie.sme.sk/":
            self.register()
        else:
            # to_do(): action based on response codes 
             return "tadaaa"
    
    def register(self, **kwargs):
        self.driver.get('https://registracia.sme.sk/')
        username = self.driver.find_element_by_id('email')
        username.send_keys(self.email)
        password = self.driver.find_element_by_id('plainPassword_password')
        password.send_keys(self.passwd)
        password_retype = self.driver.find_element_by_id('plainPassword_retype_password')
        password_retype.send_keys(self.passwd)
        consent_age = self.driver.find_element_by_class_name('checkbox')
        consent_age.click()
        submit = self.driver.find_element_by_xpath('//button[@type="submit"]')
        submit.click()
        time.sleep(5)
        self.driver.close()
    
url = "https://sme.sk/"
jm = Domain(domain=url)
jm.login()

if __name__ == "__main__":
    pass
    