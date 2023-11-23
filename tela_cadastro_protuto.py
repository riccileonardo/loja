import tkinter 
from tkinter import ttk, messagebox
from datetime import datetime

class Atividades:
    def limpar_tela(self):
        #Limpa a tela quando chamado nas caixas de informação
        self.id_entrada.delete(0, tkinter.END)
        self.entrada_nomeProturo.delete(0, tkinter.END)
        self.entrada_Quantidade.delete(0, tkinter.END)
        self.entrada_valorProduto.delete(0, tkinter.END)

        self.atualizar_lista()

    def buscar_produto(self):    
        codigo = self.id_entrada.get()
        nome = self.entrada_nomeProduto.get()

        try:
            if codigo or nome:
                # Construir a consulta SQL com base nos campos preenchidos
                query = "SELECT * FROM estoque WHERE"
                params = []

                if codigo:
                    query += " IdProduto = %s"
                    params.append(codigo)

                if nome:
                    if params:
                        query += " AND"
                    query += " nomeProduto = %s"
                    params.append(nome)

                self.cursor.execute(query, params)
                resultados = self.cursor.fetchall()

                # Atualiza a lista diretamente com os resultados
                self.listaProduto.delete(*self.listaProduto.get_children())
                for resultado in resultados:
                    self.listaProduto.insert("", "end", values=(resultado[0], resultado[1], resultado[2], resultado[3]))

            else:
                self.atualizar_lista()

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao buscar os Produtos: {e}")

    def editar_produto(self):
        Id_produto = self.id_entrada.get()
        nome = self.entrada_nomeProturo.get()
        quantidade = self.entrada_Quantidade.get()
        valorCompra = self.entrada_valorProduto.get()

        try:
            if produto:
                # Verifica se o produto existe
                self.cursor.execute('SELECT * FROM estoque WHERE IdProduto=%s', (Id_produto,))
                produto = self.cursor.fetchone()
                if not produto:
                    messagebox.showerror("Erro", "Produto não encontrado.")
                    return

                # Se os campos nome, quantidade ou valor compra foram preenchidos, atualiza no banco
                if nome or quantidade or valorCompra:
                  
                    self.cursor.execute('UPDATE estoque SET nomeProduto=%s, quantidade=%s, valorCompra=%s WHERE IdProduto=%s',
                                        (nome or produto[1], quantidade or produto[2], valorCompra, Id_produto))
                    self.db_connection.commit()
                    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

                    self.atualizar_lista()
                    self.limpar_tela()
                else:
                    messagebox.showerror("Erro", "Pelo menos um campo (nomeProduto, quantidade, valorCompra) deve ser preenchido!")

            else:
                messagebox.showerror("Erro", "O campo ID deve ser preenchido!")

        except ValueError:
            messagebox.showerror("Erro", "valorCompra. Por favor, verifique a formatação.")
    
    def excluir_produto(self):
        Id_produto = self.id_entrada.get()

        try:
            if Id_produto:
                self.cursor.execute('SELECT * FROM estoque WHERE IdProduto=%s', (Id_produto,))
                produto = self.cursor.fetchone()
                if not produto:
                    messagebox.showerror("Erro", "Produto não encontrado.")
                    return

                resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este Produto?")
                
                if resposta:
                    self.cursor.execute('DELETE FROM estoque WHERE IdVeiculo=%s', (Id_produto,))
                    self.db_connection.commit()
                    messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

                    self.atualizar_lista()
                    self.limpar_tela()

            else:
                messagebox.showerror("Erro", "O campo ID deve ser preenchido!")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao excluir o Produto: {e}")

    def cadastrar_produto(self):
        nome = self.entrada_nomeProturo.get()
        quantidade = self.entrada_Quantidade.get()
        valorCompra = self.entrada_valorProduto.get()

        try:
            if nome and quantidade and valorCompra:
                self.cursor.execute('SELECT * FROM estoque WHERE nomeProduto=%s AND quantidade=%s AND valorCompra=%s',
                                    (nome, quantidade, valorCompra))
                veiculo = self.cursor.fetchone()

                if veiculo:
                    resposta = messagebox.askyesno("Erro", "Este Produto já está cadastrado. Deseja continuar mesmo assim?")
                    if not resposta:
                        return

                self.cursor.execute('INSERT INTO estoque (nomeProduto, quantidade, valorCompra) VALUES (%s, %s, %s)',
                                    (nome, quantidade, valorCompra))

                self.db_connection.commit()
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

                self.atualizar_lista()
                self.limpar_tela()

            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")

        except ValueError:
            messagebox.showerror("Erro", "valorCompra. Por favor, verifique a formatação..")

    def atualizar_lista(self):
        self.listaProduto.delete(*self.listaProduto.get_children())

        produtos = self.seleciona_lista()

        for produto in produtos:
            self.listaProduto.insert("", "end", values=(produto[0], produto[1], produto[2], produto[3]))

    def seleciona_lista(self):
        try:
            self.cursor.execute('SELECT * FROM tabalhopoo.estoque')
            return self.cursor.fetchall()
        except Exception as e:
            tkinter.messagebox.showerror("Erro", f"Ocorreu um erro ao selecionar os Produtos: {e}")

class TelaCadastro_produtos(Atividades):
    def __init__(self, db_connection, cursor,janela_master):
        self.db_connection = db_connection
        self.cursor = cursor
        self.janela_master = janela_master

    def abrir(self):
        # Cria a janela de cadastro
        self.janela_cadastro = tkinter.Toplevel(self.janela_master)
        self.janela_cadastro.title("Estoque")
        self.janela_cadastro.configure(background='#3f3e3e')
        self.janela_cadastro.geometry("1080x720")
        self.janela_cadastro.minsize(620, 500)
        self.janela_cadastro.grab_set()

        #Chamar função para criar o frame, botões e label.
        self.criar_frame()
        self.criar_button()
        self.criar_entrada()
        self.tabela_lista()
        
    def criar_button(self):
        # Botão limpar
        self.botao_limpar = tkinter.Button(self.frame_1, text="Limpar", font=("Helvetica", 12), command=self.limpar_tela ,bd=2, 
                                         bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
        self.botao_limpar.place(relx=0.20,rely=0.15,relheight=0.1,relwidth=0.1)
        
        # Botão novo
        self.botao_novo = tkinter.Button(self.frame_1, text="Novo", font=("Helvetica", 12), bd=2, command= self.cadastrar_produto,
                                         bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
        self.botao_novo.place(relx=0.32,rely=0.15,relheight=0.1,relwidth=0.1)
                
        # Botão buscar
        botao_buscar = tkinter.Button(self.frame_1, text="Buscar", font=("Helvetica", 12),  bd=2, command= self.buscar_produto,
                                         bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
        botao_buscar.place(relx=0.88,rely=0.15,relheight=0.1,relwidth=0.1)

        # Botão Exluir
        botao_exluir = tkinter.Button(self.frame_1, text="Exluir", font=("Helvetica", 12),  bd=2, command=self.excluir_produto,
                                         bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
        botao_exluir.place(relx=0.88,rely=0.88,relheight=0.1,relwidth=0.1)

        # Botão Editar
        botao_editar = tkinter.Button(self.frame_1, text="Editar", font=("Helvetica", 12),bd=2, command= self.editar_produto,
                                         bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
        botao_editar.place(relx=0.76,rely=0.88,relheight=0.1,relwidth=0.1)

    def criar_frame(self):
        #Frame 1
        self.frame_1 = tkinter.Frame(self.janela_cadastro, bd=2, bg='#4b4b49', highlightbackground='#c4a90d',highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.02, relheight=0.46, relwidth= 0.96)
        
        #Frame 2
        self.frame_2 = tkinter.Frame(self.janela_cadastro, bd=2, bg='#92928f', highlightbackground='#c4a90d',highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.52, relheight=0.46, relwidth= 0.96)

    def criar_entrada(self):
            # Campo para a Codigo
            tkinter.Label(self.frame_1, text="Codigo", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.05,relheight=0.1,relwidth=0.1)
            
            self.id_entrada = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.id_entrada.place(relx=0.01,rely=0.15,relheight=0.1,relwidth=0.1)

            # Campo para a Marca
            tkinter.Label(self.frame_1, text="Nome Produto", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.30,relheight=0.1,relwidth=0.2)
            
            self.entrada_nomeProturo = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_nomeProturo.place(relx=0.01,rely=0.40,relheight=0.1,relwidth=0.60)

            # Campo para a Modelo
            tkinter.Label(self.frame_1, text="Quantidade", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.52,relheight=0.1,relwidth=0.2)
            
            self.entrada_Quantidade = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_Quantidade.place(relx=0.01,rely=0.62,relheight=0.1,relwidth=0.60)

            # Campo para a Ano
            tkinter.Label(self.frame_1, text="Valor Compra", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.70, rely=0.30,relheight=0.1,relwidth=0.2)
            
            self.entrada_valorProduto = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_valorProduto.place(relx=0.70,rely=0.40,relheight=0.1,relwidth=0.20)

    def tabela_lista(self):
        self.listaProduto = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3", "col4"))
        self.atualizar_lista()

        # Estilo e configurações da Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))

        self.listaProduto.heading("#0", text="")
        self.listaProduto.heading("#1", text="Codigo")
        self.listaProduto.heading("#2", text="Nome produto")
        self.listaProduto.heading("#3", text="Quantidade")
        self.listaProduto.heading("#4", text="Valor compra")
        self.listaProduto.column("#0", width=1)
        self.listaProduto.column("#1", width=50)
        self.listaProduto.column("#2", width=50)
        self.listaProduto.column("#3", width=50)
        self.listaProduto.column("#4", width=50)
        self.listaProduto.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.90)

        # Adicionar barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(self.frame_2, orient="vertical", command=self.listaProduto.yview)
        scrollbar_y.place(relx=0.99, rely=0.05, relheight=0.90)
        self.listaProduto.configure(yscrollcommand=scrollbar_y.set)
        
        # Adicionar barra de rolagem horizontal
        scrollbar_x = ttk.Scrollbar(self.frame_2, orient="horizontal", command=self.listaProduto.xview)
        scrollbar_x.place(relx=0.01, rely=0.95, relwidth=0.98)
        self.listaProduto.configure(xscrollcommand=scrollbar_x.set)
        

