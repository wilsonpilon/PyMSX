"""
Janela Principal
Interface principal da aplicação
"""
import customtkinter as ctk
from pathlib import Path


class MainWindow:
    """Janela principal da aplicação"""
    
    def __init__(self, config, config_manager):
        """
        Inicializa a janela principal
        
        Args:
            config: Configuração do sistema
            config_manager: Gerenciador de configurações
        """
        self.config = config
        self.config_manager = config_manager
        
        # Cria janela
        self.window = ctk.CTk()
        self.window.title("MSX Tools - Frontend")
        
        # Aplica tema
        ctk.set_appearance_mode(config['theme'])
        ctk.set_default_color_theme("blue")
        
        # Dimensões
        width = 1200
        height = 700
        
        # Centraliza
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Cria os widgets da interface"""
        
        # Frame lateral (sidebar)
        self.sidebar = ctk.CTkFrame(self.window, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo/Título no sidebar
        logo_label = ctk.CTkLabel(
            self.sidebar,
            text="MSX TOOLS",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        logo_label.pack(pady=(30, 10))
        
        subtitle_label = ctk.CTkLabel(
            self.sidebar,
            text="Frontend Modular",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Separador
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="#333333")
        separator.pack(fill="x", padx=20, pady=10)
        
        # Botões de menu (para futuros módulos)
        menu_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Placeholder para módulos futuros
        modules_label = ctk.CTkLabel(
            menu_frame,
            text="Módulos",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        modules_label.pack(fill="x", padx=10, pady=(10, 5))
        
        info_label = ctk.CTkLabel(
            menu_frame,
            text="Nenhum módulo instalado ainda.\n\nMódulos serão adicionados aqui conforme\nforem desenvolvidos.",
            font=ctk.CTkFont(size=11),
            text_color="#888888",
            justify="left"
        )
        info_label.pack(fill="x", padx=10, pady=10)
        
        # Botão de configurações no rodapé
        config_button = ctk.CTkButton(
            self.sidebar,
            text="⚙️ Configurações",
            command=self._open_config,
            font=ctk.CTkFont(size=13),
            height=40,
            fg_color="#2b2b2b",
            hover_color="#3b3b3b"
        )
        config_button.pack(side="bottom", fill="x", padx=10, pady=10)
        
        # Frame principal (conteúdo)
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Conteúdo de boas-vindas
        self._create_welcome_content()
    
    def _create_welcome_content(self):
        """Cria o conteúdo de boas-vindas"""
        
        # Título
        title = ctk.CTkLabel(
            self.main_frame,
            text="Bem-vindo ao MSX Tools!",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=(40, 10))
        
        # Descrição
        description = ctk.CTkLabel(
            self.main_frame,
            text="Sistema modular para ferramentas MSX\nMódulos serão adicionados em versões futuras",
            font=ctk.CTkFont(size=16),
            text_color="#888888"
        )
        description.pack(pady=(0, 40))
        
        # Frame de informações
        info_frame = ctk.CTkFrame(self.main_frame)
        info_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Título da seção
        info_title = ctk.CTkLabel(
            info_frame,
            text="Configuração Atual",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        info_title.pack(pady=(20, 10))
        
        # Informações de configuração
        config_info = [
            ("📁 Diretório Raiz:", self.config['root_directory']),
            ("💾 Banco de Dados:", self.config['database_directory']),
            ("🔧 Trabalho:", self.config['work_directory']),
            ("📥 Download:", self.config['download_directory']),
            ("🗑️ Temporário:", self.config['temp_directory']),
            ("🎨 Tema:", self.config['theme'].capitalize())
        ]
        
        for label, value in config_info:
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=40, pady=5)
            
            label_widget = ctk.CTkLabel(
                row_frame,
                text=label,
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                width=150
            )
            label_widget.pack(side="left", padx=(0, 20))
            
            value_widget = ctk.CTkLabel(
                row_frame,
                text=value,
                font=ctk.CTkFont(size=13),
                anchor="w",
                text_color="#888888"
            )
            value_widget.pack(side="left", fill="x", expand=True)
        
        # Versão
        version_label = ctk.CTkLabel(
            self.main_frame,
            text="Versão 1.0.0",
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        )
        version_label.pack(side="bottom", pady=20)
    
    def _open_config(self):
        """Abre janela de configurações"""
        from ui.config_window import ConfigWindow
        
        # Fecha janela atual
        self.window.withdraw()
        
        # Abre configurações
        config_window = ConfigWindow(self.config_manager, first_run=False)
        config_window.run()
        
        # Recarrega configuração e recria janela
        if config_window.config_saved:
            self.config = self.config_manager.load_config()
            self.window.destroy()
            self.__init__(self.config, self.config_manager)
            self.run()
        else:
            self.window.deiconify()
    
    def run(self):
        """Executa a janela"""
        self.window.mainloop()