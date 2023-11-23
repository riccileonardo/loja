import tkinter 
import tkinter.filedialog
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import webbrowser




class Atividades:


    def criar_pdf(self):
        # Exibir janela de diálogo para seleção de local e nome do arquivo
        file_path = tkinter.filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])

        if file_path:
            c = canvas.Canvas(file_path, pagesize=A4)

            # Defina a fonte e o tamanho do texto para o cabeçalho
            c.setFont("Helvetica", 14)
            c.drawString(222, 800, "Relatorio de Clientes")

            # Obtenha os dados da tabela clientes
            dados = self.seleciona_lista()

            # Adicione os títulos
            c.setFont("Helvetica", 12)
            c.drawString(52, 720, "Código")
            c.drawString(122, 720, "Nome cliente")
            c.drawString(222, 720, "CPF")
            c.drawString(342, 720, "Telefone")
            c.drawString(472, 720, "Idade")

            # Defina a posição inicial para os dados
            y = 700

            for item in self.listaCliente.get_children():
                codigo, Nome, Cpf, Telefone, idade = self.listaCliente.item(item, 'values')


                # Adicione os dados de cada veículo
                c.setFont("Helvetica", 12)
                c.drawString(52, y, f"{codigo}")
                c.drawString(122, y, f"{Nome}")
                c.drawString(222, y, f"{Cpf}")
                c.drawString(342, y, f"{Telefone}")
                c.drawString(472, y, f"{idade}")

                # Ajuste a posição para a próxima linha
                y -= 20

        # Finalize e salve o PDF
        c.save()

        # Abrir o PDF no navegador
        webbrowser.open(file_path)

    def buscar_veiculo(self):
        codigo = self.id_entrada.get()
        nome = self.entrada_Nome.get()
        telefone = self.entrada_Telefone.get()
        cpf = self.entrada_Cpf.get()
        idade = self.entrada_Idade.get() 

        try:
            if codigo or  nome or telefone or cpf or idade:

                query = "SELECT * FROM clientes WHERE"
                params = []

                if codigo:
                    query += " Idcliente = %s"
                    params.append(codigo)

                if nome:
                    if params:
                        query += " AND"
                    query += " NomCliente = %s"
                    params.append(nome)

                if telefone:
                    if params:
                        query += " AND"
                    query += " telefone = %s"
                    params.append(telefone)

                if cpf:
                    if params:
                        query += " AND"
                    query += " cpf = %s"
                    params.append(cpf)

                if idade:
                    if params:
                        query += " AND"
                    query += " idade = %s"
                    params.append(cpf)    

                self.cursor.execute(query, params)
                resultados = self.cursor.fetchall()

                # Atualiza a lista diretamente com os resultados
                self.listaCliente.delete(*self.listaCliente.get_children())
                for resultado in resultados:
                    self.listaCliente.insert("", "end", values=(resultado[0], resultado[1], resultado[2], resultado[3]))

            else:
                self.atualizar_lista()

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao buscar os veículos: {e}")

    def seleciona_lista(self):
        try:
            self.cursor.execute('SELECT * FROM tabalhopoo.clientes')
            return self.cursor.fetchall()
        except Exception as e:
            tkinter.messagebox.showerror("Erro", f"Ocorreu um erro ao selecionar os clientes: {e}")

    def limpar_tela(self):
        #Limpa a tela quando chamado nas caixas de informação
        self.id_entrada.delete(0, tkinter.END)
        self.entrada_Nome.delete(0, tkinter.END)
        self.entrada_Telefone.delete(0, tkinter.END)
        self.entrada_Cpf.delete(0, tkinter.END)
        self.entrada_Idade.delete(0, tkinter.END)

        self.atualizar_lista()

    def atualizar_lista(self):
        self.listaCliente.delete(*self.listaCliente.get_children())

        clientes = self.seleciona_lista()

        for cliente in clientes:
            self.listaCliente.insert("", "end", values=(cliente[0], cliente[1], cliente[2], cliente[3],cliente[4]))

class TelaRelatorio_clientes(Atividades):
    def __init__(self, db_connection, cursor, janela_master):
        self.db_connection = db_connection
        self.cursor = cursor
        self.janela_master = janela_master

    def abrir(self):
        # Cria a janela de relatorio
        self.janela_relatorio = tkinter.Toplevel(self.janela_master)
        self.janela_relatorio.title("Relatorio de Clientes")
        self.janela_relatorio.configure(background='#3f3e3e')
        self.janela_relatorio.geometry("1080x720")
        self.janela_relatorio.minsize(620, 380)
        self.janela_relatorio.grab_set()

        #Chamar função para criar o frame, botões e label.
        self.criar_frame()
        self.criar_button()
        self.criar_entrada()
        self.tabela_lista()
    
    def criar_entrada(self):
            # Campo para a Codigo
            tkinter.Label(self.frame_1, text="Codigo", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.05,relheight=0.1,relwidth=0.1)
            
            self.id_entrada = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.id_entrada.place(relx=0.01,rely=0.15,relheight=0.1,relwidth=0.1)

            # Campo para a NOME
            tkinter.Label(self.frame_1, text="Nome", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.30,relheight=0.1,relwidth=0.1)
            
            self.entrada_Nome = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_Nome.place(relx=0.01,rely=0.40,relheight=0.1,relwidth=0.60)

            # Campo para a TELEFONE
            tkinter.Label(self.frame_1, text="telefone", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.01, rely=0.52,relheight=0.1,relwidth=0.1)
            
            self.entrada_Telefone = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_Telefone.place(relx=0.01,rely=0.62,relheight=0.1,relwidth=0.60)

            # Campo para a CPF
            tkinter.Label(self.frame_1, text="CPF", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.70, rely=0.30,relheight=0.1,relwidth=0.2)
            
            self.entrada_Cpf = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_Cpf.place(relx=0.70,rely=0.40,relheight=0.1,relwidth=0.20)

             # Campo para a Idade
            tkinter.Label(self.frame_1, text="Idade", font=("Helvetica", 14,"bold"),bg='#4b4b49').place(
                 relx=0.70, rely=0.50,relheight=0.1,relwidth=0.2)
            
            self.entrada_Idade = tkinter.Entry(self.frame_1, font=("Helvetica", 12,"bold"),bg='#92928f', highlightbackground='#ffc400',highlightthickness=1)
            self.entrada_Idade.place(relx=0.70,rely=0.60,relheight=0.1,relwidth=0.20)

    def criar_button(self):
            # Botão Buscar
            self.botao_buscar = tkinter.Button(self.frame_1, text="Buscar", font=("Helvetica", 12),  bd=2, command= self.buscar_veiculo,
                                            bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
            self.botao_buscar.place(relx=0.88,rely=0.15,relheight=0.1,relwidth=0.1)
            
            # Botão PDF
            botao_pdf = tkinter.Button(self.frame_1, text="PDF", font=("Helvetica", 12),  bd=2, command=self.criar_pdf,
                                            bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
            botao_pdf.place(relx=0.88,rely=0.88,relheight=0.1,relwidth=0.1)


            # Botão limpar
            self.botao_limpar = tkinter.Button(self.frame_1, text="Limpar", font=("Helvetica", 12), command=self.limpar_tela ,bd=2, 
                                            bg='#c4a90d', highlightbackground='#ffc400',highlightthickness=4, width=20)
            self.botao_limpar.place(relx=0.76,rely=0.88,relheight=0.1,relwidth=0.1)

    def criar_frame(self):
            #Frame 1
            self.frame_1 = tkinter.Frame(self.janela_relatorio, bd=2, bg='#4b4b49', highlightbackground='#c4a90d',highlightthickness=2)
            self.frame_1.place(relx=0.02, rely=0.02, relheight=0.46, relwidth= 0.96)
            
            #Frame 2
            self.frame_2 = tkinter.Frame(self.janela_relatorio, bd=2, bg='#92928f', highlightbackground='#c4a90d',highlightthickness=2)
            self.frame_2.place(relx=0.02, rely=0.52, relheight=0.46, relwidth= 0.96)
    
    def tabela_lista(self):
        self.listaCliente = ttk.Treeview(self.frame_2, height=2, columns=("col1", "col2", "col3", "col4", "col5"))
        self.atualizar_lista()

        # Estilo e configurações da Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))

        self.listaCliente.heading("#0", text="")
        self.listaCliente.heading("#1", text="Codigo")
        self.listaCliente.heading("#2", text="Nome")
        self.listaCliente.heading("#3", text="Cpf")
        self.listaCliente.heading("#4", text="Telefone")
        self.listaCliente.heading("#5", text="idade")
        self.listaCliente.column("#0", width=50)
        self.listaCliente.column("#1", width=50)
        self.listaCliente.column("#2", width=50)
        self.listaCliente.column("#3", width=50)
        self.listaCliente.column("#4", width=50)
        self.listaCliente.column("#5", width=50)
        self.listaCliente.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.90)

        # Adicionar barra de rolagem vertical
        scrollbar_y = ttk.Scrollbar(self.frame_2, orient="vertical", command=self.listaCliente.yview)
        scrollbar_y.place(relx=0.99, rely=0.05, relheight=0.90)
        self.listaCliente.configure(yscrollcommand=scrollbar_y.set)
        
        # Adicionar barra de rolagem horizontal
        scrollbar_x = ttk.Scrollbar(self.frame_2, orient="horizontal", command=self.listaCliente.xview)
        scrollbar_x.place(relx=0.01, rely=0.95, relwidth=0.98)
        self.listaCliente.configure(xscrollcommand=scrollbar_x.set)
            
            


