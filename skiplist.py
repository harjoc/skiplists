#!/usr/bin/python

import sys, re, io, urllib

if len(sys.argv) != 4:
	print("usage: skiplist.py input.mp4 input.skip output.xspf")
	sys.exit(1)

video = sys.argv[1]

last = 0

def header(f):
	f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	f.write('<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">\n')
	f.write('  <trackList>\n')

def entry(f, a, b):
	f.write('    <track>\n')
	f.write('      <location>file:///./%s</location>\n' % urllib.quote_plus(video))
	f.write('      <extension application="http://www.videolan.org/vlc/playlist/0">\n')
	f.write('        <vlc:option>start-time=%.3f</vlc:option>\n' % a)
	f.write('        <vlc:option>stop-time=%.3f</vlc:option>\n' % b)
	f.write('      </extension>\n')
	f.write('    </track>\n')

def footer(f):
	f.write('  </trackList>\n')
	f.write('</playlist>\n')

with io.open(sys.argv[2], "r", encoding='utf-8-sig') as fi:
	with open(sys.argv[3], "w") as fo:
		header(fo)
		
		while True:
			seq_s = fi.readline()
			if not seq_s: break
			seq_s = seq_s.strip()
			if not seq_s: raise Exception("empty seq")
			seq = int(seq_s)

			time_s = fi.readline()
			if not time_s: raise Exception("eof at time")
			time_s = time_s.strip()
			if not time_s: raise Exception("empty time")
			
			# 00:02:03,057 --> 00:02:05,263
			m = re.match(r'(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)', time_s)
			if not m: raise Exception("error parsing time " + time_s)
			
			h1 = m.group(1)
			m1 = m.group(2)
			s1 = m.group(3)
			o1 = m.group(4)
			
			h2 = m.group(5)
			m2 = m.group(6)
			s2 = m.group(7)
			o2 = m.group(8)
			
			start = int(h1)*3600 + int(m1)*60 + int(s1) + int(o1) * 0.001
			stop  = int(h2)*3600 + int(m2)*60 + int(s2) + int(o2) * 0.001

			lines = []
			while True:
				line = fi.readline()
				if not line: raise Exception("eof in text")
				line = line.strip()
				if not line: break
				lines.append(line)
			
			entry(fo, last, start)
			last = stop
		
		entry(fo, stop, 3600*10)
		footer(fo)
