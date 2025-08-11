# ERP Simples em Python

Um projeto de aprendizado para a construção de um sistema de ERP de desktop do zero, utilizando Python para a lógica de negócios, Tkinter para a interface gráfica e SQLAlchemy para a interação com o banco de dados.

> ⚠️ **Projeto em desenvolvimento.**

### Funcionalidades Atuais

- **Sistema de Autenticação Seguro:**
  - Tela de login gráfica com tema visual moderno.
  - Armazenamento seguro de senhas utilizando hash (bcrypt).
  - Validação de credenciais de usuário contra o banco de dados.

- **Estrutura da Aplicação Principal:**
  - Janela principal multi-telas com menu de navegação funcional.
  - Transição de telas gerenciada (Login → Janela Principal).

- **Módulo de Vendas (Interface):**
  - Formulário completo e estilizado para registro de novas vendas.
  - Menus de seleção (Vendedores, Clientes) populados dinamicamente a partir do banco de dados.
  - Uso de componentes de interface avançados como calendário (`tkcalendar`) e `ttk.Combobox`.

### Tecnologias Utilizadas

- **Linguagem:** Python
- **Interface Gráfica (GUI):** Tkinter, ttk, ttkthemes, tkcalendar
- **Banco de Dados:** SQLite
- **ORM:** SQLAlchemy
- **Segurança:** passlib[bcrypt]


# Simple ERP in Python

A learning project to build a desktop ERP system from scratch, using Python for business logic, Tkinter for the graphical user interface, and SQLAlchemy for database interaction.

> ⚠️ **Work in progress.**

### Current Features

- **Secure Authentication System:**
  - Themed graphical login screen.
  - Secure password storage using bcrypt hashing.
  - User credential validation against the database.

- **Main Application Structure:**
  - Multi-window main application with a functional menubar.
  - Managed screen transitions (Login → Main Window).

- **Sales Module (UI):**
  - Complete and styled form for new sales registration.
  - Dropdown menus (Vendors, Clients) are dynamically populated from the database.
  - Use of advanced UI components like a date picker (`tkcalendar`) and `ttk.Combobox`.

### Tech Stack

- **Language:** Python
- **GUI:** Tkinter, ttk, ttkthemes, tkcalendar
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Security:** passlib[bcrypt]