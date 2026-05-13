import requests
from pprint import pprint as print
import  json


def get_word(word):
    try :
        r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        response=r.json()
        # print(response[0].keys())
        # print(response[0]['meanings'][0].keys())
        # print(response[0]['meanings'][0]['definitions'])
        # print(response[0]['meanings'][0]['definitions'][0]['definition'])
        # print(type(response[0]['meanings'][0]['definitions']))
        if 'error' in response[0]:
            return False

        output={}
        definitions=[]
        word_list=response[0]['meanings'][0]['definitions']

        for item in word_list:
            definitions.append(f"👉  {item['definition']}")

        output['definitions']='\n'.join(definitions)

        if response[0]['phonetics'][0]['audio']:
            output['audio']=response[0]['phonetics'][0]['audio']

        return output
    except Exception as e:
        return False


if __name__=='__main__':
    from pprint import pprint as print
    print(get_word('Great Britain'))
    print(get_word('America'))

    
    