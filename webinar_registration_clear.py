class Contact:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f"Contact(Name: {self.name}, Email: {self.email}, Phone: {self.phone})"

class Lead:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f"Lead(Name: {self.name}, Email: {self.email}, Phone: {self.phone})"

def process_registration(contacts, leads, registrant):
    email = registrant['email']
    phone = registrant['phone']
    name = registrant['name']
    # Contact Part
    for contact in contacts:
        if contact.email == email:
            if contact.phone is None and phone:
                contact.phone = phone
            return
        if contact.phone == phone:
            if contact.email is None and email:
                contact.email = email
            return
    # Lead Part
    for lead in leads:
        if lead.email == email:
            leads.remove(lead)
            contacts.append(Contact(name=name or lead.name, email=email, phone=lead.phone))
            return
        if lead.phone == phone:
            leads.remove(lead)
            contacts.append(Contact(name=name or lead.name, email=lead.email, phone=phone))
            return
    contacts.append(Contact(name=name, email=email, phone=phone))

# Initial Data
contacts = [
    Contact("Alice Brown", None, "1231112223"),
    Contact("Bob Crown", "bob@crowns.com", None),
    Contact("Carlos Drew", "carl@drewess.com", "3453334445"),
    Contact("Doug Emerty", None, "4564445556"),
    Contact("Egan Fair", "eg@fairness.com", "5675556667")
]

leads = [
    Lead(None, "kevin@keith.com", None),
    Lead("Lucy", "lucy@liu.com", "3210001112"),
    Lead("Mary Middle", "mary@middle.com", "3331112223"),
    Lead(None, None, "4442223334"),
    Lead(None, "ole@olson.com", None)
]

# NEW Registers
registrants = [
    {"name": "Aldo Nerio", "email": "aldo.nerio@gmail.com", "phone": 8712837858},
    {"name": "Doug", "email": "doug@emmy.com", "phone": "4564445556"},
    {"name": "Uma Thurman", "email": "uma@thurs.com", "phone": None},
    {"name": "Lucy Liu", "email": "lucy@liu.com", "phone": None},
    {"name": "Aldo Test", "email": "aldo.test@gmail.com", "phone": None},
    {"name": "Aldo", "email": "aldo.test@gmail.com", "phone": 8712837859},
    {"name": "Augusto", "email": "augusto@gmail.com", "phone": 8712837857},
    {"name": None, "email": None, "phone": None}
]

for registrant in registrants:
    process_registration(contacts, leads, registrant)

print("Contacts Resgisters:")
for contact in contacts:
    print(contact)

print("\nLeads:")
for lead in leads:
    print(lead)
