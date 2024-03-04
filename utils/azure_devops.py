from .general import str2b64, find_key_in_dict
import requests

class AzureConnection:
  def __init__(self, auth: str) -> None:
    
    self.__headers = {
      "Content-Type":"application/json",
      "Authorization": f"Basic {auth}",
    }
    
    self.__params = {
      "api-version":"7.1-preview.1",
    }
  
  def get(self, url:str, extra_headers:dict|None=None, extra_params:dict|None=None):
    headers = self.__headers.copy()
    params = self.__params.copy()
    
    if (extra_headers is not None):
      headers = { **headers, **extra_headers }
    
    if (extra_params is not None):
      params = { **params, **extra_params }
      
    x = requests.get(url, headers=headers, params=params)
    
    return {
      'json': x.json(),
      'status_code': x.status_code
    }
    

class AzureDevops:
  def __init__(self
               ,organization_name:str 
               ,project_name:str
               ,PAT:str
               ) -> None:
    self.organization_url = f"https://dev.azure.com/{organization_name}"
    self.project_name = project_name
    self.wiki_name = f"{project_name}.wiki"
    PAT = f":{PAT}"
    self.__auth = str2b64(PAT)
    
    self.__conn = AzureConnection(auth=self.__auth)
    
    self.__pages = []
    
  def get_wiki_page_by_id(self, id:str, include_content=False):
    wiki_url = f"{self.organization_url}/{self.project_name}/_apis/wiki/wikis/{self.wiki_name}/pages/{id}"
    resp = self.__conn.get(wiki_url, extra_params={ "includeContent": include_content })
    return resp['json']
    
  def get_all_wiki_pages(self, recursive=False, include_content=False):
    wiki_url = f"{self.organization_url}/{self.project_name}/_apis/wiki/wikis/{self.wiki_name}/pages"
    resp = self.__conn.get(wiki_url, extra_params={ "recursionLevel": "full" if recursive == True else "none" })
    
    if resp['status_code'] != 200:
      raise Exception(f"Respuesta inesperada.\n")
    
    pages_resp = resp['json']
    
    self.__get_all_wiki_pages(pages_resp, include_content)
    
    for page in self.__pages:
      print(self.get_wiki_page_by_id(page['path'], include_content))
    
  def __get_all_wiki_pages(self, pages_dict: dict, include_content: bool):
    pages_dict = pages_dict.copy()
    key = "isParentPage"
    content_resp = None
    
    ## Find the leafs
    if(find_key_in_dict(pages_dict, key)):
      for page in pages_dict["subPages"]:
        self.__get_all_wiki_pages(page, include_content)
    
    ## get content
    if include_content == True:
      content_resp = self.get_wiki_page_by_id(pages_dict['path'], include_content)

    ## add dict to list
    self.__pages.append({
      'path': pages_dict['path'],
      'gitItemPath': pages_dict['gitItemPath'],
      'url': pages_dict['url'],
      'content': content_resp['content'] if content_resp is not None else None,
    })
