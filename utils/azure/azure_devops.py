from ..general import str2b64, find_key_in_dict

from .azure_connection import AzureConnection

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
    page_dict = resp['json']
    return {
      'path': page_dict['path'],
      'gitItemPath': page_dict['gitItemPath'],
      'url': page_dict['url'],
      'content': page_dict['content'] if page_dict is not None else None,
    }
    
  def get_all_wiki_pages(self, recursive=False, include_content=False):
    wiki_url = f"{self.organization_url}/{self.project_name}/_apis/wiki/wikis/{self.wiki_name}/pages"
    resp = self.__conn.get(wiki_url, extra_params={ "recursionLevel": "full" if recursive == True else "none" })
    
    if resp['status_code'] != 200:
      raise Exception(f"Respuesta inesperada.\n")
    
    pages_resp = resp['json']
    
    self.__get_all_wiki_pages(pages_resp, include_content)
    
    return self.__pages.copy()
    
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
      'content': content_resp['content'] if content_resp is not None else "",
    })
