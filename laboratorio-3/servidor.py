import json
import threading
import rpyc

from pathlib import Path
from rpyc.utils.server import ThreadedServer

class DicionarioRemoto(rpyc.Service):

    def __init__(self):
        self.file_path = 'dicionario.json'
        self.file_lock = threading.Lock()
        self.monitor_thread = None
        self.file_content = None

    def on_connect(self, conn):
        with self.file_lock:
            self.file_content = self.read_file()

        self.monitor_thread = threading.Thread(target=self.monitor_file)
        self.monitor_thread.start()
    
    def on_disconnect(self, conn):
        self.monitor_thread.join()
    
    def read_file(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)   
        except json.JSONDecodeError:
            return {}
        
    def write_file(self, content):
        with open(self.file_path, 'w') as file:
            json.dump(content, file)
    
    def monitor_file(self):    
        file_path = Path(self.file_path)
        last_modified = file_path.stat().st_mtime
        while True:
            current_modified = file_path.stat().st_mtime
            if current_modified != last_modified:
                with self.file_lock:
                    self.file_content = self.read_file()
                last_modified = current_modified

    def exposed_consulta(self, chave):

        with self.file_lock:
            if chave in self.file_content:
                return self.file_content[chave]
            else:
                return "Item não existe no dicionário, seja o primeiro a adicionar!"
    
    def exposed_insere(self, chave, valor):

        with self.file_lock:
            if chave in self.file_content:
                existing_value = self.file_content[chave]
                if isinstance(existing_value, list):
                    existing_value.append(valor)
                else:
                    self.file_content[chave] = [existing_value, valor]
            else : 
                self.file_content[chave] = valor
                
            self.write_file(self.file_content)
    
    def exposed_remove(self, chave):

        with self.file_lock:
            if chave in self.file_content:
                del self.file_content[chave]
                self.write_file(self.file_content)

if __name__ == '__main__':
    dicionarioRemoto = ThreadedServer(DicionarioRemoto, port=10000)
    dicionarioRemoto.start()