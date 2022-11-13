import subprocess

proc = subprocess.run([
    'python', 'imageocr.py', '-f',
    'https://cdn.discordapp.com/attachments/952855965483561000/1041369346917814443/image0-1.jpg'
],
                      stdout=subprocess.PIPE)

print(proc.stdout.decode("utf-8"))