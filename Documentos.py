import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import pandas as pd
import webbrowser  # Importa o webbrowser para abrir PDFs

# Nome dos arquivos CSV
CSV_PLACAS = 'cadastro_placas.csv'
CSV_DESPESAS = 'despesas.csv'
CSV_DOCUMENTOS = 'documentos.csv'

# Caminhos dos arquivos PDF
PDF_DOCUMENTO_DANIELA = 'DESPACHANTE DANIELA.pdf'
PDF_DOCUMENTO_JORCE = 'DESPACHANTE JORCE.pdf'
PDF_DOCUMENTO_BEATRIZ = 'BEATRIZ.pdf'
PDF_NOTA_FISCAL = 'nota_fiscal.pdf'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard de Cadastro")

        # Cria o notebook (abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill='both')

        # Cria as abas
        self.placas_frame = ttk.Frame(self.notebook)
        self.despesas_frame = ttk.Frame(self.notebook)
        self.documentos_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.placas_frame, text='Placas')
        self.notebook.add(self.despesas_frame, text='Despesas')
        self.notebook.add(self.documentos_frame, text='Documentos')

        # Inicializa as interfaces para cada aba
        self.placas_interface()
        self.despesas_interface()
        self.documentos_interface()

    def carregar_dados(self, arquivo):
        if os.path.exists(arquivo):
            return pd.read_csv(arquivo)
        else:
            # Cria um DataFrame vazio com as colunas esperadas
            if arquivo == CSV_PLACAS:
                return pd.DataFrame(columns=['Despachante', 'Data', 'Placa', 'Veículo', 'Valor', 'Pagamento'])
            elif arquivo == CSV_DESPESAS:
                return pd.DataFrame(columns=['Data', 'Categoria', 'Descrição', 'Valor'])
            elif arquivo == CSV_DOCUMENTOS:
                return pd.DataFrame(columns=['Data', 'Tipo', 'Descrição'])
            else:
                raise ValueError("Arquivo desconhecido")

    def placas_interface(self):
        self.df_placas = self.carregar_dados(CSV_PLACAS)

        frame = ttk.Frame(self.placas_frame, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos de entrada
        ttk.Label(frame, text="Despachante").grid(row=0, column=0, sticky=tk.W)
        self.despachante_combobox = ttk.Combobox(frame, values=['Particular', 'Daniela Paludo', 'Jorce Schmidt Storck', 'Beatriz Silva Geraldo'])
        self.despachante_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Data").grid(row=1, column=0, sticky=tk.W)
        self.data_entry = ttk.Entry(frame)
        self.data_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.data_btn = ttk.Button(frame, text="Data Atual", command=self.preencher_data_atual)
        self.data_btn.grid(row=1, column=2, padx=10)

        ttk.Label(frame, text="Placa").grid(row=2, column=0, sticky=tk.W)
        self.placa_entry = ttk.Entry(frame, validate="key")
        self.placa_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))
        self.placa_entry.config(validate="key", validatecommand=(self.root.register(lambda p: len(p) <= 7), "%P"))

        ttk.Label(frame, text="Veículo").grid(row=3, column=0, sticky=tk.W)
        self.veiculo_combobox = ttk.Combobox(frame, values=['Carro', 'Moto', 'Reboque', 'Caminhonete', 'Caminhão', 'Suporte', 'Pintura', 'Remarcação'])
        self.veiculo_combobox.grid(row=3, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Valor").grid(row=4, column=0, sticky=tk.W)
        self.valor_entry = ttk.Entry(frame)
        self.valor_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Pagamento").grid(row=5, column=0, sticky=tk.W)
        self.pagamento_combobox = ttk.Combobox(frame, values=['Dinheiro', 'Pix', 'Deve'])
        self.pagamento_combobox.grid(row=5, column=1, sticky=(tk.W, tk.E))

        # Botão para adicionar o registro
        adicionar_btn = ttk.Button(frame, text="Adicionar Registro", command=self.adicionar_registro_placa)
        adicionar_btn.grid(row=6, columnspan=3, pady=10)

        # Seleção de mês
        ttk.Label(frame, text="Mês").grid(row=7, column=0, sticky=tk.W)
        self.mes_combobox = ttk.Combobox(frame, values=['Todos', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
        self.mes_combobox.set('Todos')
        self.mes_combobox.grid(row=7, column=1, sticky=(tk.W, tk.E))
        self.mes_combobox.bind('<<ComboboxSelected>>', self.atualizar_visualizacao_placas)

        # Árvore para visualização
        columns = ['Despachante', 'Data', 'Placa', 'Veículo', 'Valor', 'Pagamento']
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.tree.grid(row=8, column=0, columnspan=3)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        # Botão para salvar CSV
        salvar_btn = ttk.Button(frame, text="Salvar em CSV", command=lambda: self.salvar_csv(CSV_PLACAS))
        salvar_btn.grid(row=9, columnspan=3, pady=10)

        # Inicializa a visualização com os dados carregados
        self.atualizar_visualizacao_placas()

    def despesas_interface(self):
        self.df_despesas = self.carregar_dados(CSV_DESPESAS)

        frame = ttk.Frame(self.despesas_frame, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos de entrada
        ttk.Label(frame, text="Data").grid(row=0, column=0, sticky=tk.W)
        self.data_despesa_entry = ttk.Entry(frame)
        self.data_despesa_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Categoria").grid(row=1, column=0, sticky=tk.W)
        self.categoria_entry = ttk.Entry(frame)
        self.categoria_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Descrição").grid(row=2, column=0, sticky=tk.W)
        self.descricao_entry = ttk.Entry(frame)
        self.descricao_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Valor").grid(row=3, column=0, sticky=tk.W)
        self.valor_despesa_entry = ttk.Entry(frame)
        self.valor_despesa_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

        # Botão para adicionar a despesa
        adicionar_despesa_btn = ttk.Button(frame, text="Adicionar Despesa", command=self.adicionar_despesa)
        adicionar_despesa_btn.grid(row=4, columnspan=2, pady=10)

        # Árvore para visualização
        columns = ['Data', 'Categoria', 'Descrição', 'Valor']
        self.tree_despesas = ttk.Treeview(frame, columns=columns, show='headings')
        self.tree_despesas.grid(row=5, column=0, columnspan=2)

        for col in columns:
            self.tree_despesas.heading(col, text=col)
            self.tree_despesas.column(col, width=120)

        # Botão para salvar CSV
        salvar_btn_despesas = ttk.Button(frame, text="Salvar em CSV", command=lambda: self.salvar_csv(CSV_DESPESAS))
        salvar_btn_despesas.grid(row=6, columnspan=2, pady=10)

        # Inicializa a visualização com os dados carregados
        self.atualizar_visualizacao_despesas()

    def documentos_interface(self):
        self.df_documentos = self.carregar_dados(CSV_DOCUMENTOS)

        frame = ttk.Frame(self.documentos_frame, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Campos de entrada
        ttk.Label(frame, text="Data").grid(row=0, column=0, sticky=tk.W)
        self.data_documento_entry = ttk.Entry(frame)
        self.data_documento_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Tipo").grid(row=1, column=0, sticky=tk.W)
        self.tipo_entry = ttk.Entry(frame)
        self.tipo_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Descrição").grid(row=2, column=0, sticky=tk.W)
        self.descricao_documento_entry = ttk.Entry(frame)
        self.descricao_documento_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

        # Botão para adicionar o documento
        adicionar_documento_btn = ttk.Button(frame, text="Adicionar Documento", command=self.adicionar_documento)
        adicionar_documento_btn.grid(row=3, columnspan=2, pady=10)

        # Árvore para visualização
        columns = ['Data', 'Tipo', 'Descrição']
        self.tree_documentos = ttk.Treeview(frame, columns=columns, show='headings')
        self.tree_documentos.grid(row=4, column=0, columnspan=2)

        for col in columns:
            self.tree_documentos.heading(col, text=col)
            self.tree_documentos.column(col, width=120)

        # Botão para salvar CSV
        salvar_btn_documentos = ttk.Button(frame, text="Salvar em CSV", command=lambda: self.salvar_csv(CSV_DOCUMENTOS))
        salvar_btn_documentos.grid(row=5, columnspan=2, pady=10)

        # Botões para abrir PDFs
        documento_daniela_btn = ttk.Button(frame, text="Documento Daniela", command=lambda: self.abrir_pdf(PDF_DOCUMENTO_DANIELA))
        documento_daniela_btn.grid(row=6, column=0, pady=5, sticky=(tk.W, tk.E))
        
        documento_jorce_btn = ttk.Button(frame, text="Documento Jorce", command=lambda: self.abrir_pdf(PDF_DOCUMENTO_JORCE))
        documento_jorce_btn.grid(row=7, column=0, pady=5, sticky=(tk.W, tk.E))
        
        documento_beatriz_btn = ttk.Button(frame, text="Documento Beatriz", command=lambda: self.abrir_pdf(PDF_DOCUMENTO_BEATRIZ))
        documento_beatriz_btn.grid(row=8, column=0, pady=5, sticky=(tk.W, tk.E))

        nota_fiscal_btn = ttk.Button(frame, text="Nota Fiscal", command=lambda: self.abrir_pdf(PDF_NOTA_FISCAL))
        nota_fiscal_btn.grid(row=9, column=0, pady=5, sticky=(tk.W, tk.E))

        # Inicializa a visualização com os dados carregados
        self.atualizar_visualizacao_documentos()

    def abrir_pdf(self, caminho_pdf):
        if os.path.isfile(caminho_pdf):
            webbrowser.open(caminho_pdf)
        else:
            messagebox.showerror("Erro", "Arquivo PDF não encontrado.")

    def adicionar_registro_placa(self):
        despachante = self.despachante_combobox.get()
        data = self.data_entry.get()
        placa = self.placa_entry.get()
        veiculo = self.veiculo_combobox.get()
        valor = self.valor_entry.get()
        pagamento = self.pagamento_combobox.get()

        # Valida o comprimento da placa
        if len(placa) > 7:
            messagebox.showerror("Erro", "A placa deve ter no máximo 7 caracteres.")
            return

        # Valida o formato da data
        try:
            datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Erro", "O formato da data deve ser dd/mm/aaaa.")
            return

        # Adiciona o prefixo R$ ao valor se ainda não estiver presente
        if not valor.startswith("R$"):
            valor = f"R${valor}"

        # Cria um DataFrame temporário com o novo registro
        novo_registro = pd.DataFrame([{
            'Despachante': despachante,
            'Data': data,
            'Placa': placa,
            'Veículo': veiculo,
            'Valor': valor,
            'Pagamento': pagamento
        }])
        
        # Adiciona o novo registro ao DataFrame existente
        self.df_placas = pd.concat([self.df_placas, novo_registro], ignore_index=True)

        # Atualiza a visualização
        self.atualizar_visualizacao_placas()

        # Salva os dados no CSV
        self.salvar_csv(CSV_PLACAS)

        # Limpa os campos de entrada
        self.despachante_combobox.set('')
        self.data_entry.delete(0, tk.END)
        self.placa_entry.delete(0, tk.END)
        self.veiculo_combobox.set('')
        self.valor_entry.delete(0, tk.END)
        self.pagamento_combobox.set('')

    def adicionar_despesa(self):
        data = self.data_despesa_entry.get()
        categoria = self.categoria_entry.get()
        descricao = self.descricao_entry.get()
        valor = self.valor_despesa_entry.get()

        # Valida o formato da data
        try:
            datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Erro", "O formato da data deve ser dd/mm/aaaa.")
            return

        # Adiciona o prefixo R$ ao valor se ainda não estiver presente
        if not valor.startswith("R$"):
            valor = f"R${valor}"

        # Cria um DataFrame temporário com o novo registro
        nova_despesa = pd.DataFrame([{
            'Data': data,
            'Categoria': categoria,
            'Descrição': descricao,
            'Valor': valor
        }])
        
        # Adiciona o novo registro ao DataFrame existente
        self.df_despesas = pd.concat([self.df_despesas, nova_despesa], ignore_index=True)

        # Atualiza a visualização
        self.atualizar_visualizacao_despesas()

        # Salva os dados no CSV
        self.salvar_csv(CSV_DESPESAS)

        # Limpa os campos de entrada
        self.data_despesa_entry.delete(0, tk.END)
        self.categoria_entry.delete(0, tk.END)
        self.descricao_entry.delete(0, tk.END)
        self.valor_despesa_entry.delete(0, tk.END)

    def adicionar_documento(self):
        data = self.data_documento_entry.get()
        tipo = self.tipo_entry.get()
        descricao = self.descricao_documento_entry.get()

        # Valida o formato da data
        try:
            datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Erro", "O formato da data deve ser dd/mm/aaaa.")
            return

        # Cria um DataFrame temporário com o novo registro
        novo_documento = pd.DataFrame([{
            'Data': data,
            'Tipo': tipo,
            'Descrição': descricao
        }])
        
        # Adiciona o novo registro ao DataFrame existente
        self.df_documentos = pd.concat([self.df_documentos, novo_documento], ignore_index=True)

        # Atualiza a visualização
        self.atualizar_visualizacao_documentos()

        # Salva os dados no CSV
        self.salvar_csv(CSV_DOCUMENTOS)

        # Limpa os campos de entrada
        self.data_documento_entry.delete(0, tk.END)
        self.tipo_entry.delete(0, tk.END)
        self.descricao_documento_entry.delete(0, tk.END)

    def atualizar_visualizacao_placas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Filtra os dados com base no mês selecionado
        mes_selecionado = self.mes_combobox.get()
        if mes_selecionado != 'Todos':
            # Mapeia o nome do mês para o número do mês
            meses = {
                'Janeiro': '01',
                'Fevereiro': '02',
                'Março': '03',
                'Abril': '04',
                'Maio': '05',
                'Junho': '06',
                'Julho': '07',
                'Agosto': '08',
                'Setembro': '09',
                'Outubro': '10',
                'Novembro': '11',
                'Dezembro': '12'
            }
            mes_num = meses[mes_selecionado]
            df_filtrado = self.df_placas[self.df_placas['Data'].str[3:5] == mes_num]
        else:
            df_filtrado = self.df_placas

        for index, row in df_filtrado.iterrows():
            if row['Pagamento'] == 'Deve':
                self.tree.insert("", tk.END, values=list(row), tags=('deve',))
            else:
                self.tree.insert("", tk.END, values=list(row))
        self.tree.tag_configure('deve', foreground='red')

    def atualizar_visualizacao_despesas(self):
        for row in self.tree_despesas.get_children():
            self.tree_despesas.delete(row)

        for index, row in self.df_despesas.iterrows():
            self.tree_despesas.insert("", tk.END, values=list(row))

    def atualizar_visualizacao_documentos(self):
        for row in self.tree_documentos.get_children():
            self.tree_documentos.delete(row)

        for index, row in self.df_documentos.iterrows():
            self.tree_documentos.insert("", tk.END, values=list(row))

    def salvar_csv(self, arquivo):
        if arquivo == CSV_PLACAS:
            self.df_placas.to_csv(arquivo, index=False)
        elif arquivo == CSV_DESPESAS:
            self.df_despesas.to_csv(arquivo, index=False)
        elif arquivo == CSV_DOCUMENTOS:
            self.df_documentos.to_csv(arquivo, index=False)

    def preencher_data_atual(self):
        data_atual = datetime.now().strftime('%d/%m/%Y')
        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(0, data_atual)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
