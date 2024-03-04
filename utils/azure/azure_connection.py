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
    try:
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
    except:
      print(f"Error fetching data from {url}")
