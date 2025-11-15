"""
DAO (Data Access Object) para operações de banco de dados da tabela aluno
"""

from bd.database import DatabaseConnection
from dao.nivel_dao import NivelDAO
from model.aluno_class import Aluno
from model.parametros_class import Parametros

class AlunoDAO:
    def __init__(self, db: DatabaseConnection):
        self.__db = db
    
    def salvar(self, aluno: Aluno):
        cur = self.__db.cursor()
        
        # Converter boolean para integer (SQLite)
        ativoInt = 1 if aluno.ativo else 0
        
        nivelId = aluno.nivel.id
        
        if aluno.id is None:
            # INSERT
            cur.execute("""
                INSERT INTO aluno (nome, contato, tipoConducao,
                                 ativo, nivel_id)
                VALUES (?, ?, ?, ?, ?);
            """, (aluno.nome, aluno.contato, aluno.tipoConducao,
                  ativoInt, nivelId))

            aluno.id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("""
                UPDATE aluno SET nome = ?, contato = ?, tipoConducao = ?, ativo = ?,
                               nivel_id = ?
                WHERE id = ?;
            """, (aluno.nome, aluno.contato, aluno.tipoConducao,
                  ativoInt, nivelId))
        
        return aluno.id
    
    def buscarPorId(self, id: int):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM aluno WHERE id = ?;", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def buscarPorNome(self, nome: str):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM aluno WHERE nome LIKE ?;", (f'%{nome}%',))
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def listarTodas(self, comNivel: bool = False):
        cur = self.__db.cursor()
        
        if comNivel:
            cur.execute("""
                SELECT a.*, n.nome as nivel_nome
                FROM aluno a
                JOIN nivel n ON a.nivel_id = n.id
                ORDER BY a.nome;
            """)
        else:
            cur.execute("SELECT * FROM aluno ORDER BY nome;")
        
        rows = cur.fetchall()
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def buscarPorNivel(self, nivelId: int):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM aluno WHERE nivel_id = ? ORDER BY nome;", (nivelId,))
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row):
        # Buscar a nivel usando o NivelDAO
        nivelDao = NivelDAO(self.__db)
        nivel = nivelDao.buscarPorId(row['nivel_id'])
        
        return Aluno(
            id=row['id'],
            nome=row['nome'],
            contato=row['contato'],
            ativo=bool(row['ativo']),
            tipoConducao=row['tipoConducao'],
            nivel=nivel
        )
    
    def deletar(self, aluno: Aluno):        
        cur = self.__db.cursor()
        cur.execute("DELETE FROM aluno WHERE id = ?;", (aluno.id,))

        return cur.rowcount > 0
    
    def obterNivel(self, aluno: Aluno):
        return aluno.nivel
