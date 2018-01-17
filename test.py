def f(ts):
	def find_left(ss,start,target):
		if start>len(ss)-1:
			start=len(ss)-1
		while start>=0:
			if ss[start]==target:
				return start
			start=start-1
		return -1
	def find_right(ss,start,target):
		while start<len(ss):
			if ss[start]==target:
				return start
			start=start+1
		return -1
	m=100
	p=find_left(ts,m-1,'<')
	print('18%d'%p)
	if p!=-1:
		t=find_right(ts,p+1,'>')
		if t==-1:
			pass
		else:
			if ts[t-1]=='/':
				if t>=m-1:
					m=t+1
			else:
				s=''
				while ts[p]!=' ' and ts[p]!='>':
					s=s+ts[p]
				if s in ['hr','img']:
					if p>m-1:
						m=p+1
				else:
					t=find_right(ts,t,'<')
					t=find_right(ts,t,'>')
					m=t+1
	else:
		pass
	ts=ts[:m]

file=open('/home/cvb/Documents/hello_pic.html','rU')
ts=file.read()
print(f(ts))