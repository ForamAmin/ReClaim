# Reclaim: UniConnect

> A role-based Lost & Found web application for secure, fast, and fair recovery of lost items within a college campus.

---

## 🚀 Key Faeatures
    1) **Authentication** :  i.e student can access via college email id only.
    2) **Form* : For claimer and founder to fill the details of lost and found items.
    3) **RBAC** : Different roles i.e claimer , founder and admin with different access levels and view of dashboard. i.e claimer can only see that someone has posted an item found but cannot see who posted it and what in detail. and founder can see the details of claimer and the system will ask questions to verify the identity and truthfulness of claimer before handing over the item.
    4) **Admin Panel** : Admin can see all the items lost and found and take solve disputes. 
    
   
    

## 🛠 Tech Stack
1) Frontend: HTML , CSS, JavaScript , Jinja2 (for templating)
2) Backend: FastAPI (Python)
3) Database: SQLite
4) Authentication: OAuth2 with College Email , Session Middleware (cookies)
5) Hosting: Heroku / Vercel
6) Version Control: Git & GitHub


## ⚙️ Getting Started


### Prerequisites
* A modern web browser (Chrome, Firefox, Edge)
* Code editor (VS Code recommended)

### Installation
1. **Clone the repository:**
   git clone https://github.com/ForamAmin/ReClaim.git