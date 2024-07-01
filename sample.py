import tkinter as tk
from tkinter import messagebox
import sqlite3

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")

        # Connect to SQLite database
        self.conn = sqlite3.connect('contacts.db')
        self.c = self.conn.cursor()

        # Create contacts table if not exists
        self.c.execute('''CREATE TABLE IF NOT EXISTS contacts 
                        (name TEXT PRIMARY KEY, phone TEXT, email TEXT, age INTEGER, place TEXT)''')
        self.conn.commit()

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Labels and Entry widgets
        self.label_name = tk.Label(self.frame, text="Name:")
        self.label_name.grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(self.frame)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        self.label_phone = tk.Label(self.frame, text="Phone:")
        self.label_phone.grid(row=1, column=0, padx=5, pady=5)
        self.entry_phone = tk.Entry(self.frame)
        self.entry_phone.grid(row=1, column=1, padx=5, pady=5)

        self.label_email = tk.Label(self.frame, text="Email:")
        self.label_email.grid(row=2, column=0, padx=5, pady=5)
        self.entry_email = tk.Entry(self.frame)
        self.entry_email.grid(row=2, column=1, padx=5, pady=5)

        self.label_age = tk.Label(self.frame, text="Age:")
        self.label_age.grid(row=3, column=0, padx=5, pady=5)
        self.entry_age = tk.Entry(self.frame)
        self.entry_age.grid(row=3, column=1, padx=5, pady=5)

        self.label_place = tk.Label(self.frame, text="Place:")
        self.label_place.grid(row=4, column=0, padx=5, pady=5)
        self.entry_place = tk.Entry(self.frame)
        self.entry_place.grid(row=4, column=1, padx=5, pady=5)

        self.button_add = tk.Button(self.frame, text="Add Contact", command=self.add_contact)
        self.button_add.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.button_display = tk.Button(self.frame, text="Display Contacts", command=self.display_contacts)
        self.button_display.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.label_search = tk.Label(self.frame, text="Search:")
        self.label_search.grid(row=7, column=0, padx=5, pady=5)
        self.entry_search = tk.Entry(self.frame)
        self.entry_search.grid(row=7, column=1, padx=5, pady=5)

        self.button_search = tk.Button(self.frame, text="Search Contact", command=self.search_contact)
        self.button_search.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        self.label_delete = tk.Label(self.frame, text="Delete:")
        self.label_delete.grid(row=9, column=0, padx=5, pady=5)
        self.entry_delete = tk.Entry(self.frame)
        self.entry_delete.grid(row=9, column=1, padx=5, pady=5)

        self.button_delete = tk.Button(self.frame, text="Delete Contact", command=self.delete_contact)
        self.button_delete.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

        self.label_update = tk.Label(self.frame, text="Update:")
        self.label_update.grid(row=11, column=0, padx=5, pady=5)
        self.entry_update = tk.Entry(self.frame)
        self.entry_update.grid(row=11, column=1, padx=5, pady=5)

        self.label_new_phone = tk.Label(self.frame, text="New Phone:")
        self.label_new_phone.grid(row=12, column=0, padx=5, pady=5)
        self.entry_new_phone = tk.Entry(self.frame)
        self.entry_new_phone.grid(row=12, column=1, padx=5, pady=5)

        self.label_new_email = tk.Label(self.frame, text="New Email:")
        self.label_new_email.grid(row=13, column=0, padx=5, pady=5)
        self.entry_new_email = tk.Entry(self.frame)
        self.entry_new_email.grid(row=13, column=1, padx=5, pady=5)

        self.label_new_age = tk.Label(self.frame, text="New Age:")
        self.label_new_age.grid(row=14, column=0, padx=5, pady=5)
        self.entry_new_age = tk.Entry(self.frame)
        self.entry_new_age.grid(row=14, column=1, padx=5, pady=5)

        self.label_new_place = tk.Label(self.frame, text="New Place:")
        self.label_new_place.grid(row=15, column=0, padx=5, pady=5)
        self.entry_new_place = tk.Entry(self.frame)
        self.entry_new_place.grid(row=15, column=1, padx=5, pady=5)

        self.button_update = tk.Button(self.frame, text="Update Contact", command=self.update_contact)
        self.button_update.grid(row=16, column=0, columnspan=2, padx=5, pady=5)

        self.button_display_with_email = tk.Button(self.frame, text="Display Contacts with Email", 
                                                   command=self.display_contacts_with_email)
        self.button_display_with_email.grid(row=17, column=0, columnspan=2, padx=5, pady=5)

    def add_contact(self):
        name = self.entry_name.get().title()  # Capitalize the name for consistency
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        age = self.entry_age.get()
        place = self.entry_place.get().title()  # Capitalize the place for consistency

        if name and phone:
            # Insert data into the contacts table
            try:
                self.c.execute("INSERT INTO contacts (name, phone, email, age, place) VALUES (?, ?, ?, ?, ?)", 
                               (name, phone, email, age, place))
                self.conn.commit()
                messagebox.showinfo("Success", "Contact added successfully!")
                self.entry_name.delete(0, tk.END)
                self.entry_phone.delete(0, tk.END)
                self.entry_email.delete(0, tk.END)
                self.entry_age.delete(0, tk.END)
                self.entry_place.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "A contact with this name already exists.")
        else:
            messagebox.showerror("Error", "Please enter both name and phone.")

    def display_contacts(self):
        self.c.execute("SELECT * FROM contacts")
        contacts = self.c.fetchall()
        if contacts:
            contact_list = "\n\n".join([f"Name: {contact[0]}\nPhone: {contact[1]}\nEmail: {contact[2]}\nAge: {contact[3]}\nPlace: {contact[4]}" for contact in contacts])
            messagebox.showinfo("Contacts", contact_list)
        else:
            messagebox.showinfo("Contacts", "No contacts found.")

    def search_contact(self):
        search_term = self.entry_search.get().title()  # Capitalize the search term for consistency
        if search_term:
            self.c.execute("SELECT * FROM contacts WHERE name LIKE ?", ('%' + search_term + '%',))
            contacts = self.c.fetchall()

            if contacts:
                contact_list = "\n\n".join([f"Name: {contact[0]}\nPhone: {contact[1]}\nEmail: {contact[2]}\nAge: {contact[3]}\nPlace: {contact[4]}" for contact in contacts])
                messagebox.showinfo("Search Results", contact_list)
            else:
                messagebox.showinfo("Search Results", f"No contacts found matching '{search_term}'.")
        else:
            messagebox.showerror("Error", "Please enter a name to search.")

    def delete_contact(self):
        name_to_delete = self.entry_delete.get().title()  # Capitalize the name to delete
        if name_to_delete:
            self.c.execute("DELETE FROM contacts WHERE name=?", (name_to_delete,))
            self.conn.commit()
            if self.c.rowcount > 0:
                messagebox.showinfo("Success", "Contact deleted successfully!")
                self.entry_delete.delete(0, tk.END)
            else:
                messagebox.showinfo("Error", "Contact not found.")
        else:
            messagebox.showerror("Error", "Please enter a name to delete.")

    def update_contact(self):
        name_to_update = self.entry_update.get().title()  # Capitalize the name to update
        if name_to_update:
            new_phone = self.entry_new_phone.get()
            new_email = self.entry_new_email.get()
            new_age = self.entry_new_age.get()
            new_place = self.entry_new_place.get().title()  # Capitalize the new place

            if new_phone:
                self.c.execute("UPDATE contacts SET phone=? WHERE name=?", (new_phone, name_to_update))
                self.conn.commit()
            if new_email:
                self.c.execute("UPDATE contacts SET email=? WHERE name=?", (new_email, name_to_update))
                self.conn.commit()
            if new_age:
                self.c.execute("UPDATE contacts SET age=? WHERE name=?", (new_age, name_to_update))
                self.conn.commit()
            if new_place:
                self.c.execute("UPDATE contacts SET place=? WHERE name=?", (new_place, name_to_update))
                self.conn.commit()

            messagebox.showinfo("Success", "Contact updated successfully!")
            self.entry_update.delete(0, tk.END)
            self.entry_new_phone.delete(0, tk.END)
            self.entry_new_email.delete(0, tk.END)
            self.entry_new_age.delete(0, tk.END)
            self.entry_new_place.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a name to update.")

    def display_contacts_with_email(self):
        email_to_display = self.entry_email.get()
        if email_to_display:
            self.c.execute("SELECT * FROM contacts WHERE email=?", (email_to_display,))
            contacts = self.c.fetchall()
            if contacts:
                contact_list = "\n\n".join([f"Name: {contact[0]}\nPhone: {contact[1]}\nEmail: {contact[2]}\nAge: {contact[3]}\nPlace: {contact[4]}" for contact in contacts])
                messagebox.showinfo("Contacts with Email", contact_list)
            else:
                messagebox.showinfo("Contacts with Email", "No contacts with this email found.")
        else:
            messagebox.showerror("Error", "Please enter an email to display contacts.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
