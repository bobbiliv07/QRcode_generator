import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk 

class QRCodeApp:
    def __init__(self, master):
        self.master = master
        master.title("QR Code Generator")
        master.geometry("500x700") # Initial window size
        master.resizable(False, False) # Prevent resizing for simplicity

        # Main frame for padding
        self.main_frame = ttk.Frame(master, padding="20 20 20 20")
        self.main_frame.pack(fill="both", expand=True)

        # Input Section
        self.input_label = ttk.Label(self.main_frame, text="Enter Text or URL:")
        self.input_label.pack(pady=(10, 5))

        self.input_text = tk.StringVar()
        self.input_entry = ttk.Entry(self.main_frame, textvariable=self.input_text, width=50)
        self.input_entry.pack(pady=5)
        self.input_entry.bind("<Return>", self.generate_qr_event) # Bind Enter key to generate

        # Save File Name Section
        self.filename_label = ttk.Label(self.main_frame, text="Save As (e.g., my_qrcode.png):")
        self.filename_label.pack(pady=(10, 5))

        self.filename_text = tk.StringVar(value="my_qrcode.png") # Default filename
        self.filename_entry = ttk.Entry(self.main_frame, textvariable=self.filename_text, width=50)
        self.filename_entry.pack(pady=5)

        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=20)

        self.generate_button = ttk.Button(self.button_frame, text="Generate QR Code", command=self.generate_qr)
        self.generate_button.pack(side="left", padx=10)

        self.save_button = ttk.Button(self.button_frame, text="Save QR Code", command=self.save_qr, state="disabled")
        self.save_button.pack(side="left", padx=10)

        # QR Code Display Area
        self.qr_label = ttk.Label(self.main_frame)
        self.qr_label.pack(pady=20)

        self.qr_image = None # To hold the PIL Image object
        self.tk_qr_image = None # To hold the PhotoImage object for Tkinter

    def generate_qr_event(self, event=None):
        # This function is called when the generate button is clicked or Enter is pressed
        self.generate_qr()

    def generate_qr(self):
        data = self.input_text.get()
        if not data:
            messagebox.showwarning("Input Error", "Please enter some text or a URL to generate a QR code.")
            return

        try:
            # Create a QR code instance
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Create PIL Image from QR code
            self.qr_image = qr.make_image(fill_color="black", back_color="white").convert('RGB')

            # Resize image to fit display area if needed (e.g., max 300x300)
            max_size = 300
            current_width, current_height = self.qr_image.size
            if current_width > max_size or current_height > max_size:
                ratio = min(max_size / current_width, max_size / current_height)
                new_width = int(current_width * ratio)
                new_height = int(current_height * ratio)
                self.qr_image = self.qr_image.resize((new_width, new_height), Image.LANCZOS)


            # Convert PIL Image to Tkinter PhotoImage
            self.tk_qr_image = ImageTk.PhotoImage(self.qr_image)

            # Display the QR code in the label
            self.qr_label.config(image=self.tk_qr_image)
            self.qr_label.image = self.tk_qr_image # Keep a reference!

            self.save_button.config(state="normal") # Enable save button
            messagebox.showinfo("Success", "QR Code generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR Code: {e}")
            self.save_button.config(state="disabled")

    def save_qr(self):
        if self.qr_image is None:
            messagebox.showwarning("Save Error", "No QR code has been generated yet.")
            return

        initial_filename = self.filename_text.get()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=initial_filename,
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )

        if file_path:
            try:
                self.qr_image.save(file_path)
                messagebox.showinfo("Success", f"QR Code saved as:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save QR Code: {e}")

# Create the main window
root = tk.Tk()
app = QRCodeApp(root)
root.mainloop()
