"""
Gerenciador de Configurações
"""
import os
from pathlib import Path


class ConfigManager:
    """Gerencia as configurações do sistema"""
    
    # Valores padrão
    DEFAULT_CONFIG = {
        'root_directory': r'C:\msx',
        'work_directory': 'work',
        'temp_directory': 'temp',
        'download_directory': 'download',
        'theme': 'dark',
        'database_directory': 'data'
    }
    
    def __init__(self, db_manager):
        """
        Inicializa o gerenciador de configurações
        
        Args:
            db_manager: Instância do DatabaseManager
        """
        self.db = db_manager
    
    def config_exists(self):
        """
        Verifica se existe uma configuração salva
        
        Returns:
            bool: True se existe configuração, False caso contrário
        """
        query = "SELECT COUNT(*) as count FROM config WHERE id = 1"
        result = self.db.fetch_one(query)
        return result and result['count'] > 0
    
    def load_config(self):
        """
        Carrega a configuração do banco de dados
        
        Returns:
            dict: Configuração carregada ou padrão
        """
        if self.config_exists():
            query = "SELECT * FROM config WHERE id = 1"
            config = self.db.fetch_one(query)
            return config
        else:
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config):
        """
        Salva a configuração no banco de dados
        
        Args:
            config: Dicionário com as configurações
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            # Cria diretórios se não existirem
            self._create_directories(config)
            
            if self.config_exists():
                # Atualiza configuração existente
                query = """
                    UPDATE config SET
                        root_directory = ?,
                        work_directory = ?,
                        temp_directory = ?,
                        download_directory = ?,
                        theme = ?,
                        database_directory = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = 1
                """
            else:
                # Insere nova configuração
                query = """
                    INSERT INTO config (
                        id, root_directory, work_directory, temp_directory,
                        download_directory, theme, database_directory
                    ) VALUES (1, ?, ?, ?, ?, ?, ?)
                """
            
            params = (
                config['root_directory'],
                config['work_directory'],
                config['temp_directory'],
                config['download_directory'],
                config['theme'],
                config['database_directory']
            )
            
            self.db.execute_query(query, params)
            return True
            
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
            return False
    
    def _create_directories(self, config):
        """
        Cria os diretórios necessários
        
        Args:
            config: Dicionário com as configurações
        """
        root = Path(config['root_directory'])
        
        # Cria diretório raiz
        root.mkdir(parents=True, exist_ok=True)
        
        # Cria subdiretórios
        subdirs = [
            config['work_directory'],
            config['temp_directory'],
            config['download_directory'],
            config['database_directory']
        ]
        
        for subdir in subdirs:
            full_path = root / subdir
            full_path.mkdir(parents=True, exist_ok=True)
    
    def get_full_path(self, config, directory_key):
        """
        Retorna o caminho completo de um diretório
        
        Args:
            config: Configuração
            directory_key: Chave do diretório (ex: 'work_directory')
            
        Returns:
            str: Caminho completo
        """
        root = Path(config['root_directory'])
        subdir = config[directory_key]
        return str(root / subdir)