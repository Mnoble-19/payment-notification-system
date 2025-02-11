# payment-notification-system
This repository contains source code for the Palli technical challenge payment notification system

Bank Notification
           ↓
+------------------------+
|   FastAPI Endpoint     |
| (Receives Notification)|
+------------------------+
           ↓
+------------------------+
|  Notification Parser   |
| (Extracts Data Fields) |
+------------------------+
           ↓
+------------------------+
|   Customer Matcher     |
| (Identifies Customer)  |
+------------------------+
           ↓
+--------------------------+
|    Payment Processor     |
| (Updates Customer Record)|
+--------------------------+
           ↓
      ┌────────┐
      │        ↓ 
+------------+  +----------------+
| PostgreSQL |  | Confirmation   |
| Database   |  | API Call       |
+------------+  +----------------+
                       ↓
              Confirmation Message
              to Customer