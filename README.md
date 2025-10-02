# Grocera 🛒  
Backend for an e-commerce grocery shop system built with **Django Rest Framework (DRF)**.  

This project provides APIs for managing users, products, categories, carts, orders, wishlists, and deposits.  
It includes JWT authentication, role-based access, and auto-generated API documentation.  

---

## 🚀 Features
- User registration, login, logout, password reset  
- JWT Authentication using **Djoser**  
- Products & Categories management  
- Cart system (add, remove, update items)  
- Order management  
- Wishlist functionality  
- Deposit system for users  
- API Documentation using **drf-yasg (Swagger & Redoc)**  

---

## 🛠️ Tech Stack
- **Backend Framework:** Django, Django Rest Framework  
- **Authentication:** Djoser + JWT  
- **Database:** PostgreSQL (recommended, works with SQLite in development)  
- **API Documentation:** drf-yasg  


---

## 📦 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/grocera.git
   cd grocera
    ````

2. **Create a virtual environment & activate it**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with:

   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=your_database_url
   ALLOWED_HOSTS=*
   EMAIL_HOST=your_email_host
   ```

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**

   ```bash
   python manage.py runserver
   ```

---

## 🔑 Authentication

* Authentication is handled with **JWT**.
* Register/Login using `/auth/` endpoints provided by **Djoser**.
* Add the JWT token to the `Authorization` header for secured requests:

  ```
  Authorization: JWT <your_token>
  ```

---

## 📌 API Endpoints

| Resource       | Endpoint       | Description                              |
| -------------- | -------------- | ---------------------------------------- |
| **Auth**       | `/auth/`       | Register, login, password reset (Djoser) |
| **Products**   | `/products/`   | CRUD operations on products              |
| **Categories** | `/categories/` | Manage product categories                |
| **Cart**       | `/cart/`       | Add/remove/update cart items             |
| **Orders**     | `/orders/`     | Place and track orders                   |
| **Wishlist**   | `/wishlist/`  | Manage saved products                    |
| **Deposit**    | `/deposits/`    | Manage user deposits                     |

---

## 📖 API Documentation

Swagger and Redoc documentation available at:

* **Swagger UI:** `http://127.0.0.1:8000/swagger/`
* **Redoc:** `http://127.0.0.1:8000/redoc/`

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to fork the repo and submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License**.

---


