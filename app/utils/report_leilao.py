import requests
import json

class User():
    def __init__(self, username, url_perfil, email, qtd_repos, seguidores, seguindo):
        self.username = username
        self.url_perfil = url_perfil
        self.email = email
        self.qtd_repos = qtd_repos
        self.seguidores = seguidores
        self.seguindo = seguindo

    def __str__(self):
        return f'Username: {self.username}\nURL do Perfil: {self.url_perfil}\nE-mail: {self.email}\nQuantidade de Repositórios Públicos: {self.qtd_repos}\nSeguidores: {self.seguidores}\nSeguindo: {self.seguindo}'

def get_user(username):
    # URL para request
    url_api = f'https://api.github.com/users/{username}'

    # Request status code: 200 para usuário, 404 para notFound
    response = requests.get(url_api)
    if response.status_code == 200:
        json = response.json()
        # Determinar a quantidade de repos públicos do usuário
        repos_url = f'https://api.github.com/users/{username}/repos'

        # Retorna a contagem dos elementos da lista de dicionários gerada pela request = 'public_repos'
        qtd_repos = len(requests.get(repos_url).json())

        if json['email'] == None:
            json['email'] = '-----'

        return User(
            username=json['login'],
            url_perfil=json['html_url'],
            email=json['email'],
            qtd_repos=qtd_repos,
            seguidores=json['followers'],
            seguindo=json['following']
            )
    
    return response

def get_user_repos(username):
    # Mesmo passo do método anterior
    url_api = f'https://api.github.com/users/{username}'
    response = requests.get(url_api)
    if response.status_code == 200:
        # Request
        repos_url = f'https://api.github.com/users/{username}/repos'
        request = requests.get(repos_url).json()
        repos_dict = {}

        # Iterar cada dicionário e relacionar nome e url do repo em um novo dicionário
        for repo in request:
            repos_dict[repo['name']] = repo['html_url']
    
        json_string = json.dumps(repos_dict, indent=2)
        # return repos_dict
        return json_string
    
    # Caso inválido
    return response

def get_user_report(username):
    # Coletando informações para o txt
    user = get_user(username)

    # Caso seja válido e tenha informações
    if user:
        repos = get_user_repos(username)
        # nome_arquivo = f'Leilao-{Leilao.id}.txt'
        nome_arquivo='Arquivo.txt'
        # Criação do arquivo DET
        with open(nome_arquivo,'w') as arquivo:
            arquivo.write(str(user) + '\n')
            arquivo.write('\nRepositórios:\n')
            i = 0
            for repo, url in repos.items():
            # for dicionario in repos:
                # i += 1
                arquivo.write(f'\t{i} - {repo}: {url}\n')
                # json.dump(dicionario, arquivo, indent=2)

        # Leitura para exibição do txt
        with open(nome_arquivo, 'r') as arquivo:
            leitura = arquivo.read()

        return leitura

    return user


print(get_user_report('fernando-pacheco'))

if __name__=='__main__':
    user = get_user_repos('Victor')
    print(user)
    report = get_user_report('Victor')
    print(report)