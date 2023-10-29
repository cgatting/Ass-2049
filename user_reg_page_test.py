import unittest
from PyQt5 import QtWidgets, QtCore
from user_reg_page import user_reg  # Import your user registration code
import xmlrunner
    

class UserRegistrationTestCase1(unittest.TestCase):
    def setUp(self):
        # Initialize the application
        self.app = QtWidgets.QApplication([])

    def tearDown(self):
        # Clean up resources after each test
        self.app.quit()

    def test_valid_registration(self):
        # Test 1: Valid registration
        email = "user@example.com"
        password = "SecurePass123"
        first_name = "John"
        last_name = "Doe"
        dob = QtCore.QDate(1990, 1, 1)

        # Create the user registration window
        user_registration_window = user_reg(QtWidgets.QMainWindow())

        # Set input values
        user_registration_window.email_address.setText(email)
        user_registration_window.password.setText(password)
        user_registration_window.first_name.setText(first_name)
        user_registration_window.last_name.setText(last_name)
        user_registration_window.dateEdit.setDate(dob)

        # Trigger the registration process
        registration_successful = user_registration_window.user_register()

        # Check for the expected outcome

        self.assertTrue(registration_successful)  # Ensure the registration was successful

class UserRegistrationTestCase2(unittest.TestCase):
    def setUp(self):
        # Initialize the application
        self.app = QtWidgets.QApplication([])

    def tearDown(self):
        # Clean up resources after each test
        self.app.quit()

    def test_empty_fields(self):
        # Test 1: Valid registration
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        dob = QtCore.QDate()

        # Create the user registration window
        user_registration_window = user_reg(QtWidgets.QMainWindow())

        # Set input values
        user_registration_window.email_address.setText(email)
        user_registration_window.password.setText(password)
        user_registration_window.first_name.setText(first_name)
        user_registration_window.last_name.setText(last_name)
        user_registration_window.dateEdit.setDate(dob)

        # Trigger the registration process
        registration_successful = user_registration_window.user_register()

        # Check for the expected outcome
        self.assertFalse(registration_successful)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UserRegistrationTestCase1)
    suite = unittest.TestLoader().loadTestsFromTestCase(UserRegistrationTestCase2)
    # Run the tests with XML test reporting
    runner = xmlrunner.XMLTestRunner(output='test_reports')
    runner.run(suite)