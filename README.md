# Dashboard de Cadastro e Controle Financeiro

## Visão Geral

Este projeto é uma aplicação GUI desenvolvida com Python usando o Tkinter e a biblioteca Pandas para gerenciamento de registros financeiros e documentos. O aplicativo é dividido em três abas principais:

1. **Placas**: Gerencia registros de placas, incluindo informações sobre despachantes, veículos, valores e pagamentos.
2. **Despesas**: Gerencia registros de despesas, com informações sobre data, categoria, descrição e valor.
3. **Documentos**: Permite a visualização e a impressão de documentos PDF específicos, bem como o gerenciamento de registros de documentos.

## Estrutura dos Arquivos

### Arquivos Python

- **`main.py`**:
  - Contém a lógica principal da aplicação.
  - Inicializa a interface gráfica e as abas.
  - Implementa as funcionalidades de adicionar, visualizar e salvar registros de placas, despesas e documentos.
  - Gerencia a abertura de arquivos PDF.

- **`Despesas.py`**:
  - Gerencia a aba de despesas.
  - Permite adicionar e visualizar registros de despesas.
  - Inclui um botão para salvar as despesas em um arquivo CSV.

- **`Documentos.py`**:
  - Gerencia a aba de documentos.
  - Permite adicionar e visualizar registros de documentos.
  - Inclui botões para abrir PDFs específicos para impressão.

### Arquivos CSV

- **`cadastro_placas.csv`**:
  - Armazena os registros de placas.
  - Colunas: `Despachante`, `Data`, `Placa`, `Veículo`, `Valor`, `Pagamento`.

- **`despesas.csv`**:
  - Armazena os registros de despesas.
  - Colunas: `Data`, `Categoria`, `Descrição`, `Valor`.

- **`documentos.csv`**:
  - Armazena os registros de documentos.
  - Colunas: `Data`, `Tipo`, `Descrição`.

### Arquivos PDF

- **`documento_daniela.pdf`**:
  - Documento PDF específico para Daniela Paludo.

- **`documento_jorce.pdf`**:
  - Documento PDF específico para Jorce Schmidt Storck.

- **`documento_beatriz.pdf`**:
  - Documento PDF específico para Beatriz Silva Geraldo.

- **`nota_fiscal.pdf`**:
  - Nota fiscal em formato PDF.

## Funcionalidades

### Aba de Placas

- **Adicionar Registro**: Permite adicionar um novo registro de placa, incluindo despachante, data, placa, veículo, valor e forma de pagamento. Verifica o comprimento da placa e o formato da data.
- **Visualizar Registros**: Mostra os registros de placas em uma tabela. Filtra registros com base no mês selecionado e destaca pagamentos "Deve" em vermelho.
- **Salvar em CSV**: Salva os registros atuais no arquivo CSV `cadastro_placas.csv`.

### Aba de Despesas

- **Adicionar Despesa**: Permite adicionar uma nova despesa, incluindo data, categoria, descrição e valor. Verifica o formato da data.
- **Visualizar Despesas**: Mostra os registros de despesas em uma tabela.
- **Salvar em CSV**: Salva os registros atuais no arquivo CSV `despesas.csv`.

### Aba de Documentos

- **Adicionar Documento**: Permite adicionar um novo registro de documento, incluindo data, tipo e descrição. Verifica o formato da data.
- **Visualizar Documentos**: Mostra os registros de documentos em uma tabela.
- **Botões de PDF**: Abre documentos PDF específicos para impressão.
  - **Documento Daniela**
  - **Documento Jorce**
  - **Documento Beatriz**
  - **Nota Fiscal**
- **Salvar em CSV**: Salva os registros atuais no arquivo CSV `documentos.csv`.

## Requisitos

- Python 3.x
- Tkinter (para interface gráfica)
- Pandas (para manipulação de dados)
- Webbrowser (para abrir PDFs)

## Instruções para Executar o Projeto

1. **Instale os requisitos**:
   - Certifique-se de ter o Python 3.x instalado.
   - Instale a biblioteca Pandas usando `pip install pandas`.

2. **Configure o ambiente**:
   - Coloque os arquivos PDF no mesmo diretório do script Python ou ajuste os caminhos no código.

3. **Execute o aplicativo**:
   - Navegue até o diretório onde o arquivo `main.py` está localizado.
   - Execute o script com o comando `python main.py`.

4. **Utilize o aplicativo**:
   - Adicione registros nas abas de placas, despesas e documentos conforme necessário.
   - Use os botões na aba de Documentos para abrir e imprimir PDFs específicos.

## Nota

- Certifique-se de que os arquivos CSV e PDF estejam corretamente formatados e localizados no diretório especificado para que o aplicativo funcione corretamente.
- A aplicação foi projetada para ser simples e fácil de usar, com validações básicas e uma interface gráfica amigável.

## Conclusão

Este projeto fornece uma solução prática para o gerenciamento de registros financeiros e documentos, com uma interface gráfica intuitiva e funcionalidades robustas para atender às necessidades de controle e visualização de dados.

---

Sinta-se à vontade para ajustar ou expandir este README conforme necessário para atender às suas necessidades específicas ou para fornecer informações adicionais.
