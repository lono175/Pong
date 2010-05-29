class StartControl:
    def __init__(self):
        self.isStart = False
        self.playerType = 'SARSA'
        self.isReset = False
    def start(self):
        self.isStart = True
    def stop(self):
        self.isStart = False
    def changePlayer(self, type):
        self.playerType = type
    def reset(self):
        self.isReset = True
def Save(agent): 
    import pickle
    output = open('RL-Agent.txt', 'wb')
    pickle.dump(agent, output)
    output.close()
def Load(agentList):
    import pickle
    input = open('RL-Agent.txt', 'rb')
    agentList[0] = pickle.load(input)
def ChangeToSARSA(agentList, flowMgr):
    agentList[0] = SARSA(0.1, 0.1, 0.9, (-1, 1))
    flowMgr.changePlayer('SARSA')
    flowMgr.reset()

def ChangeToHuman(agentList, flowMgr):
    flowMgr.changePlayer('Human')
    flowMgr.reset()
    
if __name__ == "__main__":
    from SARSA import SARSA
    from PongUI import PongUI
    from Environment import Environment
    from pgu import gui
    import sys,pygame


    app = gui.App()
    form = gui.Form()
    ui = PongUI()

    frame = gui.Container(align=-1,valign=-1)
    frame.add(ui,0,0)
    app.init(frame)

    gameScreenSize = 400, 400
    uiSize = 400, 400
    assert uiSize[1] == gameScreenSize[1]
    screenSize = (gameScreenSize[0] + uiSize[0], gameScreenSize[1])
    discrete_size = 20
    delay = 100
    interval = 50
    action = 0

    pygame.init()
    pygame.key.set_repeat(delay, interval)
    clock=pygame.time.Clock()
    screen = pygame.display.set_mode(screenSize)


    agentList = []
    agentList.append(SARSA(0.01, 0.1, 0.95, (-1, 1)))

    start = StartControl()
    ui.setStartListener(start.start)
    ui.setStopListener(start.stop)
    ui.setSaveHandler(lambda : Save(agentList[0]))
    ui.setLoadHandler(lambda : Load(agentList))

    ui.setPlayerHandler( dict( 
        SARSA= (lambda : ChangeToSARSA(agentList, start)),
        Human= (lambda : ChangeToHuman(agentList, start)),
        Q_Learning= (lambda : True)
        ))

    episodeNum = 0
    stepNum = 0
    while 1:
        agent = agentList[0]
        env = Environment(gameScreenSize, discrete_size)
        state = env.start()
        if start.playerType == 'Human':
           action = 0
        else:
           action = agent.start(state)

        episodeNum += 1
        start.isReset = False
        while 1:

            #remove me
            agent = agentList[0]

            #update game status here
            form['stepLabel'].value = stepNum
            form['episodeLabel'].value = episodeNum
            #clock.tick(1000)
            clock.tick(float(form['fpsLabel'].value))
            for event in pygame.event.get():
               if start.playerType == 'Human':
                  action = 0
               if event.type == pygame.QUIT: sys.exit()
               elif event.type==pygame.KEYDOWN and start.playerType == 'Human':
                    if event.key==pygame.K_LEFT:
                        action = -1
                    if event.key==pygame.K_RIGHT:
                        action = 1
               else:
                    app.event(event)
            screen.blit(env.getScreen(), (uiSize[0], 0))
            app.paint(screen)
            #print reward
            #print state
            #print isTerminal
            pygame.display.flip()
            if start.isReset:
                break
            if start.isStart:
                (reward, state, isTerminal) = env.step(action)
                if start.playerType != 'Human':
                    action = agent.step(reward, state)
                stepNum += 1
                if isTerminal:
                    agent.end(reward)
                    break

