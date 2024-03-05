from ..general import str2b64

from .azure_connection import AzureConnection
from .azure_wiki import AzureWiki
class AzureDevops:
  def __init__(self
               ,organization_name:str 
               ,project_name:str
               ,PAT:str
               ) -> None:
    self.__conn = AzureConnection(auth=str2b64(f":{PAT}"))
    self.__wiki = AzureWiki(self.__conn, project_name, organization_name)
    
  def get_wiki(self):
    return self.__wiki
