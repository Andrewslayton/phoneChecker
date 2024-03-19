import tkinter as tk
from tkinter import messagebox
from aws.dynamodb import create_user  # Adjusted import statement

def user_login_register():
    def on_submit():
        username = username_entry.get()
        password = password_entry.get()
        if mode.get() == "Login":
            messagebox.showinfo("Feature Not Implemented", "Login functionality is not implemented yet.")
            
            login_register_window.destroy()
        elif mode.get() == "Register":
            try:
                user_id = create_user(username, password)
                messagebox.showinfo("Registration Successful", f"You have been registered successfully.\nUser ID: {user_id}")
                login_register_window.destroy()
            except Exception as e:
                messagebox.showerror("Registration Failed", str(e))

    login_register_window = tk.Tk()
    login_register_window.title("Login / Register")
    login_register_window.geometry("300x150")

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

if __name__ == '__main__':
    user_login_register()