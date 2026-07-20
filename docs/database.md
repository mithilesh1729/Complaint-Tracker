# 🗄️ Database Design

This document details the Entity-Relationship (ER) schema of the Hostel Complaint Tracking System. The database is relational, currently utilizing **PostgreSQL** in production environments.

---

## 📊 Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    %% Entities
    HOSTEL {
        int id PK
        string name "Unique"
        boolean is_active
    }

    USER {
        string roll_no PK "Used as username"
        string name
        string email
        string phone
        string role "student, office, warden, hmc, admin"
        int hostel_id FK "Nullable for Admin/HMC"
        boolean is_active
    }

    COMPLAINT_CATEGORY {
        int id PK
        string name "Unique (e.g. Plumbing, Electrical)"
    }

    COMPLAINT {
        uuid complaint_id PK
        string complaint_number "Auto-generated e.g., C-20231015-12A4"
        string user_roll_no FK
        int hostel_id FK
        int category_id FK
        string room_number
        string description
        string status "pending, in_progress, escalated_warden, escalated_hmc, resolved"
        string priority "low, medium, high"
        string image_url "Nullable"
        boolean is_confirmed "Student Confirmation"
        datetime created_at
        datetime resolved_at "Nullable"
        
        %% Assignment & Actions
        string assigned_to_roll_no FK "Nullable"
        string office_remark "Nullable"
        string warden_remark "Nullable"
        string hmc_remark "Nullable"
    }

    STATUS_LOG {
        int id PK
        uuid complaint_id FK
        string status
        string message "e.g., 'Escalated to Warden by John Doe. Remark: Cannot fix.'"
        datetime created_at
    }

    %% Relationships
    HOSTEL ||--o{ USER : "houses"
    HOSTEL ||--o{ COMPLAINT : "has"
    
    USER ||--o{ COMPLAINT : "creates"
    USER ||--o{ COMPLAINT : "assigned to (office)"
    
    COMPLAINT_CATEGORY ||--o{ COMPLAINT : "categorizes"
    
    COMPLAINT ||--o{ STATUS_LOG : "tracks timeline in"
```

---

## 🧠 Schema Design Decisions & Normalization

### 1. `User` as a Unified Table
- Instead of having separate tables for `Student`, `Staff`, `Warden`, and `Admin`, we use a **Single Unified User Table** extending Django's `AbstractBaseUser`.
- **Why?** It drastically simplifies Authentication. By driving permissions purely off a `role` enum field, we avoid complex polymorphic associations or multi-table joins just to log a user in.

### 2. UUID Primary Keys for Complaints
- `Complaint` utilizes a UUID (`complaint_id`) as its primary key rather than a sequential integer.
- **Why?** 
  - Prevents enumeration attacks (a student cannot guess `id=5` if they are `id=4`).
  - Prepares the system for distributed database scaling (sharding).
- *Note:* We also generate a human-readable `complaint_number` (e.g. `C-2023-4XF`) purely for display and searching, but relations strictly use the UUID.

### 3. The `StatusLog` (Append-Only Event Sourcing)
- Instead of just overwriting a `status` field on the `Complaint` table, we implement an append-only `StatusLog` table.
- **Why?** 
  - **Auditability:** It provides a 100% accurate, tamper-proof history of exactly *when* and *who* changed a complaint's state. 
  - **User Experience:** This table directly powers the "Timeline" UI in the student and staff portals, providing Amazon-style package tracking visibility.

### 4. Denormalization of `Hostel` in `Complaint`
- A complaint belongs to a `User`, and a `User` belongs to a `Hostel`. Strictly speaking, storing `hostel_id` on the `Complaint` table is redundant (denormalized).
- **Why?** 
  - **Read Performance:** Staff and Wardens filter the global queue by their assigned `hostel_id`. By placing `hostel_id` directly on the `Complaint` table, we save a massive `JOIN` operation on every single dashboard load, optimizing for heavy read-throughput.
