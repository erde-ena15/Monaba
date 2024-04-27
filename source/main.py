#import sys
#sys.path.append('C:\Users\kenta\Documents\GitHub\Manaba-Scheduler\source\module')
#sys.path.append('C:\\Users\\kenta\\AppData\\Local\\Temp\\serious_python*')

import flet as ft
from module import manaba as ma
#import pandas as pd 
#from IPython.display import display

#default値
save = "1"
folder = None

def main(page: ft.Page):
    page.title = "Routes Example"
    a = [["aaa","bbb"],["ccc","ddd"]]
    USER = ft.TextField(label="ユーザーID")
    PASS = ft.TextField(label="パスワード", password=True, can_reveal_password=True)
    
    #errorT = ""
    #error = ft.Text(value=f"{errorT}")
    

    def create_home():      
        layout = [
                    ft.Text(value="Manaba-Scheduler", color="green",size=40),
                    ft.Text(value="manabaから未提出課題を出力します"),
                    ft.Text(f"{a[1][0]}"),
                    #error,
                    USER,
                    PASS,
                    ft.AppBar(title=ft.Text("Manaba-Scheduler"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("ログイン", on_click=clicked),                      
                 ]
        return ft.View("/",layout)  
    
    def clicked(e):        
        page.go("/view1")
        data = ma.scraping_manaba(save,USER.value,PASS.value,folder)
        #print(type(data))
        #if not data == None :
            #df = pd.DataFrame(data)
            #display(df)
            
        #else:
            #error = "ユーザIDまたはパスワードが間違っています。"
            #page.update()
    
    def create_view1():      
        aaa = {"a":{"x":1, "y":55555}, "b":2, "c":3}

       
        data = ma.scraping_manaba(save,USER.value,PASS.value,folder)
        #print(data)
        #print(type(data['タイプ']))
        #print(type(data['タイプ'][1]))
       # print(type(data['開始日'][1]))
        #print(type(data['終了日'][1]))
        '''
        ROWS = []
        #for D in range(len(data['タイプ'])):
        CELLS = [
                    ft.DataCell(ft.Text(f"{data['タイプ'][1]}")),
                    ft.DataCell(ft.Text(f"{data['タイトル'][1]}")),
                    ft.DataCell(ft.Text(f"{data['開始日'][1]}")),
                    ft.DataCell(ft.Text(f"{data['終了日'][1]}")),
                ] 
         '''       '''      
        ROWS.append(ft.DataRow(cells = [
                    ft.DataCell(ft.Text(f"{data['タイプ'][1]}")),
                    ft.DataCell(ft.Text(f"{data['タイトル'][1]}")),
                    ft.DataCell(ft.Text(f"{data['開始日'][1]}")),
                    ft.DataCell(ft.Text(f"{data['終了日'][1]}")),
                ]))
         '''   
        layout = [                    
                    ft.AppBar(title=ft.Text("未提出課題"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.Text(ft.Text(f"{data[0][0]}")),           
                    ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("タイプ")),
                                ft.DataColumn(ft.Text("タイトル")),
                                ft.DataColumn(ft.Text("開始日")),
                                ft.DataColumn(ft.Text("終了日")),
                                    ],
                            rows= [ft.DataRow(cells = [
                    ft.DataCell(ft.Text("iiijg")),
                    ft.DataCell(ft.Text("てすと")),
                    ft.DataCell(ft.Text("テスト")),
                    ft.DataCell(ft.Text("1234/")),
                ])],
                                ),
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),               
                 ]


                    
                    
        
        #print(f"{ROWS}")
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



'''
                    
                    '''