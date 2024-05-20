import flet as ft
import module 
import sys
import time
#import pandas as pd 

def main(page: ft.Page):   
    page.theme = ft.Theme(color_scheme_seed="green")
    time.sleep(0.4)
    #global
    page.title = "Monaba"
    version = "1.2.3"
    USER = ft.TextField(label="ユーザーID")
    PASS = ft.TextField(label="パスワード", password=True, can_reveal_password=True)
    ERROR = ft.Text("",color='RED')
    SETTING = {'USER':None,'PASS':None,'MOBILE':None,'ISSAVE':False}
    temp ={'USER':None,'PASS':None}
    dlg_title=ft.Text("")
    dlg_modal = ft.AlertDialog(
                                modal=True,
                                title=dlg_title,
                                content= ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee"),
                                ) 
    
    Userdata = None
    detail = None

    def load_setting():
        nonlocal SETTING
        SETTING['USER'] = page.client_storage.get("SaveUser")    
        SETTING['PASS'] = page.client_storage.get("SavePass")
        SETTING['MOBILE'] = page.client_storage.get("Mobile")
        SETTING['ISSAVE'] = page.client_storage.get("IsSave")

    load_setting()
    if sys.platform == "linux" and SETTING['MOBILE'] == None:     
        SETTING['MOBILE'] = True
        page.client_storage.set("Mobile",SETTING['MOBILE'])

    def on_change_navi(e):
        if Navi.selected_index == 0:
            page.go("/task")
        if Navi.selected_index == 1:
            page.go("/setting")

    Navi=ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.EXPLORE_OUTLINED, 
                                    selected_icon=ft.icons.EXPLORE,
                                     label="task"),

            ft.NavigationDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon=ft.icons.SETTINGS,
                label="setting",
            ),
        ],
        on_change=on_change_navi
    ) 

    def mobile_change(e):
        nonlocal SETTING 
        if CHECKBOX.value == True:
            SETTING['MOBILE'] = True
        else:
            SETTING['MOBILE'] = False
        page.client_storage.set("Mobile",SETTING['MOBILE'])
        #再読み込み対策
        if not page.route == "/":
            time.sleep(0.2)
            page.views.clear()
            load_setting()
            page.views.append(create_setting())
            page.update()

    CHECKBOX = ft.Checkbox(label="   モバイル表示", value=SETTING['MOBILE'],on_change=mobile_change)
    
    def auto_login_change(e):
        nonlocal SETTING
        if auto_login_switch.value == True and temp["USER"]:
            SETTING['ISSAVE'] = True
            page.client_storage.set("SaveUser",temp["USER"]) 
            page.client_storage.set("SavePass",temp["PASS"])  
        else:
            SETTING['ISSAVE'] = False
            page.client_storage.remove("SaveUser")
            page.client_storage.remove("SavePass")
        page.client_storage.set("IsSave",SETTING['ISSAVE'])
        #再読み込み対策
        time.sleep(0.2)
        page.views.clear()
        load_setting()
        page.views.append(create_setting())
        page.update()
       
    auto_login_switch = ft.Switch(label="自動ログイン", value=SETTING['ISSAVE'],on_change=auto_login_change)
    
    def create_home():      
        nonlocal SETTING
        layout = [
                    ft.Text(""),
                    ft.Row([ft.Text(value="Monaba", color="green",size=40,weight="BOLD")],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.Text(value="manabaから未提出課題を出力します")],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([ERROR],alignment=ft.MainAxisAlignment.CENTER),     
                    ft.Row([USER],alignment=ft.MainAxisAlignment.CENTER), 
                    ft.Row([PASS],alignment=ft.MainAxisAlignment.CENTER),      
                    ft.Row([CHECKBOX,ft.ElevatedButton("ログイン", on_click=login_clicked)],alignment=ft.MainAxisAlignment.CENTER),     
                    ft.Row([ft.Text(value=f"                                              platform: {sys.platform}  ver.{version}")],alignment=ft.MainAxisAlignment.SPACE_AROUND)
                               
                 ]
        return ft.View("/",layout)
    
 #ft.Row([],alignment=ft.MainAxisAlignment.CENTER),
   
    def login_clicked(e):            
        page.dialog = dlg_modal
        dlg_modal.open = True
        nonlocal SETTING 
        page.update()
        if SETTING["USER"] and SETTING["ISSAVE"] == True:
           USER.value = SETTING["USER"] 
           PASS.value = SETTING["PASS"]
        nonlocal Userdata
        Userdata = module.manaba.manaba_tool(USER.value,PASS.value)
        print(id(Userdata))
        result = Userdata.login_manaba()
        if result == -1: 
            dlg_modal.open = False
            ERROR.value = "ユーザIDまたはパスワードが間違っています"
            if page.route == "/":
                page.update()
            else :
                page.go("/")
            return -1
        elif result == -2:
            dlg_modal.open = False
            ERROR.value = "その他のエラーです"
            if page.route == "/":
                page.update()
            else :
                page.go("/")
            return -2
        else:
            #ログイン情報の一時保存
            temp["USER"] = USER.value
            temp["PASS"] = PASS.value
            USER.value = None
            PASS.value = None
            ERROR.value = ""
            dlg_modal.open = False
            page.update()
            page.go("/task")
            
    def create_task():      
        
        def get_detail(e):
            search = e.control.data
            nonlocal detail
            detail = Userdata.scraping_detail(number=search)
            if detail == -1:
                ERROR.value = "セッション切れのため再ログインが必要です"
                page.go("/")
            else:
                page.go("/detail")

        print("データ取得中")
        X = Userdata.scraping_manaba()
        nonlocal SETTING 
        ROWS = []
        if SETTING['MOBILE'] == True:
            for D in range(len(X[0])):
                tit = ft.DataCell(ft.Text(f"{X[1][D]}",size=11,weight="BOLD"),on_tap=get_detail,data=D)
                CELLS = [
                            tit,
                            ft.DataCell(ft.Text(f"{X[2][D]}",size=11,weight="BOLD")),
                            ft.DataCell(ft.Text(f"{X[4][D]}",size=11,weight="BOLD")),
                        ]               
                ROWS.append(ft.DataRow(cells = CELLS))
            layout = [                    
                    ft.AppBar(title = ft.Text("未提出課題"), bgcolor=ft.colors.SURFACE_VARIANT),    
                    ft.Container(
                        ft.DataTable(
                                    border=ft.border.all(2, "green"),
                                    border_radius=10,
                                    data_row_max_height=55,
                                    column_spacing=5,
                                    horizontal_margin=1,
                                    vertical_lines = ft.border.BorderSide(1,"GREY"),
                                    columns = [
                                    ft.DataColumn(ft.Text("タイトル",size=20,)),
                                    ft.DataColumn(ft.Text("教科",size=20)),
                                    ft.DataColumn(ft.Text("終了日",size=20)),
                                            ],
                                    rows = ROWS,
                                    ),
                    margin=10,
                    ),
                    Navi,                
                 ]
        else:
            for D in range(len(X[0])):
                tit = ft.DataCell(ft.Text(f"{X[1][D]}"),on_tap=get_detail,data=D)
                CELLS = [
                            ft.DataCell(ft.Text(f"{X[0][D]}")),
                            tit,
                            ft.DataCell(ft.Text(f"{X[2][D]}")),
                            ft.DataCell(ft.Text(f"{X[3][D]}")),
                            ft.DataCell(ft.Text(f"{X[4][D]}")),
                        ]              
                ROWS.append(ft.DataRow(cells = CELLS))

            layout = [                    
                        ft.AppBar(title = ft.Text("未提出課題"), bgcolor=ft.colors.SURFACE_VARIANT),    
                        ft.Row([ft.DataTable(
                                    border=ft.border.all(2, "green"),
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
                                    )
                                ],alignment=ft.MainAxisAlignment.CENTER),                          
                        Navi,               
                    ]
            
        return ft.View("/task",layout,scroll = "ALWAYS") 

    def create_loading(e):
        return ft.View("/loading")
    
    def create_setting():      
        nonlocal SETTING
        layout = [
                    ft.AppBar(title = ft.Text("設定"), bgcolor=ft.colors.SURFACE_VARIANT), 
                    ft.Text(""),
                    ft.Row([auto_login_switch,ft.Text(""),ft.Text(""),ft.Text("")],alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Row([ft.Text("         ログイン情報を端末のローカルに保存します",size=12),ft.Text("")],alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Row([CHECKBOX,ft.Text(""),ft.Text(""),ft.Text("")],alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Text(""),ft.Text(""),
                    ft.Text(""),ft.Text(""),
                    ft.Row([ft.Text("-------------About-------------"),ft.Text("")],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text(""),
                    ft.Row([ft.Text(f"ver.{version}"),ft.Text(""),ft.Text("")],alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Row([ft.Text(value=f"  platform: {sys.platform}"),ft.Text(""),ft.Text("")],alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Row([ft.Text("       contact:erde.ena15@gmail.com"),ft.Text(""),ft.Text("")],alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    Navi,              
                    ]
        return ft.View("/setting",layout)
    
    def create_detail():      
        def task_button(e):
            page.go("/task")

        if SETTING['MOBILE'] == True:
            layout = [
                    ft.AppBar(title = ft.Text("詳細内容"), bgcolor=ft.colors.SURFACE_VARIANT), 
                    ft.Column([ft.Container(
                                            content=ft.Text(value=detail),
                                            margin=2,
                                            padding=15,
                                            bgcolor=ft.colors.GREEN_50,
                                            alignment=ft.alignment.center,
                                            border_radius=10
                                            ),
                                ft.Row([ft.ElevatedButton("戻る", on_click=task_button)],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Text("")],
                    spacing=15),
                    Navi,   
                    ]
        else:
            layout = [
                    ft.AppBar(title = ft.Text("詳細内容"), bgcolor=ft.colors.SURFACE_VARIANT), 
                    ft.Column([ft.Container(
                                            content=ft.Text(value=detail),
                                            margin=2,
                                            padding=15,
                                            bgcolor=ft.colors.GREEN_50,
                                            alignment=ft.alignment.center,
                                            border_radius=10
                                            ),
                                ft.Row([ft.ElevatedButton("戻る", on_click=task_button)],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Text("")],
                    spacing=15),
                    Navi,   
                    ]
        return ft.View("/detail",layout,scroll = "ALWAYS")

    def route_change(route):
        page.views.clear()
        load_setting()
        nonlocal SETTING
        if page.route == "/":
            if SETTING["USER"] and SETTING["PASS"] and SETTING['ISSAVE']==True:  
                print('自動ログインを実行')
                dlg_title.value = "自動ログイン中"
                page.go("/loading")
                A = login_clicked(None)
                #自動ログインに失敗したら,保存されている値を削除
                if A == -1 or A == -2:
                    page.client_storage.remove("SaveUser")
                    page.client_storage.remove("SavePass")
                return
            dlg_title.value = "ログイン中です"
            page.views.append(create_home())
            dlg_modal.open = False          
        if page.route == "/loading":
             page.views.append(create_loading())
             page.dialog = dlg_modal
             dlg_modal.open = True
        if page.route == "/task":
            if not Userdata:
                print("userdataが存在しません.トップに戻ります")
                page.go("/")
                return 
            if not Userdata.SOUP:
                print("resultが存在しません.トップに戻ります")
                page.go("/")
                return
            PAGE=create_task()
            while PAGE == None:
                time.sleep(0.4)
            dlg_modal.open = False
            Navi.selected_index = 0
            page.views.append(PAGE)
            print("データ取得完了")
        if page.route == "/setting":
            if not Userdata.SOUP:
                print("resultが存在しません.トップに戻ります")
                page.go("/")
                return
            Navi.selected_index = 1
            page.views.append(create_setting())
        if page.route == "/detail":
            PAGE=create_detail()
            while PAGE == None:
                time.sleep(0.4)
            dlg_modal.open = False
            page.views.append(PAGE)
        page.update()
 
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop #戻る操作時
    page.update()
    page.go(page.route)
    
ft.app(target=main,assets_dir="assets",name="Monaba")
