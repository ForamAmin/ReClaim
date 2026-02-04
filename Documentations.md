# Project Documentation: ReClaim – UniConnect

## 1. System Architecture Overview

The project follows a **three-tier architecture**, ensuring proper separation of concerns:

- **Frontend Layer** – User Interface  
- **Backend Layer** – Business Logic & Access Control  
- **Database Layer** – Data Storage  

---

## 2. Layered Architecture Logic

### 2.1 Frontend Layer

The frontend acts as a presentation layer and does not handle any business logic. It is responsible for:

- Rendering pages and dashboard sections based on backend responses  
- Collecting item reports and claim descriptions through forms  
- Sending requests to the backend API using JavaScript (`fetch`)  

**Security Note:**  
The frontend never receives sensitive or hidden item details. All access control is enforced on the backend.

---

### 2.2 Backend Layer (FastAPI)

The backend acts as the **central decision-maker** of the system.

Its responsibilities include:
- Authentication using college email ID  
- Context-based Role-Based Access Control (RBAC)  
- Verification logic for claims  
- Filtering and sanitizing API responses  
- Controlling which dashboard sections and data are sent to the frontend  

The backend ensures that users only see data and actions they are authorized to access.

---

### 2.3 Database Layer

The database stores information in relational tables such as:

- **Users:** College email and account information  
- **Items:** Public item details and system-protected attributes  
- **Claims:** Claim descriptions and verification status  

All data access is controlled through the backend.

---

## 3. Dynamic Role Assignment (Contextual Access)

Instead of assigning permanent roles, the system uses **context-based roles** depending on user actions and item ownership.

A single user may act as a Finder for one item and a Claimer for another.

---

### 3.1 Student (Base Role)
- Can view the public list of found items with limited information  
- Can report a found item (acts as Finder for that item)  
- Can submit a claim for an item (acts as Claimer for that item)  

---

### 3.2 Finder (Item-Level Role)
- Activated when a user reports a found item  
- Can view claim requests for that specific item  
- Cannot approve or reject claims for their own item  

This prevents conflict of interest and misuse.

---

### 3.3 Administrator
- Can view all users, items, and claims  
- Reviews claim descriptions against protected item details  
- Makes the final decision to approve or reject claims  

The admin acts as a neutral mediator.

---

## 4. Claim Verification Workflow

1. **Login:** User logs in using a valid college email ID  
2. **Dashboard Access:** Backend renders a single dashboard with context-based sections  
3. **Reporting:** Finder submits item details with partial information  
4. **Claiming:** Claimer submits a description of the item  
5. **Review:** Admin compares claim details with stored item information  
6. **Resolution:** Claim is approved or rejected based on verification  

---

## 5. Security Considerations

- Zero-trust frontend: No security logic is handled on the client side  
- Backend-controlled data filtering  
- Sensitive item attributes are never sent to unauthorized users  
- All claim actions are logged with timestamps for accountability  

---

## End of Documentation

reclaim-uniconnect/
│
├── backend/
│   ├── main.py              # 🚀 Entry Point
│   ├── database.py          # 🔌 DB Connection (SQLAlchemy)
│   ├── models.py            # 🗄️ The 3 Tables (Users, Items, Claims)
│   ├── schemas.py           # ✅ Pydantic Validators
│   ├── crud.py              # ⚙️ Database Functions (Create, Read...)
│   ├── config.py            # 🔐 Settings (Secret Key, DB URL)
│   │
│   ├── routes/
│   │   ├── auth.py          # Login routes
│   │   ├── items.py         # Reporting items
│   │   ├── claims.py        # Claiming logic
│   │   └── admin.py         # Admin decision routes
│   │
│   └── utils/
│       ├── security.py      # Hashing & Token logic
│       └── matcher.py       # 🧠 The AI Matcher Logic (New file needed!)
│
├── frontend/
│   ├── templates/
│   │   ├── base.html        # Shared Navbar/Footer (Don't repeat code!)
│   │   ├── login.html
│   │   └── dashboard.html   # 🔀 ONE dashboard with dynamic tabs
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/         # Store images here
│
├── documentation.md
└── requirements.txt