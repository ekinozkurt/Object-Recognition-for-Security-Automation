import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext, font
import json
import re
import sqlite3
from PIL import Image, ImageTk

is_fullscreen = False
fullscreen_button = None
products_window = None
users_window = None
products_window_open = False
users_window_open = False
registered_users = {}
app = None
login_window = None
entry_username = None
entry_password = None
register_window = None



def close_login_window():
    global login_window
    login_window.withdraw()

def reopen_login_window():
    global login_window
    login_window.deiconify()

#kayıt olma
def register():
    def close_register_window():
        
        register_window.destroy()
        reopen_login_window()

    close_login_window()
    register_window = tk.Toplevel()
    register_window.title("Register")
    register_window.protocol("WM_DELETE_WINDOW", reopen_login_window)
    register_window.configure(bg="black")  # Arka plan rengini beyaz yap
    register_window.geometry("750x650")
    register_window.resizable(False, False)
    register_window.update_idletasks()
    x_coordinate = (register_window.winfo_screenwidth() - register_window.winfo_reqwidth()) / 2
    y_coordinate = (register_window.winfo_screenmmheight() - register_window.winfo_reqheight()) / 2
    register_window.geometry("+%d+%d" % (x_coordinate, y_coordinate))
    
    #Arka plan
    try:
        image = Image.open("BackPhoto//regw.jpg")
        image = image.resize((750, 650), Image.BICUBIC)
        background_image = ImageTk.PhotoImage(image)
        background_label = tk.Label(register_window, image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Image upload error:", e)

    registration_frame = Frame(register_window, bg="black")
    registration_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    label_firstname = Label(registration_frame, text="                                          NAME:", bg="black", fg="white", font=("Helvetica",12,"bold"))
    label_firstname.grid(row=0, column=0, padx=5, pady=5)
    entry_firstname = Entry(registration_frame, font=("Helvetica", 12))
    entry_firstname.grid(row=0, column=1, padx=5, pady=5)

    label_lastname = Label(registration_frame, text="                                 SURNAME:", bg="black", fg="white", font=("Helvetica", 12, "bold"))
    label_lastname.grid(row=1, column=0, padx=5, pady=5)
    entry_lastname = Entry(registration_frame, font=("Helvetica", 12))
    entry_lastname.grid(row=1, column=1, padx=5, pady=5)

    label_username = Label(registration_frame, text="                             USERNAME:", bg="black", fg="white", font=("Helvetica", 12, "bold"))
    label_username.grid(row=2, column=0, padx=5, pady=5)
    entry_username = Entry(registration_frame, font=("Helvetica", 12))
    entry_username.grid(row=2, column=1, padx=5, pady=5)

    label_password = Label(registration_frame, text="                             PASSWORD:", bg="black", fg="white", font=("Helvetica", 12, "bold"))
    label_password.grid(row=3, column=0, padx=5, pady=5)
    entry_password = Entry(registration_frame, show="*", font=("Helvetica", 12))
    entry_password.grid(row=3, column=1, padx=5, pady=5)
    
    label_password_confirm = Label(registration_frame, bg="black", fg="white", font=("Helvetica", 12, "bold"))
    label_password_confirm.grid(row=4, column=0, padx=5, pady=5)
    entry_repassword = Entry(registration_frame, show="*", font=("Helvetica", 12))
    entry_repassword.grid(row=4, column=1, padx=5, pady=5)
    
    label_confirm = Label(registration_frame, text ="(Re-enter the password you entered above!)", bg ="black", fg="white", font=("Helvetica", 10))
    label_confirm.grid(row=5, column=1, padx=5, pady=5)

    def toggle_password_visibility():
        current_show_state = entry_password["show"]
        if current_show_state == "*":
            entry_password.config(show="")
            show_password_button.config(image=hide_img, command=toggle_password_visibility)
            entry_repassword.config(show="")
        else:
            entry_password.config(show="*")
            show_password_button.config(image=show_img, command=toggle_password_visibility)
            entry_repassword.config(show="*")
            
    show_img = ImageTk.PhotoImage(Image.open("BackPhoto//opene.jpg").resize((30,30)))
    hide_img = ImageTk.PhotoImage(Image.open("BackPhoto//closede.png").resize((30,30)))
    show_password_button = Button(registration_frame, image=show_img, bg="white", bd=0, command=toggle_password_visibility)
    show_password_button.grid(row=3, column=2, padx=5, pady=5)
    

    label_birthdate = Label(registration_frame, text="BIRTH DATE (GG/AA/YYYY):", bg="black",  fg="white", font=("Helvetica", 12,"bold"))
    label_birthdate.grid(row=6, column=0, padx=5, pady=5)
    entry_birthdate = Entry(registration_frame, font=("Helvetica",12))
    entry_birthdate.grid(row=6, column=1, padx=5, pady=5)

    def add_slash(event):
        entry = event.widget
        value = entry.get()
        if len(value) == 2 or len(value) == 5:
            entry.insert(END, "/")
    
    entry_birthdate.bind("<KeyRelease>", add_slash)
 
    def save_registration_info():

        firstname = entry_firstname.get().capitalize().strip()
        lastname = entry_lastname.get().capitalize().strip()
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        repassword = entry_repassword.get().strip()
        birthdate = entry_birthdate.get().strip()
        
        if password != repassword:
            messagebox.showerror("Error", "The passwords you enter must match in order for you to register!")
            return

        if not firstname or not lastname or not username or not password or not repassword or not birthdate:
            messagebox.showerror("Error", "Please fill in all information completely!")
            return
        
        pattern = r'^\d{2}/\d{2}/\d{4}$'
        if not re.match(pattern, birthdate):
            messagebox.showerror("Error", "The birth date format you entered is invalid. Please re-enter in DD/MM/YYYY format!")
            return
        
        day, month, year = map(int, birthdate.split("/"))
        if month < 1 or month > 12 or day < 1 or day > 31 or year < 0 or year > 9999:
            messagebox.showerror("Error", "The date of birth you entered contains invalid values!")
            return
        
        if not username or not password:
            messagebox.showerror("Warning!", "Please enter username and password!")
        elif username in registered_users:
            messagebox.showerror("Error" , "This user is already registered in the system!")
        else:
            registered_users[username] = password
            save_registered_users()
            messagebox.showinfo("Successful!", "Registration completed successfully")

        register_window.withdraw()
        reopen_login_window()
    
    button_save = Button(registration_frame, text="Save", command=save_registration_info, bg="gray", fg="black")
    button_save.grid(row=7, column=1, padx=5, pady=10)

    button_back = Button(registration_frame, text="Back", command=close_register_window, bg="gray", fg="black")
    button_back.grid(row=7, column=0, padx=5, pady=10)

#giriş yapma

def login():
    global entry_username, entry_password
    username = entry_username.get()
    password = entry_password.get()

    if username in registered_users and registered_users[username] == password:
        messagebox.showinfo("Your login request is successful" , f"Welcome, {username}")
        show_main_page()
        close_login_window()
    else:
        messagebox.showerror("Your login request is negative", "Invalid username or password!")

def show_main_page():
    
    global is_fullscreen, fullscreen_button,app

    app.withdraw()
    main_page =tk.Toplevel()
    main_page.title("Main Screen")
    main_page.geometry("640x412")
    main_page.resizable(False,False)
    
    try:
        image = Image.open("BackPhoto//yan.png")
        image = image.resize((640,412), Image.BICUBIC)
        background_image = ImageTk.PhotoImage(image)
        background_label = tk.Label(main_page, image = background_image)
        background_label.image = background_image
        background_label.pack(fill="both", expand=True)
    except Exception as e:
        print("Image upload error:", e)

    def go_back_to_login():
        main_page.destroy()
        login_window.deiconify()

    button_go_back = tk.Button(main_page, text="Back", command=go_back_to_login, bg="gray", fg="black")
    button_go_back.pack(side=tk.BOTTOM, pady=10)

    def show_products():
        global products_window_open, products_window
        if not products_window_open or not products_window.winfo_exists():
            products_window = tk.Toplevel()
            products_window.title("Products")
            products_window_open = True
            
            x = main_page.winfo_rootx() + main_page.winfo_width()
            y = main_page.winfo_rooty()

            products_window.geometry(f"500x400+{x}+{y}")
            products_window.resizable(False, False)
            
            try:
                image = Image.open("BackPhoto//scam.png")
                image = image.resize((500,400), Image.BICUBIC)
                background_image = ImageTk.PhotoImage(image)
                background_label = tk.Label(products_window, image=background_image)
                background_label.image = background_image
                background_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print("Image upload error:", e)
            
               
            def load_saved_products_from_db():
                db_file = "detected_objects_sqlite3.db"
                try:
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    cursor.execute("SELECT product, category, detection_time FROM detected_objects")
                    products = cursor.fetchall()
                    for product in products:
                        product_name = product[0]
                        category = product[1]
                        detection_time = product[2]
                        text_editor.insert(tk.END, f"Product:", "bold")
                        text_editor.insert(tk.END, f"{product_name}\n", "normal")
                        text_editor.insert(tk.END, f"Category:", "bold")
                        text_editor.insert(tk.END, f"{category}\n", "normal")
                        text_editor.insert(tk.END, f"Detection Time:", "bold")
                        text_editor.insert(tk.END, f"{detection_time}\n\n", "normal")
                    conn.close()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"SQLite error: {e}")
                    
            
            text_editor = scrolledtext.ScrolledText(products_window, wrap=tk.WORD, width = 43, height=50)
            text_editor.pack(pady=5)
            
            bold_font = font.Font(text_editor, text_editor.cget("font"))
            bold_font.configure(weight = "bold")
            text_editor.tag_configure("bold", font = bold_font)
            text_editor.tag_configure("normal", font=("Arial", 10))
                                         
            load_saved_products_from_db()
            
        else:
            products_window.lift()
                        
                
    def show_registered_users():
        global users_window_open , users_window
        if not users_window_open:
            users_window = tk.Toplevel()
            users_window.title("Registered Users")
            users_window_open = True
            button_show_registered_users.update()
            x = 0
            y = 0
            users_window.geometry(f"433x500+{x}+{y}")
            users_window.resizable(False,False)
            background_frame = tk.Frame(users_window)
            background_frame.pack(fill="both", expand=True)
            
            try:
                image = Image.open("BackPhoto//person.png")
                image = image.resize((500,433), Image.BICUBIC)
                background_image = ImageTk.PhotoImage(image)
                background_label = tk.Label(background_frame, image=background_image)
                background_label.image = background_image
                background_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print("Image upload error:", e)

            #Kayıtlı kullanıcıları listeleme
            label_user_list = tk.Label(users_window, text="Registered Users:")
            label_user_list.pack(pady=10)

            listbox_users = tk.Listbox(users_window)
            listbox_users.pack()

            for username in registered_users:
                listbox_users.insert(tk.END, username)
            #Kullanıcı silme özelliği
            def delete_user():
                selected_index = listbox_users.curselection()
                if selected_index:
                    selected_username = listbox_users.get(selected_index)
                    del registered_users[selected_username]
                    listbox_users.delete(selected_index)
                    save_registered_users()
                    messagebox.showinfo("Successful!" ,f"{selected_username} user has been successfully deleted from the system")
                else:
                    messagebox.showerror("Error", "Please select a user!")
                    
            def toggle_delete_button_visibility():
                if entry_username.get() == "admin":
                    button_delete_user.pack(pady=5)
                else:
                    button_delete_user.pack_forget()
                    
            button_delete_user = tk.Button(users_window, text="Delete selected user" , command=delete_user)
            
            def on_users_window_close():
                global users_window_open
                users_window_open = False
                users_window.destroy()
                button_delete_user.destroy()
                    
            users_window.protocol("WM_DELETE_WINDOW", on_users_window_close)
            toggle_delete_button_visibility()
            users_window_open = True
        else:
            users_window.lift()
    
    button_show_products = tk.Button(main_page, text="View Products", command=show_products, bg="gray", fg="black")
    button_show_products.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
    button_show_registered_users = tk.Button(main_page, text="View Registered Users", command=show_registered_users, bg="gray",fg="black")
    button_show_registered_users.place(relx=0.63, rely=0.967, anchor=tk.CENTER)
    button_show_registered_users.bind("<Button-1>", lambda event: toggle_delete_button_visibility())
    
    def toggle_delete_button_visibility():
        if entry_username.get()== "admin":
            button_delete_user.pack(pady=5)
        else:
            button_delete_user.pack_forget()
    

    #ürünler doğru bir şekilde işaretlenip ana sayfa kapandıktan sonra giriş ekranını kapatırken sorulan soru   
    def on_closing_app():
        if messagebox.askokcancel("Exit" ,"Are you sure you want to exit the application?"):
                    app.destroy()
            
    app.protocol("WM_DELETE_WINDOW", on_closing_app)

#kayıt olmuş kullanıcıların verilerinin tutulması
def save_registered_users():
    with open("registered_users.json","w") as file:
        json.dump(registered_users, file)

def load_registered_users():
    try:
        with open("registered_users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    

registered_users = load_registered_users()

def create_login_window():
    global login_window, entry_username, entry_password, app
    
    login_window = tk.Tk()
    login_window.title("Login Screen")
    login_window.geometry("750x650")  # Çerçevenin boyutunu değiştirdik
    login_window.resizable(False, False)

    # Arka plan resmi Canvas'i oluştur
    background_canvas = tk.Canvas(login_window, bg="white", width=600, height=400)  # Canvas boyutunu da değiştirdik
    background_canvas.pack(fill="both", expand=True)

    # Arka plan resmini yerleştir
    image = Image.open("BackPhoto//seclogo.jpg")
    background_image = ImageTk.PhotoImage(image)
    background_canvas.create_image(0, 0, anchor="nw", image=background_image)

    # Ana çerçeve oluştur
    main_frame = tk.Frame(background_canvas, bg="black", width=600, height=400)  # Çerçevenin boyutunu da değiştirdik
    main_frame.place(relx=0.5, rely=0.8, anchor="center")  # Çerçevenin konumunu alt kısma doğru taşıdık

    # Yazıları ortala ve büyüt
    font_style = ("Helvetica", 14)  # Yazı tipi ve boyutu
    label_username = tk.Label(main_frame, text="USER NAME:", bg="black", fg="white", font=font_style)
    label_username.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_username = tk.Entry(main_frame, font=font_style)
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    label_password = tk.Label(main_frame, text="PASSWORD:", bg="black", fg="white", font=font_style)
    label_password.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_password = tk.Entry(main_frame, show="*", font=font_style)
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    # Kayıt ol butonu oluşturulması
    button_register = tk.Button(main_frame, text="REGISTER", command=register, bg="gray", fg="black", font=("Helvetica",11))
    button_register.grid(row=2, column=0, columnspan=2, pady=10)

    # Giriş yap butonu oluşturulması
    button_login = tk.Button(main_frame, text="LOGIN", command=login, bg="gray", fg="black", font=("Helvetica",11))
    button_login.grid(row=3, column=0, columnspan=2, pady=10)
    
    app = login_window
    login_window.mainloop()
    
    
create_login_window()