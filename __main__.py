from utils import AzureDevops
from os import getenv

from dotenv import load_dotenv
load_dotenv()

def main():
  ## Connection data
  PAT = getenv('PAT') # admin token
  organization_name = "jfbarahonagUN"
  project_name = "Wiki"
  
  azure_devops = AzureDevops(organization_name, project_name, PAT)
  
  wiki_pages = azure_devops.get_wiki().get_all_wiki_pages(recursive=True, include_content=True)
  
  print(wiki_pages[0].items())
  print(
    azure_devops.get_wiki().get_wiki_page_by_id(wiki_pages[0]['path'], include_content=True).items()
  )
  
    
if __name__ == '__main__':
  main()
