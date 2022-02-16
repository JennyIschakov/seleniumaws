
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import moodle_locators as locators


from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
divider = '------------------------------'


def set_up():
    # Make a full screen
    driver.maximize_window()

    # Navigating to the Moodle app website
    driver.get(locators.moodle_url)

    # Checking that we're on the correct URL address and we're seeing correct title
    if driver.current_url == locators.moodle_url and driver.title == 'Software Quality Assurance Testing':
        print(f'We\'re at Moodle homepage -- {driver.current_url}')
        print(f'We\'re seeing title message -- "Software Quality Assurance Testing"')
    else:
        print(f'We\'re not at the Moodle homepage. Check your code!')
        driver.close()
        driver.quit()


def tear_down(scenario_num):
    if driver is not None:
        print(divider)
        text = f'{scenario_num} completed at {datetime.datetime.now()}'
        print(text)
        open('moodle_log.log', 'a').write(text + '\n')
        driver.close()
        sleep(1)


def log_in(username, password):
    if driver.current_url == locators.moodle_url:
        driver.find_element(By.LINK_TEXT, 'Log in').click()
        if driver.current_url == locators.moodle_login_url:
            driver.find_element(By.ID, 'username').send_keys(username)
            sleep(0.25)
            driver.find_element(By.ID, 'password').send_keys(password)
            sleep(0.25)
            driver.find_element(By.ID, 'loginbtn').click()
            if driver.title == 'Dashboard' and driver.current_url == locators.moodle_dashboard_url:
                assert driver.current_url == locators.moodle_dashboard_url
                print(f'Log in successfully. Dashboard is present. \n'
                      f'We logged in with Username: {username} and Password: {password}')
            else:
                print(f'We\re not at the Dashboard. Try again')


def log_out():
    driver.find_element(By.CLASS_NAME, 'userpicture').click()
    sleep(0.25)
    driver.find_element(By.XPATH, '//span[contains(., "Log out")]').click()
    sleep(0.25)
    if driver.current_url == locators.moodle_url:
        print(f'Log out successfully at: {datetime.datetime.now()}')


def create_new_user():
    driver.find_element(By.XPATH, '//span[contains(., "Site administration")]').click()
    sleep(0.25)
    assert driver.find_element(By.LINK_TEXT, 'Users').is_displayed()
    driver.find_element(By.LINK_TEXT, 'Users').click()
    sleep(0.25)
    driver.find_element(By.LINK_TEXT, 'Add a new user').click()
    sleep(0.25)
    assert driver.find_element(By.LINK_TEXT, 'Add a new user').is_displayed()
    sleep(0.25)

    # Start fill the form
    # username
    driver.find_element(By.ID, 'id_username').send_keys(locators.new_username)
    sleep(0.25)
    # password
    driver.find_element(By.LINK_TEXT, 'Click to enter text').click()
    sleep(0.25)
    driver.find_element(By.ID, 'id_newpassword').send_keys(locators.new_password)
    sleep(0.25)
    # First name
    driver.find_element(By.ID, 'id_firstname').send_keys(locators.first_name)
    sleep(0.25)
    # Last name
    driver.find_element(By.ID, 'id_lastname').send_keys(locators.last_name)
    sleep(0.25)
    # email
    driver.find_element(By.ID, 'id_email').send_keys(locators.email)
    # Select 'Allow everyone to see my email address'
    Select(driver.find_element(By.ID, 'id_maildisplay')).select_by_visible_text('Allow everyone to see my email address')
    sleep(0.25)

    # Click by 'Create user' button
    driver.find_element(By.ID, 'id_submitbutton').click()
    sleep(0.25)
    print(f'--- Test Scenario: Create a new user "{locators.new_username}" --- is passed')

    # Take users details to .csv file
    open('moodle_users_list.csv', 'a').write(f'{locators.new_username};{locators.new_password}; {locators.first_name};{locators.last_name};{locators.email};\n')


def filter_user():
    sleep(1)
    # Check that we are on the User's Main Page
    if driver.current_url == locators.moodle_users_main_page:
        assert driver.find_element(By.XPATH, "//h1[text() = 'Software Quality Assurance Testing']").is_displayed()
        if driver.find_element(By.ID, 'fgroup_id_email_grp_label') and driver.find_element(By.NAME, 'email'):
            sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, 'input#id_email').send_keys(locators.email)
            sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, 'input#id_addfilter').click()
            sleep(0.25)
            if driver.find_element(By.XPATH, f'//td[contains(., "{locators.email}")]'):
                print(f'--- User <{locators.email}> found on list')


def check_user_page():
    sleep(1)
    if driver.current_url == locators.moodle_dashboard_url:
        # --- 1. Validate user full name on top right menu - beside logo
        if driver.find_element(By.XPATH, f'//span[contains(., "{locators.full_name}")]').is_displayed():
            print(f'--- User with the name {locators.full_name} is displayed. Test Passed ---')

        # --- 2. Validate User's Dashboard. Must be only 3 options on left menu:
        #  Site Home, Calendar, Private files
        users_options = ['Site home', 'Calendar', 'Private files']

        for menu in users_options:
            sleep(0.25)
            if driver.find_element(By.XPATH, f'//span[contains(., "{menu}")]'):
                driver.find_element(By.XPATH, f'//span[contains(., "{menu}")]').click()
            else:
                print(f'<{menu}> not found. Check')

            sleep(0.25)
            if menu == 'Site home':
                assert driver.current_url == 'http://52.39.5.126/?redirect=0'
            if menu == 'Calendar':
                assert driver.current_url == 'http://52.39.5.126/calendar/view.php?view=month'
            if menu == 'Private files':
                assert driver.current_url == 'http://52.39.5.126/user/files.php'

            print(f'--- Menu <{menu}> clicked and page validated')

        # Validate that no administrative options on user page
        admin_options = ['Content bank', 'Site administration']
        for menu in admin_options:
            try:
                sleep(0.25)
                if driver.find_element(By.XPATH, f'//span[contains(., "{menu}")]'):
                    print(f'Administrative menu <{menu}> displayed on user page. Check')
            except:
                print(f'Administrative menu <{menu}> not displayed on user page. Correct')




def delete_user():
    sleep(1)
    # Navigate to Users Page
    driver.find_element(By.XPATH, '//span[contains(., "Site administration")]').click()
    driver.find_element(By.LINK_TEXT, 'Users').click()
    driver.find_element(By.LINK_TEXT, 'Browse list of users').click()
    sleep(0.25)
    # Filter user
    filter_user()

    # After filtering user, find user on table and delete
    driver.find_element(By.XPATH, f'//td[contains(., "{locators.email}")]/following::*/descendant::i[@title = "Delete"]').click()
    # Confirm
    driver.find_element(By.XPATH, '//button[text() = "Delete"]').click()
    print(f'--- User <{locators.email}> deleted successfully')





#  -----------------------------------------------

