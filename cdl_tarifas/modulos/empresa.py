class Empresa(object):

    def __init__(self, nome):
        self.nome = nome

    def organiza_faixa(self, vetor_faixa):
        for i in range(0, int(len(vetor_faixa) / 2), 1):
            vetor_faixa[i] = vetor_faixa[i] + " a " + vetor_faixa.pop(i + 1)
        return vetor_faixa

    def organiza_faixa_tarifas(self, vetor_faixa, vetor_tarifa):#ORGANIZA UM VETOR DE FAIXAS E TARIFAS, PRIMEIRAMENTE UM VALOR DE FAIXA '1 A 70' SEGUIDOS DE TUAS TARIFAS, TARIA S/IMPOSTO E TARIFA COM IMPOSTO. RESULTADO = ['1 A 70', '1.43', '1.80']
        cont = 0
        faixa_tarifa = []
        for i in range(0, len(vetor_faixa), 1):
            vetor_faixa[i] = vetor_faixa[i].replace('.', '')
            #vetor_tarifa[cont] = float(vetor_tarifa[cont].replace(',', '.'))
            #vetor_tarifa[cont+1] = float(vetor_tarifa[cont + 1].replace(',', '.'))
            faixa_tarifa.append((i+1, vetor_faixa[i], vetor_tarifa[cont], vetor_tarifa[cont + 1], "0", "0"))
            cont = cont + 2
        return faixa_tarifa

    def organiza_faixa_tarifas_parcelas(self, vetor_faixa, vetor_tarifa, vetor_parcelas):#dados(n_faixa, vetor_fxas, tar_simp, tar_cimp, par_simp, par_cimp)
        cont = 0
        dados = []
        for i in range(0, len(vetor_faixa), 1):
            vetor_faixa[i] = vetor_faixa[i].replace('.', '')
            #vetor_tarifa[cont] = float(vetor_tarifa[cont].replace(',', '.'))
            #vetor_tarifa[cont+1] = float(vetor_tarifa[cont+1].replace(',', '.'))
            dados.append((i+1, vetor_faixa[i], vetor_tarifa[cont], vetor_tarifa[cont+1], vetor_parcelas[cont], vetor_parcelas[cont+1]))
            cont = cont+2
        return dados

    def agrupa_duas_faixa(self, vetor_faixa1, vetor_faixa2):
        vetor_auxiliar = []
        for i in range(0, len(vetor_faixa1)):
            vetor_faixa1[i] = str(vetor_faixa1[i]).replace('.', '')
            vetor_faixa2[i] = str(vetor_faixa2[i]).replace('.', '')
            vetor_auxiliar.append(str(vetor_faixa1[i])+" a "+str(vetor_faixa2[i]))

        return vetor_auxiliar

    def organiza_tarifa_s_c_imposto(self, vetor_s_imposto, vetor_c_imposto):
        vetor_auxiliar = []
        for i in range(0, len(vetor_s_imposto)):
            vetor_auxiliar.append(vetor_s_imposto[i])
            vetor_auxiliar.append(vetor_c_imposto[i])

        return vetor_auxiliar

    def calcula_imposto_tarifa(self, icms, pis, confis, tarifas_s_impostos):
        total_impostos = icms + pis+confis
        vetor_tarifas = []

        for i in range(0, len(tarifas_s_impostos)):
            tarifa = float(tarifas_s_impostos[i].replace(',', '.'))
            #tarifa_c_imposto = round((tarifas_s_impostos* 100) / (100 - total_imposto), 4)
            tarifa_c_imposto = round(tarifa / ((100 - total_impostos) / 100), 3)
            vetor_tarifas.append(str(tarifa).replace('.', ','))
            vetor_tarifas.append(str(tarifa_c_imposto).replace('.', ','))

        return vetor_tarifas

    def calcula_s_imposto_tarifa(self, icms, pis, confis, tarifas_c_impostos):
        total_impostos = icms+pis+confis
        vetor_tarifas = []
        for i in range(0, len(tarifas_c_impostos)):
            valor_c_impostos = float(tarifas_c_impostos[i].replace(',', '.'))
            #valor_s_imposto = round(valor_c_imposto - (valor_c_imposto*(total_impostos/100)), 4)
            valor_s_impostos = round(valor_c_impostos * ((100 - total_impostos) / 100), 3)

            vetor_tarifas.append(str(valor_s_impostos).replace('.', ','))
            vetor_tarifas.append(str(valor_c_impostos).replace('.', ','))

        return vetor_tarifas

    def calcula_imposto_parcela(self,icms, pis, confis, parcelas_s_impostos):
        total_impostos = icms + pis + confis
        vetor_parcelas = []

        for i in range(0, len(parcelas_s_impostos)):
            valor_s_impostos = float(parcelas_s_impostos[i].replace(',', '.'))
            #parcelas_c_impostos = round((parcelas_s_impostos[i] *100)/(100-total_impostos), 3)
            valor_c_imposto = round(valor_s_impostos / ((100 - total_impostos) / 100), 3)
            vetor_parcelas.append(str(valor_s_impostos).replace('.', ','))
            vetor_parcelas.append(str(valor_c_imposto).replace('.', ','))

        return vetor_parcelas

    def calcula_s_imposto_parcela(self, icms, pis, confis, parcelas_c_impostos):
        total_impostos = icms+pis+confis
        vetor_parcelas = []

        for i in range(0, len(parcelas_c_impostos)):
            valor_c_impostos = float(parcelas_c_impostos[i].replace(',', '.'))
            #valor_s_impostos = round(valor_c_impostos * (valor_c_impostos*(total_impostos/100)), 3)
            valor_s_impostos = round(valor_c_impostos * ((100 - total_impostos) / 100), 3)
            vetor_parcelas.append(str(valor_s_impostos).replace('.', ','))
            vetor_parcelas.append(str(valor_c_impostos).replace('.', ','))

        return vetor_parcelas

    def soma_listas(self, vetor_1, vetor_2):#AS LISTAS DEVEM POSSUIR OS MESMO TAMANHO E POSSUIREM ALGUM TIPO DE RELAÇÃO
        vetor_soma = []
        for i in range(0, len(vetor_1)):
            aux1 = float(vetor_1[i].replace(',', '.'))
            aux2 = float(vetor_2[i].replace(',', '.'))
            vetor_soma.append(str(aux1+aux2).replace('.', ','))
        return vetor_soma

    def remove_string_acima(self, faixa):#REMOVE A STRING 'ACIMA' DE UMA FAIXA DE VALORES SUBSTITUINDO A STRING PELO DOBRO DA PRIMEIRA FAIXA. Ex: '60.001 acima' vai ser igual a '60.001 a 120.002'
        fxa_ini = ''
        for char in faixa:
            if char.isdigit():
                fxa_ini += char

        return faixa.replace('acima', 'a {}'.format(int(fxa_ini) * 2))