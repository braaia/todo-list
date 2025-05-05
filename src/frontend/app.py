import flet as ft

def first_view():
    return ft.Container(
        content=ft.Text("Você está na página First"),
        expand=True,
    )

def second_view():
    return ft.Container(
        content=ft.Text("Você está na página Second"),
        expand=True,
    )

def settings_view():
    return ft.Container(
        content=ft.Text("Você está na página Settings"),
        expand=True,
    )

def main(page: ft.Page):
    page.window.width = 800
    page.window.height = 600
    page.window.maximizable = False
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.scroll = ft.ScrollMode.ADAPTIVE

    views = {
        "/first": first_view,
        "/second": second_view,
        "/settings": settings_view,
    }

    # Gera a lista de rotas dinamicamente
    routes = list(views.keys())

    def route_handler(route):
        page.views.clear()

        # Obtém a view correspondente à rota atual ou exibe "Página não encontrada"
        content = views.get(route, lambda: ft.Container(content=ft.Text("Página não encontrada"), expand=True))()

        # Adiciona a nova view com o NavigationRail
        page.views.append(
            ft.View(
                route=route,
                controls=[
                    ft.Row(
                        [
                            ft.NavigationRail(
                                selected_index=routes.index(route) if route in routes else 0,
                                label_type=ft.NavigationRailLabelType.ALL,
                                destinations=[
                                    ft.NavigationRailDestination(
                                        icon=ft.Icons.HOME_OUTLINED,
                                        selected_icon=ft.Icons.HOME,
                                        label="Home",
                                        padding=ft.padding.only(0, 10, 0, 10)
                                    ),
                                    ft.NavigationRailDestination(
                                        icon=ft.Icons.BOOKMARK_BORDER,
                                        selected_icon=ft.Icons.BOOKMARK,
                                        label="Saveds",
                                    ),                                    
                                    ft.NavigationRailDestination(
                                        icon=ft.Icons.SETTINGS_OUTLINED,
                                        selected_icon=ft.Icons.SETTINGS,
                                        label="Settings",
                                        padding=ft.padding.only(0, 320, 0, 0)
                                    ),
                                ],
                                on_change=lambda e: page.go(routes[e.control.selected_index]),
                            ),
                            ft.VerticalDivider(width=1),
                            content,  # Adiciona o conteúdo da view
                        ],
                        expand=True,
                    )
                ],
            )
        )
        page.update()

    # Configura o evento de mudança de rota
    page.on_route_change = lambda e: route_handler(e.route)

    # Define a rota inicial
    page.go(page.route or "/")

ft.app(target=main)