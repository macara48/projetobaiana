"""
Serviço para interação do usuário via linha de comando com a entidade Usuario
"""
import sys
import os

# Adicionar o diretório pai ao path para permitir imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bd.database import DatabaseConnection
from dao.usuario_dao import UsuarioDAO
from dao.aluno_dao import AlunoDAO
from dao.nivel_dao import NivelDAO
from model.usuario_class import Usuario
from model.aluno_class import Aluno
from model.parametros_class import Parametros
from model.nivel_class import Nivel


class UsuarioService:
    
    def __init__(self, db: DatabaseConnection):
        self.__db = db
        self.__usuarioDao = UsuarioDAO(db)
        self.__alunoDao = AlunoDAO(db)
        self.__nivelDao = NivelDAO(db)
    
    def exibirMenu(self):
        """Exibe o menu principal de opções"""
        print("\n" + "="*50)
        print("  SISTEMA DE GERENCIAMENTO DE USUÁRIOS")
        print("="*50)
        print("1. Criar usuário")
        print("2. Listar todos os usuários")
        print("3. Buscar usuário por ID")
        print("4. Buscar usuário por login")
        print("5. Buscar usuário por aluno")
        print("6. Atualizar usuário")
        print("7. Deletar usuário")
        print("0. Sair")
        print("="*50)
    
    def listarAlunosDisponiveis(self):
        """Lista todas as alunos disponíveis para vincular a um usuário"""
        alunos = self.__alunoDao.listarTodas()
        if not alunos:
            print("⚠️  Nenhuma aluno cadastrada. Cadastre uma aluno primeiro!")
            return None
        
        print("\nAlunos disponíveis:")
        print("-"*50)
        for a in alunos:
            # Verificar se já tem usuário
            usuarioExistente = self.__usuarioDao.buscarPorAlunoId(a.id)
            status = " (já tem usuário)" if usuarioExistente else ""
            print(f"  {a.id}. {a.nome} - {a.contato}{status}")
        print("-"*50)
        return alunos
    
    def selecionarAluno(self):
        """Solicita ao usuário que selecione uma aluno sem usuário"""
        alunos = self.listarAlunosDisponiveis()
        if not alunos:
            return None
        
        try:
            alunoIdStr = input("Digite o ID da aluno: ").strip()
            alunoId = int(alunoIdStr)
            
            # Verificar se já tem usuário
            usuarioExistente = self.__usuarioDao.buscarPorAlunoId(alunoId)
            if usuarioExistente:
                print(f"❌ Erro: O aluno com ID {alunoId} já possui um usuário!")
                return None
            
            aluno = self.__alunoDao.buscarPorId(alunoId)
            if not aluno:
                print(f"❌ Erro: Aluno com ID {alunoId} não encontrada!")
                return None
            
            return aluno
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
            return None
    
    def listarNiveisDisponiveis(self):
        """Lista todas as niveis disponíveis para seleção"""
        niveis = self.__nivelDao.listarTodas()
        if not niveis:
            print("⚠️  Nenhuma nivel cadastrada. Cadastre uma nivel primeiro!")
            return None
        
        print("\nNiveis disponíveis:")
        print("-"*30)
        for cat in niveis:
            print(f"  {cat.id}. {cat.nome}")
        print("-"*30)
        return niveis
    
    def selecionarNivel(self):
        """Solicita ao usuário que selecione uma nivel"""
        niveis = self.listarNiveisDisponiveis()
        if not niveis:
            return None
        
        try:
            nivelIdStr = input("Digite o ID da nivel: ").strip()
            nivelId = int(nivelIdStr)
            
            nivel = self.__nivelDao.buscarPorId(nivelId)
            if not nivel:
                print(f"❌ Erro: Nivel com ID {nivelId} não encontrada!")
                return None
            
            return nivel
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
            return None
    
    def criarUsuario(self):
        """Solicita todos os dados de uma vez e cria aluno e usuário de forma transparente"""
        print("\n--- CADASTRAR USUÁRIO ---")
        print("Preencha todos os dados:")
        
        # Dados básicos
        nome = input("Nome: ").strip()
        if not nome:
            print("❌ Erro: O nome não pode ser vazio!")
            return
        
        contato = input("Contato: ").strip()
        if not contato:
            print("❌ Erro: O contato não pode ser vazio!")
            return
        
        # Verificar se já existe uma aluno com esse contato
        todosAlunos = self.__alunoDao.listarTodas()
        for a in todosAlunos:
            if a.contato.lower() == contato.lower():
                print(f"❌ Erro: Já existe um aluno com o contato '{contato}' (ID: {a.id})")
                return
        
        # Selecionar nivel
        nivel = self.selecionarNivel()
        if not nivel:
            return
        
        # Campos opcionais      
        ativoStr = input("Aluno está ativa? (S/n): ").strip().lower()
        ativo = ativoStr != 'n'
        
        # Dados de acesso do usuário
        login = input("Login: ").strip()
        if not login:
            print("❌ Erro: O login não pode ser vazio!")
            return
        
        # Verificar se já existe um usuário com esse login
        usuarioExistente = self.__usuarioDao.buscarPorLogin(login)
        if usuarioExistente:
            print(f"❌ Erro: Já existe um usuário com o login '{login}' (ID: {usuarioExistente.id})")
            return
        
        senha = input("Senha: ").strip()
        if not senha:
            print("❌ Erro: A senha não pode ser vazia!")
            return
        
        print("Tipos disponíveis: examinador, aluno")
        tipo = input("Tipo: ").strip().lower()
        if not tipo:
            print("❌ Erro: O tipo não pode ser vazio!")
            return
        
        try:
            # Criar o aluno primeiro (transparente para o usuário)
            aluno = Aluno(
                id=None,
                nome=nome,
                contato=contato,
                nivel=nivel,
                ativo=ativo,
                tipoConducao=Parametros
            )
            
            alunoId = self.__alunoDao.salvar(aluno)
            
            # Criar o usuário vinculado à aluno (transparente para o usuário)
            usuario = Usuario(
                id=None,
                login=login,
                senha=senha,
                tipo=tipo,
                aluno=aluno
            )
            
            usuarioId = self.__usuarioDao.salvar(usuario)
            print(f"\n✅ Usuário cadastrado com sucesso! (ID: {usuarioId})")
            self.exibirDetalhesUsuario(usuario)
        
        except ValueError as e:
            print(f"❌ Erro de validação: {e}")
        except Exception as e:
            print(f"❌ Erro ao criar usuário: {e}")
            import traceback
            traceback.print_exc()
    
    def exibirDetalhesUsuario(self, usuario: Usuario):
        """Exibe os detalhes completos de um usuário e da aluno associada"""
        print(f"\n📋 DADOS DO USUÁRIO:")
        print(f"   ID: {usuario.id}")
        print(f"   Login: {usuario.login}")
        print(f"   Tipo: {usuario.tipo}")
        print(f"\n👤 DADOS DO ALUNO:")
        print(f"   ID: {usuario.aluno.id}")
        print(f"   Nome: {usuario.aluno.nome}")
        print(f"   Contato: {usuario.aluno.contato}")
        print(f"   Nivel: {usuario.aluno.nivel.nome} (ID: {usuario.aluno.nivel.id}")
        print(f"   Tipo de Condução: {usuario.aluno.tipoConducao}")
    
    def listarUsuarios(self):
        """Lista todos os usuários cadastrados"""
        print("\n--- LISTAR TODOS OS USUÁRIOS ---")
        
        try:
            usuarios = self.__usuarioDao.listarTodos()
            
            if not usuarios:
                print("⚠️  Nenhum usuário cadastrado.")
                return
            
            print(f"\nTotal de usuários: {len(usuarios)}")
            print("\n" + "-"*80)
            print(f"{'ID':<5} | {'Login':<20} | {'Tipo':<15} | {'Aluno':<30}")
            print("-"*80)
            
            for usuario in usuarios:
                print(f"{usuario.id:<5} | {usuario.login[:19]:<20} | {usuario.tipo[:14]:<15} | {usuario.aluno.nome[:29]:<30}")
            
            print("-"*80)
        
        except Exception as e:
            print(f"❌ Erro ao listar usuários: {e}")
    
    def buscarPorId(self):
        """Solicita um ID e busca o usuário correspondente"""
        print("\n--- BUSCAR USUÁRIO POR ID ---")
        
        try:
            idStr = input("Digite o ID do usuário: ").strip()
            usuarioId = int(idStr)
            
            usuario = self.__usuarioDao.buscarPorId(usuarioId)
            
            if usuario:
                print("\n✅ Usuário encontrado:")
                self.exibirDetalhesUsuario(usuario)
            else:
                print(f"⚠️  Usuário com ID {usuarioId} não encontrado.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao buscar usuário: {e}")
    
    def buscarPorLogin(self):
        """Solicita um login e busca o usuário correspondente"""
        print("\n--- BUSCAR USUÁRIO POR LOGIN ---")
        
        login = input("Digite o login: ").strip()
        
        if not login:
            print("❌ Erro: O login não pode ser vazio!")
            return
        
        try:
            usuario = self.__usuarioDao.buscarPorLogin(login)
            
            if usuario:
                print("\n✅ Usuário encontrado:")
                self.exibirDetalhesUsuario(usuario)
            else:
                print(f"⚠️  Usuário com login '{login}' não encontrado.")
        
        except Exception as e:
            print(f"❌ Erro ao buscar usuário: {e}")
    
    def buscarPorAluno(self):
        """Solicita um ID de aluno e busca o usuário correspondente"""
        print("\n--- BUSCAR USUÁRIO POR ALUNO ---")
        
        try:
            alunoIdStr = input("Digite o ID do aluno: ").strip()
            alunoId = int(alunoIdStr)
            
            aluno = self.__alunoDao.buscarPorId(alunoId)
            if not aluno:
                print(f"❌ Erro: Aluno com ID {alunoId} não encontrada!")
                return
            
            usuario = self.__usuarioDao.buscarPorAlunoId(alunoId)
            
            if usuario:
                print("\n✅ Usuário encontrado:")
                self.exibirDetalhesUsuario(usuario)
            else:
                print(f"⚠️  O aluno '{aluno.nome}' (ID: {alunoId}) não possui usuário cadastrado.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao buscar usuário: {e}")
    
    def atualizarUsuario(self):
        """Solicita dados do usuário e atualiza um usuário existente"""
        print("\n--- ATUALIZAR USUÁRIO ---")
        
        try:
            idStr = input("Digite o ID do usuário a atualizar: ").strip()
            usuarioId = int(idStr)
            
            usuario = self.__usuarioDao.buscarPorId(usuarioId)
            
            if not usuario:
                print(f"⚠️  Usuário com ID {usuarioId} não encontrado.")
                return
            
            print(f"\nUsuário atual:")
            self.exibirDetalhesUsuario(usuario)
            
            print("\nDigite os novos dados (ou Enter para manter o valor atual):")
            
            # Login
            novoLogin = input(f"Login [{usuario.login}]: ").strip()
            if novoLogin:
                # Verificar se já existe outro usuário com esse login
                usuarioExistente = self.__usuarioDao.buscarPorLogin(novoLogin)
                if usuarioExistente and usuarioExistente.id != usuarioId:
                    print(f"❌ Erro: Já existe outro usuário com o login '{novoLogin}' (ID: {usuarioExistente.id})")
                    return
                usuario.login = novoLogin
            
            # Senha
            novaSenha = input("Senha (ou Enter para manter): ").strip()
            if novaSenha:
                usuario.senha = novaSenha
            
            # Tipo
            novoTipo = input(f"Tipo [{usuario.tipo}]: ").strip().lower()
            if novoTipo:
                usuario.tipo = novoTipo
            
            self.__usuarioDao.salvar(usuario)
            print(f"\n✅ Usuário atualizado com sucesso!")
            print("\nDados atualizados:")
            self.exibirDetalhesUsuario(usuario)
        
        except ValueError as e:
            print(f"❌ Erro: {e}")
        except Exception as e:
            print(f"❌ Erro ao atualizar usuário: {e}")
    
    def deletarUsuario(self):
        """Solicita um ID e deleta o usuário correspondente"""
        print("\n--- DELETAR USUÁRIO ---")
        
        try:
            idStr = input("Digite o ID do usuário a deletar: ").strip()
            usuarioId = int(idStr)
            
            usuario = self.__usuarioDao.buscarPorId(usuarioId)
            
            if not usuario:
                print(f"⚠️  Usuário com ID {usuarioId} não encontrado.")
                return
            
            print(f"\nUsuário a ser deletado:")
            self.exibirDetalhesUsuario(usuario)
            
            confirmacao = input("\n⚠️  Tem certeza que deseja deletar este usuário? (s/N): ").strip().lower()
            
            if confirmacao != 's':
                print("❌ Operação cancelada.")
                return
            
            sucesso = self.__usuarioDao.deletar(usuario)
            
            if sucesso:
                print(f"\n✅ Usuário deletado com sucesso!")
            else:
                print(f"\n❌ Erro ao deletar usuário.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao deletar usuário: {e}")
    
    def executar(self):
        """Método principal que executa o loop do menu"""
        try:
            while True:
                self.exibirMenu()
                opcao = input("\nEscolha uma opção: ").strip()
                
                if opcao == '0':
                    print("\n👋 Encerrando o sistema...")
                    break
                elif opcao == '1':
                    self.criarUsuario()
                elif opcao == '2':
                    self.listarUsuarios()
                elif opcao == '3':
                    self.buscarPorId()
                elif opcao == '4':
                    self.buscarPorLogin()
                elif opcao == '5':
                    self.buscarPorAluno()
                elif opcao == '6':
                    self.atualizarUsuario()
                elif opcao == '7':
                    self.deletarUsuario()
                else:
                    print("❌ Opção inválida! Tente novamente.")
                
                input("\nPressione Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Função principal para executar o serviço"""
    db = DatabaseConnection('exemplo_bd.db')
    
    try:
        # Conectar ao banco
        db.conectar()
        
        # Garantir que as tabelas existam
        db.criarTabelas()
        
        # Criar e executar o serviço
        service = UsuarioService(db)
        service.executar()
    
    except Exception as e:
        print(f"❌ Erro ao inicializar o sistema: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.fechar()
        print("✓ Conexão com banco de dados encerrada.")


if __name__ == "__main__":
    main()
