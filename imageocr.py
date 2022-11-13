import getopt, sys, tempfile, hashlib
from PIL import Image
import pytesseract
from urllib.request import urlopen, Request


def main(argv):
    # set User-Agent
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"

    # 要讀取的檔案路徑
    filepath = ''

    # 取得暫存路徑
    tmpfolder = tempfile.gettempdir()

    # 嘗試取得輸入參數
    try:
        opts, args = getopt.getopt(argv, "hf:", ["filepath="])
    except getopt.GetoptError:
        print('imageocr.py -f <filepath>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('imageocr.py -f <filepath>')
            sys.exit(0)
        elif opt in ("-f", "--filepath"):
            filepath = arg

    try:
        # 判斷是否為網路來源檔案, 是則下載處理
        if filepath.startswith('http'):
            req = Request(filepath, headers={'User-Agent': useragent})
            with urlopen(req) as webf:
                # 將檔案 md5 編碼後放入暫存資料
                m = hashlib.md5()
                m.update(filepath.encode("utf-8"))
                # 重設 filepath 到 暫存檔案路徑
                filepath = f'{tmpfolder}/{m.hexdigest()}'
                # 將網路檔案寫入暫存資料
                with open(filepath, 'wb') as f:
                    f.write(webf.read())

        # 開啟讀片檔案
        with Image.open(filepath) as imgf:
            imgf.convert('L')
            its = pytesseract.image_to_string(imgf, lang="chi_tra")
            print(its)

    except Exception:
        sys.exit(1)

    # 程式正常結束
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])