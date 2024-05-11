import requests 
from bs4 import BeautifulSoup 

if __name__ == "__main__":
  print("this ia a modlule")

class manaba_tool: 
  def __init__(self,User=None,Pass=None,Soup=None):
      self.USER = User
      self.PASS = Pass 
      self.SOUP = Soup

  def login_manaba(self):
    
    url_login = "https://cit.manaba.jp/ct/login"
    session = requests.session()
    res = session.get(url_login)
    soup = BeautifulSoup(res.text, 'html.parser')
    SessionValue1 = soup.find(attrs={'name':'SessionValue1'}).get('value')
    cookie = res.cookies

    #ログイン情報
    login_info = {
      'userid':self.USER,
      'password':self.PASS,
      'login':"ログイン",
      "manaba-form":"1",
      "SessionValue1":SessionValue1
    }

    # post時にcookieを追加
    login = session.post(url_login, data=login_info, cookies=cookie)

    url_mytask = "https://cit.manaba.jp/ct/home_library_query"
    res = session.get(url_mytask)
    self.SOUP = BeautifulSoup(res.text, "html.parser")

    #ログインできたか確認
    error_text = 'default'
    error = self.SOUP.find('ul', class_ ='errmsg')
    if not error :
      print('ログインに成功')
      return self.SOUP
    else :
      #エラーの原因調査
      error_text = error.text
      search_text = 'manabaの認証が必要です'
      if search_text in error_text :
        print('ユーザIDまたはパスワードが間違っています')
        return -1
      else :
         print('その他のエラー') 
         return -2

  def scraping_manaba(self): 
      #各要素取得
      types = self.SOUP.select('td[class="center"]') #部分一致のため
      titles = self.SOUP.find_all('div', class_='myassignments-title')
      subjects = self.SOUP.find_all('div', class_='mycourse-title')
      dates = self.SOUP.find_all('td', class_='center td-period')
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

      #各要素を2次元辞書にまとめる

      data =[]
      data.append(types_txt)
      data.append(titles_txt)
      data.append(subjects_txt)
      data.append(dates_start_txt)
      data.append(dates_finish_txt)
      '''data = [
              types_txt,
              titles_txt,
              subjects_txt,
              dates_start_txt,
              dates_finish_txt,
            ]     
      '''
      '''
      data['タイプ'] = types_txt
      data['タイトル'] = titles_txt
      data['教科'] = subjects_txt
      data['開始日'] = dates_start_txt
      data['終了日'] = dates_finish_txt
  '''
      return data
  
