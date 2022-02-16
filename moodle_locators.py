from faker import Faker

fake = Faker(locale='en_CA')

# Admin credentials
admin_username = 'jennyischakovrabinov'
admin_password = '101149Jr@'

# URLs
moodle_url = 'http://52.39.5.126/'
moodle_login_url = 'http://52.39.5.126/login/index.php'
moodle_users_main_page = 'http://52.39.5.126/admin/user.php'
moodle_dashboard_url = 'http://52.39.5.126/my/'

# Mandatory variables for Creating New User
new_username = fake.user_name()
new_password = fake.password()
first_name = fake.first_name()
last_name = fake.last_name()
full_name = f'{first_name} {last_name}'
email = fake.email()



