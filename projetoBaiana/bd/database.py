import sqlite3

class DatabaseConnection:
    def __init__(self, dbPath: str = 'exemplo_bd.db'):
        self.__dbPath = dbPath
        self.__conn = None
    
    def conectar(self):
        if self.__conn is None:
            # isolation_level=None ativa autocommit (cada operação é commitada automaticamente)
            self.__conn = sqlite3.connect(self.__dbPath, isolation_level=None)
            self.__conn.row_factory = sqlite3.Row
            self.__conn.execute("PRAGMA foreign_keys = ON")
        return self.__conn
    
    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        if self.__conn:
            self.__conn.close()
            self.__conn = None
    

    
    def cursor(self):
        """Retorna um cursor para executar queries"""
        if self.__conn is None:
            self.conectar()
        return self.__conn.cursor()

    def criarTabelas(self):
        cur = self.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS aluno(
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                nome TEXT NOT NULL,  
                nivel_id INTEGER,  
                contato TEXT NOT NULL UNIQUE,  
                tipoConducao TEXT NOT NULL UNIQUE,
                ativo INTEGER DEFAULT 1, 
                FOREIGN KEY (nivel_id) REFERENCES nivel(nivel_id),
                FOREIGN KEY (tipoConducao) REFERENCES parametros(tipoConducao)
            );
            """
        )
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS nivel(
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                nome TEXT NOT NULL UNIQUE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS avaliacao(
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                data TEXT,  
                aluno_id INTEGER,  
                obs TEXT,  
                nivel_id INTEGER,  
                examinador_id INTEGER,  
                evento_id INTEGER,
                FOREIGN KEY(aluno_id) REFERENCES aluno (aluno_id),
                FOREIGN KEY (nivel_id) REFERENCES nivel(nivel_id),
                FOREIGN KEY (examinador_id) REFERENCES examinador(examinador_id),
                FOREIGN KEY (evento_id) REFERENCES evento(evento_id)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS parametros(
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                nome TEXT NOT NULL UNIQUE,  
                tipoConducao TEXT,  
                estilo_id INTEGER,  
                nivel_id INTEGER, 
                FOREIGN KEY (nivel_id) REFERENCES nivel(nivel_id),
                FOREIGN KEY (estilo_id) REFERENCES estiloDanca(estilo_id)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS estiloDanca(
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                estilo TEXT NOT NULL UNIQUE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS itemAvaliacao(
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                parametro_id INTEGER,  
                nota INTEGER,
                FOREIGN KEY (parametro_id) REFERENCES parametros(parametro_id)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS evento(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pessoaHomenageada TEXT NOT NULL,  
                dataEvento TEXT NOT NULL UNIQUE,  
                evento TEXT NOT NULL UNIQUE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS examinador(
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                nome TEXT NOT NULL,  
                contato INTEGER NOT NULL UNIQUE 
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS parametro_estilo(
                parametro_id INTEGER NOT NULL,  
                estilo_id INTEGER NOT NULL,
                PRIMARY KEY (parametro_id, estilo_id),
                FOREIGN KEY (parametro_id) REFERENCES parametros(id) ON DELETE CASCADE,
                FOREIGN KEY (estilo_id) REFERENCES estiloDanca(id) ON DELETE CASCADE
                
            );
        """)

        # Tabela usuario (relacionamento 1:1 com aluno)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER NOT NULL,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (id) REFERENCES aluno(id) ON DELETE CASCADE
        );
        """)

    def limparTabelas(self):
        cur = self.meuCursor()
        cur.execute("DELETE FROM aluno;")
        cur.execute("DELETE FROM nivel;")
        cur.execute("DELETE FROM avaliacao;")
        cur.execute("DELETE FROM parametros;")
        cur.execute("DELETE FROM estiloDanca;")
        cur.execute("DELETE FROM itemAvaliacao;")
        cur.execute("DELETE FROM evento;")
        cur.execute("DELETE FROM examinador;")
        cur.execute("DELETE FROM parametro_estilo;")
        cur.execute("DELETE FROM usuario;")
        
        # Resetar os contadores de AUTOINCREMENT
        cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('aluno', 'nivel', 'avaliacao', 'parametros', 'estiloDanca', 'itemAvaliacao', 'evento', 'examinador', 'parametro_estilo', 'usuario');")
