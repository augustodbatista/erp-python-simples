import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from ttkthemes import ThemedTk
from datetime import date
from user_operations import verify_user
from data_operations import get_todos_vendedores, get_todos_clientes
from vendas_operation import add_venda
from cliente_operations import add_cliente

def abrir_formulario_vendas(container):
    for widget in container.winfo_children():
        widget.destroy()

    def handle_salvar_venda():
        numero_notinha = entry_notinha.get()
        valor_notinha = entry_valor.get()

        if not numero_notinha or not valor_notinha:
            messagebox.showerror("Erro de Validação", "Número da Notinha e Valor Total são obrigatórios.")
            return

        try:
            notinha_inteiro = int(numero_notinha)
            valor_decimal = float(valor_notinha.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro de Formato", "O Número da Notinha e o Valor Total devem ser números válidos.")
            return

        dados_venda = {
            'numero_notinha': notinha_inteiro,
            'data_venda': entry_data.get_date(),
            'valor_total': valor_decimal,
            'pago': status_pago.get(),
            'forma_pagamento': entry_forma_pagamento.get(),
            'data_vencimento': entry_data_vencimento.get_date(),
            'cliente_id': mapa_clientes[cliente_selecionado.get()],
            'vendedor_id': mapa_vendedores[vendedor_selecionado.get()]
        }

        resultado = add_venda(dados_venda)
        if resultado:
            messagebox.showinfo("Sucesso", f"Venda ID {resultado.id} salva com sucesso!")
            limpar_formulario()
        else:
            messagebox.showerror("Erro de Banco de Dados", "Não foi possível salvar a venda.")

    def limpar_formulario():
        entry_notinha.delete(0, tk.END)
        entry_data.set_date(date.today())
        vendedor_selecionado.set("")
        cliente_selecionado.set("")
        entry_valor.delete(0, tk.END)
        entry_forma_pagamento.delete(0, tk.END)
        entry_data_vencimento.set_date(date.today())
        status_pago.set(False)

    vendedor_selecionado = tk.StringVar()
    cliente_selecionado = tk.StringVar()
    status_pago = tk.BooleanVar()

    ttk.Label(container, text="Número Notinha:").grid(row=0, column=0, padx=5, pady=10, sticky="w")
    entry_notinha = ttk.Entry(container, style='Padded.TEntry')
    entry_notinha.grid(row=0, column=1, padx=5, pady=10)

    ttk.Label(container, text="Data da Venda:").grid(row=0, column=2, padx=5, pady=10, sticky="w")
    entry_data = DateEntry(container, date_pattern='dd/MM/yyyy', style='Padded.TEntry')
    entry_data.grid(row=0, column=3, padx=5, pady=10)

    ttk.Label(container, text="Vendedor:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    objetos_vendedor = get_todos_vendedores()
    mapa_vendedores = {v.nome_vendedor: v.id for v in objetos_vendedor}
    lista_vendedores = list(mapa_vendedores.keys())
    combo_vendedor = ttk.Combobox(container, textvariable=vendedor_selecionado, values=lista_vendedores, state='readonly')
    if lista_vendedores:
        combo_vendedor.set(lista_vendedores[0])
    combo_vendedor.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(container, text="Cliente:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    objetos_cliente = get_todos_clientes()
    mapa_clientes = {c.nome_cliente: c.id for c in objetos_cliente}
    lista_clientes = list(mapa_clientes.keys())
    combo_cliente = ttk.Combobox(container, textvariable=cliente_selecionado, values=lista_clientes, state='readonly')
    if lista_clientes:
        combo_cliente.set(lista_clientes[0])
    combo_cliente.grid(row=1, column=3, padx=5, pady=5)
    
    ttk.Label(container, text="Valor Total:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_valor = ttk.Entry(container, style='Padded.TEntry')
    entry_valor.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(container, text="Forma de Pagamento:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_forma_pagamento = ttk.Entry(container, style='Padded.TEntry')
    entry_forma_pagamento.grid(row=2, column=3, padx=5, pady=5)

    ttk.Label(container, text="Data de Vencimento:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_data_vencimento = DateEntry(container, date_pattern='dd/MM/yyyy', style='Padded.TEntry')
    entry_data_vencimento.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(container, text="Está Pago?").grid(row=3, column=2, padx=5, pady=5, sticky="w")
    check_pago = ttk.Checkbutton(container, variable=status_pago)
    check_pago.grid(row=3, column=3, padx=5, pady=5, sticky="w")
    
    botao_salvar = ttk.Button(container, text="Salvar Venda", command=handle_salvar_venda)
    botao_salvar.grid(row=4, column=0, columnspan=4, pady=20)

def abrir_formulario_clientes(container):
    for widget in container.winfo_children():
        widget.destroy()

    def handle_salvar_cliente():
        cliente_nome = entry_cliente.get()
        cliente_endereco = entry_endereco.get()
        cliente_telefone = entry_telefone.get()

        if not cliente_nome:
            messagebox.showwarning("Campo Obrigatório", "O campo 'Nome do Cliente' não pode estar vazio.")
            return
        
        dados_cliente = {
            'nome_cliente': cliente_nome,
            'endereco': cliente_endereco,
            'telefone': cliente_telefone
        }

        salvar_cliente = add_cliente(dados_cliente)
        if salvar_cliente:
            messagebox.showinfo("Sucesso", f"Cliente ID {salvar_cliente.id} salvo com sucesso!")
            limpar_formulario_cliente()
        else:
            messagebox.showerror("Erro de Banco de Dados", "Não foi possível salvar o cliente.")

    def limpar_formulario_cliente():
        entry_cliente.delete(0, tk.END)
        entry_endereco.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)

    ttk.Label(container, text="Nome do Cliente:").grid(row=0, column=0, padx=5, pady=10, sticky="w")
    entry_cliente = ttk.Entry(container, style='Padded.TEntry')
    entry_cliente.grid(row=0, column=1, padx=5, pady=10)

    ttk.Label(container, text="Endereço:").grid(row=1, column=0, padx=5, pady=10, sticky="w")
    entry_endereco = ttk.Entry(container, style='Padded.TEntry')
    entry_endereco.grid(row=1, column=1, padx=5, pady=10)

    ttk.Label(container, text="Telefone:").grid(row=2, column=0, padx=5, pady=10, sticky="w")
    entry_telefone = ttk.Entry(container, style='Padded.TEntry')
    entry_telefone.grid(row=2, column=1, padx=5, pady=10)

    botao_salvar_cliente = ttk.Button(container, text="Salvar Cliente", command=handle_salvar_cliente)
    botao_salvar_cliente.grid(row=3, column=0, columnspan=4, pady=20)


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
    menu_cadastro = tk.Menu(barra_de_menu, tearoff=0)
    menu_cadastro.add_command(label="Clientes", command=lambda: abrir_formulario_clientes(frame_principal))
    barra_de_menu.add_cascade(label="Cadastro", menu=menu_cadastro)
    janela_principal.protocol("WM_DELETE_WINDOW", janela.destroy)

def handle_login():
    username = usuario_entry.get()
    password = senha_entry.get()
    
    autenticacao_usuario = verify_user(username, password)
    if autenticacao_usuario:
        messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {autenticacao_usuario.nome_usuario}!")
        janela.withdraw()
        abrir_janela_principal()
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha incorretos.")

janela = ThemedTk(theme="clam")
janela.title("Login - Detalhes ERP")

usuario_label = ttk.Label(janela, text="Usuário:")
usuario_entry = ttk.Entry(janela)
senha_label = ttk.Label(janela, text="Senha:")
senha_entry = ttk.Entry(janela, show="*")
login_button = ttk.Button(janela, text="Entrar", command=handle_login)

usuario_label.grid(row=0, column=0, padx=5, pady=5)
usuario_entry.grid(row=0, column=1, padx=5, pady=5)
senha_label.grid(row=1, column=0, padx=5, pady=5)
senha_entry.grid(row=1, column=1, padx=5, pady=5)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

janela.mainloop()