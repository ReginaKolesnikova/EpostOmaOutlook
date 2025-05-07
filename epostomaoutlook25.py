import smtplib
import ssl
from email.message import EmailMessage
import imghdr
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pickle

#main window
root = Tk()
root.title("Email sender")
root.geometry("500x600")

#global variable (to store file)
file = None

# sending email
def send_email():
    recipient = email_box.get().split(",")  # multiple recievers separated by "," (also may be one reciever)
    message_content = message_box.get("1.0", END)
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "rkolesnikova251@gmail.com"
    password = "gkcp vlni xlnt pfla" #hide it
    context = ssl.create_default_context()
    msg = EmailMessage()
    msg.set_content(message_content)
    msg['Subject'] = "Sending an Email"
    msg['From'] = "Regina Kolesnikova"
    msg['To'] = ", ".join(recipient)
    
    # add the image if it exists
    if file:
        with open(file, 'rb') as f:
            image = f.read()
        msg.add_attachment(image, maintype='image', subtype=imghdr.what(None, image))
    
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)
        server.login(sender_email, password)
        server.send_message(msg)
        messagebox.showinfo("Information", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error occurred!", str(e))
    finally:
        server.quit()

# Attach a file (image) function
def attach_image():
    global file
    file = filedialog.askopenfilename()
    label_file_attached.configure(text=file)

# Preview email function
def preview_email():
    preview_window = Toplevel(root)
    preview_window.title("Email preview")
    preview_window.geometry("400x400")
    preview_label = Label(preview_window, text=message_box.get("1.0", END))
    preview_label.pack()

# Save draft function
def save_draft():
    draft = message_box.get("1.0", END)
    with open("draft.pkl", "wb") as f:
        pickle.dump(draft, f)

# Load draft function
def load_draft():
    try:
        with open("draft.pkl", "rb") as f:
            draft = pickle.load(f)
            message_box.insert(END, draft)
    except FileNotFoundError:
        pass

# Clear form function
def clear_form():
    email_box.delete(0, END)
    message_box.delete("1.0", END)
    label_file_attached.configure(text="No file attached.")

# labels and input fields
email_label = Label(root, text="To: (separate with commas if multiple recievers)")
email_label.pack(pady=5)
email_box = Entry(root, width=40)
email_box.pack(pady=5)

message_label = Label(root, text="Message text: ")
message_label.pack(pady=5)
message_box = Text(root, height=10, width=40)
message_box.pack(pady=5)

label_file_attached = Label(root, text="No file attached.")
label_file_attached.pack(pady=5)

# buttons (for actions)
attach_button = Button(root, text="Attach image", command=attach_image)
attach_button.pack(pady=5)

send_button = Button(root, text="Send email", command=send_email)
send_button.pack(pady=5)

preview_button = Button(root, text="Preview email", command=preview_email)
preview_button.pack(pady=5)

save_draft_button = Button(root, text="Save draft", command=save_draft)
save_draft_button.pack(pady=5)

load_draft_button = Button(root, text="Load draft", command=load_draft)
load_draft_button.pack(pady=5)

clear_button = Button(root, text="Clear form", command=clear_form)
clear_button.pack(pady=5)

# adding a loading bar for sending email
def send_email_with_loading():
    loading_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
    loading_bar.pack(pady=10)
    loading_bar.start()
    
    send_email()  # call the send email function
    
    loading_bar.stop()
    loading_bar.pack_forget()

# replace the send button with one that includes the loading bar
send_button.config(command=send_email_with_loading)

# starts Tkinter main loop
root.mainloop()
