import streamlit as st
import pandas as pd
import os
from datetime import datetime
import hashlib

# Ma'lumotlar fayli yo'li
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Foydalanuvchilar ma'lumotlari fayli
USERS_FILE = os.path.join(DATA_DIR, "users.csv")

# Parol hashlash funksiyasi
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Foydalanuvchilar ma'lumotlarini yuklash
def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    else:
        # Admin foydalanuvchisini yaratish
        admin_user = pd.DataFrame({
            "username": ["admin"],
            "password": [hash_password("admin")]
        })
        admin_user.to_csv(USERS_FILE, index=False)
        return admin_user

# Talabalar ma'lumotlarini yuklash
def load_students(year):
    file_path = os.path.join(DATA_DIR, f"students_{year}.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["ID", "Ism", "Familiya", "Guruh", "Fakultet", "Telefon", "Kiritilgan sana"])

# Talabalar ma'lumotlarini saqlash
def save_students(students_df, year):
    file_path = os.path.join(DATA_DIR, f"students_{year}.csv")
    students_df.to_csv(file_path, index=False)

# Foydalanuvchini tekshirish
def authenticate_user(username, password):
    users_df = load_users()
    user = users_df[users_df["username"] == username]
    if not user.empty:
        stored_password = user.iloc[0]["password"]
        if stored_password == hash_password(password):
            return True
    return False

# Yangi foydalanuvchi qo'shish
def add_user(username, password):
    users_df = load_users()
    if username in users_df["username"].values:
        return False
    
    new_user = pd.DataFrame({
        "username": [username],
        "password": [hash_password(password)]
    })
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(USERS_FILE, index=False)
    return True

# Kirish sahifasi
def login_page():
    st.title("Talabalar ma'lumotlarini boshqarish tizimi")
    st.subheader("Kirish")
    
    username = st.text_input("Foydalanuvchi nomi")
    password = st.text_input("Parol", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        login_button = st.button("Kirish")
    
    with col2:
        register_button = st.button("Ro'yxatdan o'tish")
    
    if login_button:
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Muvaffaqiyatli kirildi!")
            st.experimental_rerun()
        else:
            st.error("Foydalanuvchi nomi yoki parol noto'g'ri!")
    
    if register_button:
        st.session_state.registering = True
        st.experimental_rerun()

# Ro'yxatdan o'tish sahifasi
def register_page():
    st.title("Talabalar ma'lumotlarini boshqarish tizimi")
    st.subheader("Ro'yxatdan o'tish")
    
    username = st.text_input("Yangi foydalanuvchi nomi")
    password = st.text_input("Yangi parol", type="password")
    confirm_password = st.text_input("Parolni tasdiqlang", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        register_button = st.button("Ro'yxatdan o'tish")
    
    with col2:
        back_button = st.button("Orqaga")
    
    if register_button:
        if password != confirm_password:
            st.error("Parollar mos kelmadi!")
        elif len(username) < 3:
            st.error("Foydalanuvchi nomi kamida 3 ta belgidan iborat bo'lishi kerak!")
        elif len(password) < 4:
            st.error("Parol kamida 4 ta belgidan iborat bo'lishi kerak!")
        else:
            if add_user(username, password):
                st.success("Foydalanuvchi muvaffaqiyatli yaratildi!")
                st.session_state.registering = False
                st.experimental_rerun()
            else:
                st.error("Bu foydalanuvchi nomi allaqachon mavjud!")
    
    if back_button:
        st.session_state.registering = False
        st.experimental_rerun()

# Asosiy dastur sahifasi
def main_app():
    st.title("Talabalar ma'lumotlarini boshqarish tizimi")
    
    # Chiqish tugmasi
    if st.sidebar.button("Chiqish"):
        st.session_state.logged_in = False
        st.experimental_rerun()
    
    st.sidebar.write(f"Foydalanuvchi: {st.session_state.username}")
    
    # Talabalar yilini tanlash
    current_year = datetime.now().year
    years = list(range(2021, current_year + 1))
    selected_year = st.sidebar.selectbox("Yilni tanlang", years)
    
    # Tanlangan yil uchun talabalar ma'lumotlarini yuklash
    students_df = load_students(selected_year)
    
    # Tab yaratish
    tab1, tab2, tab3 = st.tabs(["Talabalar ro'yxati", "Talaba qo'shish", "Qidirish"])
    
    with tab1:
        st.header(f"{selected_year} yildagi talabalar ro'yxati")
        
        if not students_df.empty:
            # ID bo'yicha tartiblash
            students_df = students_df.sort_values("ID")
            
            # Har bir talaba uchun ekspander yaratish
            for _, student in students_df.iterrows():
                with st.expander(f"{student['ID']} - {student['Ism']} {student['Familiya']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ID:** {student['ID']}")
                        st.write(f"**Ism:** {student['Ism']}")
                        st.write(f"**Familiya:** {student['Familiya']}")
                    with col2:
                        st.write(f"**Guruh:** {student['Guruh']}")
                        st.write(f"**Fakultet:** {student['Fakultet']}")
                        st.write(f"**Telefon:** {student['Telefon']}")
                        st.write(f"**Kiritilgan sana:** {student['Kiritilgan sana']}")
                    
                    # O'chirish tugmasi
                    if st.button(f"Talabani o'chirish", key=f"delete_{student['ID']}"):
                        students_df = students_df[students_df["ID"] != student["ID"]]
                        save_students(students_df, selected_year)
                        st.success(f"{student['Ism']} {student['Familiya']} ma'lumotlari o'chirildi.")
                        st.experimental_rerun()
        else:
            st.info(f"{selected_year} yilda talabalar ro'yxati mavjud emas.")
    
    with tab2:
        st.header("Yangi talaba qo'shish")
        
        # Yangi ID yaratish
        new_id = 1
        if not students_df.empty:
            new_id = students_df["ID"].max() + 1
        
        id_input = st.number_input("ID", min_value=1, value=int(new_id))
        first_name = st.text_input("Ism")
        last_name = st.text_input("Familiya")
        group = st.text_input("Guruh")
        faculty = st.text_input("Fakultet")
        phone = st.text_input("Telefon raqami")
        
        if st.button("Talabani qo'shish"):
            if id_input in students_df["ID"].values:
                st.error("Bu ID allaqachon mavjud. Boshqa ID kiriting.")
            elif not first_name or not last_name or not group or not faculty:
                st.error("Barcha majburiy maydonlarni to'ldiring.")
            else:
                # Yangi talaba ma'lumotlarini yaratish
                new_student = pd.DataFrame({
                    "ID": [id_input],
                    "Ism": [first_name],
                    "Familiya": [last_name],
                    "Guruh": [group],
                    "Fakultet": [faculty],
                    "Telefon": [phone],
                    "Kiritilgan sana": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                })
                
                # Yangi talaba ma'lumotlarini qo'shish
                students_df = pd.concat([students_df, new_student], ignore_index=True)
                save_students(students_df, selected_year)
                st.success(f"{first_name} {last_name} ma'lumotlari qo'shildi.")
                st.experimental_rerun()
    
    with tab3:
        st.header("Talabalarni qidirish")
        
        search_query = st.text_input("Qidirish so'zini kiriting (ID, Ism, Familiya, Guruh, Fakultet)")
        
        if search_query:
            # Barcha ustunlar bo'yicha qidirish
            search_results = students_df[
                students_df.astype(str).apply(lambda row: row.str.contains(search_query, case=False).any(), axis=1)
            ]
            
            if not search_results.empty:
                st.subheader("Qidiruv natijalari")
                for _, student in search_results.iterrows():
                    with st.expander(f"{student['ID']} - {student['Ism']} {student['Familiya']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**ID:** {student['ID']}")
                            st.write(f"**Ism:** {student['Ism']}")
                            st.write(f"**Familiya:** {student['Familiya']}")
                        with col2:
                            st.write(f"**Guruh:** {student['Guruh']}")
                            st.write(f"**Fakultet:** {student['Fakultet']}")
                            st.write(f"**Telefon:** {student['Telefon']}")
                            st.write(f"**Kiritilgan sana:** {student['Kiritilgan sana']}")
                        
                        # O'chirish tugmasi
                        if st.button(f"Talabani o'chirish", key=f"search_delete_{student['ID']}"):
                            students_df = students_df[students_df["ID"] != student["ID"]]
                            save_students(students_df, selected_year)
                            st.success(f"{student['Ism']} {student['Familiya']} ma'lumotlari o'chirildi.")
                            st.experimental_rerun()
            else:
                st.info("Qidiruv bo'yicha talabalar topilmadi.")

# Dastur boshlanishi
def main():
    # Sessiya holati
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "registering" not in st.session_state:
        st.session_state.registering = False
    
    if "username" not in st.session_state:
        st.session_state.username = ""
    
    # Kirish holati tekshirish
    if not st.session_state.logged_in:
        if st.session_state.registering:
            register_page()
        else:
            login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
