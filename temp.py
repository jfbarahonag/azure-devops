import requests
def main():
  
  PAT = "tijts3y4n53gbyyurpjqtlavewubxpr6dyrbrrxyx6x36xjsc64q" # admin token
  organization_name = "jfbarahonagUN"
  project_name = "Wiki"
  
  organization_url = f"https://dev.azure.com/{organization_name}"
  wiki_name = f"{project_name}.wiki"
  
  url_request = f"{organization_url}/{project_name}/_apis/wiki/wikis/{wiki_name}/pages?api-version=7.1-preview.1"
  
  print(url_request)
  
  response = requests.get(
    f"{organization_url}/{project_name}/_apis/wiki/wikis/{wiki_name}/pages",
    headers= {
      "Content-Type":"application/json",
      "Authorization":"Basic OnRpanRzM3k0bjUzZ2J5eXVycGpxdGxhdmV3dWJ4cHI2ZHlyYnJyeHl4NngzNnhqc2M2NHE="
    },
    params={
      "api-version":"7.1-preview.1",
      "includeContent":"true",
      "path":"TestWiki/Guias/Guia 1",
    }
  )
  
  print(response.content)

if __name__ == '__main__':
  main()
