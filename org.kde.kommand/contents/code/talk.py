import os
import sys
import time
import urllib.parse
from biblioteca import Biblioteca

localPath = os.path.dirname(os.path.realpath(__file__))
bi = Biblioteca()
url_google = "https://translate.google.com/translate_tts?ie=UTF-8&q=%input_text%&tl=%lang%&client=tw-ob"
lang = sys.argv[1]

def talk(txt):
	frase_enc = urllib.parse.quote_plus(txt)
	url = url_google.replace("%lang%", lang)
	url = url.replace("%input_text%", frase_enc)
	req, res = bi.ajax(url)

	audio = open(os.path.join(localPath, "speak.mp3"), "wb")
	audio.write(res)
	audio.close()
	
	os.system("paplay --volume="+str(65536 * 50 / 100)+" "+os.path.join(localPath, "speak.mp3"))
	pass

for line in sys.stdin:
	talk( line.rstrip() ) 