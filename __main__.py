from utils import AzureDevops, FileCRUD, AzureStorageCRUD
from os import getenv, getcwd, path

from dotenv import load_dotenv
load_dotenv()

def main():
  ## Connection data
  PAT = getenv('PAT') # admin token
  STORAGE = getenv('STORAGE')
  organization_name = "jfbarahonagUN"
  project_name = "Wiki"
  option = "cloud"

  print("1. Get data from azure devops")
  
  ## Get pages from Wiki
  azure_devops = AzureDevops(organization_name, project_name, PAT)
  wiki_pages = azure_devops\
                  .get_wiki()\
                  .get_all_wiki_pages(
                    recursive=True, 
                    include_content=True, 
                    cached=True
                  )[:-1] ## remove root (/) file
  
  print("2. Upload to storage account")
  
  ## upload to file
  if (option == "local"):
    cwd = path.join(getcwd(), 'wiki')
    for page in wiki_pages:
      fp = path.join(
        cwd, 
        page['gitItemPath'][1:] ## remove /
      )
      FileCRUD.create(page['content'], fp, force=True)
  else:
    azst = AzureStorageCRUD(
      account_url=STORAGE,
      use_managed_identity=True,
    )
    
    azst.upload_blobs(
      "wiki", 
      [(page['gitItemPath'][1:], page['content']) for page in wiki_pages]
    )
    
    
if __name__ == '__main__':
  main()
