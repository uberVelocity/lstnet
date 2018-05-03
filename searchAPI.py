import sys
import requests
import re

def print_example_queries():
    print("1. What is the altitude of Mont Blanc?")
    print("2. What is the capital of Romania?")
    print("3. Who is the CEO of Samsung?")
    print("4. Who is the president of the United States?")
    print("5. What is the surface of Romania?")
    print("6. What is the boiling point of Water?")
    print("7. What is the deepest point of Earth?")
    print("8. Who is the founder of Rolex?")
    print("9. What is the location of Groningen?")
    print("10. Who is the head of state of North Korea?")
   #print("11. What is the unicode character of Earth?") this is a really cool one
params = {'action':'wbsearchentities',
          'language':'en',
          'format':'json'
          }

print_example_queries()

for line in sys.stdin:
    url = 'https://www.wikidata.org/w/api.php'
    params['type'] = 'item'
    input_question = line.rstrip()
    #params['search'] = line.rstrip()
    m = re.search('[Whoat] is the (.*) of (.*)\?',
    input_question)
    
    ok = 1
    search_object = m.group(2)
    search_property = m.group(1)
    #print (search_object)
    #print (search_property)

    params['search'] = search_object
    json = requests.get(url,params).json()
    for result in json['search']:
        if ok == 1:
            #print("{}".format(result['id']))
            ok = 0
            query_object = result['id']
    ok = 1
    params['search'] = search_property
    params['type'] = 'property';
    json = requests.get(url,params).json()
    for result in json['search']:
        if ok == 1:
            #print("{}".format(result['id']))
            ok = 0
            query_property = result['id']
    query='''
        SELECT ?valueLabel WHERE {
        wd:''' + query_object + ''' wdt:''' + query_property + ''' ?value
        SERVICE wikibase:label {
        bd:serviceParam wikibase:language "en" .
        }
        }
        '''
    #print(query)

    url = 'https://query.wikidata.org/sparql'
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    if data['results']['bindings'] == []:
        print('Unable to retrieve answer.')
    else:
      for item in data['results']['bindings']:
        for var in item:
            sys.stdout.write("The " + search_property + " of " + search_object + " is ")
            sys.stdout.write('{}.\n'.format(item[var]['value']))