import sys, pygame

class Game:
    def __init__(self):
        pygame.init()
        
        self.size = self.width, self.height = 1280, 480
        self.speed = [1,1]
        self.black = 0, 0, 0
        
        self.screen = pygame.display.set_mode(self.size)
        
        self.bg = pygame.image.load("map.jpg").convert_alpha()
        self.bgrect = self.bg.get_rect()
        self.ball = pygame.image.load("ball.gif").convert_alpha()
        self.ballrect = self.ball.get_rect()

        self._run = True
    
    def draw_pic(self):
        self.screen.blit(self.bg, self.bgrect)
        self.screen.blit(self.ball, self.ballrect)

    def play(self):
        while self._run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._run = False

            self.ballrect = self.ballrect.move(self.speed)

            if self.ballrect.left < 0 or self.ballrect.right > self.width:
                self.speed[0] = -self.speed[0]
            if self.ballrect.top < 0 or self.ballrect.bottom > self.height:
                self.speed[1] = -self.speed[1]

            self.draw_pic()
            pygame.display.flip()
            
            #pygame.time.delay(2)

        pygame.quit()
        sys.exit()

game = Game()
game.play()