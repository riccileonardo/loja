import tkinter
from tela_cadastro_protuto import TelaCadastro_produtos
from tela_cadastro_cliente import TelaCadastro_cliente
from connector import ConnectarBanco


class Lojapecas:
    def __init__(self):
        self.conect = ConnectarBanco()
        self.configTela()
        self.criando_button()
        self.conect.connectar()
        self.configuraçãoTelas()

    def configuraçãoTelas(self):
        self.cadastroClientes = TelaCadastro_cliente(self.conect.db_connection, self.conect.cursor, self.janela)
        self.cadastroProdutos = TelaCadastro_produtos(self.conect.db_connection, self.conect.cursor, self.janela)

    def configTela(self):
        self.janela = tkinter.Tk()
        self.janela.title("Loja Rostf")
        self.janela.configure(background='#3f3e3e')
        self.janela.geometry("1080x720")
        self.janela.minsize(620, 380)
        
    def criando_button(self):
        tkinter.Label(self.janela, text="Veiculos Roft", font=("Helvetica", 29, "bold"), background='#3f3e3e', fg='#d3c50a').place(relx=0.5, rely=0.1, anchor="center")
        
        botao_cadastro = tkinter.Button(self.janela, text="Cadastro Clientes", bd =3, background = '#d3c50a', font= ("Helvetica", 12,"bold"), command=self.abrir_tela_cadastro, width=20, height=5)
        botao_cadastro.place(relx=0.5, rely=0.3, relheight= 0.09, relwidth=0.15, anchor="center")

        botao_Relatorio = tkinter.Button(self.janela, text="Cadastrar Produtos", bd =3, background = '#d3c50a', font= ("Helvetica", 12, "bold"), command=self.abrir_tela_relatorio, width=20, height=5)
        botao_Relatorio.place(relx=0.5, rely=0.5, relheight= 0.09, relwidth=0.15, anchor="center") 

        botao_sair = tkinter.Button(self.janela, text="Sair", bd =3, background = '#d3c50a', font= ("Helvetica", 12, "bold"), command=self.sair, width=20, height=5)
        botao_sair.place(relx=0.5, rely=0.7, relheight= 0.09, relwidth=0.13, anchor="center")
 
    def abrir_tela_cadastro(self):
        self.cadastroClientes.abrir()

    def abrir_tela_relatorio(self):
        self.cadastroProdutos.abrir()

    def sair(self):
        self.janela.destroy()
        self.conect.desconnectar()

if __name__ == "__main__":
    loja = Lojapecas()
    loja.janela.mainloop()
    
