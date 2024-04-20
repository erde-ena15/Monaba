import module.manaba as ma
from IPython.display import display
import pandas as pd 
import os
import tkinter.filedialog

#default値
save = "1"
string = "なし"
folder = None

while True:
    print("----------Manaba-Scheduler_CUI ver.0.9----------")
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
            data = ma.scraping_manaba(save,folder)
            if not data == None :
              df = pd.DataFrame(data)
              display(df)
            Continue = input("終了しますか?(y/n): ")
            if Continue == "n":
              continue
            break
        case "2":
            data = ma.scraping_manaba(save,folder)
            if not data == None :
              df = pd.DataFrame(data)
              filename ='未提出課題.csv'
              df.to_csv(filename, index = False)
            Continue = input("終了しますか?(y/n); ")
            if Continue == "n":
              continue
            break
        case "3":
            data = ma.scraping_manaba(save,folder)
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
            data = ma.scraping_manaba(save,folder)
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
                    save = input("1.なし/2.端末に保存 ")
                    match save:
                         case "1":
                             string = "なし"
                         case "2":                           
                             iDir = os.path.expanduser('~')
                             folder = tkinter.filedialog.askdirectory(initialdir=iDir)
                             print(folder)
                             if folder == "":
                               continue
                             string = "端末に保存 保存先:" + folder                             
                         #case "3":
                             #string = "googleドライブに保存"
                         case _:
                             print('存在しないオプションです')
                case "2":
                    pass
                case _:
                    print('存在しないオプションです')

        case _:
            print('存在しないオプションです')
