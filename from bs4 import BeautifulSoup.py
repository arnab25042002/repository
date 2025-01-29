from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from pprint import pprint

# Path to your updated ChromeDriver
chromedriver_path = r"C:\Users\ARNAB BANDYOPADHYAY\Downloads\chromedriver-win64\chromedriver.exe"
chrome_binary_path = r"C:\Users\ARNAB BANDYOPADHYAY\Downloads\chrome-win64\chrome.exe"

# Initialize the Chrome driver
service = Service(chromedriver_path)
options = webdriver.ChromeOptions()
# Commenting out headless mode for troubleshooting
# options.add_argument('--headless')
options.binary_location = chrome_binary_path

# Adding arguments to make the browser more stable
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
options.add_argument('--remote-debugging-port=9222')  # Enable remote debugging
options.add_argument('--enable-logging')
options.add_argument('--v=1')
options.add_argument('--disable-background-timer-throttling')
options.add_argument('--disable-backgrounding-occluded-windows')
options.add_argument('--disable-renderer-backgrounding')
options.add_argument('--max_old_space_size=4096')

driver = webdriver.Chrome(service=service, options=options)

def get_all_forms(url):
    """Returns all form tags found on a web page's `url` """
    try:
        # Load the web page
        driver.get(url)
        
        # Wait until the form is present
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'form')))
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        return soup.find_all("form")
    except TimeoutException:
        print("Timeout while waiting for page to load")
        return []
    except WebDriverException as e:
        print(f"WebDriverException: {e}")
        return []

def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)
    action = form.attrs.get("action")
    if action:
        action = action.lower()
    else:
        action = ""
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value = input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    for select in form.find_all("select"):
        # get the name attribute
        select_name = select.attrs.get("name")
        # set the type as select
        select_type = "select"
        select_options = []
        # the default select value
        select_default_value = ""
        # iterate over options and get the value of each
        for select_option in select.find_all("option"):
            # get the option value used to submit the form
            option_value = select_option.attrs.get("value")
            if option_value:
                select_options.append(option_value)
                if select_option.attrs.get("selected"):
                    # if 'selected' attribute is set, set this option as default    
                    select_default_value = option_value
        if not select_default_value and select_options:
            # if the default is not set, and there are options, take the first option as default
            select_default_value = select_options[0]
        # add the select to the inputs list
        inputs.append({"type": select_type, "name": select_name, "values": select_options, "value": select_default_value})
    for textarea in form.find_all("textarea"):
        # get the name attribute
        textarea_name = textarea.attrs.get("name")
        # set the type as textarea
        # get the textarea value
        textarea_value = textarea.get_text()
        # add the textarea to the inputs list
        inputs.append({"type": "textarea", "name": textarea_name, "value": textarea_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


if __name__ == "__main__":
    # Directly specify the URL here for testing purposes
    url = "https://www.rcsb.org/alignment"
    # get all form tags
    forms = get_all_forms(url)
    # iterate over forms
    for i, form in enumerate(forms, start=1):
        form_details = get_form_details(form)
        print("="*50, f"form #{i}", "="*50)
        pprint(form_details)

    # Close the browser
    driver.quit()
