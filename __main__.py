from utils import AzureDevops, FileCRUD
from os import getenv, getcwd, path

from dotenv import load_dotenv
load_dotenv()

def main():
  ## Connection data
  PAT = getenv('PAT') # admin token
  organization_name = "jfbarahonagUN"
  project_name = "Wiki"

  azure_devops = AzureDevops(organization_name, project_name, PAT)
  
  wiki_pages = azure_devops\
                          .get_wiki()\
                          .get_all_wiki_pages(
                            recursive=True, 
                            include_content=True, 
                            cached=True
                          )
  cwd = path.join(getcwd(), 'wiki')
  for page in wiki_pages:
    fp = path.join(
      cwd, 
      page['gitItemPath'][1:] ## remove /
    )
    FileCRUD.create(page['content'], fp, force=True)
  
    
if __name__ == '__main__':
  main()
