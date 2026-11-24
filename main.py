import sys
N=40000
A1,H1,A8,H8=91,98,21,28
ML,MU=19000,21000
V=dict(P=100,N=320,B=335,R=500,Q=950,K=20000)
D=dict(P=(-10,-20,-11,-9),N=(-21,-19,-12,-8,8,12,19,21),B=(-11,-9,9,11),R=(-10,-1,1,10),Q=(-11,-9,9,11,-10,-1,1,10),K=(-11,-9,9,11,-10,-1,1,10))
T={}
for p in V:
	t=[0]*120
	for r in range(8):
		for c in range(8):
			m=min(c,7-c)+min(r,7-r);a=7-r;s=V[p]
			if p=='P':s+=a*a*2+m*(0<a<6)*2
			if p in'NB':s+=m*6
			if p=='R':s+=12*(a==6)+m
			if p=='Q':s+=m*2
			if p=='K':s+=(2-a)*8 if a<3 else-a*8
			t[21+r*10+c]=s
	T[p]=t
class S:
	def __init__(A,b,sc,wc,bc,ep,kp):A.b,A.s,A.wc,A.bc,A.ep,A.kp=b,sc,wc,bc,ep,kp
	def rot(A):return S(A.b[::-1].swapcase(),-A.s,A.bc,A.wc,119-A.ep if A.ep else 0,119-A.kp if A.kp else 0)
	def gen(B):
		F=B.b
		for(C,H)in enumerate(F):
			if not H.isupper():continue
			for E in D[H]:
				for A in range(C+E,120 if E>0 else 0,E):
					G=F[A]
					if G.isspace()or G.isupper():break
					if H=='P':
						if E in(-10,-20)and G!='.':break
						if E==-20 and(C<A1-10 or F[C-10]!='.'):break
						if E in(-11,-9)and G=='.'and A not in(B.ep,B.kp,B.kp-1,B.kp+1):break
						if A8<=A<=H8:
							for I in'NBRQ':yield(C,A,I)
							break
					yield(C,A,'')
					if H in'PNK'or G.islower():break
					if C==A1 and F[A+1]=='K'and B.wc[0]:yield(A+1,A-1,'')
					if C==H1 and F[A-1]=='K'and B.wc[1]:yield(A-1,A+1,'')
	def mv(D,m):
		C,A,K=m;B=D.b;H=B[C]
		def E(b,i,x):return b[:i]+x+b[i+1:]
		L=D.s+D.val(m);B=E(E(B,A,H),C,'.');F,G,J,I=D.wc,D.bc,0,0
		if C==A1:F=0,F[1]
		if C==H1:F=F[0],0
		if A==A8:G=G[0],0
		if A==H8:G=0,G[1]
		if H=='K':
			F=0,0
			if abs(A-C)==2:I=(C+A)//2;B=E(E(B,A1 if A<C else H1,'.'),I,'R')
		if H=='P':
			if A8<=A<=H8:B=E(B,A,K)
			if A-C==-20:J=C-10
			if A==D.ep:B=E(B,A+10,'.')
		return S(B,L,F,G,J,I).rot()
	def val(E,m):
		C,A,H=m;F=E.b;D,G=F[C],F[A];B=T[D][A]-T[D][C]
		if G.islower():B+=T[G.upper()][119-A]
		if abs(A-E.kp)<2:B+=T['K'][119-A]
		if D=='K'and abs(C-A)==2:B+=T['R'][(C+A)//2]-T['R'][A1 if A<C else H1]
		if D=='P':
			if A8<=A<=H8:B+=T[H][A]-T['P'][A]
			if A==E.ep:B+=T['P'][119-A-10]
		return B
	def dead(A):return any(A.val(B)>=ML for B in A.gen())
class X(Exception):0
n=0
H={}
def ab(p,a,b,d):
	global n;n+=1
	if n>N:raise X
	if p.s<=-ML:return-MU
	if d<=0:
		if p.s>=b:return p.s
		a=max(a,p.s)
	E=p.b,p.wc,p.bc,p.ep,p.kp;A=H.get(E);F=0
	if A:
		F=A[2]
		if A[0]>=d>0 and(A[3]==0 or A[3]==1 and A[1]>=b or A[3]==2 and A[1]<=a):return A[1]
	D=sorted((A for A in p.gen()if d>0 or p.b[A[1]].islower()),key=lambda m:(m!=F,-p.val(m)));B=-MU-1;G=0;J=a
	for I in D:
		C=-ab(p.mv(I),-b,-a,d-1)
		if C>B:B,G=C,I
		if C>a:a=C
		if a>=b:break
	if d>0:
		if B<=-ML and all(p.mv(A).dead()for A in D):
			if not p.rot().dead():return 0
		H[E]=d,B,G,1 if B>=b else 2 if B<=J else 0
	return B if D else p.s
def sq(c):return ord(c[0])-97+(8-int(c[1]))*10+21
def un(i):return chr((i-21)%10+97)+str(8-(i-21)//10)
def best(ms):
	I='\n';G=' ';global n;D=S(G*9+I+G*9+I+' rnbqkbnr\n pppppppp\n'+' ........\n'*4+' PPPPPPPP\n RNBQKBNR\n'+G*9+I+G*9+I,0,(1,1),(1,1),0,0)
	for(M,C)in enumerate(ms):
		A,B=sq(C[:2]),sq(C[2:4])
		if M%2:A,B=119-A,119-B
		D=D.mv((A,B,C[4:].upper()))
	n=0;H.clear();E=[A for A in D.gen()if not D.mv(A).dead()]
	if not E:return'0000'
	J=E[0]
	try:
		for N in range(1,30):
			E.sort(key=lambda m:m!=J);F=-MU-1;K=E[0]
			for C in E:
				L=-ab(D.mv(C),-MU-2,-F,N-1)
				if L>F:F,K=L,C
			J=K
			if F>=ML:break
	except X:0
	A,B,O=J
	if len(ms)%2:A,B=119-A,119-B
	return un(A)+un(B)+O.lower()
def main():
	C='moves';B=True
	for D in sys.stdin:
		A=D.split()
		if A[:1]==['position']:E=A[A.index(C)+1:]if C in A else[]
		elif A[:1]==['go']:print('bestmove',best(E),flush=B)
		elif A[:1]==['uci']:print('uciok',flush=B)
		elif A[:1]==['isready']:print('readyok',flush=B)
		elif A[:1]==['quit']:break
ms=[]
if __name__=='__main__':main()