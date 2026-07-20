# 🏗️ System Architecture

This document outlines the high-level architecture of the **Hostel Complaint Tracking System**. The architecture was designed to be modular, secure, and scalable, strictly separating the presentation layer from the business logic.

---

## 🏛️ High-Level Design (HLD)

The system follows a standard **3-Tier Client-Server Architecture**:

```mermaid
graph TD
    %% Clients
    Client_Student[Student Portal]
    Client_Office[Hostel Office Portal]
    Client_Warden[Warden Portal]
    Client_HMC[HMC Admin Portal]

    %% Frontend App
    subgraph Frontend [React SPA (Vite)]
        UI_Components[React UI Components]
        State_Mgmt[Context / Custom Hooks]
        Axios[Axios HTTP Client]
    end

    %% Backend API
    subgraph Backend [Django REST Framework]
        API_Gateway[URL Router]
        Auth[JWT Authentication]
        
        subgraph Business_Logic
            Views[API Views / Controllers]
            Services[Service Layer]
            Selectors[Selector Layer]
        end
        
        Models[ORM Models]
    end

    %% Storage & Cache
    subgraph Data_Layer
        PostgreSQL[(PostgreSQL DB)]
        Redis[(Redis Cache)]
    end

    %% Connections
    Client_Student --> Frontend
    Client_Office --> Frontend
    Client_Warden --> Frontend
    Client_HMC --> Frontend

    Frontend -- REST / JSON / JWT --> Backend
    
    API_Gateway --> Auth
    Auth --> Views
    Views --> Services
    Views --> Selectors
    
    Services --> Models
    Selectors --> Models
    
    Models --> PostgreSQL
    Models -.-> Redis
```

---

## 🧠 Design Decisions & Interview Talking Points

### 1. Why Django & Django REST Framework (DRF)?
- **Rapid Prototyping:** Django's ORM allows for extremely fast database schema migrations and complex relational querying (e.g., filtering complaints by hostel, role, and priority).
- **Security:** Built-in protection against SQL Injection, CSRF, and XSS.
- **Role-Based Access Control (RBAC):** DRF makes it trivial to write custom `BasePermission` classes (`IsWarden`, `IsHostelOffice`) to strictly enforce tenant isolation.

### 2. Separation of Concerns (Service/Selector Pattern)
Instead of putting all business logic in "Fat Views" or "Fat Models", this architecture uses a **Service/Selector Pattern**:
- **Views:** Only handle HTTP parsing, permission checks, and returning responses.
- **Selectors:** Handle all read-only database queries (e.g., `ComplaintSelector.get_assigned_complaints()`).
- **Services:** Handle all write-operations and complex business logic (e.g., `ComplaintService.escalate_to_warden()`).
- **Benefit:** Code is highly testable, DRY, and prevents circular imports.

### 3. Authentication: Stateless JWT
- We use **JSON Web Tokens (JWT)** instead of Session cookies. 
- **Why?** It completely decouples the React frontend from the Django backend, making the API stateless. This allows for horizontal scaling of the backend servers without needing "sticky sessions" or a centralized session database.

### 4. Tenant Isolation
- A "Hostel" acts as a tenant. When an Office Staff or Warden logs in, the API strictly scopes all data returned to *their* assigned hostel. A Warden from Hostel A can never see complaints from Hostel B. This is enforced at the `get_queryset()` level.

### 5. Asynchronous Preparation (Redis & Celery)
- Although currently running synchronously for MVP simplicity, the architecture is pre-configured with **Redis**. 
- Future implementations of PDF generation, email notifications, and auto-escalation crons can trivially be offloaded to Celery workers without changing the core application structure.
