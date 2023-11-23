import mysql.connector
from tkinter import messagebox

class ConnectarBanco:
    def connectar(self):
        try:
            self.db_connection = mysql.connector.connect(host='localhost', user='root', password='', database='tabalhopoo')
            self.cursor = self.db_connection.cursor()
            print("Database conectado!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados.")
            raise err
    def desconnectar(self):
        self.db_connection.close()
        print("Database desconectado!")