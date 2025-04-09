from cromossomo import Cromossomo

# Config
estado_final = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # Rota perfeita
tamanho_populacao = 100
quantidade_geracoes = 200
taxa_selecao = 25  # 30% seleção, 70% reprodução
taxa_mutacao = 10   # 10% de chance de mutação

populacao = []
nova_populacao = []

# População inicial
Cromossomo.gerar_populacao(populacao, tamanho_populacao, estado_final)
populacao.sort(key=lambda c: c.aptidao, reverse=True)
Cromossomo.exibir_populacao(populacao, 0)

for i in range(1, quantidade_geracoes + 1):

    # Seleciona os melhores
    Cromossomo.selecionar(populacao, nova_populacao, taxa_selecao)
    
    # Reproduz para criar nova população
    Cromossomo.reproduzir(populacao, nova_populacao, 100 - taxa_selecao, estado_final)
    
    # Mutação
    if i % taxa_mutacao == 0:
        Cromossomo.mutar(nova_populacao, estado_final)
    
    # Atualizar população
    populacao.clear()
    populacao.extend(nova_populacao)
    nova_populacao.clear()
    
    # Ordenar por aptidão
    populacao.sort(key=lambda c: c.aptidao, reverse=True)
    Cromossomo.exibir_populacao(populacao, i)
    
    # Solução

    if populacao[0].aptidao == 0:
        print("\nSolução encontrada!")
        break

print(populacao[0])