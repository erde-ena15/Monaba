import urllib.parse
import requests 
from bs4 import BeautifulSoup 

if __name__ == "__main__":
  print("this ia a modlule")

class manaba_tool: 
  def __init__(self,User=None,Pass=None,
               url_mytask="https://cit.manaba.jp/ct/home_library_query",
               url_login = "https://cit.manaba.jp/ct/login",
               ):
      self.USER = User
      self.PASS = Pass 
      self.session = requests.session()
      self.url_login = url_login
      self.url_mytask = url_mytask
      self.SOUP = None
      self.types_txt = None
      self.urls = None
      
  def check_login(self,sp=None):
    #ログインできたか確認
    if sp == None:
      sp = self.SOUP
    error = sp.find('ul', class_ ='errmsg')
    if not error :
      print('ログインに成功')
      return 0
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
    
  def login_manaba(self):
    res = self.session.get(self.url_login)
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
    login = self.session.post(self.url_login, data=login_info, cookies=cookie) 
    res = self.session.get(self.url_mytask)
    self.SOUP = BeautifulSoup(res.text, "html.parser")
    return self.check_login()
      
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
      #myassignments-titleクラスを取得
      title_classes = self.SOUP.find_all(class_="myassignments-title")
      self.urls =[]
      #find_allが使えないためfor文
      for title_class in title_classes:
        tag_a = title_class.find('a') #aタグのみ
        href = tag_a.get("href") #href属性のみ
        add_url = urllib.parse.urljoin(self.url_mytask,href)
        self.urls.append(add_url)
      #タグなどを取り除く
      self.types_txt =[]
      for type_ in types:
        self.types_txt.append(type_.text)
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
      #urls_txt =[]
      #for url in urls:
        #urls_txt.append(url.text)

      if (len(titles_txt)) == 0:
        return None

      #各要素を2次元辞書,タプルにまとめる
      data =[]
      data.append(self.types_txt)
      data.append(titles_txt)
      data.append(subjects_txt)
      data.append(dates_start_txt)
      data.append(dates_finish_txt)
      data.append(self.urls)
      
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
  
  def scraping_detail(self,number):
    res = self.session.get(self.urls[number])
    SOUP = BeautifulSoup(res.text, "html.parser")
    detail = SOUP.find('td', class_='left')
    if self.check_login(sp=SOUP) == -1 or self.check_login(sp=SOUP) == -2:
      print('セッションが切れています')
      return -1
    de = detail.text
    if de.isspace() == True or self.types_txt[number] == "アンケート":
      de = "詳細内容はありません"
    return de
  
  def reload_data(self): 
    res = self.session.get(self.url_mytask)
    self.SOUP = BeautifulSoup(res.text, "html.parser")
    if not self.check_login() == 0:
      print('セッションが切れています')
      return -1
    return self.scraping_manaba()


    

