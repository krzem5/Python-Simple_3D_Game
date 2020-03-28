level_data=[]
level_data+=[{"_comment":"player data","type":"player","start_pos":[13,13,13],"start_rot":[-45,45],"end_pos":[20,30,7],"end_rot":[-60,70]}]
level_data+=[{"_comment":"end block","type":"endblock","tex":"gray:end","pos":[0,-4,0],"tags":"eblk"}]
level_data+=[{"_comment":"level end","type":"end_trigger","animation":[{"tag":"wA","translate":[{"pos":[-1,0,0],"time":[5,0,0]},{"wait_time":0.3},{"pos":[0,0,10],"time":[0,0,20]}]},{"tag":"wB","translate":[{"pos":[1,0,0],"time":[5,0,0]},{"wait_time":0.3},{"pos":[0,0,-10],"time":[0,0,20]}]},{"tag":"wE","translate":[{"pos":[0,0,-1],"time":[0,0,5]},{"wait_time":0.3},{"pos":[-10,0,0],"time":[20,0,0]}]},{"tag":"wF","translate":[{"pos":[0,0,1],"time":[0,0,5]},{"wait_time":0.3},{"pos":[10,0,0],"time":[20,0,0]}]},{"tag":"tb","translate":["destroy"]},{"tag":"bb","translate":["destroy"]},{"tag":"wC","translate":[{"wait_time":0.3},{"pos":[0,-5,0],"time":[0,10,0]}]},{"tag":"wD","translate":[{"wait_time":0.3},{"pos":[0,5,0],"time":[0,10,0]}]}]}]
level_data+=[{"_comment":"button","type":"button","pos":[0,5,0],"direction":"U","tags":"tb","tex":"gray:btn","action":[{"tag":"gate","translate":[{"pos":[-1,0,0],"time":[5,0,0]},{"pos":[0,7,0],"time":[0,35,0]}]}]}]
level_data+=[{"_comment":"button","type":"button","pos":[0,-3,0],"direction":"U","tags":"bb","tex":"gray:btn","action":[{"tag":"eblk","translate":[{"pos":[0,4,0],"time":[0,50,0]}]},{"tag":"gate","translate":[{"pos":[0,-7,0],"time":[0,35,0]},{"pos":[1,0,0],"time":[5,0,0]}]}]}]
l=[(-4,-4,-4),(4,-4,-4),(-4,-4,4),(4,-4,4),(-4,4,-4),(4,4,-4),(-4,4,4),(4,4,4)]
for cp in l:
	level_data.append({"_comment":"corner","tags":f"c{l.index(cp)}","type":"block","pos":list(cp),"size":[1,1,1],"tex":"gray:corner"})
	level_data[2]["animation"]+=[{"tag":f"c{l.index(cp)}","translate":[{"wait_time":1},{"pos":[cp[0]//2,cp[1]//2,cp[2]//2],"time":[20,20,20]}]}]
l=[(-3,-4,-4),(-3,-4,4),(-3,4,-4),(-3,4,4)]
for ep in l:
	level_data.append({"_comment":"X-edge","tags":f"eX{l.index(ep)}","type":"block","pos":list(ep),"size":[7,1,1],"tex":"gray:edgeX"})
	level_data[2]["animation"]+=[{"tag":f"eX{l.index(ep)}","translate":[{"wait_time":2},{"pos":[0,ep[1]//2,ep[2]//2],"time":[0,20,20]}]}]
l=[(-4,-3,-4),(4,-3,-4),(-4,-3,4),(4,-3,4)]
for ep in l:
	level_data.append({"_comment":"Y-edge","tags":f"eY{l.index(ep)}","type":"block","pos":list(ep),"size":[1,7,1],"tex":"gray:edgeY"})
	level_data[2]["animation"]+=[{"tag":f"eY{l.index(ep)}","translate":[{"wait_time":2},{"pos":[ep[0]//2,0,ep[2]//2],"time":[20,0,20]}]}]
l=[(-4,-4,-3),(4,-4,-3),(-4,4,-3),(4,4,-3)]
for ep in l:
	level_data.append({"_comment":"Z-edge","tags":f"eZ{l.index(ep)}","type":"block","pos":list(ep),"size":[1,1,7],"tex":"gray:edgeZ"})
	level_data[2]["animation"]+=[{"tag":f"eZ{l.index(ep)}","translate":[{"wait_time":2},{"pos":[ep[0]//2,ep[1]//2,0],"time":[20,20,0]}]}]
level_data+=[{"_comment":"X-wall","tags":"gate wA","type":"block","pos":[-4,-3,-3],"size":[1,7,7],"tex":"gray:wallX"},{"_comment":"X-wall","type":"block","tags":"wB","pos":[4,-3,-3],"size":[1,7,7],"tex":"gray:wallX"}]
level_data+=[{"_comment":"Y-wall","tags":"wC","type":"block","pos":[-3,-4,-3],"size":[7,1,7],"tex":"gray:wallY"},{"_comment":"X-wall","type":"block","tags":"wD","pos":[-3,4,-3],"size":[7,1,7],"tex":"gray:wallY"}]
level_data+=[{"_comment":"Z-wall","tags":"wE","type":"block","pos":[-3,-3,-4],"size":[7,7,1],"tex":"gray:wallZ"},{"_comment":"X-wall","type":"block","tags":"wF","pos":[-3,-3,4],"size":[7,7,1],"tex":"gray:wallZ"}]
import json
with open("./levels/lvl-1.json","w") as f:
	f.write(json.dumps(level_data,indent=4,sort_keys=True))