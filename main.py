from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import base64
import glob
import os
from pathlib import Path
import shutil

def get_unique_filename(output_dir, filename):

    output_path = Path(output_dir)
    file_path = output_path / filename
    
    if not file_path.exists():
        return file_path
        
    stem = file_path.stem
    suffix = file_path.suffix
    
    counter = 1
    while file_path.exists():
        file_path = output_path / f"{stem}({counter}){suffix}"
        counter += 1
        
    return file_path

def convert_file(exact_file_path, exact_output):
    options = Options()
    options.add_argument("--headless=new")


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("file://"+exact_file_path)

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
    with open(exact_output, "wb") as f:
        f.write(pdf_bytes)
    
    driver.quit()

def strip_path(file):  #janky; I know
    steps = str(file).split("/")
    return steps[len(steps)-1]

def html_to_pdf(input_path, output):
    shutil.rmtree(os.path.expanduser(output))

    os.makedirs(os.path.expanduser(output))


    [convert_file(file, get_unique_filename(os.path.expanduser(output), strip_path(str(file))[:-5]+".pdf")) for file in glob.glob(os.path.expanduser(input_path), recursive=True)]

html_to_pdf("~/Downloads/11ty-knowledge-base-main/*/**.html", "~/files")
