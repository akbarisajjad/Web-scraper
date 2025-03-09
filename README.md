# Web-scraper-plus
برای اجرای این وب اسکرپر، باید کتابخانه‌های زیر را نصب کنید:

📌 کتابخانه‌های مورد نیاز:

pip install requests beautifulsoup4 selenium tqdm

📌 توضیحات کتابخانه‌ها:

✅ requests → برای دانلود فایل‌ها و تصاویر از وب‌سایت‌ها
✅ beautifulsoup4 → برای پردازش و استخراج اطلاعات از HTML
✅ selenium → برای دریافت صفحات داینامیک (React, Vue, AJAX)
✅ tqdm → برای نمایش نوار پیشرفت دانلود


---

📌 نصب در ویندوز یا لینوکس

pip install -r requirements.txt

یا مستقیماً:

pip install requests beautifulsoup4 selenium tqdm

📌 نصب در macOS (در صورت نیاز به درایور کروم)

brew install chromedriver

اگر Chromedriver نصب نیست، می‌توان از WebDriver Manager استفاده کرد:

pip install webdriver-manager

و در کد این خط را اضافه کنید:

from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


---

📢 آیا روی سیستمت اجرا کردی یا مشکلی پیش اومد؟ 🚀


