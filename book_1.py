import requests
from bs4 import BeautifulSoup



def books_name_link(app_name):

    books_list = {
        'books_name_list':[],
        'books_links_':[]
    }
    
        
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(f'https://www.ktaab.com/?s={app_name}', headers=headers)
        src = result.content
        soup = BeautifulSoup(src, 'xml')


        a = soup.find('section', id='content').find_all('div', {'class':'mbt'})

        if a == None :
            pass

        else:

            for i in a:
                q = i.find('h2').find('a').next_element
                books_list['books_name_list'].append(q)


            for i in a:
                q = i.find('h2').find('a')['href']
                books_list['books_links_'].append(q)
            
            return books_list
     
    except Exception as e:
        pass        



# books_name_link('الاب+الغني+الاب+الفقير')