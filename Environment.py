import sys,pygame
import copy #for copy objects
class Environment:
    def __init__(self, size, discrete_size):
        self.size = self.width, self.height = size
        self.discrete_size = discrete_size
        self.time_scale = 3
        self.stepNum = 0

    def start(self):
        self.ball = pygame.image.load("ball.bmp")
        self.bar = pygame.image.load("bar.bmp")
        self.ballRect = self.ball.get_rect()
        self.ballRect.x = self.width/3

        self.barRect = self.bar.get_rect()
        self.barRect.bottom = self.height
        self.barRect.x = self.width/2

        self.speed = [2*self.time_scale,2*self.time_scale]
        self.leftSpeed = [-2*self.time_scale,-2*self.time_scale]
        self.rightSpeed = [2*self.time_scale,-2*self.time_scale]
        self.straitSpeed = [0*self.time_scale,-3*self.time_scale]

        self.barSpeed = [3*self.time_scale, 0*self.time_scale]
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
        #if self.ballRect.top > self.height:
        if self.ballRect.bottom > self.height:
            return -1000
        else:
            return 1

    def isTerminal(self):
        if self.getReward() == -1000:
            return True
        if self.stepNum > 50000:
            return True
        return False

    def getState(self):
        return (self.ballRect.center[0]/self.discrete_size, self.ballRect.center[1]/self.discrete_size, self.barRect.center[0]/self.discrete_size)

    def updateState(self, action):
        if self.ballRect.colliderect(self.barRect):
            if self.ballRect.left < self.barRect.left:
                self.speed = copy.copy(self.leftSpeed)
            elif self.ballRect.right > self.barRect.right:
                self.speed = copy.copy(self.rightSpeed)
            else:
                self.speed = copy.copy(self.straitSpeed)
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

        #check the bar stays in the boundary
        if self.barRect.right > self.width:
            self.barRect.right = self.width
        if self.barRect.left < 0:
            self.barRect.left = 0



    def getScreen(self):
        white = 255,255,255
        black = 0, 0, 0
        self.screen.fill(black)
        self.screen.blit(self.ball,self.ballRect)
        self.screen.blit(self.bar,self.barRect)
        return self.screen

if __name__ == "__main__":
    from SARSA import SARSA
    size = 400, 400
    discrete_size = 10
    delay = 100
    interval = 50
    action = 0

    pygame.init()
    pygame.key.set_repeat(delay, interval)
    clock=pygame.time.Clock()
    screen = pygame.display.set_mode(size)


    agent = SARSA(0.1, 0.1, 0.9, (-1, 0, 1))

    while 1:
        env = Environment(size, discrete_size)
        state = env.start()
        action = agent.start(state)
        while 1:
            clock.tick(1000)
            for event in pygame.event.get():
               #action = 0
               if event.type == pygame.QUIT: sys.exit()
               #if event.type==pygame.KEYDOWN:
                    #if event.key==pygame.K_LEFT:
                        #action = -1
                    #if event.key==pygame.K_RIGHT:
                        #action = 1
            (reward, state, isTerminal) = env.step(action)
            action = agent.step(reward, state)
            screen.blit(env.getScreen(), (0, 0))
            #print reward
            #print state
            #print isTerminal
            pygame.display.flip()
            if isTerminal:
                agent.end(reward)
                break

