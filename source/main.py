import flet as ft
import module.manaba as ma
import pandas as pd 
from IPython.display import display

#default値
save = "1"
folder = None

def main(page: ft.Page):
    page.title = "Routes Example"
    
    USER = ft.TextField(label="ユーザーID")
    PASS = ft.TextField(label="パスワード", password=True, can_reveal_password=True)
    data = {}
    #errorT = ""
    #error = ft.Text(value=f"{errorT}")
    

    def create_home():      
        layout = [
                    ft.Text(value="Manaba-Scheduler", color="green",size=40),
                    ft.Text(value="manabaから未提出課題を出力します"),
                    #error,
                    USER,
                    PASS,
                    ft.AppBar(title=ft.Text("Manaba-Scheduler"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("ログイン", on_click=clicked),                      
                 ]
        return ft.View("/",layout)  
    
    def clicked(e):        
        #data = ma.scraping_manaba(save,USER.value,PASS.value,folder)
        #if not data == None :
            #df = pd.DataFrame(data)
            #display(df)
            page.go("/view1")
        #else:
            #error = "ユーザIDまたはパスワードが間違っています。"
            #page.update()
    
    def create_view1():      
        #print(data)
        data = ma.scraping_manaba(save,USER.value,PASS.value,folder)
        ROWS = []
        for D in range(len(data['タイプ'])):
            CELLS = [
                        ft.DataCell(ft.Text(f"{data['タイプ'][D]}")),
                        ft.DataCell(ft.Text(f"{data['タイトル'][D]}")),
                        ft.DataCell(ft.Text(f"{data['開始日'][D]}")),
                        ft.DataCell(ft.Text(f"{data['終了日'][D]}")),
                    ]       
            ROWS.append(ft.DataRow(cells = CELLS))
            
        layout = [                    
                    ft.AppBar(title=ft.Text("未提出課題"), bgcolor=ft.colors.SURFACE_VARIANT),

                    ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("タイプ")),
                                ft.DataColumn(ft.Text("タイトル")),
                                ft.DataColumn(ft.Text("開始日")),
                                ft.DataColumn(ft.Text("終了日")),
                                    ],
                            rows= ROWS,
                                ),
                    ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),               
                 ]
        print(f"{ROWS}")
        return ft.View("/view1",layout)  

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(create_home())    
        if page.route == "/view1":
            page.views.append(create_view1())
        page.update()
   
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
ft.app(target=main,view=ft.AppView.WEB_BROWSER)