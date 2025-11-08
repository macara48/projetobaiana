"""
Serviço para interação do usuário via linha de comando com a entidade Pessoa
"""
import sys
import os

# Adicionar o diretório pai ao path para permitir imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bd.database import DatabaseConnection
from dao.aluno_dao import AlunoDAO
from dao.nivel_dao import NivelDAO
from model.aluno_class import Aluno
from model.parametros_class import Parametros

class AlunoService:
    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.alunoDao = AlunoDAO(db)
        self.nivelDao = NivelDAO(db)

    def exibirMenu(self):
        """Exibe o menu principal de opções"""
        print("\n" + "="*50)
        print("  SISTEMA DE GERENCIAMENTO DE ALUNOS")
        print("="*50)
        print("1. Criar aluno")
        print("2. Listar todos os alunos")
        print("3. Buscar aluno por ID")
        print("4. Buscar aluno por nome")
        print("5. Buscar alunos por nivel")
        print("6. Atualizar aluno")
        print("7. Deletar aluno")
        print("0. Sair")
        print("="*50)
    
    def listarNiveisDisponiveis(self):
        """Lista todas as niveis disponíveis para seleção"""
        niveis = self.nivelDao.listarTodas()
        if not niveis:
            print("⚠️  Nenhum nivel cadastrada. Cadastre um nivel primeiro!")
            return None
        
        print("\nNíveis disponíveis:")
        print("-"*30)
        for niv in niveis:
            print(f"  {niv.nivel_id}. {niv.corNivel}")
        print("-"*30)
        return niveis
    
    def selecionarNivel(self):
        """Solicita ao usuário que selecione um nivel"""
        niveis = self.listarNiveisDisponiveis()
        if not niveis:
            return None
        
        try:
            nivelIdStr = input("Digite o ID do nivel: ").strip()
            nivelId = int(nivelIdStr)
            
            nivel = self.nivelDao.buscarPorId(nivelId)
            if not nivel:
                print(f"❌ Erro: Categoria com ID {nivelId} não encontrada!")
                return None
            
            return nivel
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
            return None
        
    def criarAluno(self):
        """Solicita dados do usuário e cria um novo aluno"""
        print("\n--- CRIAR ALUNO ---")
        
        nome = input("Digite o nome: ").strip()
        if not nome:
            print("❌ Erro: O nome não pode ser vazio!")
            return
        
        contato = input("Digite o seu contato: ").strip()
        if not contato:
            print("❌ Erro: O contato não pode ser vazio!")
            return
        
        # Verificar se já existe uma pessoa com esse contato
        alunosExistentes = self.alunoDao.buscarPorNome("")  # Buscar todas para verificar contato
        todosAlunos = self.alunoDao.listarTodas()
        for a in todosAlunos:
            if a.contato.lower() == contato.lower():
                print(f"❌ Erro: Já existe uma pessoa com o contato '{contato}' (ID: {a.aluno_id})")
                return
        
        # Selecionar nivel
        nivel = self.selecionarNivel()
        if not nivel:
            return
        
        # Campos opcionais
        ativoStr = input("Aluno está ativo? (S/N): ").strip().lower()
        ativo = ativoStr != 'n'
        
        try:
            aluno = Aluno(
                aluno_id=None,
                nome=nome,
                contato=contato,
                nivel=nivel,
                ativo=ativo,
                tipoConducao=Parametros
            )
            
            alunoId = self.alunoDao.salvar(aluno)
            print(f"\n✅ Aluno criado com sucesso!")
            self.exibirDetalhesAluno(aluno)
        
        except ValueError as e:
            print(f"❌ Erro de validação: {e}")
        except Exception as e:
            print(f"❌ Erro ao criar aluno: {e}")

    def exibirDetalhesAluno(self, aluno: Aluno):
        """Exibe os detalhes completos de uma pessoa"""
        print(f"\n   ID: {aluno.aluno_id}")
        print(f"   Nome: {aluno.nome}")
        print(f"   Contato: {aluno.contato}")
        print(f"   Nivel: {aluno.nivel.corNivel} (ID: {aluno.nivel.nivel_id})")

    def listarAlunos(self):
        """Lista todos os alunos cadastrados"""
        print("\n--- LISTAR TODOS OS ALUNOS ---")
        
        try:
            alunos = self.alunoDao.listarTodas()
            
            if not alunos:
                print("⚠️  Nenhum aluno cadastrado.")
                return
            
            print(f"\nTotal de alunos: {len(alunos)}")
            print("\n" + "-"*80)
            print(f"{'ID':<5} | {'Nome':<25} | {'Contato':<25} | {'Nivel':<15} | {'Status':<8}")
            print("-"*80)
            
            for aluno in alunos:
                status = "Ativa" if aluno.ativo else "Inativa"
                print(f"{aluno.aluno_id:<5} | {aluno.nome[:24]:<25} | {aluno.contato[:24]:<25} | {aluno.nivel.corNivel[:14]:<15} | {status:<8}")
            
            print("-"*80)
        
        except Exception as e:
            print(f"❌ Erro ao listar alunos: {e}")

    def buscarPorId(self):
        """Solicita um ID e busca o aluno correspondente"""
        print("\n--- BUSCAR ALUNO POR ID ---")
        
        try:
            idStr = input("Digite o ID do aluno: ").strip()
            alunoId = int(idStr)
            
            aluno = self.alunoDao.buscarPorId(alunoId)
            
            if aluno:
                print("\n✅ Aluno encontrada:")
                self.exibirDetalhesAluno(aluno)
            else:
                print(f"⚠️  Aluno com ID {alunoId} não encontrado.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao buscar aluno: {e}")

    def buscarPorNome(self):
        """Solicita um nome e busca alunos correspondentes"""
        print("\n--- BUSCAR ALUNO POR NOME ---")
        
        nome = input("Digite o nome (ou parte do nome) do aluno: ").strip()
        
        if not nome:
            print("❌ Erro: O nome não pode ser vazio!")
            return
        
        try:
            alunos = self.alunoDao.buscarPorNome(nome)
            
            if alunos:
                print(f"\n✅ {len(alunos)} aluno(s) encontrado(s):")
                print("\n" + "-"*80)
                for aluno in alunos:
                    print(f"ID: {aluno.aluno_id} | {aluno.nome} | {aluno.contato} | {aluno.nivel.corNivel}")
                print("-"*80)
            else:
                print(f"⚠️  Nenhum aluno encontrad com o nome contendo '{nome}'.")
        
        except Exception as e:
            print(f"❌ Erro ao buscar aluno: {e}")

    def buscarPorNivel(self):
        """Lista alunos de um nivel específico"""
        print("\n--- BUSCAR PESSOAS POR NIVEL ---")
        
        niveis = self.listarNiveisDisponiveis()
        if not niveis:
            return
        
        try:
            nivelIdStr = input("Digite o ID da nivel: ").strip()
            nivelId = int(nivelIdStr)
            
            nivel = self.nivelDao.buscarPorId(nivelId)
            if not nivel:
                print(f"❌ Erro: Nivel com ID {nivelId} não encontrado!")
                return
            
            alunos = self.nivelDao.buscarPorNivel(nivelId)
            
            if alunos:
                print(f"\n✅ {len(alunos)} aluno(s) encontrado(s) no nivel '{nivel.corNivel}':")
                print("\n" + "-"*80)
                for aluno in alunos:
                    status = "Ativa" if aluno.ativo else "Inativo"
                    print(f"ID: {aluno.aluno_id} | {aluno.nome} | {aluno.contato} | Status: {status}")
                print("-"*80)
            else:
                print(f"⚠️  Nenhum aluno encontrado na categoria '{aluno.nome}'.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao buscar alunos: {e}")

    def atualizarAluno(self):
        """Solicita dados do usuário e atualiza um aluno existente"""
        print("\n--- ATUALIZAR ALUNO ---")
        
        try:
            idStr = input("Digite o ID do aluno a atualizar: ").strip()
            alunoId = int(idStr)
            
            aluno = self.alunoDao.buscarPorId(alunoId)
            
            if not aluno:
                print(f"⚠️  Aluno com ID {alunoId} não encontrado.")
                return
            
            print(f"\nAluno atual:")
            self.exibirDetalhesAluno(aluno)
            
            print("\nDigite os novos dados (ou Enter para manter o valor atual):")
            
            # Nome
            novoNome = input(f"Nome [{aluno.nome}]: ").strip()
            if novoNome:
                aluno.nome = novoNome
            
            # Contato
            novoContato = input(f"Contato [{aluno.contato}]: ").strip()
            if novoContato:
                # Verificar se já existe outro aluno com esse contato
                todosAlunos = self.alunoDao.listarTodas()
                for a in todosAlunos:
                    if a.aluno_id != alunoId and a.contato.lower() == novoContato.lower():
                        print(f"❌ Erro: Já existe outro aluno com o contato '{novoContato}' (ID: {a.aluno_id})")
                        return
                aluno.contato = novoContato
            
            # Nivel
            nivelStr = input(f"Nivel ID [{aluno.nivel.nivel_id} - {aluno.nivel.corNivel}] (ou Enter para manter): ").strip()
            if nivelStr:
                novoNivelId = int(nivelStr)
                novoNivel = self.nivelDao.buscarPorId(novoNivelId)
                if not novoNivel:
                    print(f"❌ Erro: Nivel com ID {novoNivelId} não encontrado!")
                    return
                aluno.nivel = novoNivel
            
            # Status ativo
            ativoStr = input(f"Status ativo (S/N) [{'S' if aluno.ativo else 'n'}] (ou Enter para manter): ").strip().lower()
            if ativoStr:
                aluno.ativo = ativoStr != 'n'
            
            self.alunoDao.salvar(aluno)
            print(f"\n✅ Aluno atualizado com sucesso!")
            print("\nDados atualizados:")
            self.exibirDetalhesAluno(aluno)
        
        except ValueError as e:
            print(f"❌ Erro: {e}")
        except Exception as e:
            print(f"❌ Erro ao atualizar aluno: {e}")

    def deletarAluno(self):
        """Solicita um ID e deleta o aluno correspondente"""
        print("\n--- DELETAR ALUNO ---")
        
        try:
            idStr = input("Digite o ID do aluno a deletar: ").strip()
            alunoId = int(idStr)
            
            aluno = self.alunoDao.buscarPorId(alunoId)
            
            if not aluno:
                print(f"⚠️  Aluno com ID {alunoId} não encontrado.")
                return
            
            print(f"\nAluno a ser deletada:")
            self.exibirDetalhesAluno(aluno)
            
            confirmacao = input("\n⚠️  Tem certeza que deseja deletar este aluno? (s/N): ").strip().lower()
            
            if confirmacao != 's':
                print("❌ Operação cancelada.")
                return
            
            sucesso = self.alunoDao.deletar(aluno)
            
            if sucesso:
                print(f"\n✅ Aluno deletada com sucesso!")
            else:
                print(f"\n❌ Erro ao deletar aluno.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao deletar aluno: {e}")

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
                    self.criarAluno()
                elif opcao == '2':
                    self.listarAluno()
                elif opcao == '3':
                    self.buscarPorId()
                elif opcao == '4':
                    self.buscarPorNome()
                elif opcao == '5':
                    self.buscarPorNivel()
                elif opcao == '6':
                    self.atualizarAluno()
                elif opcao == '7':
                    self.deletarAluno()
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
        service = AlunoService(db)
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