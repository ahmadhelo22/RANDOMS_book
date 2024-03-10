import requests

api_key_short_link = 'baa3303da730c77a49cd4f0e7e6921ec2da99e07'

def short_link_opration(link_to_short):

    try:

        res = requests.get(f'https://best-cpm.com/api?api={api_key_short_link}&url={link_to_short}')
        url = res.json()
        last_value = url[list(url.keys())[-1]]

        return last_value
    
    except:
        return "يوجد مشكله في الرابط"