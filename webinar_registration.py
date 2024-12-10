import json
from typing import List, Optional, Dict, Union

class Contact:
    def __init__(self, name: str, email: Optional[str] = None, phone: Optional[str] = None):
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self) -> Dict[str, Union[str, None]]:
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }

class Lead:
    def __init__(self, name: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None):
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self) -> Dict[str, Union[str, None]]:
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }

class WebinarRegistration:
    def __init__(self):
        self.contacts: List[Contact] = [
            Contact(name="Alice Brown", phone="1231112223"),
            Contact(name="Bob Crown", email="bob@crowns.com"),
            Contact(name="Carlos Drew", email="carl@drewess.com", phone="3453334445"),
            Contact(name="Doug Emerty", phone="4564445556"),
            Contact(name="Egan Fair", email="eg@fairness.com", phone="5675556667")
        ]
        self.leads: List[Lead] = [
            Lead(email="kevin@keith.com"),
            Lead(name="Lucy", email="lucy@liu.com", phone="3210001112"),
            Lead(name="Mary Middle", email="mary@middle.com", phone="3331112223"),
            Lead(phone="4442223334"),
            Lead(email="ole@olson.com")
        ]
    
    def process_registration(self, registration: Dict[str, Optional[str]]) -> Optional[Contact]:
        name, email, phone = registration.get("name"), registration.get("email"), registration.get("phone")

        def _find_by_attribute(data_list, attr, value):
            return next((item for item in data_list if getattr(item, attr) == value), None)
        # Contact Part
        if email or phone:
            contact_email = _find_by_attribute(self.contacts, 'email', email)
            if contact_email:
                if phone and not contact_email.phone:
                    contact_email.phone = phone
                return None
            contact_phone = _find_by_attribute(self.contacts, 'phone', phone)
            if contact_phone:
                if email and not contact_phone.email:
                    contact_phone.email = email
                return None
        # Lead Part
        if email or phone:
            lead_email = _find_by_attribute(self.leads, 'email', email)
            if lead_email:
                self.leads.remove(lead_email)
                new_contact = Contact(name=name or lead_email.name, email=email, phone=phone or lead_email.phone)
                self.contacts.append(new_contact)
                return new_contact
            lead_phone = _find_by_attribute(self.leads, 'phone', phone)
            if lead_phone:
                self.leads.remove(lead_phone)
                new_contact = Contact(name=name or lead_phone.name, email=email or lead_phone.email, phone=phone)
                self.contacts.append(new_contact)
                return new_contact
        new_contact = Contact(name=name, email=email, phone=phone)
        self.contacts.append(new_contact)
        return new_contact

    def display_contacts(self):
        print("\nContacts:")
        for contact in self.contacts:
            print(f"Name: {contact.name}, Email: {contact.email}, Phone: {contact.phone}")

    def display_leads(self):
        print("\nLeads:")
        for lead in self.leads:
            print(f"Name: {lead.name}, Email: {lead.email}, Phone: {lead.phone}")

    def menu(self):
        print("Webinar Registration")
        while True:
            print("\nOptions:")
            print("\033[1;32m1. Register a New Person\033[0m")
            print("2. Display Contacts")
            print("3. Display Leads")
            print("\033[1;31m4. Save and Exit\033[0m")
            choice = input("Choose an option: ")
            if choice == "1":
                name = input("\033[1;34mEnter Name: \033[0m").strip() or None
                email = input("\033[1;34mEnter Email: \033[0m").strip() or None
                phone = input("\033[1;34mEnter Phone: \033[0m").strip() or None
                registrant = {
                    "name": name,
                    "email": email,
                    "phone": phone
                }
                new_contact = self.process_registration(registrant)
                if new_contact:
                    print(
                        f"\033[1;32mNew Contact Created:\033[0m Name: \033[1;34m{new_contact.name}\033[0m, "
                        f"Email: \033[1;35m{new_contact.email}\033[0m, Phone: \033[1;36m{new_contact.phone}\033[0m"
                    )
                else:
                    print("Registrant has been successfully updated!!!")
            elif choice == "2":
                self.display_contacts()
            elif choice == "3":
                self.display_leads()
            elif choice == "4":
                print("Exiting the Program")
                break
            else:
                print("Invalid option. Please try again")

if __name__ == "__main__":
    WebinarRegistration().menu()
