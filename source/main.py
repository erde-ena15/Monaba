import flet as ft
import module 
import sys
#import pandas as pd 

#default値
save = "1"
folder = None

def main(page: ft.Page):   
    page.title = "ManabaViewer"
    USER = ft.TextField(label="ユーザーID")
    PASS = ft.TextField(label="パスワード", password=True, can_reveal_password=True)
    ERROR = ft.Text("",color='RED')
    mobile = False
    
    def mobile_change(e):
        nonlocal mobile 
        if CHECKBOX.value == True:
            mobile = True
        else:
            mobile = False
       
    if sys.platform == "linux":
        mobile = True
    CHECKBOX = ft.Checkbox(label="モバイル表示", value=mobile,on_change=mobile_change) 
    result = None
    
    
    def create_home():      
        layout = [
                    ft.Text(""),
                    ft.Text(value="ManabaViewer", color="green",size=40,weight="BOLD"),
                    ft.Text(value="manabaから未提出課題を出力します"),
                    ERROR,
                    USER,
                    PASS,
                    ft.ElevatedButton("ログイン", on_click=login_clicked),
                    CHECKBOX,
                    ft.Text(value=f"platform: {sys.platform}"),                      
                 ]
        return ft.View("/",layout)  
    
    def login_clicked(e):        
        Userdata = module.manaba.manaba_tool(USER.value,PASS.value)
        nonlocal result
        result = Userdata.login_manaba()
        del Userdata
        if result == -1: 
          ERROR.value = "ユーザIDまたはパスワードが間違っています"
          page.update()
        elif result == -2:
          ERROR.value = "その他のエラーです"
          page.update()
        else:
          ERROR.value = ""
          page.update()
          page.go("/view1")
    
    

    def create_task():      
        Userdata = module.manaba.manaba_tool(None,None,result)
        X = Userdata.scraping_manaba()
        ROWS = []
        if mobile == True:
            for D in range(len(X[0])):
                CELLS = [
                            #ft.DataCell(ft.Text(f"{X[0][D]}")),
                            ft.DataCell(ft.Text(f"{X[1][D]}",size=11,weight="BOLD")),
                            ft.DataCell(ft.Text(f"{X[2][D]}",size=11,weight="BOLD")),
                            #ft.DataCell(ft.Text(f"{X[3][D]}")),
                            ft.DataCell(ft.Text(f"{X[4][D]}",size=11,weight="BOLD")),
                        ]               
                ROWS.append(ft.DataRow(cells = CELLS))
            layout = [                    
                    ft.AppBar(title = ft.Text("未提出課題"), bgcolor=ft.colors.SURFACE_VARIANT),    
                    ft.DataTable(
                                border=ft.border.all(2, "blue"),
                                border_radius=10,
                                data_row_max_height=55,
                                column_spacing=5,
                                horizontal_margin=1,
                                vertical_lines = ft.border.BorderSide(1,"GREY"),
                                columns = [
                                #ft.DataColumn(ft.Text("タイプ")),
                                ft.DataColumn(ft.Text("タイトル",size=20)),
                                ft.DataColumn(ft.Text("教科",size=20)),
                                #ft.DataColumn(ft.Text("開始日")),
                                ft.DataColumn(ft.Text("終了日",size=20)),
                                         ],
                                rows = ROWS,
                                ),                 
                    ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),               
                 ]
        else:
            for D in range(len(X[0])):
                CELLS = [
                            ft.DataCell(ft.Text(f"{X[0][D]}")),
                            ft.DataCell(ft.Text(f"{X[1][D]}")),
                            ft.DataCell(ft.Text(f"{X[2][D]}")),
                            ft.DataCell(ft.Text(f"{X[3][D]}")),
                            ft.DataCell(ft.Text(f"{X[4][D]}")),
                        ]               
                ROWS.append(ft.DataRow(cells = CELLS))
            layout = [                    
                        ft.AppBar(title = ft.Text("未提出課題"), bgcolor=ft.colors.SURFACE_VARIANT),    
                        ft.DataTable(
                                    border=ft.border.all(2, "blue"),
                                    border_radius=10,
                                    horizontal_margin = 10,
                                    vertical_lines = ft.border.BorderSide(1,"GREY"),
                                    columns = [
                                    ft.DataColumn(ft.Text("タイプ",size=20)),
                                    ft.DataColumn(ft.Text("タイトル",size=20)),
                                    ft.DataColumn(ft.Text("教科",size=20)),
                                    ft.DataColumn(ft.Text("開始日",size=20)),
                                    ft.DataColumn(ft.Text("終了日",size=20)),
                                            ],
                                    rows = ROWS,
                                    ),                 
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),               
                    ]
        return ft.View("/view1",layout,scroll = "ALWAYS")   

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(create_home())    
        if page.route == "/view1":
            page.views.append(create_task())
        page.update()
   
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    
ft.app(target=main)
