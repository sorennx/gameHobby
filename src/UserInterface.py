import pygame
import os
pygame.font.init()
FONT = pygame.font.SysFont('Verdana',12)
HP_BAR = pygame.image.load(os.path.join('./assets/UI/LifeBar', 'LifeBar.png'))
#HP_BAR = pygame.transform.scale(HP_BAR,(200,40))
#CHAR_SHEET_IMG = pygame.image.load(os.path.join('./assets/UI/CharacterSheet', 'CharacterSheet.png'))
from GameEvents import *

class HpBar(pygame.sprite.DirtySprite):
    def __init__(self,hero,window):
        super().__init__()
        self.window = window
        self.hero = hero
        self.image = HP_BAR
        self.rect = self.image.get_rect()
        self.rect.y = self.window.get_height() - self.image.get_height()
        self.rect.x = 0

    def update(self):
        pygame.draw.rect(self.window, (180,0,0), (self.rect.x-2, self.rect.y, self.image.get_width()*self.hero.currentHp/self.hero.maxHp, self.image.get_height()))


class XpBar(pygame.sprite.DirtySprite):
    def __init__(self,hero,window):
        super().__init__()
        self.window = window
        self.hero = hero
        self.image = HP_BAR
        self.rect = self.image.get_rect()
        self.rect.y = (self.window.get_height() - self.image.get_height()) - (self.image.get_height()+2)
        self.rect.x = 0

    def update(self):
        pygame.draw.rect(self.window, "#380349", (self.rect.x - 2, self.rect.y, self.image.get_width() * self.hero.currentXpPoints / self.hero.xpPointsForNextLevel, self.image.get_height()))

class CharacterSheetWindow(pygame.sprite.Sprite):
    def __init__(self,window,hero):
        super().__init__()
        self.isOpen = False
        self.window = window
        self.hero = hero
        self.fontsize = 24
        self.font = pygame.font.Font(os.path.join('./assets/Fonts','Fontin-Regular.ttf'),self.fontsize) #Poe font - Fontin
        self.image = pygame.image.load(os.path.join('./assets/UI/CharacterSheet', 'CharacterSheet.png'))
        self.rect = self.image.get_rect()

    def drawCharacterSheet(self):
        charName = self.font.render(f'{self.hero.characterName}', True, "#101010")
        charNameRect = charName.get_rect()
        charNameRect.x = self.rect.x+25+12
        charNameRect.y = self.rect.y + 35
        self.image.blit(charName, (charNameRect.x, charNameRect.y))

        maxHp = self.font.render(f'Max life: {self.hero.maxHp}',True,"#101010")
        maxHpRect = maxHp.get_rect()
        maxHpRect.x = self.rect.x+30
        maxHpRect.y = self.rect.y+120
        self.image.blit(maxHp, (maxHpRect.x,maxHpRect.y))

        spellPower = self.font.render(f'Spell power: {self.hero.baseSpellPower}', True, "#101010")
        spellPowerRect = maxHp.get_rect()
        spellPowerRect.x = self.rect.x+30
        spellPowerRect.y = self.rect.y + 120 + self.fontsize
        self.image.blit(spellPower, (spellPowerRect.x, spellPowerRect.y))

        movementSpeed = self.font.render(f'Movement speed: {self.hero.movementSpeed}', True, "#101010")
        movementSpeedRect = movementSpeed.get_rect()
        movementSpeedRect.x = self.rect.x+30
        movementSpeedRect.y = self.rect.y + 120 + self.fontsize*2
        self.image.blit(movementSpeed, (movementSpeedRect.x, movementSpeedRect.y))

    def update(self):
        self.drawCharacterSheet()


class InventoryWindow(pygame.sprite.DirtySprite):
    def __init__(self,window,hero,itemsGroup):
        super().__init__()
        self.window = window
        self.hero = hero
        self.isOpen = False
        self.itemsGroup = itemsGroup

        self.inventorySlotsColumns = 12
        self.inventorySlotsRows = 6
        self.slotSize = 32
        self.inventorySlotDist = 5
        self.inventorySlotsList = []
        self.inventoryItemList = [] #todo: save inventory
        self.inventorySlotGroup = pygame.sprite.Group()
        self.inventorySlotStartXcord = 8
        self.inventorySlotStartYcord = 303
        self.image = pygame.image.load(os.path.join('./assets/UI/InventoryWindow','InventoryWindow.png'))
        self.rect = self.image.get_rect()
        self.rect.x = self.hero.game.width - self.image.get_width()

        #Run on init
        self.createSockets()


    def createSockets(self):
        for j in range(self.inventorySlotsRows):
            self.createSocketRow(j)

    def createSocketRow(self,j):
        for i in range(self.inventorySlotsColumns):
            t = InventorySocket(self, self.inventorySlotStartXcord + (i * self.slotSize),
                                self.inventorySlotStartYcord + (j * self.slotSize), self.hero, [i, j])
            self.inventorySlotsList.append(t)
            self.inventorySlotGroup.add(t)


    def update(self):
        if self.isOpen:
            self.inventorySlotGroup.update()
            self.inventorySlotGroup.draw(self.image) #painting the background image of a socket




class InventorySocket(pygame.sprite.DirtySprite): #todo: change the socket frame depending on the item rarity
    def __init__(self, inventory, x, y, hero, ij, item=None, size=32):
        super().__init__()
        self.hero = hero
        self.inventory = inventory
        self.size = size
        self.item = item
        self.image = pygame.image.load(os.path.join('./assets/UI/InventoryWindow','InventorySlot.png'))
        self.imageCover = pygame.image.load(os.path.join('./assets/UI/InventoryWindow','InventorySlot.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isEmpty = True
        self.itemGroup = pygame.sprite.Group()
        self.itemList = []
        self.ij = ij

    def emptySocket(self):
        self.item.kill()
        self.item = None
        self.isEmpty = True

    def update(self):

        self.itemGroup.update()


        self.itemGroup.draw(self.image)
            #print(self.item.rect.x, self.item.rect.y)

        for event in self.hero.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                mousePos = pygame.mouse.get_pos()
                if x in range (self.rect.x+self.inventory.rect.x,self.rect.x+self.inventory.rect.x+self.size) and y in range(self.rect.y+self.inventory.rect.y,self.rect.y+self.inventory.rect.y+self.size):
                    print(len(self.itemGroup))
                    if self.isEmpty is False:
                        copy = self.item.createCopy()
                        copy.rect.center = mousePos
                        copy.isPickedUp = True
                        copy.isInInventory = False

                        self.hero.game.itemsGroup.add(copy)
                        self.emptySocket()
                        self.itemGroup.empty()

                        self.itemGroup.clear(self.image,self.imageCover) #clears the surface of the sprite image by covering that surface with a new image/background, in this case imageCover is the same as self.image. they are the same size
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if x in range(self.rect.x + self.inventory.rect.x,self.rect.x + self.inventory.rect.x + self.size) and y in range(self.rect.y + self.inventory.rect.y, self.rect.y + self.inventory.rect.y + self.size):
                    pass


class EquipmentWindow():
    pass

class SkillWindow():
    pass
