import sys,pygame
class Environment:
    def __init__(self, size):
        self.size = self.width, self.height = size

    def start(self):
        self.stepNum = 0
        self.ball = pygame.image.load("ball.bmp")
        self.bar = pygame.image.load("bar.bmp")
        self.ballRect = self.ball.get_rect()
        self.barRect = self.bar.get_rect()
        self.barRect.bottom = self.height
        self.speed = [2,2]
        self.barSpeed = [10, 0]
        self.screen = pygame.Surface(self.size)
        return self.getState()

    def step(self, action):
        self.stepNum = self.stepNum + 1
        newState = self.updateState(action)
        state = self.getState()
        flag = self.isTerminal()
        reward = self.getReward()
        #reward = calculate reward for newState
        #set observation equal to newState
        #state = newState
        return reward, state, flag

    def getReward(self):
        if self.ballRect.top > self.height:
            return -1
        else:
            return 0

    def isTerminal(self):
        if self.getReward() == -1:
            return True
        if self.stepNum > 5000:
            return True
        return False

    def getState(self):
        return (self.ballRect.center[0], self.ballRect.center[1], self.barRect.center[0])

    def updateState(self, action):
        if self.ballRect.colliderect(self.barRect):
            self.speed[1] = -self.speed[1]
        if self.ballRect.left < 0 or self.ballRect.right > self.width:
            self.speed[0] = -self.speed[0]
        if self.ballRect.top < 0:
            self.speed[1] = -self.speed[1]

        self.ballRect = self.ballRect.move(self.speed)

        #move the bar
        if action == 1:
            self.barRect = self.barRect.move(self.barSpeed) 
        if action == -1:
            self.barRect = self.barRect.move([-self.barSpeed[0], -self.barSpeed[1]]) 



    def getScreen(self):
        white = 255,255,255
        black = 0, 0, 0
        self.screen.fill(black)
        self.screen.blit(self.ball,self.ballRect)
        self.screen.blit(self.bar,self.barRect)
        return self.screen

size = 200, 200
delay = 300
interval = 50
pygame.init()
pygame.key.set_repeat(delay, interval)
screen = pygame.display.set_mode(size)
env = Environment(size)
env.start()
clock=pygame.time.Clock()
while 1:
    action = 0
    clock.tick(30)
    for event in pygame.event.get():
       if event.type == pygame.QUIT: sys.exit()
       if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                action = -1
            if event.key==pygame.K_RIGHT:
                action = 1
    (reward, state, isTerminal) = env.step(action)
    screen.blit(env.getScreen(), (0, 0))
    print reward
    print state
    print isTerminal
    pygame.display.flip()
    if isTerminal:
        break

