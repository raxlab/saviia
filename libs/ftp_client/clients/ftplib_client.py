from ftplib import FTP
from typing import List
from libs.ftp_client.ftp_client_contract import FTPClientContract
from libs.ftp_client.types.ftp_client_types import ListFilesArgs, FtpClientInitArgs

class FTPLibClient(FTPClientContract):
    def __init__(self, args: FtpClientInitArgs):
        try: 
            self.client = FTP(host=args.host, user=args.user, passwd=args.password, timeout=10)
            self.user = args.user
            self.password = args.password
        except TimeoutError:
            raise TimeoutError(f'Unable to connect the server at {args.host}:{args.port}')
        except ConnectionError:
            raise ConnectionError(f'Server is not available at {args.host}:{args.port}')
    
    
    def _close(self):
        self.client.close()
        
    def list_files(self, args: ListFilesArgs) -> List[str]:
        self.client.login(self.user, self.password)
        self.client.cwd(args.path)
        files = self.client.nlst()
        self._close() 
        return files
    
