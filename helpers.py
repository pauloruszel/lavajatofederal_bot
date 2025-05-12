import re

def normalizar_data_hora(raw: str) -> str:
    """
    Normaliza uma string de data e hora para o formato dd/mm HH:MM
    Exemplo: "12/05 as 15h" → "12/05 15:00"
    """
    texto = (
        raw.replace("ás", "às")
           .replace("as", "às")
           .replace("As", "às")
           .replace("às", "")
           .replace("h", ":")
    )
    texto = re.sub(r"\s+", " ", texto).strip()
    texto = re.sub(r":\s*$", "", texto)

    # Corrige hora com apenas H sem minutos (ex: 15 → 15:00)
    if re.match(r".*\s\d{1,2}$", texto):
        texto += ":00"

    return texto