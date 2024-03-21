import tkinter as tk
from tkinter import messagebox
from aws.dynamodb import create_user, user_exists # Adjusted import statement

def user_login_register():
    global global_user_id
    def on_submit():
        global global_user_id 
        username = username_entry.get()
        if mode.get() == "Login":
            userT = user_exists(username)
            if userT is True:
                messagebox.showerror("Login Failed", "User does not exist.")
                return
            messagebox.showinfo("Login Successful", f"Welcome {username}!")
            global_user_id = username
            login_register_window.destroy()
        elif mode.get() == "Register":
            try:
                create_user(username)
                messagebox.showinfo("Registration Successful", f"You have been registered successfully.")
                global_user_id = username
                login_register_window.destroy()
            except Exception as e:
                messagebox.showerror("Registration Failed", str(e))

    login_register_window = tk.Tk()
    login_register_window.title("Login / Register")
    login_register_window.geometry("500x500")

    tk.Label(login_register_window, text="Username:").pack()
    username_entry = tk.Entry(login_register_window)
    username_entry.pack()

    tk.Label(login_register_window, text="Password:").pack()
    password_entry = tk.Entry(login_register_window, show="*")
    password_entry.pack()

    mode = tk.StringVar(value="Login")
    tk.Radiobutton(login_register_window, text="Login", variable=mode, value="Login").pack()
    tk.Radiobutton(login_register_window, text="Register", variable=mode, value="Register").pack()

    submit_button = tk.Button(login_register_window, text="Submit", command=on_submit)
    submit_button.pack()
    login_register_window.mainloop()
    return global_user_id
    

if __name__ == '__main__':
    user_login_register()