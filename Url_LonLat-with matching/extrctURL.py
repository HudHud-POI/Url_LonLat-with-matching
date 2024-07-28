import urllib.parse
import csv
import re
from selenium import webdriver
import time
import pickle

# وظيفة لحفظ ملفات تعريف الارتباط
def save_cookies(driver, path):
    with open(path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

# وظيفة لتحميل ملفات تعريف الارتباط
def load_cookies(driver, path):
    with open(path, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(f"Could not add cookie: {cookie}, error: {e}")

def get_final_url_with_selenium(url, driver, cookies_path='cookies.pkl', first_run=False):
    # فتح الرابط
    driver.get(url)
    
    # تحميل ملفات تعريف الارتباط إذا كانت موجودة وليست أول مرة
    if not first_run:
        try:
            load_cookies(driver, cookies_path)
            driver.refresh()
        except FileNotFoundError:
            pass
    
    # إذا كانت هذه هي المرة الأولى، انتظر المستخدم لإدخال التحقق
    if first_run:
        input("press enter after completing the CAPTCHA")
        # حفظ ملفات تعريف الارتباط بعد التحقق
        save_cookies(driver, cookies_path)
    
    time.sleep(6)

    # التحقق من وجود صفحة التحقق "لست روبوت"
    while '/sorry' in driver.current_url:
        input("CAPTCHA detected. Please complete the CAPTCHA and press enter.")
        save_cookies(driver, cookies_path)
        driver.refresh()
        time.sleep(6)

    # الحصول على الرابط النهائي
    final_url = driver.current_url

    return final_url

def extract_coordinates(driver, url, first_run=False):
    # الحصول على الرابط النهائي باستخدام Selenium
    final_url = get_final_url_with_selenium(url, driver, first_run=first_run)
    
    # فك ترميز الرابط للتعامل مع الأحرف الخاصة
    decoded_url = urllib.parse.unquote(final_url)
    print(f"Decoded URL: {decoded_url}")

    # استخدام regex لاستخراج الإحداثيات من الرابط النهائي
    match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', decoded_url)
    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        return latitude, longitude

    match = re.search(r'(-?\d+\.\d+),\s*(-?\d+\.\d+)', decoded_url)
    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        return latitude, longitude

    return None, None

# قراءة ملف Photos_24Jul.csv
input_file = '/Users/rahafmasmali/Desktop/l/Photos_24Jul_final (1).csv'

with open(input_file, 'r', encoding='utf-8') as photos_file:
    photos_reader = csv.DictReader(photos_file)
    photos_data = list(photos_reader)

# إعداد WebDriver من Selenium
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # تشغيل في وضع الرأس (معطل لعرض المتصفح)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

try:
    first_run = True
    # استخراج الإحداثيات وإضافتها إلى البيانات وحفظها في الملف أول بأول
    for row in photos_data:
        url = row.get('رابط الموقع في قوقل مابس')
        if url:
            latitude, longitude = extract_coordinates(driver, url, first_run=first_run)
            if latitude and longitude:
                row['Latitude'] = latitude
                row['Longitude'] = longitude
            else:
                row['Latitude'] = ''
                row['Longitude'] = ''
            first_run = False  # بعد أول رابط، لا نحتاج إلى الانتظار للتحقق مرة أخرى
        else:
            row['Latitude'] = ''
            row['Longitude'] = ''

finally:
    driver.quit()

# كتابة البيانات المحدثة إلى نفس الملف
fieldnames = photos_data[0].keys()
with open(input_file, 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(photos_data)