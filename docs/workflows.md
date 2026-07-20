# 🔄 Workflows & Lifecycles

This document visualizes the core State Machine of a complaint and traces the exact sequence of events required to process it.

---

## 🚦 Complaint State Machine

The strict state transitions of a complaint ensure that a ticket cannot accidentally bypass an escalation tier or be closed prematurely.

```mermaid
stateDiagram-v2
    [*] --> PENDING : Student Lodges Complaint

    PENDING --> IN_PROGRESS : Office Assigns Staff
    PENDING --> ESCALATED_WARDEN : Office Escalates (Too Complex)

    IN_PROGRESS --> RESOLVED : Office Marks Done
    IN_PROGRESS --> ESCALATED_WARDEN : Office Escalates

    ESCALATED_WARDEN --> IN_PROGRESS : Warden Sends Back
    ESCALATED_WARDEN --> ESCALATED_HMC : Warden Escalates

    ESCALATED_HMC --> ESCALATED_WARDEN : HMC Returns to Warden
    ESCALATED_HMC --> RESOLVED : HMC Force Closes

    RESOLVED --> [*] : Student Confirms (is_confirmed=True)
    RESOLVED --> PENDING : Student Reopens
    RESOLVED --> IN_PROGRESS : Student Reopens (if previously assigned)
```

### State Rationale
- **PENDING:** The initial state. The Hostel Office sees this in their "Incoming Queue".
- **IN_PROGRESS:** Indicates active work. Office Staff must assign the ticket to themselves or a worker to enter this state.
- **ESCALATED_WARDEN:** Triggered manually if the issue requires Warden approval (e.g., funding for a new fan).
- **ESCALATED_HMC:** Triggered if the Warden cannot resolve it and needs Central Administration.
- **RESOLVED:** A temporary terminal state. A ticket is marked "Resolved" by staff, but it is not permanently closed until the student confirms.

---

## 🔁 Sequence Diagram (Standard Resolution)

Here is a full trace of a standard "Happy Path" resolution, from creation to confirmation.

```mermaid
sequenceDiagram
    autonumber
    
    actor Student
    participant API as Django API
    participant DB as PostgreSQL
    actor Office as Hostel Office

    Student->>API: POST /api/complaints/create/ (Title, Image, Category)
    API->>DB: INSERT into Complaint (Status=PENDING)
    API->>DB: INSERT into StatusLog (Status=PENDING)
    API-->>Student: 201 Created (UUID)

    Office->>API: GET /api/office/queue/
    API-->>Office: Returns list of PENDING complaints

    Office->>API: POST /api/office/complaints/{id}/assign/ (Remark)
    API->>DB: UPDATE Complaint (Status=IN_PROGRESS, AssignedTo=Self)
    API->>DB: INSERT into StatusLog (Status=IN_PROGRESS, Remark)
    API-->>Office: 200 OK

    Office->>API: PATCH /api/office/complaints/{id}/progress/ (Remark)
    API->>DB: INSERT into StatusLog (Remark)
    
    Office->>API: POST /api/office/complaints/{id}/resolve/ (Remark)
    API->>DB: UPDATE Complaint (Status=RESOLVED)
    API->>DB: INSERT into StatusLog (Status=RESOLVED)
    API-->>Office: 200 OK

    Student->>API: GET /api/complaints/{id}/
    API-->>Student: Status=RESOLVED, is_confirmed=False

    Student->>API: POST /api/complaints/{id}/confirm/
    API->>DB: UPDATE Complaint (is_confirmed=True, confirmed_at=Now)
    API->>DB: INSERT into StatusLog (Message="Confirmed by Student")
    API-->>Student: 200 OK (Cycle Complete)
```

### Sequence Highlights
1. **Idempotent Assignments:** Step 3 ensures a complaint can only be assigned if it is currently `PENDING`.
2. **Immutable Auditing:** Every major transition (Steps 2, 4, 6, 9, 11) forces an insertion into the `StatusLog`, ensuring complete historical traceability for the Timeline UI.
