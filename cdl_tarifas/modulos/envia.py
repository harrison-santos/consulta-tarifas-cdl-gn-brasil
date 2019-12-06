from datetime import date
import csv


def envia_dados(dados, nome_empresa, segmento, subsegmento, reducao):
    print('ENVIA DADOS FOI CHAMADO')
    print(dados)
    data_atual = date.today()
    data_atual = data_atual.strftime('%d/%m/%Y')
    volume_acumulado = 0
    fat_acumulado = 0
    fxa_igual = "VERDADEIRO"
    fxa_uni = "NAO"
    #parcela_fxa = "NAO"



    for i in range(0, len(dados), 1):  # percorrer dados pegando sempre o valor de faixa
        if str(dados[i][4]) != '0' or str(dados[i][5]) != '0':
            parcela_fxa = "SIM"
        if 'a' or 'à' in dados[i][1]:  # se possuir algum tipo de divisor entre as faixas #ISDIGIT()
            print('dados : {}'.format(dados))
            if 'a' in dados[i][1]:
                valor = dados[i][1].split('a')  # ['1 a 70'] com split-> ['1', '70']
                print('VALOR: {}'.format(valor))
            elif 'à' in dados[i][1]:
                valor = dados[i][1].split('à')
                print('VALOR: {}'.format(valor))

            # arredondamento de valores
            valor[0] = round(float(valor[0].replace(',01', '').replace(',00', '')))
            valor[1] = round(float(valor[1].replace(',01', '').replace(',00', '')))

            if int(valor[0]) % 2 != 0:
                valor[0] = int(valor[0]) - 1

            # Na última faixa o valor de "FXA_FIM" vai ser igual ao dobro de "FXA_INI"
            if (str(valor[0]) != "0" and "999999999" in str(valor[1]) or "9999999" in str(
                    valor[1]) or "999999" in str(
                valor[1])):
                valor[1] = str(int(valor[0]) * 2)

            if (str(valor[0]) == "0" and "999999999" in str(valor[1]) or "99999999" in str(
                    valor[1]) or "9999999" in str(valor[1])):
                valor[1] = "0"

            if (len(dados) == 1 and str(valor[0]) == "0" and str(valor[1]) == "0"):
                fxa_uni = "SIM"
            else:
                fxa_uni = "NAO"

            valor[0] = int(valor[0])
            valor[1] = int(valor[1])

            ###VERIFICANDO SE O INICIO DA PRÓXIMA FAIXA É IGUAL AO FINAL DA FAIXA ANTERIOR
            if (i != 0):
                fxa_anterior = dados[i - 1][1]  # dados na posicao anterior. Ex: '1 a 70'
                if ('a' in fxa_anterior):
                    valor2 = int(fxa_anterior.replace(',01', '').replace(',00', '').replace('.', '').split('a')[1])
                    if (valor[0] == valor2):
                        fxa_igual = "VERDADEIRO"
                    else:
                        valor[0] = valor2
                        if (valor[0] == valor2):
                            fxa_igual = "VERDADEIRO"


                elif ('à' in fxa_anterior):
                    valor2 = int(fxa_anterior.replace(',01', '').replace(',00', '').replace('.', '').split('à')[1])
                    if (valor[0] == valor2):
                        fxa_igual = "VERDADEIRO"
                    else:
                        valor[0] = valor2
                        if (valor[0] == valor2):
                            fxa_igual = "VERDADEIRO"
                ###VERFIM

            volume = valor[1] - valor[0]
            tarifa = float(dados[i][2].replace(',', '.'))
            fat_fxo = str(round(volume * tarifa, 2)).replace('.', ',')

            if (i == 0):
                volume_acumulado = volume
                fat_acumulado = fat_fxo
                if (volume_acumulado != 0):
                    tarifa_media = str(round(float(fat_acumulado.replace(',', '.')) / volume_acumulado, 4)).replace(
                        '.',
                        ',')
                else:
                    tarifa_media = str(round(tarifa, 4)).replace('.', ',')
            else:
                volume_acumulado += volume  # VOLUME ATUAL + VOLUME ANTERIOR
                fat_acumulado = str(
                    float(fat_acumulado.replace(',', '.')) + float(fat_fxo.replace(',', '.'))).replace(
                    '.', ',')
                tarifa_media = str(round(float(fat_acumulado.replace(',', '.')) / volume_acumulado, 4)).replace('.',
                                                                                                                ',')

            yield {  # Para cada valor envie as mesma informações.
                "DTA_CST": data_atual,
                "COD_CDL": nome_empresa,
                "NME_SEG": segmento,
                "NME_SBSEG": subsegmento,
                "FXA_INI": valor[0],
                "FXA_FIM": valor[1],
                "FXA_UNI": fxa_uni,
                "FXA_IGUAL": fxa_igual,
                "TAR_SIM": dados[i][2],
                "VOL_FXA": volume,
                "VOL_ACU": volume_acumulado,
                "FAT_FXA": fat_fxo,
                "FAT_ACU": fat_acumulado,
                "TAR_MED": tarifa_media
            }

            #Escrevendo no CSV
            with open('C:\consulta-tarifas-cdl-gn-brasil\dados_teste.csv', mode='a') as csv_file:
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([data_atual, nome_empresa, segmento, subsegmento, valor[0], valor[1], fxa_uni, fxa_igual, dados[i][2],
                                 volume, volume_acumulado, fat_fxo, fat_acumulado, tarifa_media])