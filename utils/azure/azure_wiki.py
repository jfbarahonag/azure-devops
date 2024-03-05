from ..general import find_key_in_dict

from .azure_connection import AzureConnection

class AzureWiki:
  def __init__(self, conn: AzureConnection, project_name: str, organization_name: str) -> None:
    self.project_name = project_name
    self.wiki_name = f"{project_name}.wiki"
    self.__organization_url = f"https://dev.azure.com/{organization_name}"
    self.__pages:list[dict] = []
    self.__conn = conn
    self.__wikipages_url_base = f"{self.__organization_url}/{self.project_name}/_apis/wiki/wikis/{self.wiki_name}/pages"

  def get_wiki_page_by_id(self, id:str, include_content=False):
    url = f"{self.__wikipages_url_base}/{id}"
    resp = self.__conn.get(url, extra_params={ "includeContent": include_content })
    page_dict = resp['json']
    return {
      'path': page_dict['path'],
      'gitItemPath': page_dict['gitItemPath'],
      'url': page_dict['url'],
      'content': page_dict['content'] if page_dict is not None else None,
    }

  def get_all_wiki_pages(self, recursive=False, include_content=False):
    url = f"{self.__wikipages_url_base}"
    resp = self.__conn.get(url, extra_params={ "recursionLevel": "full" if recursive == True else "none" })
    
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
