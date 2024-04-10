#from optparse import Option
#from tkinter import Y
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
from getpass import getpass
from IPython.display import display
import tkinter.filedialog
#import tkinter, tkinter.filedialog, tkinter.messagebox
#from google.colab import drive

#Load = 0でロード, =1でセーブ
def login_info_manager(Save,Load,User,Pass):
  match Save:
      case "1":
          pass
      case "2":
          match Load:
              case 0:
                  fTyp = [("","login_info.json")]
                  iDir = os.path.expanduser('~')
                  file_path = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
                  if os.path.exists(file_path) :
                    with open(file_path, mode ='r') as f :
                        login1 = json.load(f)
                        USER = login1['USER']
                        PASS = login1['PASS']
                        return USER,PASS
                  else :
                    print('ファイルが存在しない、もしくは見つかりません')
              case 1:               
                  login0 = {'USER': User, 'PASS': Pass}
                  path = folder + '/login_info.json'
                  with open(path, mode='w') as f:
                    json.dump(login0, f, ensure_ascii=False)
      case "3":  
          pass
  
  

def scraping_manaba():
 
   
  '''  
  root = tkinter.Tk()
  root.withdraw()
  fTyp = [("","*")]
  iDir = os.path.abspath(os.path.dirname(__file__))
  tkinter.messagebox.showinfo('○×プログラム','処理ファイルを選択してください！')
  file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
  



  # 処理ファイル名の出力
  tkinter.messagebox.showinfo('○×プログラム',file)
  '''
  
  



  #もし、ログイン情報があれば読み込む
  '''mount_path = '/content/drive'
  if not os.path.exists(mount_path) :
    drive.mount(mount_path)
  os.chdir('/content/drive/MyDrive')
  dir_path = 'manaba scheduler'
  os.makedirs(dir_path, exist_ok=True)
  os.chdir(dir_path)
  file_path = 'login_info.json'
  if os.path.exists(file_path) :
      with open(file_path, mode ='r') as f :
        login1 = json.load(f)
        USER = login1['USER']
        PASS = login1['PASS']
  else :'''
  login = login_info_manager(save,0,None,None)
  if not login == None:
    USER = login[0]
    PASS = login[1]
  else:
    USER = input('ユーザーIDを入力してください: ')
    PASS = getpass('パスワードを入力してください: ')

  url_login = "https://cit.manaba.jp/ct/login"
  session = requests.session()
  res = session.get(url_login)
  soup = BeautifulSoup(res.text, 'html.parser')
  SessionValue1 = soup.find(attrs={'name':'SessionValue1'}).get('value')
  cookie = res.cookies

  #ログイン情報
  login_info = {
    'userid':USER,
    'password':PASS,
    'login':"ログイン",
    "manaba-form":"1",
    "SessionValue1":SessionValue1
  }

  # post時にcookieを追加
  login = session.post(url_login, data=login_info, cookies=cookie)

  url_mytask = "https://cit.manaba.jp/ct/home_library_query"
  res = session.get(url_mytask)
  soup = BeautifulSoup(res.text, "html.parser")

  #ログインできたか確認
  error_text = 'default'
  error = soup.find('ul', class_ ='errmsg')
  if not error :
    pass
  else :
    error_text = error.text
  search_text = 'manabaの認証が必要です'
  if search_text in error_text :
    print('ユーザIDまたはパスワードが間違っています。')
    return
  else :
    #ログイン情報を保存
    login_info_manager(save,1,USER,PASS)
    
    #各要素取得
    types = soup.select('td[class="center"]') #部分一致のため
    titles = soup.find_all('div', class_='myassignments-title')
    subjects = soup.find_all('div', class_='mycourse-title')
    dates = soup.find_all('td', class_='center td-period')
    dates_start = []
    dates_finish = []
    for count, dat in enumerate(dates):
      if count % 2 == 0:
        dates_start.append(dat)
      else:
        dates_finish.append(dat)

    #タグなどを取り除く
    types_txt =[]
    for type_ in types:
      types_txt.append(type_.text)
    titles_txt = []
    for title in titles:
      titles_txt.append(title.text.replace('\n',''))
    subjects_txt =[]
    for subject in subjects:
      subjects_txt.append(subject.text)
    dates_start_txt=[]
    for date_s in dates_start:
      dates_start_txt.append(date_s.text)
    dates_finish_txt=[]
    for date_f in dates_finish:
      dates_finish_txt.append(date_f.text)

    #各要素を2次元配列にまとめる
    data = {}
    data['タイプ'] = types_txt
    data['タイトル'] = titles_txt
    data['教科'] = subjects_txt
    data['開始日'] = dates_start_txt
    data['終了日'] = dates_finish_txt

    return data

#以下実行部
save = "1"
string = "なし"

while True:
    print("----------Manaba-Scheduler ver.1.0----------")
    print('------動作モード------')
    print("1.表示のみ")
    print("2.新規csvを作成")
    print("3.既存csvを更新")
    print("4.差分csvを作成")
    print("5.オプション")
    print('----------------------')
    mode = input("動作モードの番号を入力してください: ")
    match mode:
        case "1":
            data = scraping_manaba()
            if not data == None :
              df = pd.DataFrame(data)
              display(df)
            Continue = input("終了しますか?(y/n): ")
            if Continue == "n":
              continue
            break
        case "2":
            data = scraping_manaba()
            if not data == None :
              df = pd.DataFrame(data)
              filename ='未提出課題.csv'
              df.to_csv(filename, index = False)
            Continue = input("終了しますか?(y/n); ")
            if Continue == "n":
              continue
            break
        case "3":
            data = scraping_manaba()
            if not data == None :
              #もし過去のファイルがあれば読み込む
              file_path = '未提出課題.csv'
              if os.path.exists(file_path) :
                data_old = pd.read_csv("未提出課題.csv")
                df_old = pd.DataFrame(data_old)
                df_old = df_old.fillna('') #ファイルのnanを空白化
                old = len(df_old)

                df = pd.DataFrame(data)
                #print(df_old.duplicated())
                df_old = pd.concat([df_old, df], ignore_index=True, axis=0)
                #print(df_old.duplicated())
                df_old.drop_duplicates(inplace=True, ignore_index=True)
                df_old.index = df_old.index + 1
                new = len(df_old)
                updated = new - old
                print("新規に追加された課題は%d個です" % (updated))
                filename ='未提出課題.csv'
                df_old.to_csv(filename, index = False)
              else :
                print('過去のファイルが存在しない、もしくは見つかりません')
            Continue = input("終了しますか?(y/n): ")
            if Continue == "n":
              continue
            break
        case "4":
            data = scraping_manaba()
            if not data == None :
              #もし過去のファイルがあれば読み込む
              file_path = '未提出課題.csv'
              if os.path.exists(file_path) :
                data_old = pd.read_csv("未提出課題.csv")
                df_old = pd.DataFrame(data_old)
                df_old = df_old.fillna('') #ファイルのnanを空白化

                df = pd.DataFrame(data)
                df_merged = pd.concat([df_old, df], ignore_index=True, axis=0)
                df_merged.drop_duplicates(inplace=True, ignore_index=True)
                diff = pd.concat([df_old, df]).drop_duplicates(keep=False)
                if not diff.empty: #差分があるか
                  #各差分を出力
                  diff_plus = pd.concat([df_merged, df_old]).drop_duplicates(keep=False, ignore_index=True)
                  diff_minus = pd.concat([df_merged, df]).drop_duplicates(keep=False, ignore_index=True)

                  if not diff_plus.empty:
                    if not diff_minus.empty: #両方
                      print("差分が見つかりました。")
                      filename ='未提出課題_追加差分.csv'
                      diff_plus.to_csv(filename, index=False)
                      print('追加された差分')
                      display(diff_plus)
                      filename ='未提出課題_削除差分.csv'
                      diff_minus.to_csv(filename, index=False)
                      print('削除された差分')
                      display(diff_minus)
                    else : #増えた差分のみ
                      filename ='未提出課題_追加差分.csv'
                      diff_plus.to_csv(filename, index=False)
                      print("追加された差分が見つかりました。")
                      display(diff_plus)
                  else : #減った差分のみ
                    filename ='未提出課題_削除差分.csv'
                    diff_minus.to_csv(filename, index=False)
                    print("削除された差分が見つかりました。")
                    display(diff_minus)
                else:
                  print("差分は見つかりませんでした。")
              else :
                print('過去のファイルが存在しない、もしくは見つかりません')
            Continue = input("終了しますか?(y/n)")
            if Continue == "n":
              continue    
            break
            
        case "5":
            
                    
            print("----オプション一覧----")
            print("1.ログイン情報の保存: %s" % (string))
            print("2.戻る")
            print('----------------------')
            option = input("変更したいオプションの番号を入力してください: ")
            match option:
                case "1":
                    save = input("1.なし/2.端末に保存/3.googleドライブに保存: ")
                    match save:
                         case "1":
                             string = "なし"
                         case "2":                           
                             iDir = os.path.expanduser('~')
                             folder = tkinter.filedialog.askdirectory(initialdir=iDir)
                             string = "端末に保存 保存先:" + folder
                             
                         case "3":
                             string = "googleドライブに保存"
                         case _:
                             print('存在しないオプションです')
                case "2":
                    pass
                case _:
                    print('存在しないオプションです')

        case _:
            print('存在しないオプションです')
