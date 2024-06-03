import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser, ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

class PhotoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("ویرایشگر عکس پیشرفته")
        self.root.geometry("1000x700")

        self.image = None
        self.tk_image = None

        self.create_widgets()

    def create_widgets(self):
        self.create_menu()
        self.create_toolbar()
        self.create_canvas()
        self.create_sliders()

    def create_menu(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="فایل", menu=file_menu)
        file_menu.add_command(label="باز کردن", command=self.open_image)
        file_menu.add_command(label="ذخیره کردن", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="خروج", command=self.root.quit)

    def create_toolbar(self):
        toolbar = ttk.Frame(self.root, padding="5")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_rotate = ttk.Button(toolbar, text="چرخش", command=self.rotate_image)
        btn_rotate.pack(side=tk.LEFT, padx=2)

        btn_resize = ttk.Button(toolbar, text="تغییر اندازه", command=self.resize_image)
        btn_resize.pack(side=tk.LEFT, padx=2)

        btn_crop = ttk.Button(toolbar, text="برش", command=self.crop_image)
        btn_crop.pack(side=tk.LEFT, padx=2)

        btn_filter = ttk.Button(toolbar, text="فیلتر", command=self.apply_filter)
        btn_filter.pack(side=tk.LEFT, padx=2)

        btn_color = ttk.Button(toolbar, text="تغییر رنگ", command=self.change_color)
        btn_color.pack(side=tk.LEFT, padx=2)

        btn_sharpen = ttk.Button(toolbar, text="شارپ کردن", command=self.sharpen_image)
        btn_sharpen.pack(side=tk.LEFT, padx=2)

        btn_edge_enhance = ttk.Button(toolbar, text="تقویت لبه", command=self.edge_enhance_image)
        btn_edge_enhance.pack(side=tk.LEFT, padx=2)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def create_sliders(self):
        slider_frame = ttk.Frame(self.root, padding="5")
        slider_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.brightness_slider = ttk.Scale(slider_frame, from_=0.0, to=2.0, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_slider.set(1.0)
        self.brightness_slider.pack(side=tk.LEFT, padx=5)
        ttk.Label(slider_frame, text="روشنایی").pack(side=tk.LEFT)

        self.contrast_slider = ttk.Scale(slider_frame, from_=0.0, to=2.0, orient=tk.HORIZONTAL, command=self.update_contrast)
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(side=tk.LEFT, padx=5)
        ttk.Label(slider_frame, text="کنتراست").pack(side=tk.LEFT)

        self.blur_slider = ttk.Scale(slider_frame, from_=0.0, to=10.0, orient=tk.HORIZONTAL, command=self.update_blur)
        self.blur_slider.set(0.0)
        self.blur_slider.pack(side=tk.LEFT, padx=5)
        ttk.Label(slider_frame, text="محو").pack(side=tk.LEFT)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.display_image()

    def display_image(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def rotate_image(self):
        if self.image:
            self.image = self.image.rotate(90, expand=True)
            self.display_image()

    def resize_image(self):
        if self.image:
            width = simpledialog.askinteger("ورودی", "عرض جدید را وارد کنید")
            height = simpledialog.askinteger("ورودی", "ارتفاع جدید را وارد کنید")
            if width and height:
                self.image = self.image.resize((width, height))
                self.display_image()

    def crop_image(self):
        if self.image:
            left = simpledialog.askinteger("ورودی", "مقدار چپ را وارد کنید")
            upper = simpledialog.askinteger("ورودی", "مقدار بالا را وارد کنید")
            right = simpledialog.askinteger("ورودی", "مقدار راست را وارد کنید")
            lower = simpledialog.askinteger("ورودی", "مقدار پایین را وارد کنید")
            if None not in (left, upper, right, lower):
                self.image = self.image.crop((left, upper, right, lower))
                self.display_image()

    def update_brightness(self, value):
        if self.image:
            factor = float(value)
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(factor)
            self.display_image()

    def update_contrast(self, value):
        if self.image:
            factor = float(value)
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(factor)
            self.display_image()

    def update_blur(self, value):
        if self.image:
            radius = float(value)
            self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
            self.display_image()

    def apply_filter(self):
        if self.image:
            filter_choice = simpledialog.askstring("ورودی", "نوع فیلتر را وارد کنید (BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EMBOSS, SHARPEN)")
            if filter_choice:
                if filter_choice.upper() == "BLUR" or filter_choice.upper() == "bl":
                    self.image = self.image.filter(ImageFilter.BLUR)
                elif filter_choice.upper() == "CONTOUR" or filter_choice.upper() == "co":
                    self.image = self.image.filter(ImageFilter.CONTOUR) 
                elif filter_choice.upper() == "DETAIL" or filter_choice.upper() == "de" :
                    self.image = self.image.filter(ImageFilter.DETAIL)
                elif filter_choice.upper() == "EDGE_ENHANCE" or filter_choice.upper() == "ed":
                    self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
                elif filter_choice.upper() == "EMBOSS" or filter_choice.upper() == "em":
                    self.image = self.image.filter(ImageFilter.EMBOSS)
                elif filter_choice.upper() == "SHARPEN" or filter_choice.upper() == "sh" :
                    self.image = self.image.filter(ImageFilter.SHARPEN)
                self.display_image()

    def change_color(self):
        if self.image:
            color = colorchooser.askcolor()[1]
            if color:
                r, g, b = Image.Image.split(self.image.convert("RGB"))
                self.image = Image.merge("RGB", (r.point(lambda i: i * int(color[1:3], 16) / 255),
                                                 g.point(lambda i: i * int(color[3:5], 16) / 255),
                                                 b.point(lambda i: i * int(color[5:7], 16) / 255)))
                self.display_image()

    def sharpen_image(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            self.display_image()

    def edge_enhance_image(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            self.display_image()

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoEditor(root)
    root.mainloop()
