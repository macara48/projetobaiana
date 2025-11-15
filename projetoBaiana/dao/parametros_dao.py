"""
DAO (Data Access Object) para operações de banco de dados da tabela parametros
"""

from bd.database import DatabaseConnection
from model.parametros_class import Parametros
from model.estiloDanca_class import EstiloDanca

class ParametrosDAO:
    def __init__(self, db: DatabaseConnection):
        self.__db = db
    
    def salvar(self, parametros: Parametros):
        cur = self.__db.cursor()
        
        # Converter boolean para integer (SQLite)
        if parametros.id is None:
            # INSERT
            cur.execute("""
                INSERT INTO parametros (nome, tipoConducao, estilo, nivel)
                VALUES (?, ?, ?, ?);
            """, (parametros.nome, parametros.tipoConducao, parametros.estilo, parametros.nivel))

            parametros.id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("""
                UPDATE parametros SET nome = ?, tipoConducao = ?, estilo = ?, nivel = ?
                WHERE id = ?;
            """, (parametros.nome, parametros.tipoConducao, parametros.estilo, parametros.nivel))
        
        return parametros.id
    
    def buscarPorId(self, id: int):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM parametros WHERE id = ?;", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def buscarPorNome(self, nome: str):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM parametros WHERE nome LIKE ?;", (f'%{nome}%',))
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def listarTodos(self):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM parametros ORDER BY nome;")
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row):
        return Parametros(
            id=row['id'],
            data=row['nome'],
            tipoConducao=row['tipoConducao'],
            estilo=row['estilo'],
            nivel=row['nivel']
        )
    
    def deletar(self, parametros: Parametros):        
        cur = self.__db.cursor()
        cur.execute("DELETE FROM parametros WHERE id = ?;", (parametros.id,))

        return cur.rowcount > 0
    
    # Métodos para gerenciar relacionamento N:N com Pessoa
    
    def vincularEstilo(self, parametros: Parametros, estiloDanca: EstiloDanca):
        """Vincula uma parâmetro a um estilo de dança"""
        cur = self.__db.cursor()
        
        # Verificar se já existe o vínculo
        cur.execute("""
            SELECT * FROM parametro_estilo
            WHERE parametro_id = ? AND estilo_id = ?;
        """, (parametros.id, estiloDanca.id))
        
        if cur.fetchone():
            return False  # Já existe o vínculo
        
        cur.execute("""
            INSERT INTO parametro_estilo (parametro_id, estilo_id)
            VALUES (?, ?);
        """, (parametros.id, estiloDanca.id))
        
        return True
    
    def desvincularEstilo(self, parametros: Parametros, estiloDanca: EstiloDanca):
        """Remove o vínculo entre um parâmetro e um estilo"""
        cur = self.__db.cursor()
        cur.execute("""
            DELETE FROM parametro_estilo 
            WHERE parametro_id = ? AND estilo_id = ?;
        """, (parametros.id, estiloDanca.id))
        
        return cur.rowcount > 0
    
    def buscarParametrosPorEstilo(self, estiloId: int):
        """Retorna todos os parametros vinculadas a um estilo"""
        cur = self.__db.cursor()
        cur.execute("""
            SELECT p.*
            FROM parametros p
            INNER JOIN parametro_estilo pe ON p.id = pe.parametro_id
            WHERE pe.estilo_id = ?
            ORDER BY p.nome;
        """, (estiloId,))
        
        rows = cur.fetchall()
        parametrosDao = ParametrosDAO(self.__db)
        
        resultado = []
        for row in rows:
            resultado.append(parametrosDao.criarDeRow(row))
        return resultado
    
    def buscarEstilosPorParametro(self, parametrosId: int):
        """Retorna todos as estilos vinculadas a um parametro"""
        cur = self.__db.cursor()
        cur.execute("""
            SELECT e.*
            FROM estiloDanca e
            INNER JOIN parametro_estilo pe ON e.id = pd.estilo_id
            WHERE pd.parametro_id = ?
            ORDER BY e.nome;
        """, (parametrosId,))
        
        rows = cur.fetchall()
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado