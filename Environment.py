import sys,pygame
class Environment:
    def __init__(self):
        self.size = self.width, self.height = 200, 400
        self.ball = pygame.image.load("ball.bmp")
        self.bar = pygame.image.load("bar.bmp")
        self.ballRect = self.ball.get_rect()
        self.barRect = self.bar.get_rect()
        self.barRect.top = 200
        self.speed = [2,2]
        self.barSpeed = [10, 0]
        self.screen = pygame.display.set_mode(self.size)
        self.count = 1
    #def start(self):
        #return self.observation
    def step(self):
        #newState = updateState(action, state)
        self.updateState()
        #flag = isTerminal(newState)
        #reward = calculate reward for newState
        #set observation equal to newState
        #state = newState
        #return reward, observation, flag
    def updateState(self):
        self.count = self.count + 1
        print "hi" + str(self.count)

        if self.ballRect.colliderect(self.barRect):
            self.speed[1] = -self.speed[1]
        if self.ballRect.left < 0 or self.ballRect.right > self.width:
            self.speed[0] = -self.speed[0]
        if self.ballRect.top < 0 or self.ballRect.bottom > self.height:
            self.speed[1] = -self.speed[1]
        self.ballRect = self.ballRect.move(self.speed)
        print self.ballRect
    def getScreen(self):
        white = 255,255,255
        black = 0, 0, 0
        self.screen.fill(black)
        self.screen.blit(self.ball,self.ballRect)
        self.screen.blit(self.bar,self.barRect)

pygame.init()
env = Environment()
clock=pygame.time.Clock()
while 1:
    clock.tick(30)
    for event in pygame.event.get():
       if event.type == pygame.QUIT: sys.exit()
    env.step()
    env.getScreen()
    pygame.display.flip()

