import flet as ft
import module 
import sys
import time
import datetime
import pytz
#import pandas as pd 

def main(page: ft.Page):   
    page.theme = ft.Theme(color_scheme_seed="green")
    time.sleep(0.4)
    #global
    page.title = "Monaba"
    version = "1.2.9"
    USER = ft.TextField(label="ユーザーID")
    PASS = ft.TextField(label="パスワード", password=True, can_reveal_password=True)
    ERROR = ft.Text("",color='RED')
    SETTING = {'USER':None,'PASS':None,'MOBILE':None,'ISSAVE':False}
    temp ={'USER':None,'PASS':None}
    last_update_time = None

    if page.platform_brightness.name == "DARK":
            Color = ft.colors.with_opacity(0.05, "#007000")
            Bgcolor = ft.colors.with_opacity(1.00, "#001800")
            N1color = ft.colors.with_opacity(1.00, "#6AE860")
            N2color = ft.colors.with_opacity(1.00, "#002300")
            strcolor = ft.colors.with_opacity(1.00, "#FFFFFF")
    else:
        Color = ft.colors.GREEN_50
        Bgcolor = ft.colors.GREEN_100
        N1color="green_accent_700",
        N2color = ft.colors.GREEN_100
        strcolor = ft.colors.with_opacity(1.00, "#000000")

    dlg_title=ft.Text("")
    dlg_modal = ft.AlertDialog(
                                modal=True,
                                title=dlg_title,
                                content= ft.ProgressBar(width=400, color=N1color, bgcolor=ft.colors.GREEN_50,),
                                bgcolor=N2color
                                ) 
    Userdata = None
    detail = None
    
    def reload():
        #再読み込み対策
        time.sleep(0.2)
        page.views.clear()
        load_setting()
        page.views.append(create_setting())
        page.update()
        
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
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE_OUTLINED,selected_icon=ft.icons.EXPLORE,label="task"),
            ft.NavigationBarDestination(icon=ft.icons.SETTINGS_OUTLINED,selected_icon=ft.icons.SETTINGS,label="setting"),
                    ],
        bgcolor=Bgcolor,
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
            e.control.disabled == True
            page.update()
            reload()
            e.control.disabled == False
            page.update()
        else:
            time.sleep(0.2)
            page.views.clear()
            load_setting()
            page.views.append(create_home())
            page.update()

    CHECKBOX = ft.Checkbox(label="   モバイル表示", value=SETTING['MOBILE'],on_change=mobile_change)

    def create_home():      
        nonlocal SETTING
        layout = [
                    ft.Column([
                    ft.Text(""),
                    ft.Text(""),
                    ft.Row([ft.Image(src=f"/icons/icon-512.png",width=50,height=50),
                            ft.Text(value="Monaba", color="green",size=40,weight="BOLD"),ft.Text("          ")],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(content=ft.Text("manabaから未提出課題を出力します"),margin=15,alignment=ft.alignment.center),
                    ft.Row([ERROR],alignment=ft.MainAxisAlignment.CENTER),     
                    ft.Row([USER],alignment=ft.MainAxisAlignment.CENTER), 
                    ft.Row([PASS],alignment=ft.MainAxisAlignment.CENTER),      
                    ft.Row([CHECKBOX,ft.ElevatedButton("ログイン", on_click=login_clicked)],alignment=ft.MainAxisAlignment.CENTER),     
                    ft.Row([ft.Text(value=f"                                              platform: {page.platform.value}  ver.{version}")],alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Text(""),
                    ft.Container(content=ft.Text("本アプリはmanabaのUI調整を行ったり、自動ログインを実装することでスマートフォンでも快適に使えるようにすることを目標に作られました\n現在、千葉工業大学のみ対応しています",width=500),
                    margin=15,alignment=ft.alignment.center),
                    ft.Row([ft.Text("contact:erde.ena15@gmail.com"),],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text(""),
                    ft.Row([ft.Text("© erde.ena15  2024")],alignment=ft.MainAxisAlignment.CENTER), 
                    ])     
                 ]
        return ft.View("/",layout,scroll = "HIDDEN")
    
 #ft.Row([],alignment=ft.MainAxisAlignment.CENTER),
  
    def login_clicked(e):            
        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        nonlocal SETTING 
        page.update()
        if SETTING["USER"] and SETTING["ISSAVE"] == True:
           USER.value = SETTING["USER"] 
           PASS.value = SETTING["PASS"]
        nonlocal Userdata
        Userdata = module.manaba.manaba_tool(USER.value,PASS.value)
        #print(id(Userdata))
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
    
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Enter":
            login_clicked(e)

    page.on_keyboard_event = on_keyboard

    def create_task():      
        dt_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        str = dt_now.strftime('この内容は%Y年%m月%d日 %H:%M:%Sに取得された情報です\n内容が古い場合は右の更新ボタンを押してください')
        update_snack_bar = ft.SnackBar(ft.Text("時間を置いてお試しください",color = strcolor),bgcolor = N2color)

        if page.platform_brightness.name == "DARK":
            Color = ft.colors.with_opacity(0.05, "#007000")
            Bgcolor = ft.colors.with_opacity(1.00, "#001800")
        else:
            Color = ft.colors.GREEN_50
            Bgcolor = ft.colors.GREEN_100
        Navi.bgcolor = Bgcolor

        def button_clicked(e):
            total_seconds = 0
            nonlocal last_update_time
            now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            if last_update_time == None:
                page.views.clear()
                PAGE=create_task()
                page.views.append(PAGE)
                page.update()
                last_update_time = now
                return
            elif now.date() != last_update_time.date():
                total_seconds = 86400
            total_seconds = total_seconds + now.hour * 3600 + now.minute * 60 + now.second
            last_total_seconds = last_update_time.hour * 3600 + last_update_time.minute * 60 + last_update_time.second
            if total_seconds - last_total_seconds < 5:
                update_snack_bar.open = True
                page.update()
                return
            else:
                try:
                    if busy == True:
                        return #連打対策
                except NameError:
                    busy = True
                    page.views.clear()
                    PAGE=create_task()
                    page.views.append(PAGE)
                    page.update()
                    last_update_time = now
        
        update_button = ft.IconButton(icon=ft.icons.AUTORENEW, on_click=button_clicked)

        def get_detail(e):
            dlg_title.value = "loading"
            page.overlay.append(dlg_modal)
            dlg_modal.open = True
            search = e.control.data
            nonlocal detail
            detail = Userdata.scraping_detail(number=search)
            dlg_modal.open = False
            if detail == -1:
                ERROR.value = "セッション切れのため再ログインが必要です"
                page.go("/")
            else:
                page.go("/detail")

        try:
            X = Userdata.reload_data()
            if X == -1:
                ERROR.value = "セッション切れのため再ログインが必要です"
                page.go("/")
        except NameError:
            print("データ取得中")
            X = Userdata.scraping_manaba()

        nonlocal SETTING 
        ROWS = []
        
        if SETTING['MOBILE'] == True:
            if X == None:
                layout = [ 
                        ft.AppBar(title = ft.Text("未提出課題"), bgcolor=Bgcolor),ft.Text(""),ft.Text(""),
                        ft.Container(ft.Row([ft.Text(str,size=11,width=280),update_button],spacing=0,alignment=ft.MainAxisAlignment.CENTER),margin=8),
                        ft.Row([ft.Container(content=ft.Text("未提出課題はありません( ´∀｀)b",width=250),margin=15,alignment=ft.alignment.center,
                                             padding=15,bgcolor=Color,border_radius=10,width=250)],alignment=ft.MainAxisAlignment.CENTER),
                                             update_snack_bar,Navi]
            else:
                for D in range(len(X[0])):
                    tit = ft.DataCell(ft.Text(f"{X[1][D]}",size=11,weight="BOLD"),on_tap=get_detail,data=D)
                    CELLS = [
                                tit,
                                ft.DataCell(ft.Text(f"{X[2][D]}",size=11,weight="BOLD")),
                                ft.DataCell(ft.Text(f"{X[4][D]}",size=11,weight="BOLD")),
                            ]               
                    ROWS.append(ft.DataRow(cells = CELLS))
                layout = [                    
                        ft.AppBar(title = ft.Text("未提出課題"), bgcolor=Bgcolor),    
                        ft.Container(ft.Row([ft.Text(str,size=11,width=280),update_button],spacing=0),margin=8,),
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
                        update_snack_bar,
                        Navi,                
                    ]
        else:
            if X == None:
                layout = [ 
                        ft.AppBar(title = ft.Text("未提出課題"), bgcolor=Bgcolor),ft.Text(""),ft.Text(""),
                        ft.Container(ft.Row([ft.Text(str,width=385),update_button],alignment=ft.MainAxisAlignment.CENTER),margin=10),
                        ft.Row([ft.Container(content=ft.Text("未提出課題はありません( ´∀｀)b",width=250),margin=15,alignment=ft.alignment.center,
                                             padding=15,bgcolor=Color,border_radius=10,width=250)],alignment=ft.MainAxisAlignment.CENTER),
                                             update_snack_bar,Navi]
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
                            ft.AppBar(title = ft.Text("未提出課題"), bgcolor=Bgcolor),                       
                            ft.Container(ft.Row([ft.Text(str),update_button],alignment=ft.MainAxisAlignment.CENTER),margin=10,),
                            ft.Row([
                                        ft.DataTable(
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
                            update_snack_bar,Navi,               
                        ]
        return ft.View("/task",layout,scroll = "HIDDEN") 

    def create_loading():
        return ft.View("/loading")
    
    def create_setting():      
        nonlocal SETTING
        def auto_login_change(e):
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
            e.control.disabled == True
            page.update()
            reload()
            e.control.disabled == False
            page.update()
        
        auto_login_switch = ft.Switch(label="自動ログイン", value=SETTING['ISSAVE'],on_change=auto_login_change)
        
        if page.platform_brightness.name == "DARK":
            Bgcolor = ft.colors.with_opacity(1.00, "#001800")
        else:
            Bgcolor = ft.colors.GREEN_100
        Navi.bgcolor = Bgcolor
        log = "v1.2.9 : バグを修正\nv1.2.8 : 取得時間確認機能と更新ボタン追加\nv1.2.0 : 詳細内容表示機能追加\nv1.1.0 : 自動ログイン追加\nv1.0.0 : 初期ビルド"
        ab = f"ver.{version}\nplatform: {page.platform.value}\ncontact:erde.ena15@gmail.com"
        
        layout = [
                    ft.AppBar(title = ft.Text("設定"), bgcolor=Bgcolor), 
                    ft.Text(""),
                    ft.Row([auto_login_switch,ft.Text(""),ft.Text(""),ft.Text("")],alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Row([ft.Text("         ログイン情報を端末のローカルに保存します",size=12),ft.Text("")],alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Row([CHECKBOX,ft.Text(""),ft.Text(""),ft.Text("")],alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Text(""),ft.Text(""),
                    ft.Text(""),ft.Text(""),
                    ft.Row([ft.Text("-------------About-------------"),ft.Text("")],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text(""),
                    ft.Row([ft.Text(ab)],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text(""),
                    ft.Row([ft.Text("-------------Changelog-------------"),ft.Text("")],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.Text(log)],alignment=ft.MainAxisAlignment.CENTER),
                    Navi,              
                    ]
        return ft.View("/setting",layout,scroll = "HIDDEN")
    
    def create_detail():      
        if page.platform_brightness.name == "DARK":
            Bgcolor = ft.colors.with_opacity(1.00, "#001800")
        else:
            Bgcolor = ft.colors.GREEN_100
        Navi.bgcolor = Bgcolor
        
        def task_button(e):
            page.go("/task")
        
        if page.platform_brightness.name == "DARK":
            color = ft.colors.with_opacity(0.05, "#006000")
        else:
            color = ft.colors.GREEN_50

        if SETTING['MOBILE'] == True:
            
            layout = [
                    ft.AppBar(title = ft.Text("詳細内容"), bgcolor=Bgcolor), 
                    ft.Column([ ft.Text(""),
                                ft.Container(
                                            content=ft.Text(value=detail),
                                            margin=2,
                                            padding=15,
                                            bgcolor=color,
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
                    ft.AppBar(title = ft.Text("詳細内容"), bgcolor=Bgcolor), 
                    ft.Column([ ft.Text(""),
                                ft.Row([ft.Container(
                                            content=ft.Text(value=detail),
                                            margin=2,
                                            padding=15,
                                            bgcolor=color,
                                            alignment=ft.alignment.center,
                                            border_radius=10
                                            )],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([ft.ElevatedButton("戻る", on_click=task_button)],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Text("")],
                    spacing=15),
                    Navi,   
                    ]
        return ft.View("/detail",layout,scroll = "HIDDEN")
    

    def route_change(route):
        page.views.clear()
        load_setting()
        nonlocal SETTING
        if page.route == "/":
            if SETTING["USER"] and SETTING["PASS"] and SETTING['ISSAVE']==True:  
                print('自動ログインを実行')
                dlg_title.value = "loading"
                page.go("/loading")
                A = login_clicked(None)
                #自動ログインに失敗したら,保存されている値を削除
                if A == -1 or A == -2:
                    page.client_storage.remove("SaveUser")
                    page.client_storage.remove("SavePass")
                return
            dlg_title.value = "ログイン中です"
            page.views.append(create_home())      
        if page.route == "/loading": #ダイアログが表示されない場合
             page.views.append(create_loading()) #pageがない場合必要かも？(自動ログイン時等)
             page.overlay.append(dlg_modal)
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
    
ft.app(target=main,view=ft.AppView.WEB_BROWSER,assets_dir="assets")
