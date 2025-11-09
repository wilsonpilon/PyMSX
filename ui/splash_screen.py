"""
Splash Screen
Tela inicial mostrada durante o carregamento
"""
import customtkinter as ctk
from tkinter import Canvas
import time


class SplashScreen:
    """Splash screen exibida ao iniciar a aplicação"""
    
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("")
        
        # Remove bordas da janela
        self.window.overrideredirect(True)
        
        # Dimensões
        width = 600
        height = 400
        
        # Centraliza na tela
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(
            self.window,
            corner_radius=15,
            border_width=2,
            border_color="#1f538d"
        )
        self.main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Logo/Título
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="MSX TOOLS",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="#1f538d"
        )
        self.title_label.pack(pady=(80, 10))
        
        # Subtítulo
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Frontend Modular",
            font=ctk.CTkFont(size=20),
            text_color="#666666"
        )
        self.subtitle_label.pack(pady=(0, 40))
        
        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(
            self.main_frame,
            width=400,
            height=8,
            corner_radius=4
        )
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)
        
        # Label de status
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Inicializando...",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.status_label.pack(pady=10)
        
        # Versão
        self.version_label = ctk.CTkLabel(
            self.main_frame,
            text="v1.0.0",
            font=ctk.CTkFont(size=10),
            text_color="#aaaaaa"
        )
        self.version_label.pack(side="bottom", pady=20)
        
    def show(self):
        """Mostra a splash screen"""
        self.window.update()
        
        # Anima a barra de progresso
        for i in range(101):
            self.progress_bar.set(i / 100)
            self.window.update()
            time.sleep(0.01)
    
    def update_status(self, text):
        """
        Atualiza o texto de status
        
        Args:
            text: Novo texto de status
        """
        self.status_label.configure(text=text)
        self.window.update()
    
    def close(self):
        """Fecha a splash screen"""
        self.window.destroy()