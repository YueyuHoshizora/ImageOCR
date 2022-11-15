import subprocess

proc = subprocess.run([
    'python', 'imageocr.py', '-f',
    'https://lh3.googleusercontent.com/-sE0KYI6toyA/YewQEbM_DEI/AAAAAAAADzU/dWoZznp73uQ6H3IF10_RvpCEbLc7VzV2gCNcBGAsYHQ/002.zh-cht.png',
    "-l", "eng+chi_tra", '-b',
    '/nix/store/8cgwxswxyrr6g7jz2w82bsg7nfdrdwgi-tesseract-4.1.1/bin/tesseract'
],
                      stdout=subprocess.PIPE)

print(proc.stdout.decode("utf-8"))
