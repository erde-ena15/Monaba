import flet as ft
import module 

#import pandas as pd 
#from IPython.display import display

#default値
save = "1"
folder = None

def main(page: ft.Page):   
    page.title = "Routes Example"
    USER = ft.TextField(label="ユーザーID")
    PASS = ft.TextField(label="パスワード", password=True, can_reveal_password=True)
    
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
        page.go("/view1")
        #data = ma.scraping_manaba(save,USER.value,PASS.value,folder)
        #print(type(data))
        #if not data == None :
            #df = pd.DataFrame(data)
            #display(df)
            
        #else:
            #error = "ユーザIDまたはパスワードが間違っています。"
            #page.update()
    
    def create_view1():      
        Userdata = module.manaba.manaba_tool(USER.value,PASS.value)
        X = Userdata.scraping_manaba()
        #print(type(X))
        #data = module.manaba.scraping_manaba(save,USER.value,PASS.value,folder)
       # print(data)
       # print(type(data[0]))
        #print(f"{data.scraping_manaba()[0][1]}")
       # print(type(data['開始日'][1]))
        #print(type(data['終了日'][1]))
        
        ROWS = []
        for D in range(len(X[0])):
            CELLS = [
                        ft.DataCell(ft.Text(f"{X[0][D]}")),
                        ft.DataCell(ft.Text(f"{X[1][D]}")),
                        ft.DataCell(ft.Text(f"{X[2][D]}")),
                        ft.DataCell(ft.Text(f"{X[3][D]}")),
                    ]               
            ROWS.append(ft.DataRow(cells = CELLS))
           
        layout = [                    
                    ft.AppBar(title=ft.Text("未提出課題"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.Text(f"{X[0][0]}"),           
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
    
ft.app(target=main)
