from math import sin, cos, pi, sqrt, floor
from pyglet.gl import *
from pyglet.window import key
import copy
import json
import os
import time



SAVEFILENAME="lvl-2"
OPENFILENAME="lvl-1"
class Collision:
	def  __init__(self,par):
		self.par=par
		self.boxes=[]
		self.buttons=[]
		self.buttonsC=[]
		self.eblk=[None]*2
		self.lock=False
		self.MAX_DISTANCE=40
		self.chk=False
	def b_upress(self):
		for c in self.buttonsC:c.unpress()
	def reset(self):
		for mdl in self.par.models:
			mdl.reset()
		self.b_upress()
	def process(self):
		self.boxes=[]
		self.buttons=[]
		self.buttonsC=[]
		self.eblk=[None]*2
		for mdl in self.par.models:
			self.boxes+=[mdl.hbox]
			if mdl.__class__.__name__=="Button":
				self.buttons+=[mdl.hbox]
				self.buttonsC+=[mdl]
			elif mdl.__class__.__name__=="EndBlock":
				self.eblk=[mdl.hbox,mdl]
	def chk_dst(self,pos):
		pd=sqrt(pos[0]**2+pos[1]**2+pos[2]**2)
		if self.MAX_DISTANCE-3<=pd:
			n=1-abs(self.MAX_DISTANCE-pd)/3
			self.par.col=[n*-0.025+1,n*-0.4+1,n*-0.4+1,0]
		else:
			self.par.col=[1,1,1,0]
		return self.MAX_DISTANCE<pd
	def check(self,pos):
		if (self.chk_dst(pos)):return False
		if (not self.chk):return True
		for b in self.boxes:
			if (((b[0]<=pos[0]<=b[3]) or (b[0]>=pos[0]>=b[3])) and ((b[1]<=pos[1]<=b[4]) or (b[1]>=pos[1]>=b[4])) and ((b[2]<=pos[2]<=b[5]) or (b[2]>=pos[2]>=b[5]))):
				if b==self.eblk[0] and (((self.eblk[1].ebox[0]<=pos[0]<=self.eblk[1].ebox[3]) or (self.eblk[1].ebox[0]>=pos[0]>=self.eblk[1].ebox[3])) and ((self.eblk[1].ebox[1]<=pos[1]<=self.eblk[1].ebox[4]) or (self.eblk[1].ebox[1]>=pos[1]>=self.eblk[1].ebox[4])) and ((self.eblk[1].ebox[2]<=pos[2]<=self.eblk[1].ebox[5]) or (self.eblk[1].ebox[2]>=pos[2]>=self.eblk[1].ebox[5]))):
					self.lock=True
					self.par.end=True
					return False
				elif b==self.eblk[0]:
					return True
				if b in self.buttons:
					self.buttonsC[self.buttons.index(b)].press()
				return False
		return True
	def togg(self):
		self.chk=not self.chk
class Button:
	def __init__(self,slf,pos,nms,orientation,tex_coords=("t2f",(0,0,1,0,1,1,0,1)),action=None,tags=""):
		self.d=orientation
		self.actioncmd=action or []
		self.hbox=[0]*6
		self.tbox=[0]*6
		self.h=3
		self.slf=slf
		self.transition=[0]*6
		self.waitT=0
		self.visible=True
		self.transl=[]
		self.tags=tags.split(" ")
		self.pos=[int(pos[0]),int(pos[1]),int(pos[2])]
		self.sp=[int(pos[0]),int(pos[1]),int(pos[2])]
		self.tc=tex_coords
		self.rt=nms+""
		self.theme(self.rt.split(":")[0])
	def tex_f(self,t):
		nms=f'{self.rt.split(":")[0]}:{t}'
		self.rt=nms+""
		if type(nms)==str:
			if nms.split(":")[1]=="btn":
				nms=[f'{nms.split(":")[0]}/btn_side.png',f'{nms.split(":")[0]}/btn_top.png']
		self.s=self.get_tex(nms[0])
		self.t=self.get_tex(nms[1])
		self.create()
	def theme(self,t):
		nms=f'{t}:{self.rt.split(":")[1]}'
		self.rt=nms+""
		if type(nms)==str:
			if nms.split(":")[1]=="btn":
				nms=[f'{nms.split(":")[0]}/btn_side.png',f'{nms.split(":")[0]}/btn_top.png']
		self.s=self.get_tex(nms[0])
		self.t=self.get_tex(nms[1])
		self.create()
	def set_d(self,d):
		self.d=d
		self.create()
	def reset(self):
		self.pos=copy.deepcopy(self.sp)
		self.hbox=[0]*6
		self.h=3
		self.transition=[0]*6
		self.waitT=0
		self.visible=True
		self.transl=[]
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
			x,y,z=self.pos[0]+(16-self.h)/16,self.pos[1],self.pos[2]
			X,Y,Z=self.pos[0]+1,self.pos[1]+1,self.pos[2]+1
			self.batch.add(4,GL_QUADS,self.t,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,z,x,y,z,x,Y,z,X,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)),self.tc)
		elif self.d=="E":
			x,y,z=self.pos[0],self.pos[1],self.pos[2]
			X,Y,Z=self.pos[0]+self.h/16,self.pos[1]+1,self.pos[2]+1
			self.batch.add(4,GL_QUADS,self.t,("v3f",(X,y,Z,X,y,z,X,Y,z,X,Y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,z,x,y,z,x,Y,z,X,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)),self.tc)
		elif self.d=="S":
			x,y,z=self.pos[0],self.pos[1],self.pos[2]+(16-self.h)/16
			X,Y,Z=self.pos[0]+1,self.pos[1]+1,self.pos[2]+1
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,Z,X,y,z,X,Y,z,X,Y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.t,("v3f",(X,y,z,x,y,z,x,Y,z,X,Y,z)),self.tc)
		elif self.d=="N":
			x,y,z=self.pos[0],self.pos[1],self.pos[2]
			X,Y,Z=self.pos[0]+1,self.pos[1]+1,self.pos[2]+self.h/16
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(X,y,Z,X,y,z,X,Y,z,X,Y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,y,z,X,y,z,X,y,Z,x,y,Z)),self.tc)
			self.batch.add(4,GL_QUADS,self.s,("v3f",(x,Y,Z,X,Y,Z,X,Y,z,x,Y,z)),self.tc)
			self.batch.add(4,GL_QUADS,self.t,("v3f",(x,y,Z,X,y,Z,X,Y,Z,x,Y,Z)),self.tc)
		self.hbox=[x,y,z,X,Y,Z]
		self.tbox=self.pos+[self.pos[0]+1,self.pos[1]+1,self.pos[2]+1]
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
	def move(self,x,y,z):
		self.pos[0]+=x
		self.sp[0]+=x
		self.pos[1]+=y
		self.sp[1]+=y
		self.pos[2]+=z
		self.sp[2]+=z
		self.create()
		self.slf.cam.coll.process()
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
		self.pos=[int(pos[0]),int(pos[1]),int(pos[2])]
		self.sp=[int(pos[0]),int(pos[1]),int(pos[2])]
		self.dims=list(dims)
		self.visible=True
		self.slf=slf
		self.hbox=[0]*6
		self.tbox=[0]*6
		self.transition=[0]*6
		self.waitT=0
		self.transl=[]
		self.tags=tags.split(" ")
		self.tc=tex_coords
		self.rt=nms+""
		self.theme(self.rt.split(":")[0])
	def reset(self):
		self.pos=copy.deepcopy(self.sp)
		self.visible=True
		self.hbox=[0]*6
		self.transition=[0]*6
		self.waitT=0
		self.transl=[]
		self.create()
	def tex_f(self,t):
		nms=f'{self.rt.split(":")[0]}:{t}'
		self.rt=nms+""
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
		self.create()
	def theme(self,t):
		nms=f'{t}:{self.rt.split(":")[1]}'
		self.rt=nms+""
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
		self.create()
	def f_pos(self):
		for i in range(len(self.pos)):
			if str(self.pos[i]).count("9")>5:self.pos[i]=round(self.pos[i]*100)/100
	def move(self,x,y,z):
		self.pos[0]+=x
		self.sp[0]+=x
		self.pos[1]+=y
		self.sp[1]+=y
		self.pos[2]+=z
		self.sp[2]+=z
		self.create()
		self.slf.cam.coll.process()
	def size(self,x,y,z):
		self.dims[0]+=x
		self.dims[1]+=y
		self.dims[2]+=z
		for i in range(len(self.dims)):
			if self.dims[i]<1:self.dims[i]=1
		self.create()
		self.slf.cam.coll.process()
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
		self.tbox=self.pos+[self.pos[0]+self.dims[0],self.pos[1]+self.dims[1],self.pos[2]+self.dims[2]]
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
		self.pos=[int(pos[0]),int(pos[1]),int(pos[2])]
		self.sp=[int(pos[0]),int(pos[1]),int(pos[2])]
		self.tags=tags.split(" ")
		self.slf=slf
		self.tc=tex_coords
		self.transition=[0]*6
		self.transl=[]
		self.waitT=0
		self.hbox=[0]*6
		self.tbox=[0]*6
		self.ebox=[0]*7
		self.rt=nms+""
		self.theme(self.rt.split(":")[0])
	def theme(self,t):
		nms=f'{t}:{self.rt.split(":")[1]}'
		self.rt=nms+""
		if type(nms)==str:
			if nms.split(":")[1]=="end":
				nms=f'{nms.split(":")[0]}/end.png'
		self.tex=self.get_tex(nms)
		self.create()
	def reset(self):
		self.pos=copy.deepcopy(self.sp)
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
	def move(self,x,y,z):
		self.pos[0]+=x
		self.sp[0]+=x
		self.pos[1]+=y
		self.sp[1]+=y
		self.pos[2]+=z
		self.sp[2]+=z
		self.create()
		self.slf.cam.coll.process()
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
		self.ebox=[self.pos[0]+5/16,self.pos[1]+5/16,self.pos[2]+5/16,self.pos[0]+11/16,self.pos[1]+11/16,self.pos[2]+11/16,1]
		self.hbox=self.pos+[self.pos[0]+1,self.pos[1]+1,self.pos[2]+1]
		self.tbox=self.pos+[self.pos[0]+1,self.pos[1]+1,self.pos[2]+1]
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
		self.par=par
		self.end_an_ru=False
		self.end_anim={"_comment":"end animation","type":"end_trigger","animation":[]}
		self.anim_target=[None]*2
		self.next_tag=0
		self.abl_crG=False
		self.abl_crH=False
		self.abl_crT=False
		self.draw_anim=False
		self.sh_cube=False
		self.last_stp_i=-1
		self.anim_drw_ln=[]
		self.MAX_D_WT=15
		self.MAX_D_T=30
		self.ctrlp=False
		self.sp={"pos":self.pos,"rot":self.rot}
		self.ep={"pos":self.pos,"rot":self.rot}
		self.f_ext_batch()
		self.c_f()
	def set(self,d):
		self.pos=d["pos"]
		self.rot=d["rot"]
		self.ep={"pos":d["epos"],"rot":d["erot"]}
		self.sp={"pos":self.pos,"rot":self.rot}
	def mouse_motion(self,dx,dy):
		dx/=8;dy/=8
		self.rot[0]+=dy
		self.rot[1]-=dx
		self.rot[0]=90 if self.rot[0]>90 else self.rot[0]
		self.rot[0]=-90 if self.rot[0]<-90 else self.rot[0]
	def move(self,x,y,z):
		self.pos[0]+=x
		self.pos[1]+=y
		self.pos[2]+=z
	def create_block(self,t):
		if self.abl_crT and self.abl_crG and self.abl_crH and not self.draw_anim:
			p=[floor(self.pos[0]),floor(self.pos[1]),floor(self.pos[2])]
			if t=="block":
				self.par.models+=[Block(self.par,p,"gray:corner",tags=f"blkId-{self.next_tag}")]
				self.next_tag+=1
				self.coll.process()
				return
			elif t=="button":
				self.par.models+=[Button(self.par,p,"gray:btn","U",tags=f"btnId-{self.next_tag}")]
				self.next_tag+=1
				self.coll.process()
				return
			elif t=="end_block":
				for mdli in range(len(self.par.models)-1,-1,-1):
					mdl=self.par.models[mdli]
					if mdl.__class__.__name__=="EndBlock":
						del self.par.models[mdli]
				self.par.models+=[EndBlock(self.par,p,"gray:end",tags=f"ebId-{self.next_tag}")]
				self.next_tag+=1
				self.coll.process()
	def delete_block(self):
		if not self.draw_anim:
			p=[floor(self.pos[0]),floor(self.pos[1]),floor(self.pos[2])]
			for mdli in range(len(self.par.models)-1,-1,-1):
				mdl=self.par.models[mdli]
				if self.b_chk(mdl.tbox,p):
					del self.par.models[mdli]
					self.coll.process()
					return
	def b_chk(self,b,pos):
		return (((b[0]<=pos[0]<=b[3]) or (b[0]>=pos[0]>=b[3])) and ((b[1]<=pos[1]<=b[4]) or (b[1]>=pos[1]>=b[4])) and ((b[2]<=pos[2]<=b[5]) or (b[2]>=pos[2]>=b[5])))
	def move_blk(self,KEY):
		if not self.draw_anim:
			p=[floor(self.pos[0]),floor(self.pos[1]),floor(self.pos[2])]
			for mdl in self.par.models:
				if self.b_chk(mdl.tbox,p):
					if KEY==key.J:mdl.move(1,0,0);self.move(1,0,0)
					if KEY==key.L:mdl.move(-1,0,0);self.move(-1,0,0)
					if KEY==key.I:mdl.move(0,1,0);self.move(0,1,0)
					if KEY==key.K:mdl.move(0,-1,0);self.move(0,-1,0)
					if KEY==key.U:mdl.move(0,0,1);self.move(0,0,1)
					if KEY==key.O:mdl.move(0,0,-1);self.move(0,0,-1)
					if mdl.__class__.__name__=="Block":
						if KEY==key.RIGHT:mdl.size(1,0,0)
						if KEY==key.LEFT:mdl.size(-1,0,0)
						if KEY==key.UP:mdl.size(0,1,0)
						if KEY==key.DOWN:mdl.size(0,-1,0)
						if KEY==key.SLASH:mdl.size(0,0,1)
						if KEY==key.PERIOD:mdl.size(0,0,-1)
					return
	def chk_toggle(self):
		if not self.ctrlp:
			if self.draw_anim:
				self.draw_anim=False
				self.anim_target=[None]*2
				self.anim_drw_ln=[]
				self.last_stp_i=-1
				self.f_ext_batch()
			else:
				p=[floor(self.pos[0]),floor(self.pos[1]),floor(self.pos[2])]
				for mdl in self.par.models:
					if self.b_chk(mdl.tbox,p) and mdl.__class__.__name__=="Button":
						self.draw_anim=True
						self.anim_target=[mdl,None]
						self.anim_drw_ln=[]
						self.last_stp_i=-1
						self.f_ext_batch()
		else:
			if self.draw_anim:
				self.draw_anim=False
				self.anim_target=[None]*2
				self.anim_drw_ln=[]
				self.last_stp_i=-1
			else:
				self.draw_anim=True
				self.anim_target=[self.end_anim,None]
				self.anim_drw_ln=[]
				self.last_stp_i=-1
			self.f_ext_batch()
	def ch_theme(self,keys):
		p=[floor(self.pos[0]),floor(self.pos[1]),floor(self.pos[2])]
		t=None
		if keys[key._1]:t="gray"
		if t is not None:
			for mdl in self.par.models:
				if self.b_chk(mdl.tbox,p):
					mdl.theme(t)
					return
	def ch_dir(self,keys):
		p=[floor(self.pos[0]),floor(self.pos[1]),floor(self.pos[2])]
		t=None
		if keys[key._1]:t="U"
		if keys[key._2]:t="D"
		if keys[key._3]:t="W"
		if keys[key._4]:t="S"
		if keys[key._5]:t="E"
		if keys[key._6]:t="N"
		if t is not None:
			for mdl in self.par.models:
				if mdl.__class__.__name__=="Button" and self.b_chk(mdl.tbox,p):
					mdl.set_d(t)
					return
	def ch_tex(self,keys):
		p=[floor(self.pos[0]),floor(self.pos[1]),floor(self.pos[2])]
		t=None
		tb=None
		if keys[key._1]:t="corner";tb="btn"
		if keys[key._2]:t="edgeX"
		if keys[key._3]:t="edgeY"
		if keys[key._4]:t="edgeZ"
		if keys[key._5]:t="wallX"
		if keys[key._6]:t="wallY"
		if keys[key._7]:t="wallZ"
		if t is not None:
			for mdl in self.par.models:
				if self.b_chk(mdl.tbox,p):
					if mdl.__class__.__name__=="Block":
						mdl.tex_f(t)
					elif tb is not None and mdl.__class__.__name__=="Button":
						mdl.tex_f(tb)
					return
	def add_anim_stp(self,stp):
		if type(self.anim_target[0])==dict:
			i=-1
			for at in self.anim_target[0]["animation"]:
				if at["tag"]==self.anim_target[1].tags[0]:
					i=self.anim_target[0]["animation"].index(at)
			if i==-1:
				i=len(self.anim_target[0]["animation"])
				self.anim_target[0]["animation"]+=[{"tag":self.anim_target[1].tags[0],"translate":[]}]
			self.last_stp_i=i
			if not (stp=="destroy" and self.anim_target[1].__class__.__name__=="EndBlock"):self.anim_target[0]["animation"][i]["translate"]+=[stp]
		else:
			i=-1
			for at in self.anim_target[0].actioncmd:
				if at["tag"]==self.anim_target[1].tags[0]:
					i=self.anim_target[0].actioncmd.index(at)
			if i==-1:
				i=len(self.anim_target[0].actioncmd)
				self.anim_target[0].actioncmd+=[{"tag":self.anim_target[1].tags[0],"translate":[]}]
			self.last_stp_i=i
			if not (stp=="destroy" and self.anim_target[1].__class__.__name__=="EndBlock"):self.anim_target[0].actioncmd[i]["translate"]+=[stp]
		self.f_ext_batch()
	def remove_anim_stp(self):
		if type(self.anim_target[0])==dict:
			for ati in range(len(self.anim_target[0]["animation"])-1,-1,-1):
				at=self.anim_target[0]["animation"][ati]
				if at["tag"]==self.anim_target[1].tags[0] and len(at["translate"])>0:
					del at["translate"][-1]
					if len(at["translate"])==0:
						self.last_stp_i=-1
						del self.anim_target[0]["animation"][ati]
					elif self.last_stp_i==len(at["translate"]):self.last_stp_i-=1
					self.f_ext_batch()
					return
		else:
			for ati in range(len(self.anim_target[0].actioncmd)-1,-1,-1):
				at=self.anim_target[0].actioncmd[ati]
				if at["tag"]==self.anim_target[1].tags[0] and len(at["translate"])>0:
					del at["translate"][-1]
					if len(at["translate"])==0:
						self.last_stp_i=-1
						del self.anim_target[0].actioncmd[ati]
					elif self.last_stp_i==len(at["translate"]):self.last_stp_i-=1
					self.f_ext_batch()
					return
	def time(self,xt,yt,zt):
		if self.last_stp_i>-1:
			if type(self.anim_target[0])==dict:
				if type(self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1])==dict and "pos" in list(self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1].keys()):
					self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["time"][0]+=xt
					self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["time"][1]+=yt
					self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["time"][2]+=zt
					for n in range(3):
						if self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["time"][n]<0:self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["time"][n]=0
						if self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["time"][n]>self.MAX_D_T:self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["time"][n]=self.MAX_D_T
			else:
				if type(self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1])==dict and "pos" in list(self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1].keys()):
					self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["time"][0]+=xt
					self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["time"][1]+=yt
					self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["time"][2]+=zt
					for n in range(3):
						if self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["time"][n]<0:self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["time"][n]=0
						if self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["time"][n]>self.MAX_D_T:self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["time"][n]=self.MAX_D_T
			self.f_ext_batch()
	def wtime(self,td):
		if self.last_stp_i>-1:
			if type(self.anim_target[0])==dict:
				if type(self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1])==dict and "wait_time" in list(self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1].keys()):
					self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["wait_time"]=round((self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["wait_time"]+td)*10)/10
					if self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["wait_time"]<0.1:self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["wait_time"]=0.1
					if self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["wait_time"]>self.MAX_D_WT:self.anim_target[0]["animation"][self.last_stp_i]["translate"][-1]["wait_time"]=self.MAX_D_WT
			else:
				if type(self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1])==dict and "wait_time" in list(self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1].keys()):
					self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["wait_time"]=round((self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["wait_time"]+td)*10)/10
					if self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["wait_time"]<0.1:self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["wait_time"]=0.1
					if self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["wait_time"]>self.MAX_D_WT:self.anim_target[0].actioncmd[self.last_stp_i]["translate"][-1]["wait_time"]=self.MAX_D_WT
			self.f_ext_batch()
	def draw_ext(self):
		self.ext_batch.draw()
		self.cb_b.draw()
	def g_mdl(self,t):
		for mdl in self.par.models:
			if mdl.tags[0]==t:
				return mdl
		return None
	def reset_blks(self):
		self.coll.reset()
		self.end_an_ru=False
	def c_f(self):
		self.cb_b=pyglet.graphics.Batch()
		if self.sh_cube:
			x,y,z=floor(self.pos[0]),floor(self.pos[1]),floor(self.pos[2])
			self.cb_b.add(2,GL_LINES,None,("v3f",(x,y,z,x,y,z+1)),("c3B",(0,)*6))
			self.cb_b.add(2,GL_LINES,None,("v3f",(x,y,z+1,x+1,y,z+1)),("c3B",(0,)*6))
			self.cb_b.add(2,GL_LINES,None,("v3f",(x+1,y,z+1,x+1,y,z)),("c3B",(0,)*6))
			self.cb_b.add(2,GL_LINES,None,("v3f",(x+1,y,z,x,y,z)),("c3B",(0,)*6))
			self.cb_b.add(2,GL_LINES,None,("v3f",(x,y+1,z,x,y+1,z+1)),("c3B",(0,)*6))
			self.cb_b.add(2,GL_LINES,None,("v3f",(x,y+1,z+1,x+1,y+1,z+1)),("c3B",(0,)*6))
			self.cb_b.add(2,GL_LINES,None,("v3f",(x+1,y+1,z+1,x+1,y+1,z)),("c3B",(0,)*6))
			self.cb_b.add(2,GL_LINES,None,("v3f",(x+1,y+1,z,x,y+1,z)),("c3B",(0,)*6))
			self.cb_b.add(2,GL_LINES,None,("v3f",(x,y,z,x,y+1,z)),("c3B",(0,)*6))
			self.cb_b.add(2,GL_LINES,None,("v3f",(x,y,z+1,x,y+1,z+1)),("c3B",(0,)*6))
			self.cb_b.add(2,GL_LINES,None,("v3f",(x+1,y,z+1,x+1,y+1,z+1)),("c3B",(0,)*6))
			self.cb_b.add(2,GL_LINES,None,("v3f",(x+1,y,z,x+1,y+1,z)),("c3B",(0,)*6))
	def f_ext_batch(self):
		self.ext_batch=pyglet.graphics.Batch()
		self.ext_batch.add(2,GL_LINES,None,("v3f",(-5/16,0,0,5/16,0,0)),("c3B",(100,0,0,220,0,0)))
		self.ext_batch.add(2,GL_LINES,None,("v3f",(0,-5/16,0,0,5/16,0)),("c3B",(0,100,0,0,220,0)))
		self.ext_batch.add(2,GL_LINES,None,("v3f",(0,0,-5/16,0,0,5/16)),("c3B",(0,0,100,0,0,220)))
		if self.anim_target[0] is not None:
			if type(self.anim_target[0])==dict:
				for ni in range(len(self.anim_target[0]["animation"])-1,-1,-1):
					n=self.anim_target[0]["animation"][ni]
					mdl=self.g_mdl(n["tag"])
					if mdl is None:
						del self.anim_target[0]["animation"][ni]
					else:
						p=mdl.sp
						for k in n["translate"]:
							if k=="destroy":
								[x,y,z]=p
								y-=0.003
								y-=6/16
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x-4/16,y,z-4/16,x-4/16,y,z+4/16,x+4/16,y,z+4/16,x+4/16,y,z-4/16)),("c3B",(0,220,220)*4))
							elif type(k)==dict and "wait_time" in list(k.keys()):
								[x,y,z]=p
								y-=0.001
								X=x-2/16+(k["wait_time"]*(0.25/self.MAX_D_WT))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-2/16,y,z-2/16,x-2/16,y,z+2/16)),("c3B",(220,220,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-2/16,y,z+2/16,x+2/16,y,z+2/16)),("c3B",(220,220,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+2/16,y,z+2/16,x+2/16,y,z-2/16)),("c3B",(220,220,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+2/16,y,z-2/16,x-2/16,y,z-2/16)),("c3B",(220,220,0)*2))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x-2/16,y,z-2/16,x-2/16,y,z+2/16,X,y,z+2/16,X,y,z-2/16)),("c3B",(220,220,0)*4))
							elif type(k)==dict and "pos" in list(k.keys()):
								[x,y,z]=p
								X,Y,Z=x+k["pos"][0],y+k["pos"][1],z+k["pos"][2]
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x,y,z,X,Y,Z)),("c3B",(220,0,220)*2))
								p=[X,Y,Z]
								del X,Y,Z
								[x,y,z]=p
								y-=0.002
								X,Y,Z=x-3/16+(k["time"][0]*((3/8)/self.MAX_D_T)),y-6/16+(k["time"][1]*((3/8)/self.MAX_D_T)),z-3/16+(k["time"][2]*((3/8)/self.MAX_D_T))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y,z-3/16,x-3/16,y,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y,z+3/16,x+3/16,y,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y,z+3/16,x+3/16,y,z-3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y,z-3/16,x-3/16,y,z-3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y-6/16,z-3/16,x-3/16,y-6/16,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y-6/16,z+3/16,x+3/16,y-6/16,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y-6/16,z+3/16,x+3/16,y-6/16,z-3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y-6/16,z-3/16,x-3/16,y-6/16,z-3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y,z-3/16,x-3/16,y-6/16,z-3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y,z+3/16,x-3/16,y-6/16,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y,z+3/16,x+3/16,y-6/16,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y,z-3/16,x+3/16,y-6/16,z-3/16)),("c3B",(220,128,0)*2))
								x-=3/16
								y-=6/16
								z-=3/16
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),("c3B",(220,0,0)*4))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(X,y,z,X,y,Z,X,Y,Z,X,Y,z)),("c3B",(220,0,0)*4))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x,y,z,x,y,Z,X,y,Z,X,y,z)),("c3B",(0,220,0)*4))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x,Y,z,x,Y,Z,X,Y,Z,X,Y,z)),("c3B",(0,220,0)*4))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x,y,z,x,Y,z,X,Y,z,X,y,z)),("c3B",(0,0,220)*4))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x,y,Z,x,Y,Z,X,Y,Z,X,y,Z)),("c3B",(0,0,220)*4))
						self.anim_drw_ln=[p]
			else:
				for ni in range(len(self.anim_target[0].actioncmd)-1,-1,-1):
					n=self.anim_target[0].actioncmd[ni]
					mdl=self.g_mdl(n["tag"])
					if mdl is None:
						del self.anim_target[0].actioncmd[ni]
					else:
						p=mdl.sp
						for k in n["translate"]:
							if k=="destroy":
								[x,y,z]=p
								y-=0.003
								y-=6/16
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x-4/16,y,z-4/16,x-4/16,y,z+4/16,x+4/16,y,z+4/16,x+4/16,y,z-4/16)),("c3B",(0,220,220)*4))
							elif type(k)==dict and "wait_time" in list(k.keys()):
								[x,y,z]=p
								y-=0.001
								X=x-2/16+(k["wait_time"]*(0.25/self.MAX_D_WT))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-2/16,y,z-2/16,x-2/16,y,z+2/16)),("c3B",(220,220,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-2/16,y,z+2/16,x+2/16,y,z+2/16)),("c3B",(220,220,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+2/16,y,z+2/16,x+2/16,y,z-2/16)),("c3B",(220,220,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+2/16,y,z-2/16,x-2/16,y,z-2/16)),("c3B",(220,220,0)*2))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x-2/16,y,z-2/16,x-2/16,y,z+2/16,X,y,z+2/16,X,y,z-2/16)),("c3B",(220,220,0)*4))
							elif type(k)==dict and "pos" in list(k.keys()):
								[x,y,z]=p
								X,Y,Z=x+k["pos"][0],y+k["pos"][1],z+k["pos"][2]
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x,y,z,X,Y,Z)),("c3B",(220,0,220)*2))
								p=[X,Y,Z]
								del X,Y,Z
								[x,y,z]=p
								y-=0.002
								X,Y,Z=x-3/16+(k["time"][0]*((3/8)/self.MAX_D_T)),y-6/16+(k["time"][1]*((3/8)/self.MAX_D_T)),z-3/16+(k["time"][2]*((3/8)/self.MAX_D_T))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y,z-3/16,x-3/16,y,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y,z+3/16,x+3/16,y,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y,z+3/16,x+3/16,y,z-3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y,z-3/16,x-3/16,y,z-3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y-6/16,z-3/16,x-3/16,y-6/16,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y-6/16,z+3/16,x+3/16,y-6/16,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y-6/16,z+3/16,x+3/16,y-6/16,z-3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y-6/16,z-3/16,x-3/16,y-6/16,z-3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y,z-3/16,x-3/16,y-6/16,z-3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x-3/16,y,z+3/16,x-3/16,y-6/16,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y,z+3/16,x+3/16,y-6/16,z+3/16)),("c3B",(220,128,0)*2))
								self.ext_batch.add(2,GL_LINES,None,("v3f",(x+3/16,y,z-3/16,x+3/16,y-6/16,z-3/16)),("c3B",(220,128,0)*2))
								x-=3/16
								y-=6/16
								z-=3/16
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x,y,z,x,y,Z,x,Y,Z,x,Y,z)),("c3B",(220,0,0)*4))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(X,y,z,X,y,Z,X,Y,Z,X,Y,z)),("c3B",(220,0,0)*4))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x,y,z,x,y,Z,X,y,Z,X,y,z)),("c3B",(0,220,0)*4))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x,Y,z,x,Y,Z,X,Y,Z,X,Y,z)),("c3B",(0,220,0)*4))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x,y,z,x,Y,z,X,Y,z,X,y,z)),("c3B",(0,0,220)*4))
								self.ext_batch.add(4,GL_QUADS,None,("v3f",(x,y,Z,x,Y,Z,X,Y,Z,X,y,Z)),("c3B",(0,0,220)*4))
						self.anim_drw_ln=[p]
	def add_trans(self,KEY):
		if self.draw_anim:
			p=[floor(self.pos[0]),floor(self.pos[1]),floor(self.pos[2])]
			if KEY==key.V:
				for mdl in self.par.models:
					if self.b_chk(mdl.tbox,p):
						self.anim_target[1]=mdl
						self.add_anim_stp(None)
						self.remove_anim_stp()
						return
			if self.anim_target[1] is not None:
				if KEY==key.DELETE:self.add_anim_stp("destroy")
				if KEY==key.C:
					self.anim_drw_ln+=[p]
					if len(self.anim_drw_ln)==2:
						if self.anim_drw_ln[0]!=self.anim_drw_ln[1]:
							self.add_anim_stp({"pos":[-(self.anim_drw_ln[0][0]-self.anim_drw_ln[1][0]),-(self.anim_drw_ln[0][1]-self.anim_drw_ln[1][1]),-(self.anim_drw_ln[0][2]-self.anim_drw_ln[1][2])],"time":[5,5,5]})
						self.anim_drw_ln=[p]
				if KEY==key.B:self.add_anim_stp({"wait_time":2})
				if KEY==key.X:self.remove_anim_stp()
				if KEY==key.M:self.wtime(0.1)
				if KEY==key.N:self.wtime(-0.1)
				if KEY==key.L:self.time(1,0,0)
				if KEY==key.J:self.time(-1,0,0)
				if KEY==key.I:self.time(0,1,0)
				if KEY==key.K:self.time(0,-1,0)
				if KEY==key.O:self.time(0,0,1)
				if KEY==key.U:self.time(0,0,-1)
	def update(self,dt,keys):
		dx=dt*7*self.speed*sin(-self.rot[1]/180*pi)
		dy=dt*7*self.speed
		dz=dt*7*self.speed*cos(-self.rot[1]/180*pi)
		self.pos=[self.pos[0]+dx,self.pos[1],self.pos[2]-dz] if keys[key.W] and self.coll.check([self.pos[0]+dx,self.pos[1],self.pos[2]-dz]) else self.pos
		self.pos=[self.pos[0]-dx,self.pos[1],self.pos[2]+dz] if keys[key.S] and self.coll.check([self.pos[0]-dx,self.pos[1],self.pos[2]+dz]) else self.pos
		self.pos=[self.pos[0]-dz,self.pos[1],self.pos[2]-dx] if keys[key.A] and self.coll.check([self.pos[0]-dx,self.pos[1],self.pos[2]-dz]) else self.pos
		self.pos=[self.pos[0]+dz,self.pos[1],self.pos[2]+dx] if keys[key.D] and self.coll.check([self.pos[0]+dx,self.pos[1],self.pos[2]+dz]) else self.pos
		self.pos=[self.pos[0],self.pos[1]+dy,self.pos[2]] if keys[key.SPACE] and self.coll.check([self.pos[0],self.pos[1]+dy,self.pos[2]]) else self.pos
		self.pos=[self.pos[0],self.pos[1]-dy,self.pos[2]] if keys[key.LSHIFT] and self.coll.check([self.pos[0],self.pos[1]-dy,self.pos[2]]) else self.pos
		self.speed=2 if keys[key.LCTRL] else self.speed
		self.speed=0.5 if keys[key.RCTRL] else self.speed
		self.speed=1 if not keys[key.LCTRL] and not keys[key.RCTRL] and not keys[key.W] and not keys[key.A] and not keys[key.S] and not keys[key.D] and not keys[key.SPACE] and not keys[key.LSHIFT] else self.speed
		self.reset_blks() if keys[key.E] else 0
		self.sp={"pos":self.pos,"rot":self.rot} if not keys[key.LCTRL] and not keys[key.RCTRL] and keys[key.R] else self.sp
		self.ep={"pos":self.pos,"rot":self.rot} if (keys[key.LCTRL] or keys[key.RCTRL]) and keys[key.R] else self.ep
		self.c_f()
		self.ctrlp=(keys[key.LCTRL] or keys[key.RCTRL])
		if not self.draw_anim:
			if keys[key.T]:self.ch_theme(keys);self.abl_crT=False
			else:self.abl_crT=True
			if keys[key.G]:self.ch_tex(keys);self.abl_crG=False
			else:self.abl_crG=True
			if keys[key.Y]:self.ch_dir(keys);self.abl_crH=False
			else:self.abl_crH=True
class Main(pyglet.window.Window):
	"""
==========KEYS==========
>MOTION
	W --> forward
	S --> backward
	A --> left
	D --> right
	SPACE --> up
	SHIFT --> down
	Q --> toggle collision
	LCTRL --> increases speed by x2
	RCTRL --> decreases speed by x2
	CTRL + R --> sets end position
	R --> sets start position

>BLOCK CREATION (not in animation mode)
	1 --> normal block
	2 --> button
	3 --> end block (one per level)
	TAB --> delete current block

>BLOCK CONTROLS (not in animation mode)
	L --> move on x-axis by 1
	J --> move on x-axis by -1
	I --> move on y-axis by 1
	K --> move on y-axis by -1
	O --> move on z-axis by 1
	U --> move on z-axis by -1
	RIGHT ARROW --> increase width by 1
	LEFT ARROW --> decrease width by 1
	UP ARROW --> increase height by 1
	DOWN ARROW --> decrease height by 1
	SLASH --> increase depth by 1
	PERIOD (DOT) --> decrease depth by 1
	T + 1 --> select current block theme:
		1 -> gray
	G + 1..7 --> select current block texture:
		BUTTON:
			1 -> default
		BLOCK:
			1 -> corner
			2 -> edge X
			3 -> edge Y
			4 -> edge Z
			5 -> wall X
			6 -> wall Y
			7 -> wall Z
	Y + 1..6 --> selcect button rotation:
		1 -> Up
		2 -> Down
		3 -> West
		4 -> South
		5 -> East
		6 -> North

>ANIMATION CONTROL (in animation mode)
	V --> selects object to animation
	X --> deletes last movement
	DEL --> adds "delete" to animation list
	C --> adds start/end of an animation step
	B --> adds wait time to animation list
	N --> increases wait time by 0.1
	M --> decreases wait time by 0.1
	L --> increses X travel time by 0.1
	J --> decreases X travel time by 0.1
	I --> increses Y travel time by 0.1
	K --> decreases Y travel time by 0.1
	O --> increses Z travel time by 0.1
	U --> decreases Z travel time by 0.1

>ANIMATION TOGGLE
	Z --> toggles animation draw mode
	CTRL + Z --> toggles end animation draw mode
	E --> reset animation & buttons

>MISC
	ESC --> exit
	ENTER / RETURN --> save
	F --> toggles fps text
	COMMA --> toggle current cube visibility
	H --> show this list
"""
	def __init__(self):
		super().__init__(caption="Perspective",resizable=False,fullscreen=True)
		glClearColor(1,1,1,0)
		glEnable(GL_DEPTH_TEST)
		glLineWidth(2)
		self.models=[]
		self.col=[1,1,1,0]
		self.dr_fps=False
		self.cam=Camera(self,pos=(0,3,0),rot=(-90,0))
		self.load(OPENFILENAME)
		self.set_exclusive_mouse(1)
		self.keys=key.KeyStateHandler()
		self.push_handlers(self.keys)
		pyglet.clock.schedule(self.update)
		self.fps=pyglet.clock.ClockDisplay()
		pyglet.app.run()
	def on_mouse_motion(self,x,y,dx,dy):
		self.cam.mouse_motion(dx,dy)
	def on_key_press(self,KEY,MOD):
		if KEY==key.ESCAPE:
			self.close()
		if KEY==key.Q:
			self.cam.coll.togg()
		if KEY==key.F:
			self.dr_fps=not self.dr_fps
		if KEY==key._1:
			self.cam.create_block("block")
		if KEY==key._2:
			self.cam.create_block("button")
		if KEY==key._3:
			self.cam.create_block("end_block")
		if KEY==key.TAB:
			self.cam.delete_block()
		if KEY==key.Z:
			self.cam.chk_toggle()
		if KEY==key.QUOTELEFT:
			self.end_anim_r()
		if KEY==key.COMMA:
			self.cam.sh_cube=not self.cam.sh_cube
		if KEY==key.H:
			print(self.__doc__)
		if KEY==key.RETURN:
			self.save(SAVEFILENAME)
		self.cam.move_blk(KEY)
		self.cam.add_trans(KEY)
	def update(self,dt):
		self.cam.update(dt,self.keys)
	def end_anim_r(self):
		if not self.cam.end_an_ru and self.cam.end_anim is not None:
			for b in self.cam.end_anim["animation"]:
				for n in self.models:
					if b["tag"] in n.tags:
						n.transl+=b["translate"]
						if n.transition==[0]*6:n.action(n.transl[0])
			self.cam.end_an_run=True
	def load(self,fn):
		if fn!="" and os.path.exists(f"./levels/{fn}.json"):
			with open(f"./levels/{fn}.json","r") as f:
				l=json.loads(f.read())
			models=[]
			player=None
			endblock=None
			end_anim=None
			for obj in l:
				if obj["type"]=="block":
					models+=[Block(self,obj["pos"],obj["tex"],dims=obj["size"],tags=obj["tags"])]
				elif obj["type"]=="button":
					models+=[Button(self,obj["pos"],obj["tex"],obj["direction"],action=obj["action"],tags=obj["tags"])]
				elif obj["type"]=="endblock":
					endblock=obj
				elif obj["type"]=="player":
					player={"pos":obj["start_pos"],"rot":obj["start_rot"],"epos":obj["end_pos"],"erot":obj["end_rot"]}
				elif obj["type"]=="end_trigger":
					end_anim=obj
			if player is not None:
				self.cam.set(player)
			if endblock is not None:
				models+=[EndBlock(self,endblock["pos"],endblock["tex"],tags=endblock["tags"])]
			self.cam.end_anim=end_anim
			self.models+=models
			self.cam.coll.process()
	def save(self,fn):
		data=[]
		data+=[{"_comment":"player data","type":"player","start_pos":self.cam.sp["pos"],"start_rot":self.cam.sp["rot"],"end_pos":self.cam.ep["pos"],"end_rot":self.cam.ep["rot"]}]
		data+=[self.cam.end_anim]
		eb=None
		btns=[]
		blks=[]
		for mdl in self.models:
			if mdl.__class__.__name__=="EndBlock":
				eb={"_comment":"end block","type":"endblock","pos":mdl.sp,"tex":mdl.rt,"tags":" ".join(mdl.tags)}
			elif mdl.__class__.__name__=="Button":
				btns+=[{"_comment":"button","type":"button","pos":mdl.sp,"direction":mdl.d,"tex":mdl.rt,"tags":" ".join(mdl.tags),"action":mdl.actioncmd}]
			elif mdl.__class__.__name__=="Block":
				btns+=[{"_comment":"block","type":"block","pos":mdl.sp,"tex":mdl.rt,"tags":" ".join(mdl.tags),"size":mdl.dims}]
		if eb is not None:data+=[eb]
		data+=btns
		data+=blks
		with open(f"./levels/{fn}.json","w") as f:
			f.write(json.dumps(data,indent=4,sort_keys=True))
	def on_draw(self):
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
		self.cam.draw_ext()
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
