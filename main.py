"""
MSX Tools Frontend
Ponto de entrada principal da aplicação
"""
import sys
import os
import time
import threading
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import DatabaseManager
from config.settings import ConfigManager
from ui.splash_screen import SplashScreen
from ui.config_window import ConfigWindow
from ui.main_window import MainWindow


class MSXToolsApp:
    """Classe principal da aplicação MSX Tools"""
    
    def __init__(self):
        self.db_manager = None
        self.config_manager = None
        self.splash = None
        
    def initialize(self):
        """Inicializa a aplicação"""
        # Mostra splash screen
        self.splash = SplashScreen()
        self.splash.show()
        
        # Simula carregamento
        time.sleep(2)
        
        # Inicializa banco de dados
        self.db_manager = DatabaseManager()
        self.db_manager.initialize()
        
        # Carrega configurações
        self.config_manager = ConfigManager(self.db_manager)
        
        # Verifica se precisa configurar
        if not self.config_manager.config_exists():
            self.splash.update_status("Primeira execução detectada...")
            time.sleep(1)
            self.splash.close()
            self.show_config_window(first_run=True)
        else:
            self.splash.update_status("Carregando configurações...")
            time.sleep(1)
            config = self.config_manager.load_config()
            self.splash.close()
            self.show_main_window(config)
    
    def show_config_window(self, first_run=False):
        """Mostra janela de configuração"""
        config_window = ConfigWindow(self.config_manager, first_run)
        config_window.run()
        
        # Após salvar configurações, mostra janela principal
        if config_window.config_saved:
            config = self.config_manager.load_config()
            self.show_main_window(config)
    
    def show_main_window(self, config):
        """Mostra janela principal"""
        main_window = MainWindow(config, self.config_manager)
        main_window.run()
    
    def run(self):
        """Executa a aplicação"""
        try:
            self.initialize()
        except Exception as e:
            print(f"Erro ao inicializar aplicação: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    app = MSXToolsApp()
    app.run()