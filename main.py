f = open('index.html')
html = f.read()
f.close

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80)) # localhost ip (empty) on port 80
s.listen(1) # Let only one device connect to AP

currentPos = [0,0,0,0,0,0,0]

def mapping(pos, index):
    #Mapping slider values to servo values
    
    #Min/max thresholds for each joint
    minOut = [340,345,350,280,165,300,250]
    maxOut = [465,490,490,510,255,410,300]
    minIn = -60 #Minimum input of positionRaw
    maxIn = 60 #Maximum input of positionRaw
    
    output = minOut[index] + (maxOut[index] - minOut[index]) * (pos - minIn) / (maxIn - minIn)
    return int(output)
    
    
    
def move(index, pos, mode):
    
    if mode is "M":
        print("Raw: ", index, pos)
        pos = mapping(pos,index)
        print("Remapped: ", index, pos)
        
    currentPos[index] = pos
    print(currentPos)
    pca.duty(index,pos)

def pose(poseId):
    
    poses = {1:[[403, 413, 455, 473, 177, 348, 297]], #pinch
             2: [[340, 345, 350, 421, 195, 355, 275]], #open
             3: [[465, 490, 490, 510, 210, 393, 250]]} #close
    
    numFrames = len(poses[poseId])

    print(poseId)
    
    for frame in range(numFrames):
        print("frame: ", frame)
        
        for joint in range(len(currentPos)):
            
            print("joint: ", joint, "pos: ", poses[poseId][frame][joint])
            move(joint, poses[poseId][frame][joint], "P")
            if numFrames > 1:
                time.sleep(1)


while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)
    start = request.find('BGN')
    end = request.find('END')
    mode = request[start+3]
    index = request[start+4]
    pos = request[start+5:end]
    
    if mode is "M":
        
        print("Move!")
        print("joint:", index, "pos:", pos)
        
        try:
            index = int(index)-1
            pos = int(pos)
            move(index, pos, mode)
            
        except:
            print("Conversion error")
            
        finally:
            mode = "N"
        
    elif mode is "P":
        print("Pose!")
        index = int(index)
        pose(index)
        mode = "N"
    
    gc.collect()
    response = html
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close
    


