import tkinter as tk
from user_operations import verify_user
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from ttkthemes import ThemedTk
from data_operations import get_todos_vendedores, get_todos_clientes

janela = ThemedTk(theme="clam")
janela.title("Login - Detalhes ERP")


def abrir_formulario_vendas(container):
    """Cria o formulário de vendas dentro do container (frame) fornecido."""
    # Limpa o frame de qualquer widget que estivesse lá antes
    for widget in container.winfo_children():
        widget.destroy()

    # --- Linha 0: Identificação da Venda ---
    ttk.Label(container, text="Número Notinha:").grid(row=0, column=0, padx=5, pady=10, sticky="w")
    entry_notinha = ttk.Entry(container, style='Padded.TEntry')
    entry_notinha.grid(row=0, column=1, padx=5, pady=10)

    ttk.Label(container, text="Data da Venda:").grid(row=0, column=2, padx=5, pady=10, sticky="w")
    entry_data = DateEntry(container, date_pattern='dd/MM/yyyy', style='Padded.TEntry')
    entry_data.grid(row=0, column=3, padx=5, pady=10)

    # --- Linha 1: Partes Envolvidas ---
    ttk.Label(container, text="Vendedor:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    objetos_vendedor = get_todos_vendedores()
    lista_vendedores = [v.nome_vendedor for v in objetos_vendedor] if objetos_vendedor else ["Nenhum vendedor cadastrado"]
    vendedor_selecionado = tk.StringVar()
    combo_vendedor = ttk.Combobox(container, textvariable=vendedor_selecionado, values=lista_vendedores, state='readonly')
    if lista_vendedores:
        combo_vendedor.set(lista_vendedores[0])
    combo_vendedor.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(container, text="Cliente:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    objetos_cliente = get_todos_clientes()
    lista_clientes = [c.nome_cliente for c in objetos_cliente] if objetos_cliente else ["Nenhum cliente cadastrado"]
    cliente_selecionado = tk.StringVar()
    combo_cliente = ttk.Combobox(container, textvariable=cliente_selecionado, values=lista_clientes, state='readonly')
    if lista_clientes:
        combo_cliente.set(lista_clientes[0])
    combo_cliente.grid(row=1, column=3, padx=5, pady=5)

    # --- Linha 2: Detalhes Financeiros ---
    ttk.Label(container, text="Valor Total:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_valor = ttk.Entry(container, style='Padded.TEntry')
    entry_valor.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(container, text="Forma de Pagamento:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_forma_pagamento = ttk.Entry(container, style='Padded.TEntry')
    entry_forma_pagamento.grid(row=2, column=3, padx=5, pady=5)

    # --- Linha 3: Status e Prazos ---
    ttk.Label(container, text="Data de Vencimento:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_data_vencimento = DateEntry(container, date_pattern='dd/MM/yyyy', style='Padded.TEntry')
    entry_data_vencimento.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(container, text="Está Pago?").grid(row=3, column=2, padx=5, pady=5, sticky="w")
    status_pago = tk.BooleanVar()
    check_pago = ttk.Checkbutton(container, variable=status_pago)
    check_pago.grid(row=3, column=3, padx=5, pady=5, sticky="w")

    # --- Linha 4: Botão de Ação ---
    botao_salvar = ttk.Button(container, text="Salvar Venda") # command virá depois
    botao_salvar.grid(row=4, column=0, columnspan=4, pady=20)

def abrir_janela_principal():
    janela_principal = tk.Toplevel(janela)
    janela_principal.title("Sistema ERP - Principal")
    janela_principal.geometry("850x500")

    style = ttk.Style(janela_principal)
    style.configure('Padded.TEntry', padding=(5, 5, 5, 5))

    frame_principal = ttk.Frame(janela_principal)
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    barra_de_menu = tk.Menu(janela_principal)
    janela_principal.config(menu=barra_de_menu)
    
    menu_vendas = tk.Menu(barra_de_menu, tearoff=0)
    menu_vendas.add_command(label="Registrar Nova Venda", command=lambda: abrir_formulario_vendas(frame_principal))
    
    barra_de_menu.add_cascade(label="Vendas", menu=menu_vendas)

    janela_principal.protocol("WM_DELETE_WINDOW", janela.destroy)

def handle_login():
    username = usuario_entry.get()
    password = senha_entry.get()
    autenticacao_usuario = verify_user(username, password)
    if autenticacao_usuario:
        messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {autenticacao_usuario.nome_usuario}!")
        janela.withdraw()  # Esconde a janela de login
        abrir_janela_principal()  # Abre a janela principal
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha incorretos.")

usuario_label = ttk.Label(janela, text="Usuário:")
usuario_entry = ttk.Entry(janela)
senha_label = ttk.Label(janela, text="Senha:")
senha_entry = ttk.Entry(janela, show="*")
login_button = ttk.Button(janela, text="Entrar", command=handle_login)


usuario_label.grid(row=0, column=0)
usuario_entry.grid(row=0, column=1)
senha_label.grid(row=1, column=0)
senha_entry.grid(row=1, column=1)
login_button.grid(row=2, column=0, columnspan=2)  


janela.mainloop()