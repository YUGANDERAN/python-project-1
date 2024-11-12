import tkinter as tk
import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import geocoder
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

class CarRentalApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600")
        self.root.title("Car Rental Booking")
        self.root.resizable(False, False)

        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

        self.canvas = tk.Canvas(self.root, width=1000, height=600, bd=0, highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)

        image_paths = ["./assets/image1.jpg", "./assets/image2.jpg", "./assets/image3.jpg"]
        self.background_images = self.load_images(image_paths)

        self.images_on_canvas = []
        if self.background_images:
            self.setup_images_on_canvas()
            self.slide_background()

        self.selected_location = None
        self.create_ui()

    def load_images(self, image_paths):
        images = []
        for path in image_paths:
            try:
                img = Image.open(path)
                img = img.resize((1000, 600))
                images.append(ImageTk.PhotoImage(img))
            except FileNotFoundError:
                print(f"Image file not found: {path}")
        return images

    def setup_images_on_canvas(self):
        if not self.background_images:
            return

        total_width = 0
        for img in self.background_images:
            image_id = self.canvas.create_image(total_width, 0, image=img, anchor=tk.NW)
            self.images_on_canvas.append(image_id)
            total_width += img.width()

    def slide_background(self):
        if not self.images_on_canvas:
            return

        for image_id in self.images_on_canvas:
            self.canvas.move(image_id, -2, 0)

        first_image_x = self.canvas.coords(self.images_on_canvas[0])[0]
        if first_image_x < -self.background_images[0].width():
            self.canvas.move(self.images_on_canvas[0], len(self.background_images) * self.background_images[0].width(), 0)
            self.images_on_canvas.append(self.images_on_canvas.pop(0))

        self.root.after(30, self.slide_background)

    def create_ui(self):
        frame = customtkinter.CTkFrame(master=self.root, width=700, height=500, corner_radius=20)
        frame.pack(pady=50, padx=50, fill="both", expand=True)

        self.form_frame = customtkinter.CTkFrame(master=frame, width=500, height=600, corner_radius=20)
        self.form_frame.pack(side="left", fill="both", padx=20, pady=20, expand=True)

        title = customtkinter.CTkLabel(master=self.form_frame, text="Enter Details To Search", font=("Helvetica", 20))
        title.pack(pady=6, padx=55)

        self.create_form_elements(self.form_frame)

        self.image_placeholder = customtkinter.CTkLabel(master=frame, text="")
        self.image_placeholder.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        self.load_right_image()

    def create_form_elements(self, parent):
        self.create_label_and_entry(parent, "Name:", "your name", "email")

        self.location_entry = customtkinter.CTkEntry(master=parent, placeholder_text="Location will be fetched or enter manually")
        self.location_entry.pack(pady=(10, 10), padx=(0, 10), anchor="w", fill="x")

        fetch_location_button = customtkinter.CTkButton(master=parent, text="Fetch Current Location", command=self.fetch_location)
        fetch_location_button.pack(pady=(0, 10), anchor="w")

        label_car_type = customtkinter.CTkLabel(master=parent, text="Car Type:")
        label_car_type.pack(pady=(5, 0), anchor="w")
        self.combo_car_type = customtkinter.CTkComboBox(master=parent, values=["Sedan", "SUV", "Truck", "Convertible"])
        self.combo_car_type.pack(pady=(0, 5), padx=(0, 10), anchor="w", fill="x")

        label_start_date = customtkinter.CTkLabel(master=parent, text="Start Date:")
        label_start_date.pack(pady=(10, 0), anchor="w")
        self.entry_start_date = DateEntry(parent, date_pattern="yyyy-mm-dd")
        self.entry_start_date.pack(pady=(0, 10), padx=(0, 10), anchor="w", fill="x")

        label_end_date = customtkinter.CTkLabel(master=parent, text="End Date:")
        label_end_date.pack(pady=(10, 0), anchor="w")
        self.entry_end_date = DateEntry(parent, date_pattern="yyyy-mm-dd")
        self.entry_end_date.pack(pady=(0, 10), padx=(0, 10), anchor="w", fill="x")

        submit_button = customtkinter.CTkButton(master=parent, text="Proceed to Payment", command=self.open_payment_page, width=40)
        submit_button.pack(pady=10, padx=(10, 10), anchor="e")

    def create_label_and_entry(self, parent, label_text, placeholder_text, entry_name):
        label = customtkinter.CTkLabel(master=parent, text=label_text)
        label.pack(pady=(10, 0), anchor="w")
        setattr(self, f"entry_{entry_name}", customtkinter.CTkEntry(master=parent, placeholder_text=placeholder_text))
        getattr(self, f"entry_{entry_name}").pack(pady=(0, 10), padx=(0, 10), anchor="w", fill="x")

    def load_right_image(self):
        try:
            image = Image.open("./assets/loginlog.jpg")
            image = image.resize((600, 500))
            photo = ImageTk.PhotoImage(image)
            self.image_placeholder.configure(image=photo)
            self.image_placeholder.image = photo
        except FileNotFoundError:
            print("Image for right side not found")

    def fetch_location(self):
        g = geocoder.ip('me')
        if g.ok:
            self.selected_location = g.address
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, self.selected_location)
        else:
            messagebox.showwarning("Location Error", "Could not fetch location. Please enter manually.")

    def open_payment_page(self):
        self.payment_window = tk.Toplevel(self.root)
        self.payment_window.title("Payment")
        self.payment_window.geometry("400x400")

        customtkinter.CTkLabel(self.payment_window, text="Select Payment Method", font=("Helvetica", 16)).pack(pady=10)

        self.payment_method = tk.StringVar(value="Card")
        payment_options = [("Card Payment", "Card"), ("UPI Payment", "UPI"), ("Cash on Arrival", "Cash")]
        for text, value in payment_options:
            customtkinter.CTkRadioButton(self.payment_window, text=text, variable=self.payment_method, value=value, command=self.update_payment_fields).pack(anchor="w", padx=20, pady=5)

        self.payment_frame = customtkinter.CTkFrame(self.payment_window)
        self.payment_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.update_payment_fields()

        confirm_button = customtkinter.CTkButton(self.payment_window, text="Confirm Payment", command=self.confirm_payment)
        confirm_button.pack(pady=20)

    def update_payment_fields(self):
        for widget in self.payment_frame.winfo_children():
            widget.destroy()

        if self.payment_method.get() == "Card":
            customtkinter.CTkLabel(self.payment_frame, text="Card Number").pack(anchor="w", pady=5)
            customtkinter.CTkEntry(self.payment_frame, placeholder_text="Card Number").pack(fill="x", pady=5)
            customtkinter.CTkLabel(self.payment_frame, text="Expiration Date (MM/YY)").pack(anchor="w", pady=5)
            customtkinter.CTkEntry(self.payment_frame, placeholder_text="MM/YY").pack(fill="x", pady=5)
            customtkinter.CTkLabel(self.payment_frame, text="CVV").pack(anchor="w", pady=5)
            customtkinter.CTkEntry(self.payment_frame, placeholder_text="CVV").pack(fill="x", pady=5)

        elif self.payment_method.get() == "UPI":
            customtkinter.CTkLabel(self.payment_frame, text="Enter UPI ID").pack(anchor="w", pady=5)
            customtkinter.CTkEntry(self.payment_frame, placeholder_text="UPI ID").pack(fill="x", pady=5)

        elif self.payment_method.get() == "Cash":
            customtkinter.CTkLabel(self.payment_frame, text="Cash on Arrival Selected.").pack(anchor="w", pady=5)
            customtkinter.CTkLabel(self.payment_frame, text="Please proceed with cash payment at the time of pickup.").pack(anchor="w", pady=5)

    def confirm_payment(self):
        self.payment_window.destroy()
        messagebox.showinfo("Payment Confirmation", "Your payment has been confirmed!")

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CarRentalApp(root)
    root.mainloop()
