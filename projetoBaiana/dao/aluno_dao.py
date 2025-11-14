"""
DAO (Data Access Object) para operações de banco de dados da tabela aluno
"""

from bd.database import DatabaseConnection
from dao.nivel_dao import NivelDAO
from model.aluno_class import Aluno
from model.nivel_class import Nivel

class AlunoDAO:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def salvar(self, aluno: Aluno):
        cur = self.db.cursor()
        
        # Converter boolean para integer (SQLite)
        ativoInt = 1 if aluno.ativo else 0
        
        nivelId = aluno.nivel.nivel_id
        
        if aluno.id is None:
            # INSERT
            cur.execute("""
                INSERT INTO aluno (aluno_id, nome, contato, nivel, tipoConducao,
                                 ativo)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (aluno.aluno_id, aluno.nome, aluno.contato, aluno.nivel, aluno.tipoConducao,
                  aluno.ativo))

            aluno.aluno_id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("""
                UPDATE aluno SET aluno_id = ?, nome = ?, contato = ?, nivel = ?, tipoConducao = ?,
                               ativo = ?
                WHERE id = ?;
            """, (aluno.aluno_id, aluno.nome, aluno.contato, aluno.nivel, aluno.tipoConducao,
                  aluno.ativo))
        
        return aluno.aluno_id
    
    def buscarPorId(self, id: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM pessoa WHERE id = ?;", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def buscarPorNome(self, nome: str):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM pessoa WHERE nome LIKE ?;", (f'%{nome}%',))
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def listarTodas(self, comNivel: bool = False):
        cur = self.db.cursor()
        
        if comNivel:
            cur.execute("""
                SELECT a.*, n.corNivel as nivel_nome
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
    
    def buscarPorCategoria(self, nivel_id: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM aluno WHERE nivel_id = ? ORDER BY nome;", (nivel_id,))
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row):
        # Buscar a categoria usando o CategoriaDAO
        nivelDao = NivelDAO(self.db)
        nivel = nivelDao.buscarPorId(row['nivel_id'])
        
        return Aluno(
            aluno_id=row['id'],
            nome=row['nome'],
            contato=row['contato'],
            nivel=Nivel,
            tipoConducao=row['Condutor/Conduzido'],
            ativo=bool(row['ativo'])
        )
    
    def deletar(self, aluno: Aluno):        
        cur = self.db.cursor()
        cur.execute("DELETE FROM aluno WHERE id = ?;", (aluno.aluno_id,))

        return cur.rowcount > 0
    
    def obterCategoria(self, aluno: Aluno):
        return aluno.nivel
