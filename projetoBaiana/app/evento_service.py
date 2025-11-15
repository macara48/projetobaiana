"""
Serviço para interação do usuário via linha de comando com a entidade evento
e gerenciamento do relacionamento N:N com Avaliacao
"""
import sys
import os

# Adicionar o diretório pai ao path para permitir imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bd.database import DatabaseConnection
from dao.evento_dao import EventoDAO
from dao.avaliacao_dao import AvaliacaoDAO
from model.evento_class import Evento


class EventoService:
    
    def __init__(self, db: DatabaseConnection):
        self.__db = db
        self.__eventoDao = EventoDAO(db)
        self.__avaliacaoDao = AvaliacaoDAO(db)
    
    def exibirMenu(self):
        """Exibe o menu principal de opções"""
        print("\n" + "="*50)
        print("  SISTEMA DE GERENCIAMENTO DE EVENTOS")
        print("="*50)
        print("1. Criar evento")
        print("2. Listar todos os eventos")
        print("3. Buscar evento por ID")
        print("4. Buscar evento por nome")
        print("5. Atualizar evento")
        print("6. Deletar evento")
        print("7. Vincular avaliacao a evento")
        print("8. Desvincular avaliacao de evento")
        print("9. Listar avaliacoes de uma evento")
        print("0. Sair")
        print("="*50)
    
    def criarEvento(self):
        """Solicita dados do usuário e cria um novo evento"""
        print("\n--- CRIAR EVENTO ---")
        
        nome = input("Digite o nome do evento: ").strip()
        if not nome:
            print("❌ Erro: O nome do evento não pode ser vazio!")
            return
        
        # Verificar se já existe um evento com esse nome
        eventosExistentes = self.__eventoDao.buscarPorNome(nome)
        for e in eventosExistentes:
            if e.nome.lower() == nome.lower():
                print(f"❌ Erro: Já existe um evento com o nome '{nome}' (ID: {e.id})")
                return
        
        dataEventoStr = input("Digite a data do evento: ").strip()
        dataEvento = int(dataEventoStr) if dataEventoStr else None
        
        homenageado = input("Informe a pessoa homenageada no evento: ").strip()
        homenageado = homenageado if homenageado else None
        
        try:
            evento = Evento(
                id=None,
                nome=nome,
                dataEvento=dataEvento,
                homenageado=homenageado
            )
            
            eventoId = self.__eventoDao.salvar(evento)
            print(f"\n✅ Evento criado com sucesso!")
            self.exibirDetalhesEvento(evento)
        
        except ValueError as e:
            print(f"❌ Erro de validação: {e}")
        except Exception as e:
            print(f"❌ Erro ao criar evento: {e}")
    
    def exibirDetalhesEvento(self, evento: Evento):
        """Exibe os detalhes completos de um evento"""
        print(f"\n   ID: {evento.id}")
        print(f"   Nome: {evento.nome}")
        if evento.dataEvento is not None:
            print(f"   Data: {evento.dataEvento} ")
        if evento.homenageado:
            print(f"   Homenageado(a): {evento.homenageado}")
    
    def listarEventos(self):
        """Lista todos os evento cadastrados"""
        print("\n--- LISTAR TODOS OS EVENTOS ---")
        
        try:
            eventos = self.__eventoDao.listarTodas()
            
            if not eventos:
                print("⚠️  Nenhum evento cadastrado.")
                return
            
            print(f"\nTotal de eventos: {len(eventos)}")
            print("\n" + "-"*80)
            print(f"{'ID':<5} | {'Nome':<40} | {'Data':<10}")
            print("-"*80)
            
            for evento in eventos:
                dataEvento = f"{evento.dataEvento}" if evento.dataEvento else "N/A"
                print(f"{evento.id:<5} | {evento.nome[:39]:<40} | {dataEvento:<15}")
            
            print("-"*80)
        
        except Exception as e:
            print(f"❌ Erro ao listar eventos: {e}")
    
    def buscarPorId(self):
        """Solicita um ID e busca o evento correspondente"""
        print("\n--- BUSCAR EVENTO POR ID ---")
        
        try:
            idStr = input("Digite o ID do evento: ").strip()
            eventoId = int(idStr)
            
            evento = self.__eventoDao.buscarPorId(eventoId)
            
            if evento:
                print("\n✅ Evento encontrada:")
                self.exibirDetalhesEvento(evento)
            else:
                print(f"⚠️  Evento com ID {eventoId} não encontrado.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao buscar evento: {e}")
    
    def buscarPorNome(self):
        """Solicita um nome e busca eventos correspondentes"""
        print("\n--- BUSCAR EVENTO POR NOME ---")
        
        nome = input("Digite o nome (ou parte do nome) do evento: ").strip()
        
        if not nome:
            print("❌ Erro: O nome não pode ser vazio!")
            return
        
        try:
            eventos = self.__eventoDao.buscarPorNome(nome)
            
            if eventos:
                print(f"\n✅ {len(evento)} evento(s) encontrada(s):")
                print("\n" + "-"*80)
                for evento in eventos:
                    dataEvento = f"{evento.dataEvento}h" if evento.dataEvento else "N/A"
                    print(f"ID: {evento.id} | {evento.nome} | Data: {dataEvento}")
                print("-"*80)
            else:
                print(f"⚠️  Nenhum evento encontrado com o nome contendo '{nome}'.")
        
        except Exception as e:
            print(f"❌ Erro ao buscar evento: {e}")
    
    def atualizarevento(self):
        """Solicita dados do usuário e atualiza um evento existente"""
        print("\n--- ATUALIZAR EVENTO ---")
        
        try:
            idStr = input("Digite o ID do evento a atualizar: ").strip()
            eventoId = int(idStr)
            
            evento = self.__eventoDao.buscarPorId(eventoId)
            
            if not evento:
                print(f"⚠️  Evento com ID {eventoId} não encontrada.")
                return
            
            print(f"\nEvento atual:")
            self.exibirDetalhesEvento(evento)
            
            print("\nDigite os novos dados (ou Enter para manter o valor atual):")
            
            # Nome
            novoNome = input(f"Nome [{evento.nome}]: ").strip()
            if novoNome:
                # Verificar se já existe outro evento com esse nome
                eventosExistentes = self.__eventoDao.buscarPorNome(novoNome)
                for e in eventosExistentes:
                    if e.id != eventoId and e.nome.lower() == novoNome.lower():
                        print(f"❌ Erro: Já existe outro evento com o nome '{novoNome}' (ID: {e.id})")
                        return
                evento.nome = novoNome
            
            # Data
            cargaStr = input(f"Data [{evento.dataEvento or 'N/A'}] (ou Enter para manter): ").strip()
            if cargaStr:
                evento.dataEvento = int(cargaStr) if cargaStr else None
            
            # Homenageado
            descStr = input(f"Descrição [{evento.homenageado or 'N/A'}] (ou Enter para manter): ").strip()
            if descStr:
                evento.homenageado = descStr if descStr else None
            
            self.__eventoDao.salvar(evento)
            print(f"\n✅ Evento atualizado com sucesso!")
            print("\nDados atualizados:")
            self.exibirDetalhesEvento(evento)
        
        except ValueError as e:
            print(f"❌ Erro: {e}")
        except Exception as e:
            print(f"❌ Erro ao atualizar evento: {e}")
    
    def deletarEvento(self):
        """Solicita um ID e deleta o evento correspondente"""
        print("\n--- DELETAR EVENTO ---")
        
        try:
            idStr = input("Digite o ID do evento a deletar: ").strip()
            eventoId = int(idStr)
            
            evento = self.__eventoDao.buscarPorId(eventoId)
            
            if not evento:
                print(f"⚠️  Evento com ID {eventoId} não encontrado.")
                return
            
            print(f"\nEvento a ser deletada:")
            self.exibirDetalhesEvento(evento)
            
            confirmacao = input("\n⚠️  Tem certeza que deseja deletar este evento? (s/N): ").strip().lower()
            
            if confirmacao != 's':
                print("❌ Operação cancelada.")
                return
            
            sucesso = self.__eventoDao.deletar(evento)
            
            if sucesso:
                print(f"\n✅ Evento deletada com sucesso!")
            else:
                print(f"\n❌ Erro ao deletar evento.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao deletar evento: {e}")
    
    def vincularAvaliacao(self):
        """Vincula uma avaliacao a um evento"""
        print("\n--- VINCULAR AVALIACAO A EVENTO ---")
        
        try:
            # Selecionar evento
            eventos = self.__eventoDao.listarTodas()
            if not eventos:
                print("⚠️  Nenhum evento cadastrada.")
                return
            
            print("\nEventos disponíveis:")
            for e in eventos:
                print(f"  {e.id}. {e.nome}")
            
            eventoIdStr = input("\nDigite o ID do evento: ").strip()
            eventoId = int(eventoIdStr)
            evento = self.__eventoDao.buscarPorId(eventoId)
            
            if not evento:
                print(f"❌ Erro: Evento com ID {eventoId} não encontrado!")
                return
            
            # Selecionar avaliacao
            avaliacoes = self.__avaliacaoDao.listarTodas()
            if not avaliacoes:
                print("⚠️  Nenhuma avaliação cadastrada.")
                return
            
            print("\nAvaliações disponíveis:")
            for a in avaliacoes:
                print(f"  {a.id}. {a.data} - {a.aluno} - {a.examinador} - {a.evento}")
            
            avaliacaoIdStr = input("\nDigite o ID da avaliação: ").strip()
            avaliacaoId = int(avaliacaoIdStr)
            avaliacao = self.__avaliacaoDao.buscarPorId(avaliacaoId)
            
            if not avaliacao:
                print(f"❌ Erro: Avaliação com ID {avaliacaoId} não encontrada!")
                return
            
            # Verificar se já está vinculado
            eventosAvaliacao = self.__eventoDao.buscarEventosPorAvaliacao(avaliacaoId)
            if evento in eventosAvaliacao:
                print(f"❌ Erro: A avaliacao '{avaliacao.id}' já está vinculada ao evento '{evento.nome}'!")
                return
            
            sucesso = self.__eventoDao.vincularAvaliacao(avaliacao, evento)
            
            if sucesso:
                print(f"\n✅ Avaliação '{avaliacao.id}' vinculada ao evento '{evento.nome}' com sucesso!")
            else:
                print(f"\n❌ Erro: A avaliação já está vinculada a este evento.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao vincular avaliação: {e}")
    
    def desvincularAvaliacao(self):
        """Remove o vínculo entre uma avaliação e um evento"""
        print("\n--- DESVINCULAR AVALIAÇÃO DE EVENTO ---")
        
        try:
            # Selecionar evento
            eventos = self.__eventoDao.listarTodas()
            if not eventos:
                print("⚠️  Nenhum evento cadastrada.")
                return
            
            print("\nEventos disponíveis:")
            for e in eventos:
                print(f"  {e.id}. {e.nome}")
            
            eventoIdStr = input("\nDigite o ID do evento: ").strip()
            eventoId = int(eventoIdStr)
            evento = self.__eventoDao.buscarPorId(eventoId)
            
            if not evento:
                print(f"❌ Erro: Evento com ID {eventoId} não encontrada!")
                return
            
            # Listar avaliacoes vinculadas
            avaliacoesVinculadas = self.__eventoDao.buscarAvaliacoesPorEvento(eventoId)
            if not avaliacoesVinculadas:
                print(f"⚠️  Nenhuma avaliação vinculada ao evento '{evento.nome}'.")
                return
            
            print(f"\nAvaliações vinculadas ao evento '{evento.nome}':")
            for a in avaliacoesVinculadas:
                print(f"  {a.id}. {a.data} - {a.aluno} - {a.examinador} - {a.evento}")
            
            avaliacaoIdStr = input("\nDigite o ID da avaliação a desvincular: ").strip()
            avaliacaoId = int(avaliacaoIdStr)
            avaliacao = self.__avaliacaoDao.buscarPorId(avaliacaoId)
            
            if not avaliacao:
                print(f"❌ Erro: Avaliação com ID {avaliacaoId} não encontrada!")
                return
            
            sucesso = self.__avaliacaoaDao.desvincularAvaliacao(avaliacao, evento)
            
            if sucesso:
                print(f"\n✅ Avaliação '{avaliacao.nome}' desvinculada do evento '{evento.nome}' com sucesso!")
            else:
                print(f"\n❌ Erro: A avaliação não está vinculada a este evento.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao desvincular avaliação: {e}")
    
    def listarAvaliacoesEvento(self):
        """Lista todas as avaliações vinculadas a um evento"""
        print("\n--- LISTAR AVALIAÇÕES DE UM EVENTO ---")
        
        try:
            eventos = self.__eventoDao.listarTodas()
            if not eventos:
                print("⚠️  Nenhum evento cadastrado.")
                return
            
            print("\nEventos disponíveis:")
            for e in eventos:
                print(f"  {e.id}. {e.nome}")
            
            eventoIdStr = input("\nDigite o ID do evento: ").strip()
            eventoId = int(eventoIdStr)
            evento = self.__eventoDao.buscarPorId(eventoId)
            
            if not evento:
                print(f"❌ Erro: Evento com ID {eventoId} não encontrada!")
                return
            
            avaliacoes = self.__eventoDao.buscarAvaliacoesPorEvento(eventoId)
            
            if avaliacoes:
                print(f"\n✅ {len(avaliacoes)} avaliação(s) vinculada(s) ao evento '{evento.nome}':")
                print("\n" + "-"*80)
                for avaliacao in avaliacoes:
                    print(f"ID: {avaliacao.id} | {avaliacao.data} | {avaliacao.aluno} | {avaliacao.examinador} {avaliacao.nivel}")
                print("-"*80)
            else:
                print(f"⚠️  Nenhuma avaliação vinculada à e '{evento.nome}'.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao listar avaliações: {e}")
    
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
                    self.criarEvento()
                elif opcao == '2':
                    self.listarEventos()
                elif opcao == '3':
                    self.buscarPorId()
                elif opcao == '4':
                    self.buscarPorNome()
                elif opcao == '5':
                    self.atualizarEvento()
                elif opcao == '6':
                    self.deletarEvento()
                elif opcao == '7':
                    self.vincularAvaliacao()
                elif opcao == '8':
                    self.desvincularAvaliacao()
                elif opcao == '9':
                    self.listarAvaliacoesEvento()
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
        service = EventoService(db)
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
