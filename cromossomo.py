import random

class Cromossomo:
    def __init__(self, rota, estado_final):
        self.rota = rota
        self.aptidao = self.calcular_aptidao(estado_final)

    def calcular_aptidao(self, estado_final):
        penalidade = 0

        # Restrição 1: cidade maior antes de cidade menor (nota 10)
        for i in range(len(self.rota) - 1):
            if self.rota[i] > self.rota[i+1]:
                penalidade += 10

        # Restrição 2: cidade repetida (nota 20 por par)
        cidades_vistas = set()
        for cidade in self.rota:
            if cidade in cidades_vistas:
                penalidade += 20
            cidades_vistas.add(cidade)

        # Quanto menor a penalidade, melhor o indivíduo
        return -penalidade

    def __str__(self):
        return f'{self.rota} - {self.aptidao}'

    def __eq__(self, other):
        if isinstance(other, Cromossomo):
            return self.rota == other.rota
        return False

    @staticmethod
    def gerar_populacao(populacao, tamanho_populacao, estado_final):
        for _ in range(tamanho_populacao):
            rota = list(range(1, 10))  # Cidades de 1 a 9
            random.shuffle(rota)
            individuo = Cromossomo(rota, estado_final)
            populacao.append(individuo)

    @staticmethod
    def exibir_populacao(populacao, numero_geracao):
        print(f'\nGeração {numero_geracao + 1}: Melhor rota = {populacao[0].rota} - Aptidão = {populacao[0].aptidao}')

    @staticmethod
    def selecionar(populacao, nova_populacao, taxa_selecao):
        quantidade_selecionados = int(len(populacao) * taxa_selecao / 100)
        torneio = []

        # Elitismo - o mais apto sempre é selecionado
        nova_populacao.append(populacao[0])

        i = 1
        while i < quantidade_selecionados:
            # Seleciona 3 indivíduos aleatórios para o torneio
            participantes = random.sample(populacao, 3)

            # Ordena pelo melhor (maior aptidão)
            participantes.sort(key=lambda c: c.aptidao, reverse=True)
            selecionado = participantes[0]

            if selecionado not in nova_populacao:
                nova_populacao.append(selecionado)
                i += 1

    @staticmethod
    def reproduzir(populacao, nova_populacao, taxa_reproducao, estado_final):
        quantidade_reproduzidos = int(len(populacao) * taxa_reproducao / 100)

        for _ in range(int(quantidade_reproduzidos/2)+1):
            # Seleciona dois pais diferentes
            pai, mae = random.sample(populacao[:int(len(populacao)*0.2)], 2)

            # Crossover OX (Order Crossover)
            filho1, filho2 = Cromossomo.crossover_ox(pai.rota, mae.rota)

            nova_populacao.append(Cromossomo(filho1, estado_final))
            nova_populacao.append(Cromossomo(filho2, estado_final))

            # Remove excedentes
            while len(nova_populacao) > len(populacao):
                nova_populacao.pop()

    @staticmethod
    def crossover_ox(pai, mae):
        tamanho = len(pai)
        ponto1, ponto2 = sorted(random.sample(range(tamanho), 2))

        def criar_filho(p1, p2):
            filho = [None] * tamanho
            filho[ponto1:ponto2] = p1[ponto1:ponto2]

            pos_p = 0
            for i in range(tamanho):
                if filho[i] is None:
                    while p2[pos_p % tamanho] in filho:
                        pos_p += 1
                    filho[i] = p2[pos_p % tamanho]
                    pos_p += 1
            return filho

        filho1 = criar_filho(pai, mae)
        filho2 = criar_filho(mae, pai)
        return filho1, filho2

    @staticmethod
    def mutar(nova_populacao, estado_final):
        for individuo in nova_populacao:
            if random.random() < 0.1:  # 10% de chance de mutação
                idx1, idx2 = random.sample(range(len(individuo.rota)), 2)
                individuo.rota[idx1], individuo.rota[idx2] = individuo.rota[idx2], individuo.rota[idx1]
                individuo.aptidao = individuo.calcular_aptidao(estado_final)