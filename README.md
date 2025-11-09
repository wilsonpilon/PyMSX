# MSX Tools Frontend

Frontend modular em Python para centralizar ferramentas MSX usando CustomTkinter e SQLite.

## 🚀 Características

- Interface gráfica moderna com CustomTkinter
- Sistema de configuração persistente com SQLite
- Splash screen profissional
- Gerenciamento automático de diretórios
- Temas personalizáveis
- Arquitetura modular para expansão futura

## 📋 Requisitos

- Python 3.8+
- CustomTkinter
- SQLite3 (incluído no Python)

## 🔧 Instalação

```bash
# Clone o repositório
git clone https://github.com/wilsonpilon/PyMSX.git
cd PyMSX

# Instale as dependências
pip install -r requirements.txt
```

## 🎯 Uso

```bash
python main.py
```

Na primeira execução, o sistema irá:
1. Exibir uma splash screen
2. Criar o banco de dados de configuração
3. Mostrar a tela de configuração com valores padrão
4. Criar os diretórios necessários

## 📁 Estrutura do Projeto

```
PyMSX/
├── main.py                 # Ponto de entrada
├── requirements.txt        # Dependências
├── config/
│   ├── database.py        # Gerenciamento do banco
│   └── settings.py        # Configurações
├── ui/
│   ├── splash_screen.py   # Splash screen
│   ├── main_window.py     # Janela principal
│   └── config_window.py   # Configurações
└── assets/
    └── images/            # Recursos visuais
```

## ⚙️ Configurações Padrão

- **Diretório Raiz**: `C:\msx`
- **Banco de Dados**: `data/`
- **Downloads**: `download/`
- **Temporários**: `temp/`
- **Trabalho**: `work/`
- **Tema**: Dark

## 🛠️ Desenvolvimento

Este é o frontend base que será expandido com módulos de ferramentas MSX futuramente.

## 📝 Licença

MIT License

## 👤 Autor

Wilson Pilon (@wilsonpilon)
