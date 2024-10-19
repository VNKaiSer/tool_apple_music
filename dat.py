from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By



# define the proxy address and port

proxy = "20.235.159.154:80"



# set Chrome options to run in headless mode using a proxy

options = Options()

options.add_argument("--headless=new")

options.add_argument(f"--proxy-server={proxy}")



# initialize Chrome driver

driver = webdriver.Chrome(

    service=Service(ChromeDriverManager().install()),

    options=options

)



# navigate to the target webpage

driver.get("https://httpbin.io/ip")



# print the body content of the target webpage

print(driver.find_element(By.TAG_NAME, "body").text)



# release the resources and close the browser

driver.quit()
