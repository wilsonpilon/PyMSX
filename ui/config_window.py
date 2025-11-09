"""
Janela de Configuração
Interface para configurar o sistema
"""
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path


class ConfigWindow:
    """Janela para configuração do sistema"""
    
    def __init__(self, config_manager, first_run=False):
        """
        Inicializa a janela de configuração
        
        Args:
            config_manager: Instância do ConfigManager
            first_run: Se é a primeira execução
        """
        self.config_manager = config_manager
        self.first_run = first_run
        self.config_saved = False
        
        # Carrega configuração atual ou padrão
        self.config = config_manager.load_config()
        
        # Cria janela
        self.window = ctk.CTk()
        self.window.title("MSX Tools - Configuração")
        
        # Define tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Dimensões
        width = 700
        height = 650
        
        # Centraliza
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        self.window.resizable(False, False)
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Cria os widgets da interface"""
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_text = "Configuração Inicial" if self.first_run else "Configurações"
        title = ctk.CTkLabel(
            main_frame,
            text=title_text,
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(10, 5))
        
        if self.first_run:
            subtitle = ctk.CTkLabel(
                main_frame,
                text="Configure os diretórios e preferências do sistema",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            )
            subtitle.pack(pady=(0, 20))
        
        # Frame de campos
        fields_frame = ctk.CTkFrame(main_frame)
        fields_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Diretório Raiz
        self._create_directory_field(
            fields_frame,
            "Diretório Raiz:",
            "root_directory",
            0,
            "Diretório base para todos os outros"
        )
        
        # Diretório de Banco de Dados
        self._create_simple_field(
            fields_frame,
            "Banco de Dados:",
            "database_directory",
            1,
            "(relativo ao raiz)"
        )
        
        # Diretório de Trabalho
        self._create_simple_field(
            fields_frame,
            "Diretório de Trabalho:",
            "work_directory",
            2,
            "(relativo ao raiz)"
        )
        
        # Diretório Temporário
        self._create_simple_field(
            fields_frame,
            "Diretório Temporário:",
            "temp_directory",
            3,
            "(relativo ao raiz)"
        )
        
        # Diretório de Download
        self._create_simple_field(
            fields_frame,
            "Diretório de Download:",
            "download_directory",
            4,
            "(relativo ao raiz)"
        )
        
        # Tema
        self._create_theme_field(fields_frame, 5)
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 10))
        
        save_button = ctk.CTkButton(
            button_frame,
            text="Salvar Configuração",
            command=self._save_config,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            corner_radius=8
        )
        save_button.pack(side="right", padx=5)
        
        if not self.first_run:
            cancel_button = ctk.CTkButton(
                button_frame,
                text="Cancelar",
                command=self.window.destroy,
                font=ctk.CTkFont(size=14),
                height=40,
                corner_radius=8,
                fg_color="#666666",
                hover_color="#555555"
            )
            cancel_button.pack(side="right", padx=5)
    
    def _create_directory_field(self, parent, label_text, config_key, row, hint=""):
        """Cria um campo de diretório com botão de busca"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=8, padx=10)
        
        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
            width=180
        )
        label.pack(side="left", padx=(0, 10))
        
        entry = ctk.CTkEntry(
            frame,
            placeholder_text=self.config[config_key],
            font=ctk.CTkFont(size=12),
            height=35
        )
        entry.insert(0, self.config[config_key])
        entry.pack(side="left", fill="x", expand=True, padx=5)
        setattr(self, f"{config_key}_entry", entry)
        
        browse_button = ctk.CTkButton(
            frame,
            text="📁",
            width=40,
            height=35,
            command=lambda: self._browse_directory(config_key)
        )
        browse_button.pack(side="right")
        
        if hint:
            hint_label = ctk.CTkLabel(
                parent,
                text=hint,
                font=ctk.CTkFont(size=10),
                text_color="#888888",
                anchor="w"
            )
            hint_label.pack(fill="x", padx=200, pady=(0, 5))
    
    def _create_simple_field(self, parent, label_text, config_key, row, hint=""):
        """Cria um campo simples de texto"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=8, padx=10)
        
        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
            width=180
        )
        label.pack(side="left", padx=(0, 10))
        
        entry = ctk.CTkEntry(
            frame,
            placeholder_text=self.config[config_key],
            font=ctk.CTkFont(size=12),
            height=35
        )
        entry.insert(0, self.config[config_key])
        entry.pack(side="left", fill="x", expand=True, padx=5)
        setattr(self, f"{config_key}_entry", entry)
        
        if hint:
            hint_label = ctk.CTkLabel(
                frame,
                text=hint,
                font=ctk.CTkFont(size=10),
                text_color="#888888"
            )
            hint_label.pack(side="right", padx=10)
    
    def _create_theme_field(self, parent, row):
        """Cria campo de seleção de tema"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=8, padx=10)
        
        label = ctk.CTkLabel(
            frame,
            text="Tema:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
            width=180
        )
        label.pack(side="left", padx=(0, 10))
        
        self.theme_combo = ctk.CTkComboBox(
            frame,
            values=["dark", "light", "system"],
            font=ctk.CTkFont(size=12),
            height=35,
            state="readonly"
        )
        self.theme_combo.set(self.config['theme'])
        self.theme_combo.pack(side="left", fill="x", expand=True, padx=5)
    
    def _browse_directory(self, config_key):
        """Abre diálogo para selecionar diretório"""
        current_value = getattr(self, f"{config_key}_entry").get()
        directory = filedialog.askdirectory(
            title="Selecione o Diretório",
            initialdir=current_value if current_value else "/"
        )
        
        if directory:
            entry = getattr(self, f"{config_key}_entry")
            entry.delete(0, "end")
            entry.insert(0, directory)
    
    def _save_config(self):
        """Salva a configuração"""
        # Coleta valores dos campos
        new_config = {
            'root_directory': self.root_directory_entry.get(),
            'database_directory': self.database_directory_entry.get(),
            'work_directory': self.work_directory_entry.get(),
            'temp_directory': self.temp_directory_entry.get(),
            'download_directory': self.download_directory_entry.get(),
            'theme': self.theme_combo.get()
        }
        
        # Valida
        if not new_config['root_directory']:
            self._show_error("O diretório raiz é obrigatório!")
            return
        
        # Salva
        if self.config_manager.save_config(new_config):
            self.config_saved = True
            
            # Aplica tema
            ctk.set_appearance_mode(new_config['theme'])
            
            self.window.destroy()
        else:
            self._show_error("Erro ao salvar configuração!")
    
    def _show_error(self, message):
        """Mostra mensagem de erro"""
        error_window = ctk.CTkToplevel(self.window)
        error_window.title("Erro")
        error_window.geometry("400x150")
        error_window.resizable(False, False)
        
        # Centraliza
        error_window.transient(self.window)
        error_window.grab_set()
        
        label = ctk.CTkLabel(
            error_window,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        label.pack(pady=30)
        
        button = ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy,
            width=100
        )
        button.pack(pady=10)
    
    def run(self):
        """Executa a janela"""
        self.window.mainloop()