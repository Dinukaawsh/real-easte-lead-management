---

# 🏡 Real Estate Lead Management

## 📌 Overview  
The **Real Estate Lead Management** system is a web-based application designed to help real estate agents and admins manage seller, buyer, renter, and landlord leads efficiently. It allows lead tracking, AI-powered match scoring, and an admin panel for lead management.

## 🚀 Features  

### **1️⃣ Lead Management**  
✅ Add, update, and delete leads  
✅ View lead details with property type, budget, and location  
✅ Download lead details in a structured format  

### **2️⃣ AI-Powered Matching**  
✅ AI-based lead matching system using OpenAI API  
✅ Rule-based match scoring (before AI integration)  
✅ Option to switch between AI and rule-based matching  
✅ View matching leads with scores  

### **3️⃣ Admin Panel**  
✅ Secure Django Admin Panel  
✅ Role-based access control 
✅ Filtering and sorting leads by type, location, or budget  

### **4️⃣ Validation & Security**  
✅ Input validation for leads  
✅ Error handling for API failures and invalid inputs  

## 🛠️ Tech Stack  

| **Technology**  | **Usage** |
|---------------|------------|
| **Django** | Backend framework (Lead management, API) |
| **Django Rest Framework (DRF)** | API development |
| **SQLite** | Database |
| **Bootstrap** | UI Styling |
| **OpenAI API** | AI-powered lead matching |

---

## 🔧 Installation & Setup  

### **1️⃣ Clone the Repository**  
git clone https://github.com/Dinukaawsh/real-estate-lead-management.git
cd real-estate-lead-management


### **2️⃣ Create and Activate a Virtual Environment**  
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows


### **3️⃣ Install Dependencies**  
pip install -r requirements.txt


### **4️⃣ Run Database Migrations**  
python manage.py makemigrations
python manage.py migrate


### **5️⃣ Create a Superuser**  
python manage.py createsuperuser
Set a username, email, and password.

### **6️⃣ Run the Development Server**  
python manage.py runserver
Visit **`http://127.0.0.1:8000`** to log in as an admin.

### Setup
1. Add your own API key in the `.env` file (real_eatate_leads/ .env)
2. Run the project

---

## 📜 License  
This project is **open-source** under the **MIT License**.

---

## 📩 Contact  
✉️ **Dinuka** – [dinukaaw.sh@gmail.com](mailto:dinukaaw.sh@gmail.com)  
🔗 **GitHub** – [github.com/Dinukaawsh](https://github.com/Dinukaawsh)  

---

