import os, sys, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(DIR, os.pardir, 'INTCDE23DNFSC001')

options = Options()
options.add_argument(f'--user-data-dir={os.path.join(DIR, "User")}')
driver = webdriver.Chrome('chromedriver', options=options)

def find(xpath, timeout = 3600, parent = driver):
    wait = WebDriverWait(parent, timeout)
    try:
        return wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except TimeoutException:
        return []

def sanitize_folder_name(folder_name):
    sanitized = re.sub(r'([<>:"/\\|?*]|[\s])+', ' ', folder_name)
    return sanitized.strip()

def log(text, indent = 0, file = False):
    if file:
        text = f"{'│   ' * (indent - 1)}├── {text}"
    else:
        text = f"{'│   ' * indent}{text}"
    print(text)
    with open(os.path.join(DIR, "FileList.txt"), "a+", encoding="utf-8") as f:
        f.write(text + '\n')

driver.get("https://cognizant.tekstac.com/blocks/learningpath/learningpath.php")

cards = find("//div[contains(@class, 'card-container')]//a/h5")
modules = {c.get_attribute('innerText') : find("..", parent=c)[0].get_attribute('href') for c in cards}

log(f"{len(modules)} modules found!")

for i, m in enumerate(modules):
    log(f"{i}/{len(modules)} {m}", 1, True)

    driver.get(modules[m])
    xpath = "//li[contains(@class, 'modtype_vpl')][//span[contains(@class, 'autocompletion')]/img[contains(@src, 'completion-auto-pass')]]//a/span"
    spans = find(xpath, timeout=5)
    handsons = {s.get_attribute('innerText').split('\n')[0] : find("..", parent=s)[0].get_attribute('href') for s in spans}
    
    log(f"{len(handsons)} hands-ons found!", 1)
    for j, h in enumerate(handsons):
        log(f"{j}/{len(handsons)} {h}", 2, True)
        
        driver.get(handsons[h])
        xpath = "//li/a[text()='Code Editor' and @title='Code Editor']"
        button = find(xpath, timeout=2)
        if len(button) == 0:
            log("Code Editor button not found!", 2)
            continue
        button[0].click()
        xpath = "//ul[@id='vpl_tabs_ul']/li/a"
        files = find(xpath, timeout=5)
        if len(files) == 0:
            log("Files not found!", 2)
            continue
    
        log(f"{len(files)} files found!", 2)
        for k, file in enumerate(files):
            fileName = file.get_attribute('title')
            if fileName == '':
                fileName = file.get_attribute('innerText').strip()
            log(f"{k}/{len(files)} {fileName}", 3, True)
            fileName += '.txt'
            filePath = os.path.join(DOWNLOAD_DIR, sanitize_folder_name(m),  sanitize_folder_name(h), fileName)
            
            dirPath = os.path.abspath(os.path.join(filePath, os.pardir))
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            tabId = file.get_attribute('href').split("#")[-1]
            script = f"return ace.edit('{tabId}').getValue();"
            fileContent = driver.execute_script(script)
            if fileContent == '':
                log("Cannot get file content!", 3)
                continue
            
            utf8_bytes = fileContent.encode('utf-8', errors='ignore')
            log(f"File size: {len(utf8_bytes)} bytes", 3)

            with open(filePath, "w", encoding='utf-8') as f:
                f.write(utf8_bytes.decode('utf-8'))