"""
Gerenciador de Banco de Dados SQLite
"""
import sqlite3
import os
from pathlib import Path


class DatabaseManager:
    """Gerencia conexões e operações com o banco de dados SQLite"""
    
    def __init__(self, db_path="msx_config.db"):
        """
        Inicializa o gerenciador de banco de dados
        
        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Conecta ao banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return self.conn
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def initialize(self):
        """Inicializa o banco de dados criando as tabelas necessárias"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Cria tabela de configurações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                root_directory TEXT NOT NULL,
                work_directory TEXT NOT NULL,
                temp_directory TEXT NOT NULL,
                download_directory TEXT NOT NULL,
                theme TEXT NOT NULL,
                database_directory TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        self.close()
    
    def execute_query(self, query, params=None):
        """
        Executa uma query no banco de dados
        
        Args:
            query: Query SQL a ser executada
            params: Parâmetros para a query (opcional)
            
        Returns:
            Cursor com os resultados
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {e}")
            conn.rollback()
            raise
        finally:
            self.close()
    
    def fetch_one(self, query, params=None):
        """
        Busca um único registro
        
        Args:
            query: Query SQL
            params: Parâmetros (opcional)
            
        Returns:
            Registro encontrado ou None
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar registro: {e}")
            raise
        finally:
            self.close()
    
    def fetch_all(self, query, params=None):
        """
        Busca múltiplos registros
        
        Args:
            query: Query SQL
            params: Parâmetros (opcional)
            
        Returns:
            Lista de registros
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return [dict(row) for row in results]
        except sqlite3.Error as e:
            print(f"Erro ao buscar registros: {e}")
            raise
        finally:
            self.close()