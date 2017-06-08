import requests, json

REQUEST_URL = "https://api.cognitive.microsoft.com/bing/v5.0/search[?q][&count][&offset][&mkt][&safesearch]"
ROOT_URL = "https://api.cognitive.microsoft.com/bing/v5.0/search"


def read_bing_key():
    bing_api_key = None
    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline()
    except:
        raise IOError("bing.key file not found")

    return bing_api_key


def run_query(search_terms):
    bing_api_key = read_bing_key()
    if not bing_api_key:
        raise KeyError('Bing Key Not Found')

    params = {  'q': search_terms,
                'count': '10',
                'offset': '0',
                'mkt': 'en-us',}

    headers = {'Ocp-Apim-Subscription-Key': bing_api_key}

    response = requests.get(ROOT_URL, params=params, headers=headers)
    # response.raise_for_status()
    results = []


    json_response = json.loads(response.content.decode('utf-8'))
    for result in json_response['webPages']['value']:
        results.append({'title': result['name'],
                        'link': result['url'],
                        'summary': result['snippet']})

    return results


def main():
    user_input = input("Enter the search query: ")
    results = run_query(user_input)
    for result in results:
	    print(result['title'])


if __name__ == '__main__':
    main()