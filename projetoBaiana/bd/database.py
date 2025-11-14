import sqlite3

class DatabaseConnection:
    def __init__(self, dbPath: str = 'exemplo_bd.db'):
        self.dbPath = dbPath
        self.conn = None
    
    def conectar(self):
        if self.conn is None:
            # isolation_level=None ativa autocommit (cada operação é commitada automaticamente)
            self.conn = sqlite3.connect(self.dbPath, isolation_level=None)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON")
        return self.conn
    
    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def cursor(self):
        """Retorna um cursor para executar queries"""
        if self.conn is None:
            self.conectar()
        return self.conn.cursor()

    def criarTabelas(self):
        cur = self.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS aluno(
                aluno_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                nome TEXT NOT NULL,  
                nivel_id INTEGER,  
                contato TEXT UNIQUE NOT NULL,  
                tipoConducao TEXT NOT NULL,
                ativo INTEGER DEFAULT 1, 
                FOREIGN KEY (nivel_id) REFERENCES nivel(nivel_id),
                FOREIGN KEY (tipoConducao) REFERENCES parametros(tipoConducao)
            );
            """
        )
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS nivel(
                nivel_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                corNivel TEXT NOT NULL UNIQUE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS avaliacao(
                ava_id INTEGER PRIMARY KEY AUTOINCREMENT,  
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
                parametro_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                parametro TEXT,  
                tipoConducao TEXT,  
                estilo_id INTEGER,  
                nivel_id INTEGER, 
                FOREIGN KEY (nivel_id) REFERENCES nivel(nivel_id),
                FOREIGN KEY (estilo_id) REFERENCES estiloDanca(estilo_id)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS estiloDanca(
                estilo_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                estilo TEXT
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS itemAvaliacao(
                ava_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                parametro_id INTEGER,  
                nota INTEGER,
                FOREIGN KEY (parametro_id) REFERENCES parametros(parametro_id)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS evento(
                evento_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pessoaHomenageada TEXT NOT NULL,  
                dataEvento TEXT NOT NULL,  
                evento TEXT NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS examinador(
                examinador_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                nome TEXT NOT NULL,  
                contato INTEGER UNIQUE NOT NULL 
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS parametro_estilo(
                parametro_id INTEGER,  
                estilo_id INTEGER,
                FOREIGN KEY (parametro_id) REFERENCES parametros(parametro_id),
                FOREIGN KEY (estilo_id) REFERENCES estiloDanca(estilo_id)
                
            );
        """)

    def limparTabelas(self):
        cur = self.meuCursor()
        cur.execute("DELETE FROM pessoa;")
        cur.execute("DELETE FROM categoria;")
        
        # Resetar os contadores de AUTOINCREMENT
        cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('pessoa', 'categoria');")
