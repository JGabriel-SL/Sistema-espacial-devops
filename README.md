# Documentação

Membros da equipe:

- Alex Custodio Rabelo Gomes - 2516112
- Luis Henrique Lima Santos - 2527800
- João Gabriel de Souza Lima - 2516625

- Endereço da aplicação: http://127.0.0.1:5000/

Para criar o ambiente virtual:

```
python -m venv env    
```

Para executar o ambiente virtual:
```
.\env\Scripts\activate.bat
```

Para instalar as dependências:

```
pip install -r requiriments.txt
```

Para iniciar a aplicação é necessário usar o seguinte comando:

```
python app.py
```

## Rotas para requisição

### GET - /view_missions

- Retorna todas as missões espaciais, ordenadas por data de lançamento, da mais recente para a mais antiga.

**Body:** Nenhum

### POST - /view_mission 

- Retorna uma missão selecionada por ID.

**Body:** (JSON)

Exemplo:
```json
{
    "id": 1
}
```

### POST - /view_missions_per_date 

- Retorna as missões em um determinado período de tempo. Filtrado pelo campo launch_date (data de lançamento).

**Body:** (JSON)

Exemplo:
```json
{
  "date_start": "01/01/2024",
  "date_end": "07/07/2024"
}
```

### POST  - /create_mission

- Cria uma nova missão.

Exemplo:
```json
{
  "name": "Quinta Missao",
  "launch_date": "03/07/2024",
  "destination": "Jupiter",
  "status": "Ativo",
  "tripulation": "Wesley, Tiago",
  "util_charge": "nenhuma",
  "duration": "1800",
  "cost": "1500",
  "status_descr": "Tudo normal"
}
```

### PUT  - /update_mission

- Atualiza uma missão já existente por ID.

Exemplo:
```json
{
  "id": "1",
  "name": "Decima Missao",
  "launch_date": "05/04/2024",
  "destination": "Jupiter",
  "status": "Ativo",
  "tripulation": "Wesley, Tiago",
  "util_charge": "nenhuma",
  "duration": "1800",
  "cost": "1500",
  "status_descr": "Tudo normal"
}
```

### DELETE  - /delete_mission

- Deleta uma missão por ID.

exemplo:
```json
{
  "id": 3
}
```
