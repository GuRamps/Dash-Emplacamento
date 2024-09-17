import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime
import os

CSV_DESPESAS = 'despesas.csv'

class DespesasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Despesas")

        # Carrega os dados
        self.df_despesas = self.carregar_dados()

        # Layout
        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos de entrada
        ttk.Label(frame, text="Data (dd/mm/aaaa)").grid(row=0, column=0, sticky=tk.W)
        self.data_entry = ttk.Entry(frame)
        self.data_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Categoria").grid(row=1, column=0, sticky=tk.W)
        self.categoria_entry = ttk.Entry(frame)
        self.categoria_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Descrição").grid(row=2, column=0, sticky=tk.W)
        self.descricao_entry = ttk.Entry(frame)
        self.descricao_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Valor").grid(row=3, column=0, sticky=tk.W)
        self.valor_entry = ttk.Entry(frame)
        self.valor_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

        ttk.Button(frame, text="Adicionar Despesa", command=self.adicionar_despesa).grid(row=4, columnspan=2, pady=10)

        # Árvore para visualização
        columns = ['Data', 'Categoria', 'Descrição', 'Valor']
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.tree.grid(row=5, column=0, columnspan=2)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        # Adiciona botão para salvar CSV
        ttk.Button(frame, text="Salvar em CSV", command=self.salvar_csv).grid(row=6, columnspan=2, pady=10)

        # Inicializa a visualização com os dados carregados
        self.atualizar_visualizacao()

    def carregar_dados(self):
        if os.path.exists(CSV_DESPESAS):
            return pd.read_csv(CSV_DESPESAS)
        else:
            return pd.DataFrame(columns=['Data', 'Categoria', 'Descrição', 'Valor'])

    def adicionar_despesa(self):
        data = self.data_entry.get()
        categoria = self.categoria_entry.get()
        descricao = self.descricao_entry.get()
        valor = self.valor_entry.get()

        try:
            datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            tk.messagebox.showerror("Erro", "O formato da data deve ser dd/mm/aaaa.")
            return

        if not valor.startswith("R$"):
            valor = f"R${valor}"

        novo_registro = pd.DataFrame([{
            'Data': data,
            'Categoria': categoria,
            'Descrição': descricao,
            'Valor': valor
        }])

        self.df_despesas = pd.concat([self.df_despesas, novo_registro], ignore_index=True)
        self.atualizar_visualizacao()
        self.salvar_csv()

    def atualizar_visualizacao(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, row in self.df_despesas.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def salvar_csv(self):
        self.df_despesas.to_csv(CSV_DESPESAS, index=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = DespesasApp(root)
    root.mainloop()
