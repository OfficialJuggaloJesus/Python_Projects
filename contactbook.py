import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __str__(self):
        return f"Name: {self.name}\nPhone: {self.phone}\nEmail: {self.email}\nAddress: {self.address}"

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }

contacts = []

def load_contacts():
    global contacts
    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as file:
            contacts_data = json.load(file)
            contacts = [Contact(**data) for data in contacts_data]

def save_contacts():
    with open("contacts.json", "w") as file:
        contacts_data = [contact.to_dict() for contact in contacts]
        json.dump(contacts_data, file)

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    
    if name and phone and email and address:
        contact = Contact(name, phone, email, address)
        contacts.append(contact)
        messagebox.showinfo("Success", "Contact added successfully.")
        clear_fields()
        save_contacts()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

def view_contacts():
    if not contacts:
        messagebox.showinfo("No Contacts", "No contacts found.")
        return
    contact_list.delete(1.0, tk.END)
    for contact in contacts:
        contact_list.insert(tk.END, str(contact) + "\n\n")

def search_contact():
    search_name = search_entry.get()
    if not search_name:
        messagebox.showwarning("Input Error", "Please enter a name to search.")
        return
    found_contacts = [contact for contact in contacts if search_name.lower() in contact.name.lower()]
    if not found_contacts:
        messagebox.showinfo("No Contact", "No contact found with that name.")
        return
    contact_list.delete(1.0, tk.END)
    for contact in found_contacts:
        contact_list.insert(tk.END, str(contact) + "\n\n")

def update_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name to update.")
        return
    
    for contact in contacts:
        if contact.name.lower() == name.lower():
            if phone:
                contact.phone = phone
            if email:
                contact.email = email
            if address:
                contact.address = address
            messagebox.showinfo("Success", "Contact updated successfully.")
            clear_fields()
            save_contacts()
            return
    
    messagebox.showinfo("No Contact", "No contact found with that name.")

def delete_contact():
    name = search_entry.get()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name to delete.")
        return
    global contacts
    contacts = [contact for contact in contacts if contact.name.lower() != name.lower()]
    messagebox.showinfo("Success", "Contact deleted successfully.")
    clear_fields()
    save_contacts()
    contact_list.delete(1.0, tk.END)

def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)

# Setup GUI
root = tk.Tk()
root.title("Contact Book")
root.configure(bg="black")

# Frames for better layout
input_frame = tk.Frame(root, bg="black")
input_frame.grid(row=0, column=0, padx=10, pady=10)

button_frame = tk.Frame(root, bg="black")
button_frame.grid(row=0, column=1, padx=10, pady=10)

search_frame = tk.Frame(root, bg="black")
search_frame.grid(row=1, column=0, padx=10, pady=10)

list_frame = tk.Frame(root, bg="black")
list_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Input fields
tk.Label(input_frame, text="Name", bg="black", fg="red").grid(row=0, column=0)
name_entry = tk.Entry(input_frame, bg="black", fg="red")
name_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Phone", bg="black", fg="red").grid(row=1, column=0)
phone_entry = tk.Entry(input_frame, bg="black", fg="red")
phone_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Email", bg="black", fg="red").grid(row=2, column=0)
email_entry = tk.Entry(input_frame, bg="black", fg="red")
email_entry.grid(row=2, column=1)

tk.Label(input_frame, text="Address", bg="black", fg="red").grid(row=3, column=0)
address_entry = tk.Entry(input_frame, bg="black", fg="red")
address_entry.grid(row=3, column=1)

# Buttons
tk.Button(button_frame, text="Add Contact", command=add_contact, bg="black", fg="red").grid(row=0, column=0, pady=10)
tk.Button(button_frame, text="View Contacts", command=view_contacts, bg="black", fg="red").grid(row=1, column=0, pady=10)
tk.Button(button_frame, text="Search Contact", command=search_contact, bg="black", fg="red").grid(row=2, column=0, pady=10)
tk.Button(button_frame, text="Update Contact", command=update_contact, bg="black", fg="red").grid(row=3, column=0, pady=10)
tk.Button(button_frame, text="Delete Contact", command=delete_contact, bg="black", fg="red").grid(row=4, column=0, pady=10)
tk.Button(button_frame, text="Exit", command=root.quit, bg="black", fg="red").grid(row=5, column=0, pady=10)

# Search field
tk.Label(search_frame, text="Search by Name", bg="black", fg="red").grid(row=0, column=0)
search_entry = tk.Entry(search_frame, bg="black", fg="red")
search_entry.grid(row=0, column=1)

# Scrollable Text Area for Displaying Contacts
contact_list = tk.Text(list_frame, width=60, height=15, bg="black", fg="red")
scrollbar = tk.Scrollbar(list_frame, command=contact_list.yview, bg="black")
contact_list.config(yscrollcommand=scrollbar.set)
contact_list.grid(row=0, column=0)
scrollbar.grid(row=0, column=1, sticky='ns')

# Load contacts from file
load_contacts()

# Start the GUI loop
root.mainloop()
