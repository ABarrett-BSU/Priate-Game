import simpleGE, pygame, random

class Coin(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Coin.png")
        self.setSize(25, 25)
        self.minSpeed = 3
        self.maxSpeed = 10
        self.reset()

    def reset(self):
        
        self.y = -self.rect.height // 2 
        self.x = random.randint(0, self.screen.get_width())
        self.dy = random.randint(self.minSpeed, self.maxSpeed)


    def checkBounds(self):
        
        bottom = self.y + self.rect.height / 2
        if bottom > self.screen.get_height():
            self.reset()


class Pirate(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Pirate2.png")
        self.setSize(90, 90)
        self.setposition = (320, 400)
        self.moveSpeed = 15

    def process(self):
        if self.scene.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.scene.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
        if self.scene.isKeyPressed(pygame.K_UP):
            self.y -= self.moveSpeed
        if self.scene.isKeyPressed(pygame.K_DOWN):
            self.y += self.moveSpeed

class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 15"
        self.center = (500, 30)        
        


class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("ship.png")
        self.sndCoin = simpleGE.Sound("coin.wav")
        self.numCoins = 10
        self.score = 0
        self.lblScore = LblScore()
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 15    
        self.timer.start()
        self.lblTime = LblTime()

        self.pirate = Pirate(self)

        self.coins = []
        for i in range(self.numCoins):
            self.coins.append(Coin(self))

        self.sprites = [self.pirate,
                        self.coins,
                        self.lblScore,
                        self.lblTime]

                                                        

    def process(self):
        for coin in self.coins:
            hit = coin.collidesWith(self.pirate)
            if hit:
                coin.reset()
                self.sndCoin.play()
                self.score += 10
                self.lblScore.text = f"Score: {self.score}"
                
            self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
            if self.timer.getTimeLeft() < 0:
                print(f"Score: {self.score}")
                self.stop()

class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        
        self.prevScore = prevScore

        self.setImage("ship.png")
        self.response ="Quit"

        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
           "Ahoy, matey! You’re a pirate on a quest for treasure!",
           "Use the arrow keys to sail left or right or up and down.",
           "Snatch as many gold coins as ye can before time runs out!",
           "before time runs out!",
           "Hoist the sails and good luck!"]
        
        self.directions.center = (320, 350)
        self.directions.size = (550, 250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 25)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (500, 25)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score: 0"
        self.lblScore.center = (300, 25)
        
        self.lblScore.text = f"Last score: {self.prevScore}"

        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
        
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop() 

        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop() 

def main():
    
    keepGoing = True
    lastScore = 0
            
    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()

        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
            
        else:
            keepGoing = False


if __name__ == "__main__":
    main()