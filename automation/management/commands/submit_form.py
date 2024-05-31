from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Automates form submission and sends an email with the confirmation screenshot'

    def handle(self, *args, **options):
        # Specify the path to chromedriver
        driver_path = 'C:/Users/Rahul Khatik/Saved Games/Documents/chromedriver-win64/chromedriver.exe'  # Adjust this path
        driver = webdriver.Chrome(executable_path=driver_path)

        try:
            # Open the Google Form
            driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdUCd3UWQ3VOgeg0ZzNeT-xzNawU8AJ7Xidml-w1vhfBcvBWQ/viewform")

            # Wait for the form to fully load
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))

            # Fill in the form fields
            fields = [
                "Rahul Didvaniya",    # Name
                "8347061850",         # Phone Number
                "khatik.rk111@gmail.com",  # Email
                #"1, Sahjanand Apartments, Mahadev Nager, Vastral, Ahmedabad, Gujarat - 382418",  # Address
                #"2003-11-11",         # Date of Birth
                '382418',
                "Male",               # Gender
                "GNFPYC"              # Verification Code
            ]

            for index, field_value in enumerate(fields, start=1):
                try:
                    # Use XPath with index to find input element
                    input_element = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, f"(//input[@type='text'])[position()={index}]")))
                    input_element.send_keys(field_value)
                except Exception as e:
                    print(f"Failed to fill element at index {index}. Exception: {str(e)}")
            
            driver.find_element_by_class_name('KHxj8b').send_keys('1, Sahjanand Apartments, Mahadev Nager, Vastral, Ahmedabad, Gujarat - 382418')

            date_field = driver.find_element_by_xpath("//input[@type='date']")
            driver.execute_script("arguments[0].removeAttribute('readonly')", date_field)
            date_field.send_keys('11-11-2003')
            # Submit the form
            driver.find_element(By.XPATH, "//span[text()='Submit']").click()

            # Wait for the confirmation page to load
            time.sleep(5)

            # Take a screenshot
            screenshot_path = 'confirmation.png'
            driver.save_screenshot(screenshot_path)

            self.stdout.write(self.style.SUCCESS(f'Screenshot saved at {screenshot_path}'))

            # Send the email
            email = EmailMessage(
                'Python (Selenium) Assignment - Rahul Didvaniya',
                'Please find the attached confirmation screenshot.',
                'khatik.rk111@gmail.com',
                ['tech@themedius.ai'],
                cc=['HR@themedius.ai']
            )
            email.attach_file(screenshot_path)
            email.send()

            self.stdout.write(self.style.SUCCESS('Email sent successfully'))

        finally:
            # Close the driver
            driver.quit()
