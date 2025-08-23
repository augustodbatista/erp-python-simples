import tkinter as tk
from tkinter import ttk
from data_operations import search_clientes_por_nome

class WidgetBuscaCliente(ttk.Frame):
    def __init__(self, container, on_cliente_selecionado):
        super().__init__(container)
        self.on_cliente_selecionado = on_cliente_selecionado
        self.dados_cliente_selecionado = {}
        self.label_busca_cliente = ttk.Label(self, text="Buscar Cliente:")
        self.entry_busca_cliente = ttk.Entry(self, style='Padded.TEntry')
        self.botao_buscar_cliente = ttk.Button(self, text="Buscar", command=self._handle_busca_cliente)

        colunas = ('id', 'nome', 'telefone', 'endereco')
        self.tabela_clientes = ttk.Treeview(self, columns=colunas, show='headings', height=4)
        self.tabela_clientes.heading('id', text='ID')
        self.tabela_clientes.heading('nome', text='Nome')
        self.tabela_clientes.heading('telefone', text='Telefone')
        self.tabela_clientes.heading('endereco', text='Endereço')
        self.tabela_clientes.column('id', width=40)
        self.tabela_clientes.column('nome', width=200)
        self.tabela_clientes.column('telefone', width=100)
        self.tabela_clientes.column('endereco', width=250)

        self.label_cliente_selecionado = ttk.Label(self, text="Cliente Selecionado: Nenhum")

        #Layout
        row_counter = 0
        self.label_busca_cliente.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
        self.entry_busca_cliente.grid(row=row_counter, column=1, padx=5, pady=5)
        self.botao_buscar_cliente.grid(row=row_counter, column=2, padx=5, pady=5)
        row_counter += 1

        self.tabela_clientes.grid(row=row_counter, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        row_counter += 1

        self.label_cliente_selecionado.grid(row=row_counter, column=0, columnspan=4, padx=5, pady=5, sticky="w")
        self.tabela_clientes.bind('<<TreeviewSelect>>', self._handle_selecao_cliente)
    

    def _handle_busca_cliente(self):
        termo_busca = self.entry_busca_cliente.get()
        resultados = search_clientes_por_nome(termo_busca)
        
        # Limpa a tabela de resultados antigos (com a correção)
        for item in self.tabela_clientes.get_children():
            self.tabela_clientes.delete(item)
            
        if resultados:
            for cliente in resultados:
                self.tabela_clientes.insert(parent='', index='end', values=(
                    cliente.id, cliente.nome_cliente, cliente.telefone, cliente.endereco
                ))

    def _handle_selecao_cliente(self, event):
        item_selecionado_id = self.tabela_clientes.selection()
        if not item_selecionado_id:
            return
        
        id_da_linha = item_selecionado_id[0]
        valores = self.tabela_clientes.item(id_da_linha, 'values')
        self.dados_cliente_selecionado['id'] = int(valores[0])
        self.dados_cliente_selecionado['nome'] = valores[1]
        self.label_cliente_selecionado.config(text=f"Cliente Selecionado: {self.dados_cliente_selecionado['nome']}")
        
        if self.on_cliente_selecionado:
            self.on_cliente_selecionado(self.dados_cliente_selecionado)
    
