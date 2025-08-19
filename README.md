# ERP Simples em Python 🐍

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-orange?style=for-the-badge&logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

> ⚠️ **Status do Projeto:** Em desenvolvimento.

Um projeto de aprendizado para a construção de um sistema de ERP de desktop do zero, utilizando Python para a lógica de negócios, Tkinter para a interface gráfica e SQLAlchemy para a interação com o banco de dados.

---

### ✅ Funcionalidades Atuais

- **Sistema de Autenticação Seguro:**
  - Tela de login gráfica com tema visual moderno.
  - Armazenamento seguro de senhas utilizando hash (bcrypt).
  - Validação de credenciais de usuário contra o banco de dados.

- **Estrutura da Aplicação Principal:**
  - Janela principal multi-telas com menu de navegação funcional para acesso aos módulos.
  - Transição de telas gerenciada (Login → Janela Principal).

- **Módulos de Cadastro:**
  - Interface completa para criar, buscar e selecionar Clientes e Fornecedores.

- **Módulo de Vendas e Pagamentos:**
  - Formulário completo e estilizado para registro de novas vendas e pagamentos.
  - Uso de componentes de interface avançados como calendário (`tkcalendar`) e busca dinâmica com `Treeview`.
  - Funcionalidade para consultar vendas não pagas e marcá-las como pagas.
  
- **Módulo de Relatórios (Em construção):**
  - Interface com filtros dinâmicos para gerar relatórios de vendas por período, vendedor ou cliente.

  ------------------------------------------------------------

  # Simple ERP in Python 🐍

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-orange?style=for-the-badge&logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

> ⚠️ **Project Status:** In Development.

A learning project to build a desktop ERP system from scratch, using Python for business logic, Tkinter for the graphical user interface, and SQLAlchemy for database interaction.

---

### ✅ Current Features

-   **Secure Authentication System:**
    -   Themed graphical login screen.
    -   Secure password storage using bcrypt hashing.
    -   User credential validation against the database.

-   **Core Application Structure:**
    -   Multi-screen main application with a functional menubar for module navigation.
    -   Managed screen transitions (Login → Main Window).

-   **Entity Management Modules:**
    -   Complete interfaces to Create, Search, and Select Clients and Suppliers.

-   **Sales & Payments Modules:**
    -   Styled forms for registering new sales and supplier payments.
    -   Use of advanced UI components like a date picker (`tkcalendar`) and dynamic search with `Treeview`.
    -   Functionality to query and update the status of unpaid sales.

-   **Reporting Module (Work in Progress):**
    -   UI with dynamic filters to generate sales reports by date range, vendor, or client.

---

### 🛠️ Tech Stack

| Category          | Technology                               |
| ----------------- | ---------------------------------------- |
| **Language** | Python                                   |
| **GUI** | Tkinter, ttk, ttkthemes, tkcalendar      |
| **Database** | SQLite via SQLAlchemy (ORM)              |
| **Security** | passlib[bcrypt]                          |
| **Versioning** | Git & GitHub                             |

---

### 🚀 How to Run the Project

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/augustodbatista/erp-python-simples.git](https://github.com/augustodbatista/erp-python-simples.git)
    cd erp-python-simples
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    # .\venv\Scripts\activate
    # On Linux/macOS:
    # source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create the database:**
    ```bash
    python create_db.py
    ```

5.  **(Optional) Populate the database with test data:**
    *If you have a `populate_db.py` script locally (it's in the `.gitignore`), you can use it to add initial data.*
    ```bash
    python populate_db.py
    ```

6.  **Run the application:**
    ```bash
    python main.py
    ```