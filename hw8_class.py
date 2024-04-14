from collections import UserDict
from datetime import datetime, timedelta

class Field:    
    def __init__(self, value):
        if self.is_valid(value):
            self.value = value            
        else:
            return None
        
    def is_valid(self, value):
        return True
        
    def __str__(self):
        return str(self.value)
    

class Name(Field):
    # реалізація класу
    	pass


class Phone(Field):
    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()
    
    
class Birthday(Field):
    def is_valid(self, value):
        datetime.strptime(value, "%d.%m.%Y")
        return True
    
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        if self.find_phone(new_phone.value):
            pass
        else:
            self.phones.append(new_phone)
            return new_phone        
           
    def find_phone(self, f_phone):
        for num in self.phones:
            if num.value == f_phone:
                return num
        else:
            return None            
    
    def remove_phone(self, phone_del_number):
        if self.find_phone(phone_del_number):
            phone = self.find_phone(phone_del_number)
            self.phones.remove(phone)
        else:
            return None

    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
        else:
            return None          
    
    def __str__(self):
        return f"Contact name: {str(self.name.value)}, phones: {'; '.join(str(p) for p in self.phones)} birthday: {str(self.birthday)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        if name in self.data:
            return self.data.get(name)
        else:
            return None

    def delete(self, name):
        if name in self.data:
            return self.data.pop(name)
        else:
            return None    
    
# -----------------------------------------------------  
    @staticmethod
    def now_year(book): 
        today = datetime.today().date()
        birthday_this_year = []        
        for record in book.values():
            birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday = birthday.replace(year=today.year)
            if birthday < today and birthday.weekday() < 5: 
                birthday = birthday.replace(year=today.year + 1)
            birthday_this_year.append({"name": record.name.value, "birthday": birthday})
        return birthday_this_year
    
    @staticmethod
    def week(book): 
        birthday_week = []
        for user in book:
            if user["birthday"].weekday() == 5:
                perenos_day5 = timedelta(days=2)
                user["birthday"] = user["birthday"] + perenos_day5
            elif user["birthday"].weekday() == 6:
                perenos_day6 = timedelta(days=1)
                user["birthday"] = user["birthday"] + perenos_day6
            birthday_week.append({"name": user['name'], "birthday": user["birthday"]})
        return birthday_week
    
    @staticmethod
    def get_upcoming_birthdays(book): 
        today = datetime.today().date()
        upcoming_birthdays = []    
        updated_users = AddressBook.now_year(book)
        for user in AddressBook.week(updated_users):
            delta = user["birthday"].toordinal() - today.toordinal()
            if 0 <= delta <= 7:
                birthday_str = user["birthday"].strftime('%d.%m.%Y') 
                upcoming_birthdays.append({"name": user['name'], "congratulation_date": birthday_str})
        return upcoming_birthdays
# -----------------------------------------------------
        
    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())
        
