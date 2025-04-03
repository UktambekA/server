import pandas as pd
import numpy as np
import os
import hashlib
from datetime import datetime, timedelta
import random

# Ma'lumotlar jildi
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Foydalanuvchilar faylini yaratish
def create_users_file():
    users_file = os.path.join(DATA_DIR, "users.csv")
    
    # Admin foydalanuvchisi uchun
    admin_password = hashlib.sha256("admin".encode()).hexdigest()
    
    # Test foydalanuvchisi uchun
    test_password = hashlib.sha256("test123".encode()).hexdigest()
    
    users_df = pd.DataFrame({
        "username": ["admin", "test"],
        "password": [admin_password, test_password]
    })
    
    users_df.to_csv(users_file, index=False)
    print(f"Foydalanuvchilar fayli yaratildi: {users_file}")

# Fakultetlar ro'yxati
FACULTIES = [
    "Kompyuter injiniringi",
    "Axborot texnologiyalari",
    "Telekommunikatsiya",
    "Dasturiy injiniring",
    "Elektron tijorat",
    "Raqamli iqtisodiyot"
]

# Ismlar ro'yxati
FIRST_NAMES = [
    "Abror", "Alisher", "Aziz", "Bobur", "Davron", "Elyor", "Farrukh", "Gayrat", 
    "Humoyun", "Ikrom", "Jahongir", "Kamol", "Laziz", "Mansur", "Nodir", "Otabek", 
    "Pulat", "Qodir", "Rustam", "Sardor", "Temur", "Umid", "Valijon", "Xurshid", 
    "Yusuf", "Zafar", "Aziza", "Barno", "Charos", "Dilnoza", "Erkinoy", "Feruza", 
    "Gulnora", "Hulkar", "Iroda", "Jamila", "Kamola", "Lola", "Malika", "Nilufar", 
    "Ozoda", "Parizoda", "Qunduz", "Rayhona", "Sabina", "Tahmina", "Umida", "Vasila", 
    "Xurshida", "Yulduz", "Zarina"
]

# Familiyalar ro'yxati
LAST_NAMES = [
    "Abdullayev", "Bahodiriy", "Choriyev", "Davronov", "Ergashev", "Fayziyev", 
    "G'ofurov", "Hakimov", "Islomov", "Jo'rayev", "Karimov", "Latipov", "Mahmudov", 
    "Nishonov", "Olimov", "Po'latov", "Qodirov", "Rahmonov", "Salimov", "Tojiboev", 
    "Umarov", "Vohidov", "Xolmatov", "Yusupov", "Zokirov", "Ahmedova", "Berdiyeva", 
    "Choriyeva", "Davronova", "Ergasheva", "Fayziyeva", "G'ofurova", "Hakimova", 
    "Islomova", "Jo'rayeva", "Karimova", "Latipova", "Mahmudova", "Nishonova", 
    "Olimova", "Po'latova", "Qodirova", "Rahmonova", "Salimova", "Tojiboyeva", 
    "Umarova", "Vohidova", "Xolmatova", "Yusupova", "Zokirova"
]

# Telefon raqamlarini yaratish funksiyasi
def generate_phone_number():
    operators = ["90", "91", "93", "94", "97", "98", "99", "33", "88"]
    operator = random.choice(operators)
    number = ''.join(random.choices('0123456789', k=7))
    return f"+998 {operator} {number[:3]}-{number[3:]}"

# Guruh nomlarini yaratish funksiyasi
def generate_group_name(year):
    group_types = ["AT", "KIF", "DI", "TI", "AA", "RI", "ET"]
    group_type = random.choice(group_types)
    group_number = random.randint(1, 12)
    last_digits = str(year)[-2:]  # yilning oxirgi 2 raqami
    return f"{group_type}-{group_number}{last_digits}"

# Talabalar ma'lumotlarini yaratish
def create_students_data(start_year=2021, end_year=2025):
    for year in range(start_year, end_year + 1):
        # Har yil uchun tasodifiy talabalar sonini aniqlash
        num_students = random.randint(50, 200)
        
        students_data = []
        for i in range(1, num_students + 1):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            faculty = random.choice(FACULTIES)
            group = generate_group_name(year)
            phone = generate_phone_number()
            
            # Ro'yxatga olish sanasi - shu yilning tasodifiy kuni
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
            registration_date = start_date + (end_date - start_date) * random.random()
            registration_date_str = registration_date.strftime("%Y-%m-%d %H:%M:%S")
            
            students_data.append({
                "ID": i,
                "Ism": first_name,
                "Familiya": last_name,
                "Guruh": group,
                "Fakultet": faculty,
                "Telefon": phone,
                "Kiritilgan sana": registration_date_str
            })
        
        # Ma'lumotlarni faylga saqlash
        students_df = pd.DataFrame(students_data)
        file_path = os.path.join(DATA_DIR, f"students_{year}.csv")
        students_df.to_csv(file_path, index=False)
        print(f"{year} yil uchun {num_students} ta talaba ma'lumotlari yaratildi: {file_path}")

if __name__ == "__main__":
    # Foydalanuvchilar faylini yaratish
    create_users_file()
    
    # Talabalar ma'lumotlarini yaratish
    create_students_data()
    
    print("Barcha sintetik ma'lumotlar muvaffaqiyatli yaratildi!")
