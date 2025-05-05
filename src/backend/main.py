from fastapi import FastAPI, HTTPException
from .schemas import ClienteIn, ClienteOut
from . import models, database

app = FastAPI()

@app.on_event("startup")
def startup():
    database.init_db()

@app.post("/clientes", response_model=ClienteOut)
def criar(cliente: ClienteIn):
    return models.criar_cliente(cliente.nome, cliente.email)

@app.get("/clientes", response_model=list[ClienteOut])
def listar():
    return models.listar_clientes()

@app.put("/clientes/{id}", response_model=ClienteOut)
def editar(id: int, cliente: ClienteIn):
    sucesso = models.atualizar_cliente(id, cliente.nome, cliente.email)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return ClienteOut(id=id, nome=cliente.nome, email=cliente.email)

@app.delete("/clientes/{id}")
def remover(id: int):
    models.deletar_cliente(id)
    return {"ok": True}
