import tkinter 
from tkinter import ttk, messagebox
from tela_relatorio_clientes import TelaRelatorio_clientes

#classe para separar as funções usadas para o crud do cliente
class Atividades:

    def limpar_tela(self):
        #Limpa a tela quando chamado nas caixas de informação
        self.id_entrada.delete(0, tkinter.END)
        self.entrada_Nome.delete(0, tkinter.END)
        self.entrada_Telefone.delete(0, tkinter.END)
        self.entrada_Cpf.delete(0, tkinter.END)
        self.entrada_Idade.delete(0, tkinter.END)

 
    def editar_cliente(self):
        IdCliente = self.id_entrada.get()
        nome = self.entrada_Nome.get()
        telefone = self.entrada_Telefone.get()
        cpf = self.entrada_Cpf.get() 

        try:
            if IdCliente:
                # Verifica se o cliente existe
                self.cursor.execute('SELECT * FROM clientes WHERE IdCliente=%s', (IdCliente,))
                cliente = self.cursor.fetchone()
                if not cliente:
                    messagebox.showerror("Erro", "CLiente não encontrado.")
                    return

                # Se os campos nome, telefone ou cpf foram preenchidos, atualiza no banco
                if nome or telefone or cpf:

                    self.cursor.execute('UPDATE clientes SET nome=%s, telefone=%s, cpf=%s WHERE IdCliente=%s',
                                        (nome or cliente[1], telefone or cliente[2], IdCliente))
                    self.db_connection.commit()
                    messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")

                    self.limpar_tela()
                else:
                    messagebox.showerror("Erro", "Pelo menos um campo (Nome, Telefone, CPF) deve ser preenchido!")

            else:
                messagebox.showerror("Erro", "O campo ID deve ser preenchido!")

        except ValueError:
            messagebox.showerror("Erro", "CPF invalidado. Por favor, verifique novamente.")
    
    def excluir_cliente(self):
        IdCliente = self.id_entrada.get()

        try:
            if IdCliente:
                self.cursor.execute('SELECT * FROM clientes WHERE IdCliente=%s', (IdCliente,))
                cliente = self.cursor.fetchone()
                if not cliente:
                    messagebox.showerror("Erro", "Cliente não encontrado.")
                    return

                resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este Cliente?")
                
                if resposta:
                    self.cursor.execute('DELETE FROM clientes WHERE IdCliente=%s', (IdCliente,))
                    self.db_connection.commit()
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")

                    self.limpar_tela()

            else:
                messagebox.showerror("Erro", "O campo ID deve ser preenchido!")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao excluir o Cliente: {e}")

    def cadastrar_cliente(self):
        nome = self.entrada_Nome.get()
        telefone = self.entrada_Telefone.get()
        cpf = self.entrada_Cpf.get()
        idade = self.entrada_Idade.get()  

        try:
            if nome and cpf and telefone and idade:
                self.cursor.execute('SELECT * FROM clientes WHERE NomCliente=%s AND telefone=%s AND cpf=%s AND idade=%s',
                                    (nome, cpf, telefone, idade))
                cliente = self.cursor.fetchone()

                if cliente:
                    resposta = messagebox.askyesno("Cliente já cadastrado", "Este cliente já está cadastrado. Deseja continuar mesmo assim?")
                    if not resposta:
                        return

                self.cursor.execute('INSERT INTO clientes (NomCliente, telefone, cpf, idade) VALUES (%s, %s, %s,%s)',
                                    (nome, cpf, telefone, idade))

                self.db_connection.commit()
                messagebox.showinfo("Sucesso", "cliente cadastrado com sucesso!")

                self.limpar_tela()

            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")

        except ValueError:
            messagebox.showerror("Erro", "CPF invalidado. Por favor, verifique novamente.")

    def seleciona_lista(self):
        try:
            self.cursor.execute('SELECT * FROM tabalhopoo.clientes')
            return self.cursor.fetchall()
        except Exception as e:
            tkinter.messagebox.showerror("Erro", f"Ocorreu um erro ao selecionar os clientes: {e}")

class TelaCadastro_cliente(Atividades):
    def __init__(self, db_connection, cursor,janela_master):
        self.db_connection = db_connection
        self.cursor = cursor
        self.janela_master = janela_master

    #Cria a tela e chama sus funções que compoem a tela
    def abrir(self):
        # Cria a janela de cadastro de cliente
        self.janela_cadastro = tkinter.Toplevel(self.janela_master)
        self.janela_cadastro.title("Cadastro de Veículos")
        self.janela_cadastro.configure(background='#3f3e3e')
        self.janela_cadastro.geometry("1080x720")
        self.janela_cadastro.minsize(620, 500)
        self.janela_cadastro.grab_set()

        #Chamar função para criar o frame, botões, label e barra de menus.
        self.criar_frame()
        self.criar_button()
        self.criar_entrada()
        self.AppComBarraDeMenu()
        
    # Crie a barra de menu
    def AppComBarraDeMenu(self):

        #variavel definida para chamar o relatorio
        self.relatorioClientes = TelaRelatorio_clientes(self.db_connection, self.cursor, self.janela_cadastro)
        
        #Cria o menu e define a janela que ele vai ficar
        barra_menu = tkinter.Menu(self.janela_cadastro)
        self.janela_cadastro.config(menu=barra_menu)

        # Adicione um menu "Relatorio" à barra de menu
        menu_relatorio = tkinter.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Relatorios", menu=menu_relatorio)
        menu_relatorio.add_command(label="Relatorio Clientes", command=self.acao_abrir_relatorio)
        menu_relatorio.add_separator()
        menu_relatorio.add_command(label="Sair", command=self.sair_cadastro_clientes)

    def acao_abrir_relatorio(self):
        self.relatorioClientes.abrir()

    def sair_cadastro_clientes(self):
        self.janela_cadastro.destroy()
    #Fim da barra de menu

    #Criar botões
    def criar_button(self):
        # Botão Limpar
        self.botao_limpar = tkinter.Button(self.frame_1, text="Limpar", font=("Helvetica", 12), command=self.limpar_tela,
                                        bd=2, bg='#c4a90d', highlightbackground='#ffc400', highlightthickness=2, width=20)
        self.botao_limpar.place(relx=0.20, rely=0.15, relheight=0.08, relwidth=0.1)

        # Botão Novo
        self.botao_novo = tkinter.Button(self.frame_1, text="Novo", font=("Helvetica", 12), bd=2, command=self.cadastrar_cliente,
                                        bg='#c4a90d', highlightbackground='#ffc400', highlightthickness=2, width=20)
        self.botao_novo.place(relx=0.32, rely=0.15, relheight=0.08, relwidth=0.1)

        # Botão Excluir
        botao_excluir = tkinter.Button(self.frame_1, text="Excluir", font=("Helvetica", 12), bd=2, command=self.excluir_cliente,
                                    bg='#c4a90d', highlightbackground='#ffc400', highlightthickness=2, width=20)
        botao_excluir.place(relx=0.88, rely=0.15, relheight=0.08, relwidth=0.1)

        # Botão Editar
        botao_editar = tkinter.Button(self.frame_1, text="Editar", font=("Helvetica", 12), bd=2, command=self.editar_cliente,
                                    bg='#c4a90d', highlightbackground='#ffc400', highlightthickness=2, width=20)
        botao_editar.place(relx=0.76, rely=0.15, relheight=0.08, relwidth=0.1)

    #Criar Frames
    def criar_frame(self):
        #Frame 1
        self.frame_1 = tkinter.Frame(self.janela_cadastro, bd=2, bg='#4b4b49', highlightbackground='#c4a90d',highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.02, relheight=0.96, relwidth= 0.96)
        
    #Criar entradas
    def criar_entrada(self):
            # Campo para a Codigo
            tkinter.Label(self.frame_1, text="Codigo", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.05,relheight=0.1,relwidth=0.1)
            
            self.id_entrada = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.id_entrada.place(relx=0.01,rely=0.15,relheight=0.05,relwidth=0.1)

            # Campo para a NOME
            tkinter.Label(self.frame_1, text="NOME CLIENTE", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.30,relheight=0.1,relwidth=0.2)
            
            self.entrada_Nome = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_Nome.place(relx=0.01,rely=0.40,relheight=0.05,relwidth=0.60)

            # Campo para a TELEFONE
            tkinter.Label(self.frame_1, text="TELEFONE", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.52,relheight=0.1,relwidth=0.2)
            
            self.entrada_Telefone = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_Telefone.place(relx=0.01,rely=0.62,relheight=0.05,relwidth=0.20)

            # Campo para a CPF
            tkinter.Label(self.frame_1, text="CPF", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.70, rely=0.30,relheight=0.1,relwidth=0.2)
            
            self.entrada_Cpf = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_Cpf.place(relx=0.70,rely=0.40,relheight=0.05,relwidth=0.20)

             # Campo para a Idade
            tkinter.Label(self.frame_1, text="IDADE", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.70, rely=0.52,relheight=0.1,relwidth=0.2)
            
            self.entrada_Idade = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_Idade.place(relx=0.70,rely=0.62,relheight=0.05,relwidth=0.20)

            # Campo para a e ENDEREÇO
            tkinter.Label(self.frame_1, text="ENDEREÇO", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.72,relheight=0.1,relwidth=0.2)
            
            self.entrada_Idade = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_Idade.place(relx=0.01,rely=0.82,relheight=0.05,relwidth=0.20)