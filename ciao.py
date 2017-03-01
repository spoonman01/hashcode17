#author: Luca Rospocher
class CacheServer:
    def __init__(self):
        self.numberEnds = 0
        self.ends = []
        self.vvv = []
        pass

class Endpoint:
    def __init__(self):
        self.dataCenterLat = 0
        self.numberCaches = 0
        self.videos = []
        self.cachess = []
        pass
    
videos = []
endPoints = []
cacheServers = []
    
def main():
    
    fileLines = open('kittens.in', 'r').readlines()
    firstLine = fileLines[0]
    splittedFirst = firstLine.split(' ')
    
    nVideos = int(splittedFirst[0])
    nEndpoints = int(splittedFirst[1])
    nRequests = int(splittedFirst[2])
    nCaches = int(splittedFirst[3])
    cacheSize = int(splittedFirst[4])
    
    for i in range(nCaches):
        cacheServers.append(CacheServer()) #fill with empty
    
    
    videoLine = fileLines[1]
    splittedVideo = videoLine.split(' ')
    for i in range(nVideos): #read from file videos
        videos.append(int(splittedVideo[i]))
    
    lineCounter = 2
    for i in range(nEndpoints): #read from file endpoints features
        endPointLine = fileLines[lineCounter]
        lineCounter += 1
        splittedEndPoint = endPointLine.split(' ')
        
        endPoints.append(Endpoint()) #fill with empty
        endPoints[i].dataCenterLat = int(splittedEndPoint[0])
        endPoints[i].numberCaches = int(splittedEndPoint[1])
        
        for k in range(endPoints[i].numberCaches): #read from file link between caches and endpoints
            latencyLine = fileLines[lineCounter]
            lineCounter += 1
            splittedLatency = latencyLine.split(' ')
            
            c = int(splittedLatency[0])
            lat = int(splittedLatency[1])
            endPoints[i].cachess.append((cacheServers[c], lat))
            
            #reference add
            cacheServers[c].ends.append((endPoints[i], lat))
            cacheServers[c].numberEnds += 1
            
    for req in range(nRequests): #read from file video request
        requestLine = fileLines[lineCounter]
        lineCounter += 1
        splittedRequest = requestLine.split(' ')
            
        v = int(splittedRequest[0])
        e = int(splittedRequest[1])
        r = int(splittedRequest[2])
        endPoints[e].videos.append((v,r))
        
    for i in range(nCaches):
        videoValues = [0] * nVideos
        for k in range(cacheServers[i].numberEnds):
            delta = cacheServers[i].ends[k][0].dataCenterLat - cacheServers[i].ends[k][1] #latency difference
            for j in range (len(cacheServers[i].ends[k][0].videos)):
                #calculate the best video for each cache server
                videoValues[cacheServers[i].ends[k][0].videos[j][0]] += delta * cacheServers[i].ends[k][0].videos[j][1]
        
        tmp = videoValues * 1
        videoValues.sort(reverse=True)
        maxSize = cacheSize
        for h in range(len(videoValues)): #adding the best videos to cache servers
            if (maxSize - videos[tmp.index(videoValues[h])] >= 0):
                cacheServers[i].vvv.append(tmp.index(videoValues[h]))
                maxSize = maxSize - videos[tmp.index(videoValues[h])]
            else:
                break
    
    #print result to file
    fileOutput = open('kittens.out', 'w')
    fileOutput.write(str(nCaches) + '\n')
    for b in range(nCaches):
        fileOutput.write(str(b) + ' ') 
        for t in range(len(cacheServers[b].vvv)):
            fileOutput.write(str(cacheServers[b].vvv[t]) + ' ')
        fileOutput.write('\n')
        
if  __name__ =='__main__':
    main()