import pandas as pd
from datetime import datetime
from tvDatafeed import TvDatafeed, Interval
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt

def fetch_data():
    # دریافت اطلاعات از ورودی‌های کاربر
    start_date_str = start_date_entry.get() + ' ' + start_hour.get() + ':' + start_minute.get() + ':' + start_second.get()
    end_date_str = end_date_entry.get() + ' ' + end_hour.get() + ':' + end_minute.get() + ':' + end_second.get()
    username = username_entry.get()
    password = password_entry.get()
    symbol = symbol_entry.get()
    exchange = exchange_entry.get()

    # اطمینان از پر بودن همه ورودی‌ها
    if not all([start_date_str, end_date_str, username, password, symbol, exchange]):
        messagebox.showerror("خطا", "لطفاً تمام فیلدها را پر کنید.")
        return

    try:
        # تبدیل تاریخ‌ها به فرمت مناسب
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        messagebox.showerror("خطا", "فرمت تاریخ وارد شده صحیح نیست. لطفاً دوباره تلاش کنید.")
        return

    try:
        # اتصال به TradingView با نام کاربری و رمز عبور
        tv = TvDatafeed(username, password)

        # دریافت داده‌های تاریخی
        data = tv.get_hist(symbol=symbol, exchange=exchange, interval=Interval.in_1_minute)

        # بررسی وجود داده‌ها
        if data is None or data.empty:
            messagebox.showerror("خطا", "داده‌ای برای نماد و بازار وارد شده یافت نشد. لطفاً ورودی‌ها را بررسی کنید.")
            return

        # فیلتر کردن داده‌ها بر اساس بازه زمانی کاربر
        data = data[(data.index >= start_date) & (data.index <= end_date)]

        # تحلیل داده‌ها برای پیدا کردن کانال‌های سعودی و نزولی
        data['price_change'] = data['close'].diff()

        bullish_channels = data[data['price_change'] > 0]['price_change'].sum()
        bearish_channels = data[data['price_change'] < 0]['price_change'].sum()

        # محاسبه نتیجه نهایی
        result = bullish_channels + bearish_channels

        # نمایش نتیجه در پیغام
        messagebox.showinfo("نتایج", f"جمع کانال‌های سعودی: {bullish_channels}\nجمع کانال‌های نزولی: {bearish_channels}\nنتیجه نهایی: {result}")

        # رسم نمودار قیمت
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['close'], label='قیمت پایانی')
        plt.title(f'نمودار قیمت پایانی {symbol}')
        plt.xlabel('تاریخ')
        plt.ylabel('قیمت')
        plt.legend()
        plt.grid()
        plt.show()

    except Exception as e:
        messagebox.showerror("خطا", f"خطایی رخ داده است: {e}")

# ایجاد رابط کاربری
root = tk.Tk()
root.title("تحلیل داده‌های TradingView")

# تنظیمات کلی پنجره
root.geometry("600x700")
root.resizable(True, True)

# فونت بزرگ‌تر برای عنوان‌ها
title_font = ('B Nazanin', 14, 'bold')
entry_font = ('B Nazanin', 12)

# استایل کلی
style = ttk.Style()
style.configure('TFrame', background='white')
style.configure('TLabel', background='white', font=title_font)
style.configure('TButton', font=entry_font, background='#0066CC', foreground='black')
style.map('TButton', background=[('active', '#004C99')], foreground=[('active', 'black')])

# ایجاد فریم برای تاریخ‌ها
date_frame = ttk.LabelFrame(root, text="بازه زمانی", padding=(10, 10))
date_frame.pack(fill="x", padx=10, pady=5)

# ورودی‌های مربوط به تاریخ شروع و پایان
ttk.Label(date_frame, text="تاریخ شروع:").pack(pady=5, anchor='e')
start_date_entry = DateEntry(date_frame, date_pattern='yyyy-mm-dd', font=entry_font, justify='right')
start_date_entry.pack(fill="x", padx=5)

ttk.Label(date_frame, text="ساعت شروع:").pack(pady=5, anchor='e')
start_time_frame = ttk.Frame(date_frame, style='TFrame')
start_time_frame.pack(fill="x", padx=5)
start_hour = ttk.Spinbox(start_time_frame, from_=0, to=23, width=5, font=entry_font, justify='right')
start_hour.pack(side='left', padx=2)
start_minute = ttk.Spinbox(start_time_frame, from_=0, to=59, width=5, font=entry_font, justify='right')
start_minute.pack(side='left', padx=2)
start_second = ttk.Spinbox(start_time_frame, from_=0, to=59, width=5, font=entry_font, justify='right')
start_second.pack(side='left', padx=2)

ttk.Label(date_frame, text="تاریخ پایان:").pack(pady=5, anchor='e')
end_date_entry = DateEntry(date_frame, date_pattern='yyyy-mm-dd', font=entry_font, justify='right')
end_date_entry.pack(fill="x", padx=5)

ttk.Label(date_frame, text="ساعت پایان:").pack(pady=5, anchor='e')
end_time_frame = ttk.Frame(date_frame, style='TFrame')
end_time_frame.pack(fill="x", padx=5)
end_hour = ttk.Spinbox(end_time_frame, from_=0, to=23, width=5, font=entry_font, justify='right')
end_hour.pack(side='left', padx=2)
end_minute = ttk.Spinbox(end_time_frame, from_=0, to=59, width=5, font=entry_font, justify='right')
end_minute.pack(side='left', padx=2)
end_second = ttk.Spinbox(end_time_frame, from_=0, to=59, width=5, font=entry_font, justify='right')
end_second.pack(side='left', padx=2)

# ایجاد فریم برای اعتبارسنجی
auth_frame = ttk.LabelFrame(root, text="اطلاعات حساب", padding=(10, 10))
auth_frame.pack(fill="x", padx=10, pady=5)

# ورودی‌های مربوط به نام کاربری و رمز عبور
ttk.Label(auth_frame, text="نام کاربری تریدینگ ویو:").pack(pady=5, anchor='e')
username_entry = ttk.Entry(auth_frame, font=entry_font, justify='right')
username_entry.pack(fill="x", padx=5)

ttk.Label(auth_frame, text="رمز عبور تریدینگ ویو:").pack(pady=5, anchor='e')
password_entry = ttk.Entry(auth_frame, show='*', font=entry_font, justify='right')
password_entry.pack(fill="x", padx=5)

# ایجاد فریم برای نماد و بازار
symbol_frame = ttk.LabelFrame(root, text="نماد و بازار", padding=(10, 10))
symbol_frame.pack(fill="x", padx=10, pady=5)

# ورودی‌های مربوط به نماد و بازار
ttk.Label(symbol_frame, text="نماد:").pack(pady=5, anchor='e')
symbol_entry = ttk.Entry(symbol_frame, font=entry_font, justify='right')
symbol_entry.pack(fill="x", padx=5)

ttk.Label(symbol_frame, text="بازار:").pack(pady=5, anchor='e')
exchange_entry = ttk.Entry(symbol_frame, font=entry_font, justify='right')
exchange_entry.pack(fill="x", padx=5)

# دکمه برای اجرای تحلیل
analyze_button = ttk.Button(root, text='تحلیل', command=fetch_data, style='TButton')
analyze_button.pack(pady=20)

root.mainloop()
