import unittest
import moodle_methods as methods
import moodle_locators as locators


class MoodleApplicationPositiveCases(unittest.TestCase):

    # Scenario_01: create new user with mandatory fields
    @staticmethod
    def test_create_new_user():
        methods.set_up()
        # --- Create new user
        # Admin Log in
        methods.log_in(locators.admin_username, locators.admin_password)
        # Create a new user
        methods.create_new_user()
        # Check a new user has been added
        methods.filter_user()
        # Admin Log out
        methods.log_out()

        # --- Validate new user
        # Log In With New User Credentials
        methods.log_in(locators.new_username, locators.new_password)
        # Check we logged in with the new credentials
        methods.check_user_page()
        # # New user Log out
        methods.log_out()

        # --- Delete new user
        # Admin Log in
        methods.log_in(locators.admin_username, locators.admin_password)
        # Delete user
        methods.delete_user()
        # Admin Log out
        methods.log_out()

        # Close the web browser
        methods.tear_down('Scenario_01')





