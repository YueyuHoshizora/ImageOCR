import getopt, sys, tempfile, os
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import pytesseract
from urllib.request import urlopen, urlretrieve, Request
from io import BytesIO


def main(argv):
    # set User-Agent
    useragent = "imageocr/1.0"

    # 要讀取的檔案路徑
    filepath = ''

    # 建立暫存檔案
    tf = tempfile.TemporaryFile()

    # 預設語言
    lang = "eng"

    # 初始化設定參數
    tessdataPath = './tessdata/'
    os.environ["TESSDATA_PREFIX"] = tessdataPath

    # 嘗試取得輸入參數
    try:
        try:
            opts, args = getopt.getopt(argv, "hf:l:b:",
                                       ["filepath=", "lang=", "tesseract_bin"])
        except getopt.GetoptError:
            print('imageocr.py -f <filepath> -l <lang> -b <tesseract_bin>')
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print('imageocr.py -f <filepath>')
                sys.exit(0)
            elif opt in ("-f", "--filepath"):
                filepath = arg
            elif opt in ("-b", "--tesseract_bin"):
                pytesseract.pytesseract.tesseract_cmd = arg
            elif opt in ("-l", "--lang"):
                lang = arg

        # 判斷是否下載語系
        for l in lang.split('+'):
            if not os.path.isfile(f'{tessdataPath}{l}.traineddata'):
                urlretrieve(
                    f'https://github.com/tesseract-ocr/tessdata_best/raw/main/{l}.traineddata',
                    f'{tessdataPath}{l}.traineddata')

        try:
            # 判斷是否為網路來源檔案, 是則下載處理
            if filepath.startswith('http'):
                req = Request(filepath, headers={'User-Agent': useragent})
                with urlopen(req) as webf:
                    # 將網路檔案寫入暫存資料
                    tf.seek(0)
                    tf.write(webf.read())
        except Exception as ex:
            raise ex

        # 建立 BytesIO
        bio = BytesIO()
        try:
            # 讀取到 BIO
            with Image.open(tf) as img:
                bio.seek(0)
                img.save(bio, format='png', dpi=(300, 300))

            # 處理檔案提供辨識
            bio.seek(0)
            with Image.open(bio) as img:
                # 轉換色彩空間
                img = img.convert('L')

                # 調整銳利度
                img = img.filter(ImageFilter.SHARPEN)
                img.filter(
                    ImageFilter.UnsharpMask(radius=1,
                                            percent=100,
                                            threshold=10))

                # 調整對比
                img = ImageEnhance.Contrast(img).enhance(20)

                # 轉換色彩空間
                img = img.convert('1')

                # 計算色相
                colors = img.getcolors(img.size[0] * img.size[1])
                maxColor = max(colors, key=lambda tup: tup[0])[1]

                # 處理色彩反轉
                if (maxColor == 0):
                    img = ImageOps.invert(img)

                # 增加外框
                img = ImageOps.expand(img, border=5, fill=0)

                # 儲存進 bio
                bio.seek(0)
                img.save(bio, format='png')
        except Exception as ex:
            raise ex

        # 儲存檔案
        # bio.seek(0)
        # with Image.open(bio) as img:
        #     img.save('./123.png')

        # 進行文字辨識
        try:
            bio.seek(0)
            with Image.open(bio) as img:
                its = pytesseract.image_to_string(img, lang=lang)
                print(its)
                pass
        except Exception as ex:
            raise ex
    except Exception as ex:
        raise ex
        sys.exit(1)

    # 程式正常結束
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
