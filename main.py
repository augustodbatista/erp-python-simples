import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from ttkthemes import ThemedTk
from datetime import date
from user_operations import verify_user
from data_operations import get_todos_vendedores, get_todos_clientes, search_clientes_por_nome, search_fornecedores_por_nome, search_vendas_nao_pagas, get_pagamentos_por_periodo
from vendas_operation import add_venda, get_sales_by_period_and_vendedor, get_sales_by_period_and_cliente, get_total_sales_by_period, get_paid_unpaid_sales_by_client
from cliente_operations import add_cliente
from pagamento_operations import add_pagamento
from fornecedor_operations import add_fornecedor
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
        if 'id' not in dados_cliente_selecionado:
            messagebox.showwarning("Seleção Necessária", "Por favor, busque e selecione um cliente na tabela antes de salvar.")
            return
        dados_venda = {
            'numero_notinha': notinha_inteiro,
            'data_venda': entry_data.get_date(),
            'valor_total': valor_decimal,
            'pago': status_pago.get(),
            'forma_pagamento': entry_forma_pagamento.get(),
            'data_vencimento': entry_data_vencimento.get_date(),
            'cliente_id': dados_cliente_selecionado['id'], 
            'vendedor_id': mapa_vendedores[vendedor_selecionado.get()],
            'participacao_vendas': status_participacao.get()
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
        for item in tabela_clientes.get_children():
            tabela_clientes.delete(item)
        label_cliente_selecionado.config(text="Cliente Selecionado: Nenhum")
        entry_valor.delete(0, tk.END)
        entry_forma_pagamento.delete(0, tk.END)
        entry_data_vencimento.set_date(date.today())
        status_pago.set(False)
    
    def handle_busca_cliente():
        termo_busca = entry_busca_cliente.get()
        resultados = search_clientes_por_nome(termo_busca)
        
        # Limpa a tabela de resultados antigos (com a correção)
        for item in tabela_clientes.get_children():
            tabela_clientes.delete(item)
            
        if resultados:
            for cliente in resultados:
                tabela_clientes.insert(parent='', index='end', values=(
                    cliente.id, cliente.nome_cliente, cliente.telefone, cliente.endereco
                ))
    
    dados_cliente_selecionado = {}

    def handle_selecao_cliente(event):
        item_selecionado_id = tabela_clientes.selection()
        if not item_selecionado_id:
            return
        
        id_da_linha = item_selecionado_id[0]
        valores = tabela_clientes.item(id_da_linha, 'values')
        dados_cliente_selecionado['id'] = int(valores[0])
        dados_cliente_selecionado['nome'] = valores[1]
        label_cliente_selecionado.config(text=f"Cliente Selecionado: {dados_cliente_selecionado['nome']}")
            

    vendedor_selecionado = tk.StringVar()
    status_pago = tk.BooleanVar()
    status_participacao = tk.BooleanVar()
    
    # ... (criação de todos os labels, entries, combos, etc.)
    label_notinha = ttk.Label(container, text="Número Notinha:")
    entry_notinha = ttk.Entry(container, style='Padded.TEntry')
    label_data = ttk.Label(container, text="Data da Venda:")
    entry_data = DateEntry(container, date_pattern='dd/MM/yyyy', style='Padded.TEntry')
    label_vendedor = ttk.Label(container, text="Vendedor:")
    objetos_vendedor = get_todos_vendedores()
    mapa_vendedores = {v.nome_vendedor: v.id for v in objetos_vendedor}
    lista_vendedores = list(mapa_vendedores.keys())
    combo_vendedor = ttk.Combobox(container, textvariable=vendedor_selecionado, values=lista_vendedores, state='readonly')
    if lista_vendedores:
        combo_vendedor.set(lista_vendedores[0])
        
    label_busca_cliente = ttk.Label(container, text="Buscar Cliente:")
    entry_busca_cliente = ttk.Entry(container, style='Padded.TEntry')
    botao_buscar_cliente = ttk.Button(container, text="Buscar", command=handle_busca_cliente)

    colunas = ('id', 'nome', 'telefone', 'endereco')
    tabela_clientes = ttk.Treeview(container, columns=colunas, show='headings', height=4)
    tabela_clientes.heading('id', text='ID')
    tabela_clientes.heading('nome', text='Nome')
    tabela_clientes.heading('telefone', text='Telefone')
    tabela_clientes.heading('endereco', text='Endereço')
    tabela_clientes.column('id', width=40)
    tabela_clientes.column('nome', width=200)
    tabela_clientes.column('telefone', width=100)
    tabela_clientes.column('endereco', width=250)

    label_cliente_selecionado = ttk.Label(container, text="Cliente Selecionado: Nenhum")

    label_valor = ttk.Label(container, text="Valor Total:")
    entry_valor = ttk.Entry(container, style='Padded.TEntry')
    label_forma_pagamento = ttk.Label(container, text="Forma de Pagamento:")
    entry_forma_pagamento = ttk.Entry(container, style='Padded.TEntry')
    label_data_vencimento = ttk.Label(container, text="Data de Vencimento:")
    entry_data_vencimento = DateEntry(container, date_pattern='dd/MM/yyyy', style='Padded.TEntry')
    label_pago = ttk.Label(container, text="Está Pago?")
    check_pago = ttk.Checkbutton(container, variable=status_pago)
    check_participacao = ttk.Checkbutton(container, variable=status_participacao)

    # Linha 0
    label_notinha.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_notinha.grid(row=0, column=1, padx=5, pady=5)
    label_data.grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_data.grid(row=0, column=3, padx=5, pady=5)
    
    # Linha 1
    label_vendedor.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    combo_vendedor.grid(row=1, column=1, padx=5, pady=5)
    
    # Linha 2 - Busca de Cliente
    label_busca_cliente.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_busca_cliente.grid(row=2, column=1, padx=5, pady=5)
    botao_buscar_cliente.grid(row=2, column=2, padx=5, pady=5)
    
    # Linha 3 - Tabela de Resultados
    tabela_clientes.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    # Linha 4 - Cliente Selecionado
    label_cliente_selecionado.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="w")
    tabela_clientes.bind('<<TreeviewSelect>>', handle_selecao_cliente)
    
    # Linha 5 - Detalhes Financeiros
    label_valor.grid(row=5, column=0, padx=5, pady=5, sticky="w")
    entry_valor.grid(row=5, column=1, padx=5, pady=5)
    label_forma_pagamento.grid(row=5, column=2, padx=5, pady=5, sticky="w")
    entry_forma_pagamento.grid(row=5, column=3, padx=5, pady=5)
    
    # Linha 6 - Prazos e Status
    label_data_vencimento.grid(row=6, column=0, padx=5, pady=5, sticky="w")
    entry_data_vencimento.grid(row=6, column=1, padx=5, pady=5)
    label_pago.grid(row=6, column=2, padx=5, pady=5, sticky="w")
    check_pago.grid(row=6, column=3, padx=5, pady=5, sticky="w")

    # Linha 7: Participação
    ttk.Label(container, text="Com participação?").grid(row=7, column=0, padx=5, pady=5, sticky="w")
    check_participacao.grid(row=7, column=1, padx=5, pady=5, sticky="w")

     # --- Linha 8: Botão Salvar (AJUSTADO) ---
    botao_salvar = ttk.Button(container, text="Salvar Venda", command=handle_salvar_venda)
    botao_salvar.grid(row=8, column=0, columnspan=4, pady=20)

def abrir_formulario_vendas_nao_pagas(container):
    for widget in container.winfo_children():
        widget.destroy()

    def handle_buscar_vendas():
        termo_busca = entry_busca_venda.get()
        vendas = search_vendas_nao_pagas(termo_busca)
        
        for item in tabela_vendas.get_children():
            tabela_vendas.delete(item)
            
        if vendas:
            for venda in vendas:
                # Fetch client name for display
                cliente_nome = ""
                if venda.cliente: # Check if client relationship is loaded
                    cliente_nome = venda.cliente.nome_cliente
                
                tabela_vendas.insert(parent='', index='end', values=(
                    venda.id,
                    venda.numero_notinha,
                    venda.data_venda.strftime('%d/%m/%Y'),
                    venda.valor_total,
                    cliente_nome,
                    venda.data_vencimento.strftime('%d/%m/%Y') if venda.data_vencimento else 'N/A'
                ))
        else:
            messagebox.showinfo("Busca de Vendas", "Nenhuma venda não paga encontrada com o termo de busca.")

    def handle_marcar_como_paga():
        item_selecionado_id = tabela_vendas.selection()
        if not item_selecionado_id:
            messagebox.showwarning("Seleção Necessária", "Por favor, selecione uma venda na tabela para marcar como paga.")
            return
        
        id_da_linha = item_selecionado_id[0]
        venda_id = tabela_vendas.item(id_da_linha, 'values')[0] # Get the ID from the first column
        
        confirmar = messagebox.askyesno("Confirmar Pagamento", f"Tem certeza que deseja marcar a venda ID {venda_id} como paga?")
        if confirmar:
            from vendas_operation import marcar_venda_como_paga # Import here to avoid circular dependency
            forma_pagamento_texto = entry_forma_pagamento.get()
            resultado = marcar_venda_como_paga(int(venda_id), forma_pagamento_texto)
            if resultado:
                messagebox.showinfo("Sucesso", f"Venda ID {venda_id} marcada como paga com sucesso!")
                handle_buscar_vendas() # Refresh the list
            else:
                messagebox.showerror("Erro", f"Não foi possível marcar a venda ID {venda_id} como paga.")

    # UI Elements
    label_busca_venda = ttk.Label(container, text="Buscar Venda (Notinha ou Cliente):")
    entry_busca_venda = ttk.Entry(container, style='Padded.TEntry')
    botao_buscar_venda = ttk.Button(container, text="Buscar", command=handle_buscar_vendas)

    colunas = ('id', 'notinha', 'data_venda', 'valor_total', 'cliente', 'data_vencimento')
    tabela_vendas = ttk.Treeview(container, columns=colunas, show='headings', height=10)
    tabela_vendas.heading('id', text='ID')
    tabela_vendas.heading('notinha', text='Notinha')
    tabela_vendas.heading('data_venda', text='Data Venda')
    tabela_vendas.heading('valor_total', text='Valor Total')
    tabela_vendas.heading('cliente', text='Cliente')
    tabela_vendas.heading('data_vencimento', text='Vencimento')

    tabela_vendas.column('id', width=50)
    tabela_vendas.column('notinha', width=80)
    tabela_vendas.column('data_venda', width=100)
    tabela_vendas.column('valor_total', width=100)
    tabela_vendas.column('cliente', width=200)
    tabela_vendas.column('data_vencimento', width=100)

    label_forma_pagamento = ttk.Label(container, text="Forma de Pagamento")
    entry_forma_pagamento = ttk.Entry(container, style="Padded.TEntry")

    botao_marcar_paga = ttk.Button(container, text="Marcar como Paga", command=handle_marcar_como_paga)

    # Layout
    row_counter = 0
    label_busca_venda.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    entry_busca_venda.grid(row=row_counter, column=1, padx=5, pady=5, sticky="ew")
    botao_buscar_venda.grid(row=row_counter, column=2, padx=5, pady=5)
    row_counter += 1

    tabela_vendas.grid(row=row_counter, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
    # Add a scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=tabela_vendas.yview)
    scrollbar.grid(row=row_counter, column=3, sticky="ns")
    tabela_vendas.configure(yscrollcommand=scrollbar.set)
    row_counter += 1

    label_forma_pagamento.grid(row=row_counter, column=0, padx=(5,0), pady=5, sticky='w')
    entry_forma_pagamento.grid(row=row_counter, column=1, columnspan=4, sticky='ew')
    botao_marcar_paga.grid(row=row_counter, column=5, pady=10, padx=5)

    # Configure grid to expand with window
    container.grid_rowconfigure(1, weight=1)
    container.grid_columnconfigure(1, weight=1)


    handle_buscar_vendas()

def abrir_formulario_relatorios_vendas(container):
    for widget in container.winfo_children():
        widget.destroy()

    def handle_gerar_relatorio():
        start_date = entry_data_inicio.get_date()
        end_date = entry_data_fim.get_date()
        status_selecionado = status_pagamento_selecionado.get()
        vendas = []
        if cliente_id_selecionado is not None:
            vendas = get_sales_by_period_and_cliente(start_date=start_date, end_date=end_date, cliente_id=cliente_id_selecionado, status_pagamento=status_selecionado)
        
        else:
            vendedor_nome = vendedor_selecionado.get()
            vendedor_id = mapa_vendedores.get(vendedor_nome) if vendedor_nome != "Todos" else None
            vendas = get_sales_by_period_and_vendedor(start_date=start_date, end_date=end_date, vendedor_id=vendedor_id, status_pagamento=status_selecionado)
        preencher_tabela_vendas(vendas)

    label_data_inicio = ttk.Label(container, text="Data Início:")
    entry_data_inicio = DateEntry(container, date_pattern='dd/MM/yyyy')
    label_data_fim = ttk.Label(container, text="Data Fim:")
    entry_data_fim = DateEntry(container, date_pattern='dd/MM/yyyy')

    # Vendedor selection
    label_vendedor = ttk.Label(container, text="Vendedor:")
    vendedor_selecionado = tk.StringVar()
    objetos_vendedor = get_todos_vendedores()
    mapa_vendedores = {v.nome_vendedor: v.id for v in objetos_vendedor}
    lista_vendedores = ["Todos"] + list(mapa_vendedores.keys())
    combo_vendedor = ttk.Combobox(container, textvariable=vendedor_selecionado, values=lista_vendedores, state='readonly')
    combo_vendedor.set("Todos")


    label_cliente = ttk.Label(container, text="Cliente (Nome ou ID):")
    entry_cliente_busca = ttk.Entry(container)
    cliente_id_selecionado = None 
    
    status_pagamento_selecionado = tk.StringVar()
    lista_status_pagamento = ['Todos', 'Pagas', 'Não Pagas']
    status_pagamento = ttk.Label(container, text="Status Pagamento")
    combo_status_pagamento = ttk.Combobox(container, textvariable=status_pagamento_selecionado, values=lista_status_pagamento, state="readonly")
    combo_status_pagamento.set("Todos")

    def handle_buscar_cliente_relatorio():
        nonlocal cliente_id_selecionado
        termo_busca = entry_cliente_busca.get()
        if not termo_busca:
            cliente_id_selecionado = None
            messagebox.showinfo("Busca de Cliente", "Nenhum termo de busca fornecido. O relatório incluirá todos os clientes.")
            return

        if termo_busca.isdigit():
            cliente_id_selecionado = int(termo_busca)
            messagebox.showinfo("Busca de Cliente", f"Cliente ID {cliente_id_selecionado} selecionado.")
        else:
            resultados = search_clientes_por_nome(termo_busca)
            if resultados:
                if len(resultados) == 1:
                    cliente_id_selecionado = resultados[0].id
                    messagebox.showinfo("Busca de Cliente", f"Cliente '{resultados[0].nome_cliente}' (ID: {resultados[0].id}) selecionado.")
                else:
                    # For multiple results, a more complex UI would be needed to select one
                    messagebox.showwarning("Múltiplos Clientes", "Múltiplos clientes encontrados. Por favor, refine a busca ou insira o ID exato.")
                    cliente_id_selecionado = None
            else:
                cliente_id_selecionado = None
                messagebox.showinfo("Busca de Cliente", "Cliente não encontrado.")

    botao_buscar_cliente_relatorio = ttk.Button(container, text="Buscar Cliente", command=handle_buscar_cliente_relatorio)

    # Treeview for results
    colunas = ('id', 'notinha', 'data_venda', 'valor_total', 'cliente', 'vendedor', 'pago', 'data_vencimento')
    tabela_relatorio = ttk.Treeview(container, columns=colunas, show='headings', height=15)
    tabela_relatorio.heading('id', text='ID')
    tabela_relatorio.heading('notinha', text='Notinha')
    tabela_relatorio.heading('data_venda', text='Data Venda')
    tabela_relatorio.heading('valor_total', text='Valor Total')
    tabela_relatorio.heading('cliente', text='Cliente')
    tabela_relatorio.heading('vendedor', text='Vendedor')
    tabela_relatorio.heading('pago', text='Pago')
    tabela_relatorio.heading('data_vencimento', text='Vencimento')

    tabela_relatorio.column('id', width=50)
    tabela_relatorio.column('notinha', width=80)
    tabela_relatorio.column('data_venda', width=100)
    tabela_relatorio.column('valor_total', width=100)
    tabela_relatorio.column('cliente', width=150)
    tabela_relatorio.column('vendedor', width=150)
    tabela_relatorio.column('pago', width=60)
    tabela_relatorio.column('data_vencimento', width=100)

    label_total_vendas = ttk.Label(container, text="Total de Vendas no Período: R$ 0.00")

    def preencher_tabela_vendas(vendas):
        for item in tabela_relatorio.get_children():
            tabela_relatorio.delete(item)
        
        total_valor = 0.0
        for venda in vendas:
            cliente_nome = venda.cliente.nome_cliente if venda.cliente else "N/A"
            vendedor_nome = venda.vendedor.nome_vendedor if venda.vendedor else "N/A"
            tabela_relatorio.insert(parent='', index='end', values=(
                venda.id,
                venda.numero_notinha,
                venda.data_venda.strftime('%d/%m/%Y'),
                f"R$ {venda.valor_total:.2f}",
                cliente_nome,
                vendedor_nome,
                "Sim" if venda.pago else "Não",
                venda.data_vencimento.strftime('%d/%m/%Y') if venda.data_vencimento else 'N/A'
            ))
            total_valor += float(venda.valor_total)
        label_total_vendas.config(text=f"Total de Vendas no Período: R$ {total_valor:.2f}")
        

    # Layout
    row_counter = 0
    label_data_inicio.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    entry_data_inicio.grid(row=row_counter, column=1, padx=5, pady=5)
    row_counter += 1
    label_data_fim.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    entry_data_fim.grid(row=row_counter, column=1, padx=5, pady=5)
    row_counter += 1

    label_vendedor.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    combo_vendedor.grid(row=row_counter, column=1, padx=5, pady=5)
    row_counter += 1

    label_cliente.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    entry_cliente_busca.grid(row=row_counter, column=1, padx=5, pady=5)
    botao_buscar_cliente_relatorio.grid(row=row_counter, column=2, padx=5, pady=5)
    row_counter += 1

    status_pagamento.grid(row=row_counter,column=0, padx=5, pady=5, sticky="w")
    combo_status_pagamento.grid(row= row_counter, column=1,padx=5, pady=5)
    row_counter+=1

    tabela_relatorio.grid(row=row_counter, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
    scrollbar_relatorio = ttk.Scrollbar(container, orient="vertical", command=tabela_relatorio.yview)
    scrollbar_relatorio.grid(row=row_counter, column=4, sticky="ns")
    tabela_relatorio.configure(yscrollcommand=scrollbar_relatorio.set)
    row_counter += 1

    label_total_vendas.grid(row=row_counter, column=0, columnspan=4, padx=5, pady=5, sticky="w")

    container.grid_rowconfigure(tabela_relatorio.grid_info()['row'], weight=1)
    container.grid_columnconfigure(1, weight=1)
    row_counter += 1

    botao_gerar_relatorio = ttk.Button(container, text="Gerar Relatório", command=handle_gerar_relatorio)
    botao_gerar_relatorio.grid(row=row_counter, column=0, columnspan=4, pady=20)

def abrir_formulario_relatorio_pagamentos(container):
    for widget in container.winfo_children():
         widget.destroy()

    def handle_buscar_relatorio_pagamentos():
        start_date = entry_data_inicio.get_date()
        end_date = entry_data_fim.get_date()
        status_selecionado = status_pagamento_selecionado.get()
        lista_pagamentos = get_pagamentos_por_periodo(start_date, end_date, status_selecionado)
        

        def preencher_relatorio_pagamentos(pagamentos):
            for item in tabela_relatorio.get_children():
                tabela_relatorio.delete(item)
            for pagamento in lista_pagamentos:
                valores_da_linha = (
                    pagamento.id,
                    pagamento.numero_nota,
                    pagamento.data_vencimento.strftime('%d/%m/%Y'),
                    pagamento.valor_nota,
                    pagamento.data_pagamento.strftime('%d/%m/%Y')if pagamento.data_pagamento else 'N/A',
                    pagamento.forma_pagamento if pagamento.forma_pagamento else 'N/A',
                    pagamento.fornecedor.nome_fornecedor
                )

                tabela_relatorio.insert(parent='', index='end', values=valores_da_linha)
        preencher_relatorio_pagamentos(lista_pagamentos)
    
    label_data_inicio = ttk.Label(container, text="Data Início:")
    entry_data_inicio = DateEntry(container, date_pattern='dd/MM/yyyy')
    label_data_fim = ttk.Label(container, text="Data Fim:")
    entry_data_fim = DateEntry(container, date_pattern='dd/MM/yyyy')
    botao_buscar_relatorio_pagamentos = ttk.Button(container, text="Buscar Pagamentos", command=handle_buscar_relatorio_pagamentos)
    status_pagamento_selecionado = tk.StringVar()
    lista_status_pagamento = ['Todos', 'Pagas', 'Não Pagas']
    status_pagamento = ttk.Label(container, text="Status Pagamento")
    combo_status_pagamento = ttk.Combobox(container, textvariable=status_pagamento_selecionado, values=lista_status_pagamento, state="readonly")
    combo_status_pagamento.set("Todos")

    colunas = ('id', 'numero_nota', 'data_vencimento', 'valor_nota', 'data_pagamento', 'fornecedor')
    tabela_relatorio = ttk.Treeview(container, columns=colunas, show='headings', height=15)
    tabela_relatorio.heading('id', text='ID')
    tabela_relatorio.heading('numero_nota', text='Numero Nota')
    tabela_relatorio.heading('data_vencimento', text='Data Vencimento')
    tabela_relatorio.heading('valor_nota', text='Valor Nota')
    tabela_relatorio.heading('fornecedor', text='Fornecedor')
    tabela_relatorio.heading('data_pagamento', text='Data Pagamento')
    tabela_relatorio.heading('forma_pagamento', text="Forma de Pagamento")

    tabela_relatorio.column('id', width=50)
    tabela_relatorio.column('numero_nota', width=80)
    tabela_relatorio.column('data_vencimento', width=100)
    tabela_relatorio.column('valor_nota', width=100)
    tabela_relatorio.column('fornecedor', width=150)
    tabela_relatorio.column('data_pagamento', width=100)
    tabela_relatorio.column('forma_pagamento', width=120)

    # Layout

    row_counter = 0
    label_data_inicio.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    entry_data_inicio.grid(row=row_counter, column=1, padx=5, pady=5)
    row_counter += 1

    label_data_fim.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    entry_data_fim.grid(row=row_counter, column=1, padx=5, pady=5)
    row_counter += 1

    status_pagamento.grid(row=row_counter,column=0, padx=5, pady=5, sticky="w")
    combo_status_pagamento.grid(row= row_counter, column=1,padx=5, pady=5)
    row_counter+=1

    botao_buscar_relatorio_pagamentos.grid(row=row_counter, column=0, padx=4, pady=20)
    row_counter += 1
    
    tabela_relatorio.grid(row=row_counter, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
    scrollbar_relatorio = ttk.Scrollbar(container, orient="vertical", command=tabela_relatorio.yview)
    scrollbar_relatorio.grid(row=row_counter, column=4, sticky="ns")
    tabela_relatorio.configure(yscrollcommand=scrollbar_relatorio.set)
    row_counter += 1

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

def abrir_formulario_pagamentos(container):
    for widget in container.winfo_children():
        widget.destroy()

    def handle_busca_fornecedor():
        termo_busca = entry_buscar_fornecedor.get()
        resultados = search_fornecedores_por_nome(termo_busca)

        for item in tabela_fornecedores.get_children():
            tabela_fornecedores.delete(item)
            
        if resultados:
            for fornecedor in resultados:
                tabela_fornecedores.insert(parent='', index='end', values=(
                    fornecedor.id, fornecedor.nome_fornecedor, fornecedor.cpf_cnpj, fornecedor.telefone, fornecedor.endereco
            ))

    dados_fornecedor_selecionado = {}

    def handle_selecao_fornecedor(event):
        item_selecionado_id = tabela_fornecedores.selection()
        if not item_selecionado_id:
            return
        
        id_da_linha = item_selecionado_id[0]
        valores = tabela_fornecedores.item(id_da_linha, 'values')
        dados_fornecedor_selecionado['id'] = int(valores[0])
        dados_fornecedor_selecionado['nome'] = valores[1]
        label_fornecedor_selecionado.config(text=f"Fornecedor Selecionado: {dados_fornecedor_selecionado['nome']}")

    def handle_salvar_pagamento():
        valor_nota = entry_valor.get()
        data_vencimento = entry_data_vencimento.get_date()

        if not valor_nota:
            messagebox.showerror("Erro de Validação","O valor da nota é OBRIGATÓRIO")
            return

        try:
            valor_decimal = float(valor_nota.replace(',','.'))
        except ValueError:
            messagebox.showerror("Erro de Formato", "O Valor Total deve ser um número válido.")
            return
        if 'id' not in dados_fornecedor_selecionado:
            messagebox.showwarning("Seleção Necessária", "Por favor, busque e selecione um fornecedor na tabela antes de salvar.")
            return
        try:
            data_pagamento_final = entry_data_pagamento.get_date()
        except ValueError:
            data_pagamento_final = None

        dados_pagamento = {
            'numero_nota': entry_numero_nota.get(),
            'data_vencimento': data_vencimento,
            'valor_nota': valor_decimal,
            'data_pagamento': data_pagamento_final,
            'fornecedor_id': dados_fornecedor_selecionado['id']
        }

        resultado = add_pagamento(dados_pagamento)
        if resultado:
            messagebox.showinfo("Sucesso", f"Pagamento ID {resultado.id} salvo com sucesso")
            limpar_formulario_pagamento()
        else:
            messagebox.showerror("Erro de Banco de Dados", "Não foi possível salvar o pagamento.")

    def limpar_formulario_pagamento():
        for item in tabela_fornecedores.get_children():
            tabela_fornecedores.delete(item)
        label_fornecedor_selecionado.config(text="Fornecedor Selecionado: Nenhum")
        entry_numero_nota.delete(0, tk.END)
        entry_data_vencimento.set_date(date.today())
        entry_valor.delete(0, tk.END)
        entry_data_pagamento.delete(0, tk.END)
        entry_buscar_fornecedor.delete(0, tk.END)
        entry_forma_pagamento.delete(0, tk.END)


    label_buscar_fornecedor = ttk.Label(container, text="Buscar Fornecedor:")
    entry_buscar_fornecedor = ttk.Entry(container, style='Padded.TEntry')
    botao_buscar_fornecedor = ttk.Button(container, text="Buscar", command=handle_busca_fornecedor)

    colunas = ('id', 'nome_fornecedor', 'cpf_cnpj','telefone', 'endereco')
    tabela_fornecedores = ttk.Treeview(container, columns=colunas, show='headings', height=4)
    tabela_fornecedores.heading('id', text='ID')
    tabela_fornecedores.heading('nome_fornecedor', text='Nome')
    tabela_fornecedores.heading('cpf_cnpj', text="CPF/CNPJ")
    tabela_fornecedores.heading('telefone', text='Telefone')
    tabela_fornecedores.heading('endereco', text='Endereço')
    tabela_fornecedores.column('id', width=40)
    tabela_fornecedores.column('nome_fornecedor', width=200)
    tabela_fornecedores.column('cpf_cnpj', width=120)
    tabela_fornecedores.column('telefone', width=100)
    tabela_fornecedores.column('endereco', width=250)
    label_fornecedor_selecionado = ttk.Label(container, text="Fornecedor Selecionado: Nenhum")

    label_numero_nota = ttk.Label(container, text="Número da nota:")
    entry_numero_nota = ttk.Entry(container, style='Padded.TEntry')

    label_valor = ttk.Label(container, text="Valor:")
    entry_valor = ttk.Entry(container, style='Padded.TEntry')

    label_data_vencimento = ttk.Label(container, text="Data de Vencimento:")
    entry_data_vencimento = DateEntry(container, date_pattern='dd/MM/yyyy', style='Padded.TEntry')

    label_data_pagamento = ttk.Label(container, text="Data de Pagamento:")
    entry_data_pagamento = DateEntry(container, date_pattern='dd/MM/yyyy', style='Padded.TEntry')
    entry_data_pagamento.delete(0, tk.END)

    label_forma_pagamento = ttk.Label(container, text="Forma de Pagamento")
    entry_forma_pagamento = ttk.Entry(container, style='Padded.TEntry')

    botao_salvar = ttk.Button(container, text="Salvar", command=handle_salvar_pagamento) # FALTA COMMAND

    row_counter = 0
    label_buscar_fornecedor.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    entry_buscar_fornecedor.grid(row=row_counter, column=1, padx=5, pady=5)
    botao_buscar_fornecedor.grid(row=row_counter, column=2, padx=5, pady=5)
    row_counter += 1

    tabela_fornecedores.grid(row=row_counter, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
    row_counter += 1
    
    label_fornecedor_selecionado.grid(row=row_counter, column=0, columnspan=4, padx=5, pady=5, sticky="w")
    tabela_fornecedores.bind('<<TreeviewSelect>>', handle_selecao_fornecedor)
    row_counter += 1
    
    label_numero_nota.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    entry_numero_nota.grid(row=row_counter, column=1, padx=5, pady=5)
    label_data_vencimento.grid(row=row_counter, column=2, padx=5, pady=5, sticky='w')
    entry_data_vencimento.grid(row=row_counter, column=3, padx=5, pady=5)
    row_counter += 1

    label_valor.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    entry_valor.grid(row=row_counter, column=1, padx=5, pady=5)
    label_data_pagamento.grid(row=row_counter, column=2, padx=5, pady=5, sticky='w')
    entry_data_pagamento.grid(row=row_counter, column=3, padx=5, pady=5)
    row_counter += 1

    label_forma_pagamento.grid(row=row_counter, column=0, padx=5, pady=5, sticky='w')
    entry_forma_pagamento.grid(row= row_counter, column=1,padx=5, pady=5)
    row_counter += 1

    botao_salvar.grid(row=row_counter, column=0, padx=4, pady=20)

def abrir_formulario_fornecedores(container):
    for widget in container.winfo_children():
        widget.destroy()
    
    def handle_salvar_fornecedor():
        fornecedor_nome = entry_fornecedor.get()
        fornecedor_cpfcnpj = entry_cpfcnpj.get()
        fornecedor_telefone = entry_telefone.get()
        fornecedor_endereco = entry_endereco.get()
        
        if not fornecedor_nome:
            messagebox.showwarning("Campo Obrigatório", "O campo 'Nome do Fornecedor' não pode estar vazio.")
            return
        
        dados_fornecedor = {
            'nome_fornecedor': fornecedor_nome,
            'cpf_cnpj': fornecedor_cpfcnpj,
            'telefone': fornecedor_telefone,
            'endereco': fornecedor_endereco
        }

        salvar_fornecedor = add_fornecedor(dados_fornecedor)
        if salvar_fornecedor:
            messagebox.showinfo("Sucesso", f"Fornecedor ID {salvar_fornecedor.id} salvo com sucesso.")
            limpar_formulario_fornecedor()
        else:
            messagebox.showerror("Erro de Banco de Dados", "Não foi possível salvar o fornecedor.")

    def limpar_formulario_fornecedor():
        entry_fornecedor.delete(0, tk.END)
        entry_cpfcnpj.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_endereco.delete(0, tk.END)

    # Linha 0 -----
    ttk.Label(container, text="Nome do Fornecedor:").grid(row=0, column=0, padx=5, pady=10, sticky="w")
    entry_fornecedor = ttk.Entry(container, style='Padded.TEntry')
    entry_fornecedor.grid(row=0, column=1, padx=5, pady=10)

    # Linha 1 -----

    ttk.Label(container, text="CPF/CNPJ:").grid(row=1, column=0, padx=5, pady=10, sticky="w")
    entry_cpfcnpj = ttk.Entry(container, style='Padded.TEntry')
    entry_cpfcnpj.grid(row=1, column=1, padx=5, pady=10)

    # Linha 2 -----

    ttk.Label(container, text="Endereço:").grid(row=2, column=0, padx=5, pady=10, sticky="w")
    entry_endereco = ttk.Entry(container, style='Padded.TEntry')
    entry_endereco.grid(row=2, column=1, padx=5, pady=10)

    # Linha 3 -----

    ttk.Label(container, text="Telefone:").grid(row=3, column=0, padx=5, pady=10, sticky="w")
    entry_telefone = ttk.Entry(container, style='Padded.TEntry')
    entry_telefone.grid(row=3, column=1, padx=5, pady=10)

    # Linha 4 -----

    botao_salvar_fornecedor = ttk.Button(container, text="Salvar Fornecedor", command=handle_salvar_fornecedor)
    botao_salvar_fornecedor.grid(row=4, column=0, columnspan=4, pady=20)

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
    menu_vendas.add_command(label="Vendas Não Pagas", command=lambda: abrir_formulario_vendas_nao_pagas(frame_principal))
    barra_de_menu.add_cascade(label="Vendas", menu=menu_vendas)
    menu_cadastro = tk.Menu(barra_de_menu, tearoff=0)
    menu_cadastro.add_command(label="Clientes", command=lambda: abrir_formulario_clientes(frame_principal))
    menu_cadastro.add_command(label="Fornecedores", command=lambda: abrir_formulario_fornecedores(frame_principal))
    barra_de_menu.add_cascade(label="Cadastro", menu=menu_cadastro)
    menu_financeiro = tk.Menu(barra_de_menu, tearoff=0)
    menu_financeiro.add_command(label="Adicionar Contas a Pagar", command=lambda: abrir_formulario_pagamentos(frame_principal))
    barra_de_menu.add_cascade(label="Financeiro", menu=menu_financeiro)
    
    menu_relatorios = tk.Menu(barra_de_menu, tearoff=0)
    menu_relatorios.add_command(label="Vendas", command=lambda: abrir_formulario_relatorios_vendas(frame_principal))
    menu_relatorios.add_command(label="Pagamentos", command=lambda: abrir_formulario_relatorio_pagamentos(frame_principal))
    barra_de_menu.add_cascade(label="Relatórios", menu=menu_relatorios)

    janela_principal.protocol("WM_DELETE_WINDOW", janela.destroy)

def handle_login(event=None):
    username = usuario_entry.get()
    password = senha_entry.get()
    
    autenticacao_usuario = verify_user(username, password)
    if autenticacao_usuario:
        logging.info(f"Login bem-sucedido para o usuário '{autenticacao_usuario.nome_usuario}'.")
        janela.withdraw()
        abrir_janela_principal()
    else:
        logging.warning(f"Tentativa de login falhou para o usuário '{usuario_entry.get()}'.")
        messagebox.showerror("Erro de Login, Usuário ou senha incorretos.")

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
janela.bind("<Return>", handle_login)

janela.mainloop()