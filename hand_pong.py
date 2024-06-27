import cv2
print(cv2.__version__)

class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tal1=.5,tal2=.5):
        self.hands = self.mp.solutions.hands.Hands(False,maxHands,tal1,tal2)
    def Marks(self,frame):
        myHands = []
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand =[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands

width=1000
height=500

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
findHands = mpHands(1)

paddleWidth = 125
paddleHeight =25
paddleColor = (0,255,0)
paddleYpos = 20
paddleXpos = 0

ballXpos = int(width/2)
ballYpos = int(height/2)
ballRad = 20
ballSpeedX = 5
ballSpeedY = 5
ballColor = (0,0,255)

Score = 0
life = 3
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ignore,  frame = cam.read()
    
    frame = cv2.flip(frame,1) 

    ballXpos -= ballSpeedX
    ballYpos -= ballSpeedY
    cv2.circle(frame,(ballXpos,ballYpos),ballRad,ballColor,-1) 
    cv2.putText(frame,("Score: "+ str(Score)),(10,height-10),font ,1, (0,255,0),2)
    cv2.putText(frame,("Live: "+ str(life)),(200,height-10),font ,1, (0,0,255),2)
    

    handData = findHands.Marks(frame)
    for hand in handData:
        paddleXpos = hand[8][0]
        cv2.rectangle(frame,(int(paddleXpos-paddleWidth/2),paddleYpos),(int(paddleXpos+paddleWidth/2),paddleHeight+paddleYpos),paddleColor,-1)

        if (ballXpos+ballRad >= int(paddleXpos-paddleWidth/2) and ballXpos+ballRad <= paddleXpos +paddleWidth and paddleYpos+ballRad == ballYpos and ballSpeedY >0):
            ballSpeedY +=4
            ballSpeedX +=4
            ballSpeedY = -ballSpeedY
            ballSpeedX = -ballSpeedX

            Score +=1
            

    if (ballYpos -ballRad <= 0 ):
        ballSpeedY = -ballSpeedY
        life -=1
    
    if (ballYpos -ballRad >= height):
        ballSpeedY = -ballSpeedY

    
    if (ballXpos -ballRad <= 0 or ballXpos- ballRad >= 920):
        ballSpeedX = -ballSpeedX

    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)

    if life ==0:
        break
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()

print("Score : ",Score)