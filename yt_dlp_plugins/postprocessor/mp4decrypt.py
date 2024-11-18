from yt_dlp.postprocessor import FFmpegMergerPP
from yt_dlp.postprocessor.common import PostProcessor
import os
import subprocess

class MP4DecryptPP(PostProcessor):
    def __init__(self, downloader=None, **kwargs):
        super().__init__(downloader)
        self._kwargs = kwargs

    def run(self, info):
        if 'requested_formats' in info:
            for part in info['requested_formats']:
                self.decrypt(part)
        elif info['__real_download']:
            self.decrypt(info)

        if '+' in info['format_id']:
            info['__files_to_merge'] = [part['filepath'] for part in info['requested_formats']]
            info = self._downloader.run_pp(FFmpegMergerPP(), info)

        return [], info

    def decrypt(self, info):
        filepath = info.get('filepath')

        if filepath:
            if 'decryption_key' in self._kwargs:
                decryption_key = self._kwargs['decryption_key']
                success = self.decrypt_single_key(filepath, decryption_key)
                if success:
                    self.to_screen(f'Decryption successful for "{filepath}" using decryption_key: {decryption_key}')
                else:
                    self.to_screen(f'Decryption failed for "{filepath}" using decryption_key: {decryption_key}')
            elif 'keyfile' in self._kwargs:
                keyfile = self._kwargs['keyfile']
                if os.path.exists(keyfile):
                    success = self.decrypt_with_keyfile(filepath, keyfile)
                    if success:
                        self.to_screen(f'Decryption successful for "{filepath}" using keyfile: "{keyfile}"')
                    else:
                        self.to_screen(f'Decryption failed for "{filepath}" using keyfile  "{keyfile}"')
                else:
                    self.to_screen(f'Keyfile not found: "{keyfile}"')
            else:
                self.to_screen("No decryption key or keyfile provided.")

    def decrypt_single_key(self, filepath, decryption_key):
        try:
            output_file = f"{os.path.splitext(filepath)[0]}_decrypted{os.path.splitext(filepath)[1]}"
            cmd = ["mp4decrypt", "--key", decryption_key, filepath, output_file]
            #USE FOR DEBUGGING PURPOSES
            #self.to_screen(f'Executing command: {" ".join(cmd)}')
            subprocess.run(cmd, check=True)
            os.remove(filepath)
            os.rename(output_file, filepath)
            return True
        except subprocess.CalledProcessError:
            return False

    def decrypt_with_keyfile(self, filepath, keyfile):
        try:
            with open(keyfile, 'r') as f:
                keys = f.read().splitlines()

            output_file = f"{os.path.splitext(filepath)[0]}_decrypted{os.path.splitext(filepath)[1]}"
            cmd = ["mp4decrypt"]
            for key in keys:
                cmd.extend(["--key", key])
            cmd.extend([filepath, output_file])
            #USE FOR DEBUGGING PURPOSES
            #self.to_screen(f'Executing command: {" ".join(cmd)}')
            subprocess.run(cmd, check=True)
            os.remove(filepath)
            os.rename(output_file, filepath)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False
