from math import sin, cos, pi, sqrt
from pyglet.gl import *
from pyglet.window import key
import copy
import glob
import json
import os
import pyglet.image as ScrImage
import time



class Collision:
	def  __init__(self,par):
		self.par=par
		self.boxes=[]
		self.buttons=[]
		self.buttonsC=[]
		self.lock=False
		self.MAX_DISTANCE=40
		self.chk=True
	def b_upress(self):
		for c in self.buttonsC:c.unpress()
	def process(self):
		self.boxes=[]
		self.buttons=[]
		self.buttonsC=[]
		for mdl in self.par.models:
			self.boxes+=[mdl.hbox]
			if mdl.__class__.__name__=="Button":
				self.buttons+=[mdl.hbox]
				self.buttonsC+=[mdl]
	def chk_dst(self,pos):
		pd=sqrt(pos[0]**2+pos[1]**2+pos[2]**2)
		if self.MAX_DISTANCE-3<=pd:
			n=1-abs(self.MAX_DISTANCE-pd)/3
			self.par.col=[n*-0.025+1,n*-0.4+1,n*-0.4+1,0]
		else:
			self.par.col=[1,1,1,0]
		return self.MAX_DISTANCE<pd
	# def ext_box(self,box):
	# 	def chk(n,b):
	# 		if n>0:return n+b
	# 		return -n-b
	# 	nbox=copy.deepcopy(box)
	# 	n=1/16
	# 	d=sqrt((box[3]-box[0])**2+(box[4]-box[1])**2+(box[5]-box[2])**2)
	# 	nbox[0]=chk(sqrt(((d+n)**2)/(1+(box[1]-box[4])/(box[0]-box[3])+(box[2]-box[5])/(box[0]-box[3]))),box[0])
	# 	nbox[3]=chk(-sqrt(((d+n)**2)/(1+(box[1]-box[4])/(box[0]-box[3])+(box[2]-box[5])/(box[0]-box[3]))),box[0])
	# 	return nbox
	def check(self,pos):
		if (self.chk_dst(pos)):return False
		if (not self.chk):return True
		for b in self.boxes:
			if (((b[0]<=pos[0]<=b[3]) or (b[0]>=pos[0]>=b[3])) and ((b[1]<=pos[1]<=b[4]) or (b[1]>=pos[1]>=b[4])) and ((b[2]<=pos[2]<=b[5]) or (b[2]>=pos[2]>=b[5]))):
				if len(b)==7 and b[6]==1:
					self.lock=True
					self.par.end=True
					return False
				if b in self.buttons:
					self.buttonsC[self.buttons.index(b)].press()
				return False
		return True
	def togg(self):
		self.chk=not self.chk
class Button:
	def __init__(self,slf,pos,nms,orientation,tex_coords=("t2f",(0,0,1,0,1,1,0,1)),action=None,tags=""):
		if type(nms)==str:
			if nms.split(":")[1]=="btn":
				nms=[f'{nms.split(":")[0]}/btn_side.png',f'{nms.split(":")[0]}/btn_top.png']
		self.s=self.get_tex(nms[0])
		self.t=self.get_tex(nms[1])
		self.d=orientation
		self.actioncmd=action
		self.hbox=[0]*6
		self.h=3
		self.slf=slf
		self.transition=[0]*6
		self.waitT=0
		self.visible=True
		self.transl=[]
		self.tags=tags.split(" ")
		self.pos=[int(pos[0]),int(pos[1]),int(pos[2])]
		self.tc=tex_coords
		self.create()
	def get_tex(self,n):
		tex=pyglet.image.load(f"./img/{n}").texture
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
		return pyglet.graphics.TextureGroup(tex)
	def create(self):
		self.batch=pyglet.graphics.Batch()
		if self.d=="U":
			x,y,z=self.pos[0],self.pos[1],self.pos[2]
			X,Y,Z=self.pos[0]+1,self.pos[1]+self.h/16,self.pos[2]+1
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,Z,X,y,z,X,Y,z,X,Y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.t,("v3f",(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,z,x,y,z,x,Y,z,X,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)),self.tc)
		elif self.d=="D":
			x,y,z=self.pos[0],self.pos[1]+(16-self.h)/16,self.pos[2]
			X,Y,Z=self.pos[0]+1,self.pos[1]+1,self.pos[2]+1
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,Z,X,y,z,X,Y,z,X,Y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.t,("v3f",(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,z,x,y,z,x,Y,z,X,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)),self.tc)
		elif self.d=="W":
			x,y,z=self.pos[0],self.pos[1],self.pos[2]
			X,Y,Z=self.pos[0]+self.h/16,self.pos[1]+1,self.pos[2]+1
			self.batch.add(4,GL_QUADS,self.t,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,z,x,y,z,x,Y,z,X,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)),self.tc)
		elif self.d=="E":
			x,y,z=self.pos[0]+(16-self.h)/16,self.pos[1],self.pos[2]
			X,Y,Z=self.pos[0]+1,self.pos[1]+1,self.pos[2]+1
			self.batch.add(4,GL_QUADS,self.t,("v3f",(X,y,Z,X,y,z,X,Y,z,X,Y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,z,x,y,z,x,Y,z,X,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)),self.tc)
		elif self.d=="S":
			x,y,z=self.pos[0],self.pos[1],self.pos[2]
			X,Y,Z=self.pos[0]+1,self.pos[1]+1,self.pos[2]+self.h/16
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,Z,X,y,z,X,Y,z,X,Y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.t,("v3f",(X,y,z,x,y,z,x,Y,z,X,Y,z)),self.tc)
		elif self.d=="N":
			x,y,z=self.pos[0],self.pos[1],self.pos[2]+(16-self.h)/16
			X,Y,Z=self.pos[0]+1,self.pos[1]+1,self.pos[2]+1
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,Z,X,y,z,X,Y,z,X,Y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.t,("v3f",(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)),self.tc)
		self.hbox=[x,y,z,X,Y,Z]
		self.slf.cam.coll.process()
	def f_pos(self):
		for i in range(len(self.pos)):
			if str(self.pos[i]).count("9")>5:self.pos[i]=round(self.pos[i]*100)/100
	def draw(self):
		if self.visible:
			if self.waitT!=0:
				if time.time()>=self.waitT:
					self.waitT=0
					if len(self.transl)>0:self.action(self.transl[0])
			else:
				if self.transition[0]!=0:
					self.pos[0]+=self.transition[0]
				if self.transition[1]!=0:
					self.pos[1]+=self.transition[1]
				if self.transition[2]!=0:
					self.pos[2]+=self.transition[2]
				if self.transition!=[0]*6:
					self.create()
					self.f_pos()
					if int(self.pos[0]*10)/10==self.transition[3]:self.transition[0]=0;self.pos[0]=self.transition[3];self.transition[3]=0
					if int(self.pos[1]*10)/10==self.transition[4]:self.transition[1]=0;self.pos[1]=self.transition[4];self.transition[4]=0
					if int(self.pos[2]*10)/10==self.transition[5]:self.transition[2]=0;self.pos[2]=self.transition[5];self.transition[5]=0
					if self.transition==[0]*6:
						self.pos=[int(self.pos[0]),int(self.pos[1]),int(self.pos[2])]
						self.create()
						if len(self.transl)>0:self.action(self.transl[0])
			try:
				self.batch.draw()
			except BaseException:
				self.create();self.batch.draw()
	def press(self):
		if self.h==3:
			self.h=1
			self.create()
			for b in self.actioncmd:
				for n in self.slf.models:
					if b["tag"] in n.tags:
						n.transl+=b["translate"]
						if n.transition==[0]*6:n.action(n.transl[0])
	def unpress(self):
		if self.h==1:
			self.h=3
			self.create()
	def destroy(self):
		self.batch=None
		self.hbox=[0]*6
		self.visible=False
		self.slf.cam.coll.process()
	def unshift(self,l):
		l2=[]
		for i in range(1,len(l)):l2+=[l[i]]
		return l2
	def action(self,trns):
		self.transl=self.unshift(self.transl)
		if trns=="destroy":
			self.destroy()
		else:
			if "wait_time" in list(trns.keys()):
				self.waitT=time.time()+trns["wait_time"]
			else:
				for t in range(len(trns["time"])):
					if trns["time"][t]<=0:trns["time"][t]=1
				self.transition=[((self.pos[0]+trns["pos"][0])-self.pos[0])/trns["time"][0],((self.pos[1]+trns["pos"][1])-self.pos[1])/trns["time"][1],((self.pos[2]+trns["pos"][2])-self.pos[2])/trns["time"][2],self.pos[0]+trns["pos"][0],self.pos[1]+trns["pos"][1],self.pos[2]+trns["pos"][2]]
class Block:
	def __init__(self,slf,pos,nms,tex_coords=("t2f",(0,0,1,0,1,1,0,1)),dims=(1,1,1),tags=""):
		if type(nms)==str:
			pr=nms.split(":")[0]
			if nms.split(":")[1]=="edgeX":
				nms=["corner.png","edgeX.png","corner.png","edgeX.png","edgeX.png","edgeX.png"]
			elif nms.split(":")[1]=="edgeY":
				nms=["edgeZ.png","edgeZ.png","edgeZ.png","edgeZ.png","corner.png","corner.png"]
			elif nms.split(":")[1]=="edgeZ":
				nms=["edgeX.png","corner.png","edgeX.png","corner.png","edgeZ.png","edgeZ.png"]
			elif nms.split(":")[1]=="wallX":
				nms=["wallS.png","edgeZ.png","wallS.png","edgeZ.png","edgeZ.png","edgeZ.png"]
			elif nms.split(":")[1]=="wallY":
				nms=["edgeX.png","edgeX.png","edgeX.png","edgeX.png","wallS.png","wallS.png"]
			elif nms.split(":")[1]=="wallZ":
				nms=["edgeZ.png","wallS.png","edgeZ.png","wallS.png","edgeX.png","edgeX.png"]
			elif nms.split(":")[1]=="corner":
				nms=["corner.png"]*6
			for i in range(len(nms)):
				nms[i]=f"{pr}/{nms[i]}"
		self.w=self.get_tex(nms[0])
		self.s=self.get_tex(nms[1])
		self.e=self.get_tex(nms[2])
		self.n=self.get_tex(nms[3])
		self.u=self.get_tex(nms[4])
		self.d=self.get_tex(nms[5])
		self.pos=[int(pos[0]),int(pos[1]),int(pos[2])]
		self.dims=dims
		self.visible=True
		self.slf=slf
		self.hbox=[0]*6
		self.transition=[0]*6
		self.waitT=0
		self.transl=[]
		self.tags=tags.split(" ")
		self.tc=tex_coords
		self.create()
	def f_pos(self):
		for i in range(len(self.pos)):
			if str(self.pos[i]).count("9")>5:self.pos[i]=round(self.pos[i]*100)/100
	def draw(self):
		if self.visible:
			if self.waitT!=0:
				if time.time()>=self.waitT:
					self.waitT=0
					if len(self.transl)>0:self.action(self.transl[0])
			else:
				if self.transition[0]!=0:
					self.pos[0]+=self.transition[0]
				if self.transition[1]!=0:
					self.pos[1]+=self.transition[1]
				if self.transition[2]!=0:
					self.pos[2]+=self.transition[2]
				if self.transition!=[0]*6:
					self.create()
					self.f_pos()
					if int(self.pos[0]*10)/10==self.transition[3]:self.transition[0]=0;self.pos[0]=self.transition[3];self.transition[3]=0
					if int(self.pos[1]*10)/10==self.transition[4]:self.transition[1]=0;self.pos[1]=self.transition[4];self.transition[4]=0
					if int(self.pos[2]*10)/10==self.transition[5]:self.transition[2]=0;self.pos[2]=self.transition[5];self.transition[5]=0
					if self.transition==[0]*6:
						self.pos=[int(self.pos[0]),int(self.pos[1]),int(self.pos[2])]
						self.create()
						if len(self.transl)>0:self.action(self.transl[0])
			try:
				self.batch.draw()
			except BaseException:
				self.create();self.batch.draw()
	def get_tex(self,n):
		tex=pyglet.image.load(f"./img/{n}").texture
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
		return pyglet.graphics.TextureGroup(tex)
	def create(self):
		self.hbox=self.pos+[self.pos[0]+self.dims[0],self.pos[1]+self.dims[1],self.pos[2]+self.dims[2]]
		x,y,z=self.pos[0],self.pos[1],self.pos[2]
		X,Y,Z=self.pos[0]+self.dims[0],self.pos[1]+self.dims[1],self.pos[2]+self.dims[2]
		self.batch=pyglet.graphics.Batch()
		self.batch.add(4,GL_QUADS,self.w,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),self.tc)
		self.batch.add(4,GL_QUADS,self.e,("v3f",(X,y,Z,X,y,z,X,Y,z,X,Y,Z)),self.tc)
		self.batch.add(4,GL_QUADS,self.d,("v3f",(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tc)
		self.batch.add(4,GL_QUADS,self.u,("v3f",(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tc)
		self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,z,x,y,z,x,Y,z,X,Y,z)),self.tc)
		self.batch.add(4,GL_QUADS,self.n,("v3f",(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)),self.tc)
		self.slf.cam.coll.process()
	def destroy(self):
		self.batch=None
		self.hbox=[0]*6
		self.visible=False
		self.slf.cam.coll.process()
	def unshift(self,l):
		l2=[]
		for i in range(1,len(l)):l2+=[l[i]]
		return l2
	def action(self,trns):
		self.transl=self.unshift(self.transl)
		if trns=="destroy":
			self.destroy()
		else:
			if "wait_time" in list(trns.keys()):
				self.waitT=time.time()+trns["wait_time"]
			else:
				for t in range(len(trns["time"])):
					if trns["time"][t]<=0:trns["time"][t]=1
				self.transition=[((self.pos[0]+trns["pos"][0])-self.pos[0])/trns["time"][0],((self.pos[1]+trns["pos"][1])-self.pos[1])/trns["time"][1],((self.pos[2]+trns["pos"][2])-self.pos[2])/trns["time"][2],self.pos[0]+trns["pos"][0],self.pos[1]+trns["pos"][1],self.pos[2]+trns["pos"][2]]
class EndBlock:
	def __init__(self,slf,pos,nms,tex_coords=("t2f",(0,0,1,0,1,1,0,1)),tags=""):
		if type(nms)==str:
			if nms.split(":")[1]=="end":
				nms=f'{nms.split(":")[0]}/end.png'
		self.pos=pos
		self.tags=tags.split(" ")
		self.slf=slf
		self.tex=self.get_tex(nms)
		self.tc=tex_coords
		self.pos=[int(pos[0]),int(pos[1]),int(pos[2])]
		self.transition=[0]*6
		self.transl=[]
		self.waitT=0
		self.hbox=[0]*7
		self.create()
	def get_tex(self,n):
		tex=pyglet.image.load(f"./img/{n}").texture
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
		return pyglet.graphics.TextureGroup(tex)
	def f_pos(self):
		for i in range(len(self.pos)):
			if str(self.pos[i]).count("9")>5:self.pos[i]=round(self.pos[i]*100)/100
	def draw(self):
		if self.waitT!=0:
			if time.time()>=self.waitT:
				self.waitT=0
				if len(self.transl)>0:self.action(self.transl[0])
		else:
			if self.transition[0]!=0:
				self.pos[0]+=self.transition[0]
			if self.transition[1]!=0:
				self.pos[1]+=self.transition[1]
			if self.transition[2]!=0:
				self.pos[2]+=self.transition[2]
			if self.transition!=[0]*6:
				self.create()
				self.f_pos()
				if int(self.pos[0]*10)/10==self.transition[3]:self.transition[0]=0;self.pos[0]=self.transition[3];self.transition[3]=0
				if int(self.pos[1]*10)/10==self.transition[4]:self.transition[1]=0;self.pos[1]=self.transition[4];self.transition[4]=0
				if int(self.pos[2]*10)/10==self.transition[5]:self.transition[2]=0;self.pos[2]=self.transition[5];self.transition[5]=0
				if self.transition==[0]*6:
					self.pos=[int(self.pos[0]),int(self.pos[1]),int(self.pos[2])]
					self.create()
					if len(self.transl)>0:self.action(self.transl[0])
					else:self.hbox[6]=1
		try:
			self.batch.draw()
		except BaseException:
			self.create();self.batch.draw()
	def cube(self,x,y,z,s=3):
		X,Y,Z=x+s/16,y+s/16,z+s/16
		self.batch.add(4,GL_QUADS,self.tex,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),self.tc)
		self.batch.add(4,GL_QUADS,self.tex,("v3f",(X,y,Z,X,y,z,X,Y,z,X,Y,Z)),self.tc)
		self.batch.add(4,GL_QUADS,self.tex,("v3f",(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tc)
		self.batch.add(4,GL_QUADS,self.tex,("v3f",(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tc)
		self.batch.add(4,GL_QUADS,self.tex,("v3f",(X,y,z,x,y,z,x,Y,z,X,Y,z)),self.tc)
		self.batch.add(4,GL_QUADS,self.tex,("v3f",(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)),self.tc)
	def create(self):
		self.hbox=[self.pos[0]+5/16,self.pos[1]+5/16,self.pos[2]+5/16,self.pos[0]+11/16,self.pos[1]+11/16,self.pos[2]+11/16,1]
		self.batch=pyglet.graphics.Batch()
		[x,y,z]=self.pos
		X,Y,Z=x+13/16,y+13/16,z+13/16
		self.cube(x,y,z)
		self.cube(X,y,z)
		self.cube(x,y,Z)
		self.cube(X,y,Z)
		self.cube(x,Y,z)
		self.cube(X,Y,z)
		self.cube(x,Y,Z)
		self.cube(X,Y,Z)
		self.cube(x+7/16,y+7/16,z+7/16,s=2)
		glLineWidth(2)
		X,Y,Z=x+1,y+1,z+1
		self.batch.add(2,GL_LINES,None,('v3f',(x,y,z,X,Y,Z)),('c3B',(102,)*6))
		self.batch.add(2,GL_LINES,None,('v3f',(X,y,z,x,Y,Z)),('c3B',(102,)*6))
		self.batch.add(2,GL_LINES,None,('v3f',(x,y,Z,X,Y,z)),('c3B',(102,)*6))
		self.batch.add(2,GL_LINES,None,('v3f',(X,y,Z,x,Y,z)),('c3B',(102,)*6))
		self.slf.cam.coll.process()
	def unshift(self,l):
		l2=[]
		for i in range(1,len(l)):l2+=[l[i]]
		return l2
	def action(self,trns):
		self.hbox[6]=0
		self.transl=self.unshift(self.transl)
		if trns=="destroy":
			self.destroy()
		else:
			if "wait_time" in list(trns.keys()):
				self.waitT=time.time()+trns["wait_time"]
			else:
				for t in range(len(trns["time"])):
					if trns["time"][t]<=0:trns["time"][t]=1
				self.transition=[((self.pos[0]+trns["pos"][0])-self.pos[0])/trns["time"][0],((self.pos[1]+trns["pos"][1])-self.pos[1])/trns["time"][1],((self.pos[2]+trns["pos"][2])-self.pos[2])/trns["time"][2],self.pos[0]+trns["pos"][0],self.pos[1]+trns["pos"][1],self.pos[2]+trns["pos"][2]]
class Camera:
	def __init__(self,par,pos=(0,0,0),rot=(0,0)):
		self.coll=Collision(par)
		self.speed=1
		self.pos=list(pos)
		self.rot=list(rot)
		self.sp={}
		self.ep={}
		self.lock=False
	def set(self,d):
		self.sp=copy.deepcopy(d)
		self.pos=d["pos"]
		self.rot=d["rot"]
	def reset(self):
		self.pos=self.sp["pos"]
		self.rot=self.sp["rot"]
		self.coll.b_upress()
	def end(self):
		self.pos=self.sp["epos"]
		self.rot=self.sp["erot"]
	def mouse_motion(self,dx,dy):
		if not self.lock:
			dx/=8;dy/=8
			self.rot[0]+=dy
			self.rot[1]-=dx
			self.rot[0]=90 if self.rot[0]>90 else self.rot[0]
			self.rot[0]=-90 if self.rot[0]<-90 else self.rot[0]
	def update(self,dt,keys):
		if not self.lock:
			dx=dt*7*self.speed*sin(-self.rot[1]/180*pi)
			dy=dt*7*self.speed
			dz=dt*7*self.speed*cos(-self.rot[1]/180*pi)
			self.pos=[self.pos[0]+dx,self.pos[1],self.pos[2]-dz] if keys[key.W] and self.coll.check([self.pos[0]+dx,self.pos[1],self.pos[2]-dz]) else self.pos
			self.pos=[self.pos[0]-dx,self.pos[1],self.pos[2]+dz] if keys[key.S] and self.coll.check([self.pos[0]-dx,self.pos[1],self.pos[2]+dz]) else self.pos
			self.pos=[self.pos[0]-dz,self.pos[1],self.pos[2]-dx] if keys[key.A] and self.coll.check([self.pos[0]-dx,self.pos[1],self.pos[2]-dz]) else self.pos
			self.pos=[self.pos[0]+dz,self.pos[1],self.pos[2]+dx] if keys[key.D] and self.coll.check([self.pos[0]+dx,self.pos[1],self.pos[2]+dz]) else self.pos
			self.pos=[self.pos[0],self.pos[1]+dy,self.pos[2]] if keys[key.SPACE] and self.coll.check([self.pos[0],self.pos[1]+dy,self.pos[2]]) else self.pos
			self.pos=[self.pos[0],self.pos[1]-dy,self.pos[2]] if (keys[key.LSHIFT] or keys[key.RSHIFT]) and self.coll.check([self.pos[0],self.pos[1]-dy,self.pos[2]]) else self.pos
			self.speed=2 if (keys[key.LCTRL] or keys[key.RCTRL]) else self.speed
			self.speed=1 if (not keys[key.LCTRL] and not keys[key.RCTRL] and not keys[key.W] and not keys[key.A] and not keys[key.S] and not keys[key.D] and not keys[key.SPACE] and not keys[key.LSHIFT] and not keys[key.RSHIFT]) else self.speed
			self.lock=self.coll.lock
class World:
	def __init__(self,slf):
		self.lvl_list=[]
		self.levels=self.read()
		self.cli=0
		self.last=False
		self.slf=slf
	def read(self):
		lvls={}
		for fn in glob.iglob(".\\levels\\*.json"):
			with open(fn,"r") as f:
				if fn.replace(".\\levels\\","").replace(".json","")!="levels":
					lvls[fn.replace(".\\levels\\","").replace(".json","")]=json.loads(f.read())
				else:
					self.lvl_list=json.loads(f.read())
		return lvls
	def get(self,ln):
		return self.parse(self.levels[ln])
	def next(self):
		self.get(self.lvl_list[self.cli])
		if self.cli+1<len(self.lvl_list):
			self.cli+=1
		else:
			self.last=True
	def end_level(self):
		if self.end_anim is not None:
			for b in self.end_anim["animation"]:
				for n in self.slf.models:
					if b["tag"] in n.tags:
						n.transl+=b["translate"]
						if n.transition==[0]*6:n.action(n.transl[0])
			self.end_anim=None
	def parse(self,l):
		models=[]
		player=None
		endblock=None
		end_anim=None
		for obj in l:
			if obj["type"]=="block":
				models+=[Block(self.slf,obj["pos"],obj["tex"],dims=obj["size"],tags=obj["tags"])]
			elif obj["type"]=="button":
				models+=[Button(self.slf,obj["pos"],obj["tex"],obj["direction"],action=obj["action"],tags=obj["tags"])]
			elif obj["type"]=="endblock":
				endblock=obj
			elif obj["type"]=="player":
				player={"pos":obj["start_pos"],"rot":obj["start_rot"],"epos":obj["end_pos"],"erot":obj["end_rot"]}
			elif obj["type"]=="end_trigger":
				end_anim=obj
		if player is not None:
			self.slf.cam.set(player)
		if endblock is not None:
			models+=[EndBlock(self.slf,endblock["pos"],endblock["tex"],tags=endblock["tags"])]
		self.end_anim=end_anim
		self.slf.models+=models
		self.slf.cam.coll.process()
class Main(pyglet.window.Window):
	def __init__(self):
		super().__init__(caption="Perspective",resizable=False,fullscreen=True)
		glClearColor(1,1,1,0)
		glEnable(GL_DEPTH_TEST)
		self.models=[]
		self.col=[1,1,1,0]
		self.dr_fps=False
		self.end=False
		self.darker=False
		self.scn=self.get_scn()
		self.tend=False
		self.world=World(self)
		self.cam=Camera(self)
		self.set_exclusive_mouse(1)
		self.keys=key.KeyStateHandler()
		self.push_handlers(self.keys)
		pyglet.clock.schedule(self.update)
		self.fps=pyglet.clock.ClockDisplay()
		self.world.next()
		pyglet.app.run()
	def on_mouse_motion(self,x,y,dx,dy):
		self.cam.mouse_motion(dx,dy)
	def on_key_press(self,KEY,MOD):
		if not self.tend and KEY==key.ESCAPE:
			self.close()
		if not self.tend and KEY==key.Q:
			self.cam.coll.togg()
		if not self.tend and KEY==key.F:
			self.dr_fps=not self.dr_fps
		if KEY==key.F1:
			if not os.path.isdir("./screenshots"):
				os.makedirs("./screenshots")
			ScrImage.get_buffer_manager().get_color_buffer().save(f"./screenshots/{self.scn}.png")
			self.scn+=1
		if self.tend and KEY==key.SPACE:
			if self.world.last:
				self.close()
			else:
				self.next()
	def update(self,dt):
		self.cam.update(dt,self.keys)
	def get_scn(self):
		return len(list(glob.iglob("./screenshots/*.png")))+1
	def next(self):
		glClearColor(1,1,1,0)
		self.tend=False
		self.models.clear()
		self.col=[1,1,1,0]
		self.dr_fps=False
		self.end=False
		self.darker=False
		self.cam=Camera(self)
		self.world.next()
	def on_draw(self):
		if self.end and not self.darker:
			self.cam.end()
			self.dr_fps=False
			if self.world.end_anim is not None:self.world.end_level()
			d=True
			for mdl in self.models:
				if not (mdl.transl==[] and (mdl.transition==[0]*6 or mdl.transition==[0]*6+[1])):
					d=False
			if d:
				self.darker=True
		if self.darker:
			self.dr_fps=False
			s=True
			for i in range(3):
				if self.col[i]>-0.5:
					s=False
					self.col[i]-=0.02
			if s:
				self.tend=True
		glClearColor(self.col[0],self.col[1],self.col[2],self.col[3])
		self.clear()
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(70,self.width/self.height,0.05,1000)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glPushMatrix()
		glRotatef(-self.cam.rot[0],1,0,0)
		glRotatef(-self.cam.rot[1],0,1,0)
		glTranslatef(-self.cam.pos[0],-self.cam.pos[1],-self.cam.pos[2])
		for mdl in self.models:mdl.draw()
		glPopMatrix()
		if self.dr_fps:
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()
			gluOrtho2D(0,self.width,0,self.height)
			glMatrixMode(GL_MODELVIEW)
			glLoadIdentity()
			self.fps.draw()
if __name__=="__main__":Main()
