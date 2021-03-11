from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import os
def take_screenshot(name):
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = Firefox(options=driver_options)
    driver.get(f"https://www.faceit.com/en/players/{name}")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "game-card__info"))) # We wait for the stats to be loaded
    try:
        driver.find_element(By.XPATH, "//*[text()[contains(., 'I understand')]]").click() # If there are cookies to be accepted we accept them
    except Exception as err:
        print("No cookie button: "+str(err))
    stats = driver.find_element(By.CLASS_NAME, "game-card__info")
    if not "screenshots" in os.listdir():
        os.mkdir("screenshots")
    stats.screenshot(f"screenshots/{name}.png")
    driver.quit()
    image = Image.open(f"screenshots/{name}.png")
    new_image = image.crop((5,1,630,188))
    new_image.save(f"screenshots/{name}.png")
    
    
    
    

if __name__ == "__main__":
    take_screenshot(input("Name?:"))