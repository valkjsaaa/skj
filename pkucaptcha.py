#-*- coding: utf-8 -*-
'''
Created on 2013-9-10

@author: nzk
@modified by: jackieyang9
'''
import  math, zlib, base64
from PIL import Image
data = 'eJztWsmOFUcQ/JW5zWUOXWCw8Q2zWd5k2YAxozmAV9kCeZF38e9Qgx6vKjMiMqvfa6bHM9IcICO7OzMisrq6X/93eOXw/YPj43J0MPV/ryLl5OjgeHLItEVK/1fBipTdkeY6IGyRbbhDuvAWseGuU1sh5WASyCvo8J0NsYn6W/rHQCSZudQY2LIwAGIiJEtSeEDCAFj5v97zHxHl7A2NIkFtJAumh22yoO2JXjMF+lYmABKGCLeV//ca/u3RlsUc/8Ng61WpeRb0/u/FmcO/lDXBP6q28v/BKf/gUOU11MswIq/jRoHXlqhAkkyQySKcA0jsbUJs1JxsMW8o5anIc2eNy/ojATL2bWS6y2QiR5Oi9xzOGO3tVNKHK2MfNoytzDgOx395/Kzrn4lXmT5yG8vGN5dhEZaTV0C4nY5PxHRkHh8uDpKfylNiPxtYdnwKusB8vLiUYdykkLHuTjcDb908Ey8xvrl+lenz/e4nx/ZsEVFju7n1zEwl9gtBbEQvvQCRx4s/E0/Kr3BOUITblHn9bVNS/r/Pt/2RBxscF7gt8xLfAa8yPZR3k9IpIVLkW55pNMVn9ebcZ0obdlOy55Q3YEInL9Wj1I0fMhwpIOmXrEV8JMggTOx0fln/TvxI/qtMj8XCpzd9UlQplxQqYXxOXgoBnCyw8X265BPFZEmChaAXy654JOASCK+AV+06rcR+i3564e4bQNprNUik/QqJ5VWTTiux38N3+uh0aJDQTpzFyDCvI1ap+HHh1wGR2YnCCztpYaQS+5P/3c6t8W5Udcb5C3CZp40BnzsDXljL/NJT0fV3gW59e1h1Ukil/DdPufYtPOdbCtSC/+TrNRepH1EwNEdsyzgAtnjP1a6gdUgIVqL+JkQRInijpMtMoXgbQpD+GDAbujbSaaXi3xk/IXL7cPkjbVF7ekxFgShcm70650OwzRkTXUsEKcXV7UB6ttlbfWAHzp2uuhJ7bfbzMxCWS55E0EDJttZL7LvLv5goARVjrywKQJwY4IAjuipkEOAIgVRib5BPt9DRSDN7AAC5QyLQn1Y8z3aqmla45KGZOxIkiLxLb2Eb/m+SX/iJ7rmUru/FUkwVvGswAPkUrHTAPUnh8kI84dcmpap5i3+IOoGukXmBtnQmGklodWcLkmplnxFDhNvK/5113n+d0Tiy3wrStUXvr+9JY4feDuxdLD5quIVxR9BMvOUnwkfM/8b/H+snX9rmNgLw7r8Wt+cawkGh1odSJnl8rr6ovwQ/CX4bmatMn/bLFDQkmUuctXCi57GLL5xoQTs1yya2lJR9JQpvfImezdFkcMMJH4owqJ9sX8l2lDw5iTCYMtEl4qQy9mDH130XCwR+DR/yvAda/r8SbxFhUK2xJL2w2l2Ev4ct2fSpSbfBeekwCxx3Fum0CbzjoJGF06vTvl7RV0QRbgYGdQ0KOW+4/TuV6Yl4p0TXGvSWxYkSyYXOhhBoNrJ37BH7h++cp0il4htGBamPrNPjd/M5YXdJUiBqpzb7HWqWi46uPOFmHTWEMRReqNkfyD4NmULqKwteEkEV8Kq9rD2CrgPHmV9H/eJXKf9Zf+8r99kzQOdSi9AlA53Wnl8+hiWPjK4ZVRv12ahZ+X8mPkPxEdCDdY8aC3r26An9MpfI9ytZnuVMrnDF6mvjVctOkcf3i1TKf4c3CXTLQnOLpgLtN1CzaCN3Yh65Hbmc1tcL8B/B9yLnCEHulhNhlP0LUWHFiq6eSiw4sZh64T/Wlei76p2KWZE2x4lVoH/+nx+BAU/gZ86ZYBkFAYkaPHnxEiqAO44='
chars = '23456789ABCDEFGHJKLMNPRSTUVWXYZabcdefghjkmnpqrsuvwxyz'
charims = eval(zlib.decompress(base64.decodestring(data)))
def identify(filepath):
	img=Image.open(filepath)
	(width,height)=img.size
	imarr = []
	for i in range(0, height):
		imarr.append([])
		for j in range(0, width):
			(a,b,c) = img.getpixel((j,i));
			imarr[i].append(0 if a < 127 else 1)
	s = ''
	for i in range(0, height):
		for j in range(0, width):
			if imarr[i][j] == 0:
				black = 0.0
				cnt = 0
				for k in range(-3, 3):
					for l in range(-3, 3):
						if (k != 0 or l != 0) and i + k >= 0 and i + k < height and j + l >= 0 and j + l < width:
							cnt += 1.0 / math.exp(math.sqrt(k * k + l * l))
							if imarr[i + k][j + l] == 0:
								black += 1.0 / math.exp(math.sqrt(k * k + l * l))
				if black < cnt * 0.2: img.putpixel((j,i), (255, 255, 255, 0))
	#print imarr
	for i in range(0, width):
		for j in range(0, height):
			chlist = []
			for ch in chars:
				nowerror = 0
				h = len(charims[ch])
				w = len(charims[ch][0])
				error = h * w * 0.1
				for k in range(0, h):
					for l in range(0, w):
						if j + k >= height:
							nowerror += 5
						elif i + l >= width:
							if charims[ch][k][l] == 0:
								nowerror += 0.4
						elif imarr[j + k][i + l] != charims[ch][k][l]:
							if imarr[j + k][i + l] == 1: nowerror += 3
							else: nowerror += 1*1/(1+((k-h/2)/h*(l-w/2)/w)*((k-h/2)/h*(l-w/2)/w)*9)
						if nowerror > error: break
					if nowerror > error: break
				if nowerror <= error:
					chlist.append((nowerror*1.0/h/w, ch, h*w))
			if chlist == []: continue
			chlist.sort()
			ch, size = chlist[0][1:]
			for k in range(1, len(chlist)):
				if chlist[k][0] - chlist[0][0] > 0.02: break
				if chlist[k][2] > size: ch, size = chlist[k][1:]
			h = len(charims[ch])
			w = len(charims[ch][0])
			for k in range(0, h):
				for l in range(0, w):
					if j + k < height and i + l < width and charims[ch][k][l] == 0:
						imarr[j + k][i + l] = 1
			s += ch
	#print'the vaild code is'
	#print s
	return s

if __name__ == '__main__':
	import sys
	print identify(sys.argv[1])
