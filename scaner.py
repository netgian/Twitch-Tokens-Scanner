import requests
import threading
import time

unchecked_tokens_path = "unchecked_tokens.txt"
valid_tokens_path = "valid_tokens.txt"


class TokensScanner:
    def __init__(self, path1, path2):
        self.unchecked_tokens_path = path1
        self.valid_tokens_path = path2
        self.total_valid_tokens = 0
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "accept-charset": "utf-8",
            "accept-encoding": "br, gzip, deflate",
        }
        
        self._main()

    def _restart(self):
        with open(self.valid_tokens_path, "w") as f:
            f.write("")

    def _get_tokens(self):
        with open(self.unchecked_tokens_path, 'r', encoding='utf-8') as f:
            tokens = [line.strip('\n') for line in f]
        return tokens

    def _validate(self, current_token):
        url = 'https://id.twitch.tv/oauth2/validate'

        r = requests.get(url, headers=self.headers)
        if not "invalid access token" in r.text:
            with open(self.valid_tokens_path, "a", encoding='utf-8') as f:
                f.write(current_token + "\n")
            self.total_valid_tokens += 1
            print('\33[32m', f"Valid: {current_token}", '\33[0m')
        else:
            print('\33[31m', f"Invalid: {current_token}", '\33[0m')

    def _main(self):
        self._restart()
        for token in self._get_tokens():
            self.headers['Authorization'] = 'OAuth ' + token
            threading.Thread(target=self._validate, args=[token]).start()
            time.sleep(0.05)
        time.sleep(1)
        print(f"Valid tokens: {self.total_valid_tokens} of {len(self._get_tokens())}")


if __name__ == '__main__':
    TokensScanner(unchecked_tokens_path, valid_tokens_path)
