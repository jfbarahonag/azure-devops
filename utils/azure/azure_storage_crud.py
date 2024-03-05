from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

class AzureStorageCRUD:
    def __init__(self, account_url, use_managed_identity=True, connection_string=None):
        if use_managed_identity:
            # Utiliza Identidad Administrada para la autenticación
            self.credential = DefaultAzureCredential()
            self.blob_service_client = BlobServiceClient(account_url=account_url, credential=self.credential)
        elif connection_string:
            # Utiliza la cadena de conexión para la autenticación
            self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        else:
            raise ValueError("Debe proporcionar un método de autenticación válido.")

    def upload_blob(self, container_name, blob_name, content):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(content, overwrite=True)
        print(f"Blob '{blob_name}' uploaded to container '{container_name}'.")

    def download_blob(self, container_name, blob_name):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        download_stream = blob_client.download_blob()
        return download_stream.readall()

    def delete_blob(self, container_name, blob_name):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.delete_blob()
        print(f"Blob '{blob_name}' deleted from container '{container_name}'.")

    def list_blobs(self, container_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        return [blob.name for blob in container_client.list_blobs()]
    
    def upload_blobs(self, container_name, blobs_info):
      """
      Sube una lista de blobs a un contenedor especificado.

      Parámetros:
      - container_name (str): El nombre del contenedor donde se subirán los blobs.
      - blobs_info (list): Una lista de tuplas, donde cada tupla contiene el nombre del blob y su contenido.
                          Por ejemplo: [('blob1.txt', b'contenido1'), ('blob2.txt', b'contenido2')]
      """
      for blob_name, content in blobs_info:
          blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
          blob_client.upload_blob(content, overwrite=True)
          print(f"Blob '{blob_name}' uploaded to container '{container_name}'.")

