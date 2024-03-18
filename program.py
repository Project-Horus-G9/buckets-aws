import customtkinter as ctk
import mysql.connector
import os
import sys
from PIL import Image

host = 'localhost'
user = 'root'
password = 'root'
database = 'horus'
port = 3306

connection = mysql.connector.connect(
host=host,
user=user,
password=password,
database=database,
port=port)

cursor = connection.cursor()

if connection.is_connected():
    print("Connected to MySQL server")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Hórus - Sistema de Monitoramento de Energia Solar")
        self.geometry("700x400")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        def get_assets_path():
            if getattr(sys, 'frozen', False):
                # Se o programa estiver empacotado como um executável
                return os.path.join(os.path.dirname(sys.executable), "assets")
            else:
                # Se estiver em modo de desenvolvimento
                return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
            
        image_path = get_assets_path()
        self.home_image = ctk.CTkImage(Image.open(os.path.join(image_path, "home.png")).resize((20, 20)))    
            
        self.navegacao_frame = ctk.CTkFrame(self, corner_radius=0, width=150)
        self.navegacao_frame.grid(row=0, column=0, sticky="nsew")
        self.navegacao_frame.grid_rowconfigure(4, weight=1)

        self.navegacao_frame_label = ctk.CTkLabel(self.navegacao_frame, text="Hórus",
            compound="left", font=ctk.CTkFont(size=20, weight="bold"))
        self.navegacao_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.home_button = ctk.CTkButton(self.navegacao_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
            fg_color="transparent", hover_color="gray70", text_color="black", anchor="w", image=self.home_image ,command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")
        
        self.luminosidade_button = ctk.CTkButton(self.navegacao_frame, corner_radius=0, height=40, border_spacing=10, text="Luminosidade",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=self.luminosidade_button_event)
        self.luminosidade_button.grid(row=2, column=0, sticky="ew")
        
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent", width=450)
        
        self.luminosidade_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent", width=450)
        
        self.grafico_lumi = ctk.CTk
        
        
        
        self.selecionar_frame_por_nome("home")
        ctk.set_appearance_mode('light')
        
    def grafico_luminosidade(self):
        select = "SELECT * FROM luminosidade"
        cursor.execute(select)
        result = cursor.fetchall()
        
        print(result)
        
    def selecionar_frame_por_nome(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.luminosidade_button.configure(fg_color=("gray75", "gray25") if name == "luminosidade" else "transparent")
        
        self.home_frame.grid_forget()
        self.luminosidade_frame.grid_forget()
        
        self.home_button.configure(fg_color="transparent")
        self.luminosidade_button.configure(fg_color="transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
            self.home_button.configure(fg_color=("gray75", "gray25"))
        elif name == "luminosidade":
            self.luminosidade_frame.grid(row=0, column=1, sticky="nsew")     
            self.luminosidade_button.configure(fg_color=("gray75", "gray25"))
            self.grafico_luminosidade()  

    def home_button_event(self):
        self.selecionar_frame_por_nome("home")

    def luminosidade_button_event(self):
        self.selecionar_frame_por_nome("luminosidade")

    def configuracao_button_event(self):
        self.selecionar_frame_por_nome("configuracao")
        
            
if __name__ == "__main__":         
    app = App()
    app.mainloop()