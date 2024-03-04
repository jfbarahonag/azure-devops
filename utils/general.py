import base64

def str2b64(str_in: str) -> str:
  str_bytes = str_in.encode('utf-8')  # Convierte la cadena a bytes
  base64_bytes = base64.b64encode(str_bytes)  # Codifica los bytes a Base64
  base64_str = base64_bytes.decode('utf-8')  # Convierte los bytes de Base64 a cadena
  return base64_str

def print_object(obj: object):
  for items in obj.__dict__.items():
    print(items)
    
def find_key_in_dict(d: dict, key:str):
  return d.get(key) is not None

if __name__ == "__main__":
  text = input("Type the text:\n")
  b64 = str2b64(text)
  print(b64)