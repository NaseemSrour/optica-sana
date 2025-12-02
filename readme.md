# Keyboard-First Data Entry System (Python + Textual)

A modern, keyboard-driven desktop application built with **Python** and **Textual**.  
Designed for fast data entry, clean architecture, and robust validation — with a
dedicated **database layer** as the foundation. A future **Flutter mobile app**
will provide read-only access to synced records.

---

## 🚀 Features

- **Keyboard-only workflow** (fast navigation, no mouse required)
- **Textual TUI** with clean panels, tables, and forms
- **Modular architecture**: UI, application logic, and database separated
- **Real-time UI validations** (field requirements, dependencies, max lengths)
- **Business-rule validations** in application layer
- **Database integrity** enforced via schema constraints
- **Supports Hebrew data input** inside an English UI
- **Future mobile companion** built with Flutter

---

## 🛠 Project Structure

project/

├── app/ # Textual UI layer

├── core/ # Application services and validation logic

├── db/ # Database models, schema, CRUD operations

├── tests/ # Unit tests for logic and database

└── main.py # Entry point


---

## 📚 Development Philosophy

1. **Database-first foundation**  
   Define schema, models, and CRUD operations before the UI.

2. **Logic before visuals**  
   All business rules live in the application layer — independent of Textual.

3. **UI as a thin layer**
   
   The UI doesn't need to know anything about the storage layer, it only uses the API provided by the services - so that in the future, any UI can be implemented and incorporated, not just Textual.

   The Textual interface handles:
   - keyboard navigation  
   - user feedback  
   - real-time input validation  
   - sending clean data to the core logic  

5. **Multi-layer validation**
   - UI: user feedback & field dependencies  
   - Logic: business/value rules  
   - DB: constraints & integrity  

---

## 📦 Installation

```bash
git clone <repository-url>
cd project
pip install -r requirements.txt
python main.py
