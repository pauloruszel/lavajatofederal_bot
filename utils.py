import csv
import os

def salvar_agendamento(dados):
    with open('agendamentos_lavajato.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            dados['nome'],
            dados['telefone'],
            dados['tipo_lavagem'],
            dados['data_horario']
        ])

def carregar_agendamentos():
    if not os.path.exists('agendamentos_lavajato.csv'):
        return []
    agendamentos = []
    with open('agendamentos_lavajato.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            agendamentos.append({
                "nome": row[0],
                "telefone": row[1],
                "tipo_lavagem": row[2],
                "data_horario": row[3]
            })
    return agendamentos