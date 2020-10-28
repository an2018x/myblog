import math
from pyecharts import options as opts
from pyecharts.charts import Graph

class Infection:

    def readfile(self, filepath):
        self.dicOID = {}
        self.dicTime = {}
        with open(filepath) as f:
            for line in f.readlines():
                line = line.strip('\n');
                oid, timestamp, lon, lat = line.split(',')
                oid = int(oid)
                timestamp = int(timestamp)
                lon = float(lon)
                lat = float(lat)
                if (self.dicOID.get(oid, 0) == 0):
                    self.dicOID[oid] = []
                if (self.dicTime.get(timestamp, 0) == 0):
                    self.dicTime[timestamp] = []
                self.dicOID[oid].append([timestamp, lon, lat])
                self.dicTime[timestamp].append([oid, lon, lat])

    def setData(self,sources,alpha,beta):
        self.sourceList=[]
        for it in sources:
            self.sourceList.append(int(it))
        self.alphaVal = int(alpha)
        self.betaVal = int(beta)

    def calNum(self):
        for source in self.sourceList:
            for it in self.dicOID[source]:
                t = it[0]
                lon1 = it[1]
                lat1 = it[2]
                for item in self.dicTime[t]:
                    id = item[0]
                    lon2 = item[1]
                    lat2 = item[2]
                    dis = self.getDistance(lon1,lat1,lon2,lat2)
                    if dis <= self.betaVal:
                        if self.cntOID.get(id,0)==0:
                            self.cntOID[id]={}
                        if self.cntOID[id].get(source,0)==0:
                            self.cntOID[id][source] = 0
                        self.cntOID[id][source]+=1

    def getAns(self):
        self.vis = {}
        self.ans = []
        for source in self.sourceList:
            self.vis[source] = 1
        for k,v in self.cntOID.items():
            if self.vis.get(k,0)==1:
                continue
            else:
                for key,val in self.cntOID[k].items():
                    if val>=self.alphaVal:
                        self.ans.append((key,k))



    def getDistance(self, lon1, lat1, lon2, lat2):
        radLat1 = math.radians(lat1)
        radLat2 = math.radians(lat2)
        a = radLat1 - radLat2
        b = math.radians(lon1)-math.radians(lon2)
        s = 2*math.asin(math.sqrt(math.pow(math.sin(a/2), 2)+
                                  math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2), 2)))
        s = s*self.EARTH_RADIUS
        return s
    def __init__(self):
        self.EARTH_RADIUS = 6378137.0
        self.sourceList = []
        self.sourceList.append(121)
        self.sourceList.append(436)
        self.cntOID = {}
        self.dicSource = {}
        self.dicOID = {}
        self.dicTime = {}
        self.ans = []
        self.source = []
        self.alphaVal = 3
        self.betaVal = 400
        self.vis = {}

    def toChart(self):
        nodes_data = []
        links_data = []
        for source in self.sourceList:
            name = "结点"
            name += str(source)
            nodes_data.append(opts.GraphNode(name=name, symbol_size=20))
        for item in self.ans:
            name = "结点"
            name += str(item[1])

            nodes_data.append(opts.GraphNode(name=name, symbol_size=20))
        cnt=1
        for item in self.ans:
            name = "结点"
            sourcename = name + str(item[0])
            targetname = name + str(item[1])
            links_data.append(
                opts.GraphLink(source=sourcename, target=targetname, value=cnt)
            )
            cnt+=1
        c = (
            Graph(init_opts=opts.InitOpts(bg_color='rgba(255,250,205,0.2)',
                                width='1500px',
                                height='780px',
                                page_title='page',

                                ))
                .add(
                "",
                nodes_data,
                links_data,
                repulsion=4000,
                edge_label=opts.LabelOpts(
                    is_show=False, position="middle", formatter="{b} 传染了 {c}"
                ),
            )
                .set_global_opts(
                #init_opts=opts.InitOpts(width='1900px',height='900px'),
                title_opts=opts.TitleOpts(title="传染关系图"),

            )
                .render("./templates/graph_with_edge_options.html")
        )

#
# if __name__ == "__main__":
#     model = Infection()
#     model.readfile('data.txt')
#     model.calNum()
#     model.getAns()
#     model.ans.sort()
#     print(model.ans)
#     model.toChart()
#     #print(model.dicOID[18])






