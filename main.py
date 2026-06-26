from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import base64

def html_to_pdf(input_path, output):
    options = Options()
    options.add_argument("--headless=new")


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(input_path)

    print_options = {
        "landscape": False,
        "displayHeaderFooter": False,
        "printBackground": True,
        "preferCSSPageSize": True
    }
    time.sleep(1.5) # let page load

    driver.execute_script("""
        const style = document.createElement('style');
        style.innerHTML = `
            html, body, #root, #__next, .main-container { 
                height: auto !important; 
                overflow: visible !important; 
                position: relative !important;
            }
        `;
        document.head.appendChild(style);
    """)

    result = driver.execute_cdp_cmd("Page.printToPDF", print_options)

    pdf_bytes = base64.b64decode(result['data'])
    with open(output, "wb") as f:
        f.write(pdf_bytes)

    driver.quit()