import flet as ft
import httpx
import asyncio  # Import asyncio for creating tasks

API_URL = "http://localhost:8000"

def main(page: ft.Page):
    page.title = "Cadastro de Clientes"
    nome = ft.TextField(label="Nome")
    email = ft.TextField(label="Email")
    clientes_list = ft.Column()

    async def listar():
        clientes_list.controls.clear()
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_URL}/clientes")
            for c in resp.json():
                clientes_list.controls.append(
                    ft.Row([
                        ft.Text(f"{c['id']} - {c['nome']} - {c['email']}"),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            on_click=lambda e, cid=c['id']: asyncio.run(deletar(cid))  # Use asyncio.run
                        )
                    ])
                )
            page.update()

    async def adicionar(e):
        async with httpx.AsyncClient() as client:
            await client.post(f"{API_URL}/clientes", json={"nome": nome.value, "email": email.value})
        await listar()

    async def deletar(id):
        async with httpx.AsyncClient() as client:
            await client.delete(f"{API_URL}/clientes/{id}")
        await listar()

    btn_add = ft.ElevatedButton("Adicionar", on_click=adicionar)
    page.add(nome, email, btn_add, ft.Divider(), clientes_list)
    page.on_load = lambda _: asyncio.run(listar())  # Use asyncio.run for page load

ft.app(target=main)