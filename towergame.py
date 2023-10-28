import tkinter as tk
import math
import random

window = tk.Tk()
canvas = tk.Canvas(window, height=450, width=400)
canvas.pack()
canvas.create_line(0, 400, 400, 400, fill="black")

gridwidth = 25

class Stats:
    def __init__(self, canvas):
        self.money = 200
        self.life = 100
        self.canvas = canvas
        self.money_text = canvas.create_text(50, 410, text=f"Money:  {self.money}")
        self.tower_text = canvas.create_text(250, 410, text="Wall Cost: 25")
        # self.life_text = canvas.create_text(250, 410, text=f"Life:  {self.life}")

    def getMoney(self):
        return self.money

    def setMoney(self, change):
        self.money = self.money + change

    def updateMoney(self):
        self.canvas.itemconfig(self.money_text, tex=f"Money:  {self.money}")

    def getLife(self):
        return self.life

    def setLife(self, change):
        self.life = self.life + change

    def updateLife(self):
        self.canvas.itemconfig(self.life_text, tex=f"Life:  {self.life}")

class Block:
    def __init__(self, canvas, id) -> None:
        self.canvas = canvas
        self.id = id
        self.health = 0
        # self.text_id = self.canvas.create_text(self.canvas.bbox(self.id)[0] + gridwidth // 2, 
        #                                        self.canvas.bbox(self.id)[1] + gridwidth // 2, 
        #                                        text="", fill="white")

    def create(self):
        self.health = 3
        self.canvas.itemconfig(self.id, fill="black", activefill="black", tags="wall")
        # self.canvas.itemconfig(self.text_id, text=str(self.health))

    def damage(self):
        self.health -= 1
        # self.canvas.itemconfig(self.text_id, text=str(self.health))
        # if self.health == 2:
        #    self.canvas.itemconfig(self.id, fill="gray25", activefill="green")
        # elif self.health == 1:
        #    self.canvas.itemconfig(self.id, fill="gray50", activefill="green") 

    def isDead(self):
        # if self.health == 0:
        #     self.canvas.itemconfig(self.text_id, text="")
        return self.health == 0

class Tower:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = self.canvas.create_polygon(
            (200, 151),
            (243, 175),
            (243, 225),
            (200, 249),
            (157, 225),
            (157, 175),
            fill="cyan",
            tags=["tower"],
        )
        self.tower_stats = Stats(self.canvas)
        self.life_text_id = self.canvas.create_text(200, 200, text=str(self.tower_stats.getLife()), fill="Black")

        self.blocks = {}

        for i in range(math.floor(400 / gridwidth)):
            for j in range(math.floor(400 / gridwidth)):
                newblock = self.canvas.create_rectangle(
                    (i * gridwidth, j * gridwidth),
                    ((i + 1) * gridwidth, (j + 1) * gridwidth),
                    fill="",
                    activefill="green",
                    outline="",
                )
                self.blocks[newblock] = Block(canvas, newblock)
                #print("Block ", newblock, " added")

        # print(self.blocks)

        # print(self.canvas.bbox(self.id))

        # self.canvas.create_rectangle(self.canvas.bbox(self.id), outline="red")

        for i in self.canvas.find_overlapping(*self.canvas.bbox(self.id)):
            if i in self.blocks.keys():
                self.canvas.delete(i)
                self.blocks.pop(i)

    def loseLife(self):
        if self.tower_stats.getLife() > 0:
            self.tower_stats.setLife(-10)
            # self.tower_stats.updateLife()
            self.canvas.itemconfig(self.life_text_id, text=str(self.tower_stats.getLife()))
        
    def drawWall(self, event):
        if self.tower_stats.getMoney() >= 25:
            # print(event)
            closest = canvas.find_closest(event.x, event.y)[0]
            # print(closest)
            if closest in self.blocks:
                self.tower_stats.setMoney(-25)
                self.tower_stats.updateMoney()
                self.blocks[closest].create()

    def damageWall(self, id):
        self.blocks[id].damage()
        # print(
        #     f"Block {id} was damaged! It has {self.blocks[id].health}  health remaining"
        # )
        if self.blocks[id].isDead():
            canvas.itemconfig(id, fill="", activefill="green", tags="")

class Enemy:
    def __init__(self, canvas, id):
        self.canvas = canvas
        self.id = id
        self.tickCount = 100
        self.isMoving = False
        self.isExploded = False
        self.collidedId = ""

    def moving(self):
        return self.isMoving

    def moveEnemy(self):
        x1, y1, _, _ = self.canvas.coords(self.id)
        if self.tickCount > 0:
            self.isMoving = True
            x_distance = 200 - x1
            y_distance = 200 - y1
            x_increment = math.floor(x_distance / self.tickCount)
            y_increment = math.floor(y_distance / self.tickCount)
            self.canvas.move(self.id, x_increment, y_increment)
            self.tickCount -= 1
            self.checkCollision()

    def explode(self):
        self.isExploded = True
        self.canvas.delete(self.id)

    def exploded(self):
        return self.isExploded

    def checkCollision(self):
        overlaps = self.canvas.find_overlapping(*self.canvas.bbox(self.id))
        for object in overlaps:
            if "tower" in self.canvas.gettags(object):
                self.collidedId = object
                self.explode()
            elif "wall" in self.canvas.gettags(object):
                self.collidedId = object
                self.explode()


class Enemies:
    def __init__(self, canvas, max=25) -> None:
        self.canvas = canvas
        self.numEnemies = 0
        self.maxEnemies = max
        self.enemyList = []

    def spawn_enemy(self):
        if self.numEnemies < self.maxEnemies:
            pickedWall = random.choice(["top", "left", "bottom", "right"])
            newX = 0
            newY = 0
            if pickedWall == "top":
                newX = random.randint(0, 400)
            elif pickedWall == "left":
                newY = random.randint(0, 400)
            elif pickedWall == "bottom":
                newX = random.randint(0, 400)
                newY = 400
            elif pickedWall == "right":
                newX = 400
                newY = random.randint(0, 400)
            self.enemyList.append(
                Enemy(
                    self.canvas,
                    self.canvas.create_oval(newX, newY, newX + 5, newY + 5, fill="red"),
                )
            )
            self.numEnemies += 1

    def delete_enemy(self, enemy):
        if enemy in self.enemyList:
            self.enemyList.remove(enemy)
            self.numEnemies -= 1


class Game:
    def __init__(self, canvas):
        self.canvas = canvas
        self.enemies = Enemies(self.canvas)
        self.enemies.spawn_enemy()
        self.enemyTicks = 10
        self.tower = Tower(self.canvas)

    def gameLoop(self):
        deletionList = []
        for enemy in self.enemies.enemyList:
            enemy.moveEnemy()
            if enemy.exploded():
                deletionList.append(enemy)
                if enemy.collidedId == self.tower.id:
                    self.tower.loseLife()
                elif enemy.collidedId in self.tower.blocks.keys():
                    self.tower.damageWall(enemy.collidedId)
                    self.tower.tower_stats.setMoney(10)
                    self.tower.tower_stats.updateMoney()
        for enemy in deletionList:
            self.enemies.delete_enemy(enemy)

        if (
            self.tower.tower_stats.getLife() > 0
            and self.tower.tower_stats.getMoney() < 1000
        ):
            self.enemyTicks -= 1
            if self.enemyTicks == 0:
                self.enemies.spawn_enemy()
                self.enemyTicks = 10
            self.canvas.after(100, self.gameLoop)
        elif self.tower.tower_stats.getLife() == 0:
            losetext = self.canvas.create_text(
                200,
                190,
                text="You lose! :(",
                fill="white",
                font=("Times New Roman", "30"),
                tags="fg",
            )
            self.canvas.create_rectangle(
                self.canvas.bbox(losetext), fill="black", tags="bg"
            )
            self.canvas.tag_raise("fg")
        else:
            wintext = self.canvas.create_text(
                200,
                190,
                text="You win!  :)",
                fill="lawn green",
                font=("Times New Roman", "30"),
                tags="fg",
            )
            self.canvas.create_rectangle(
                self.canvas.bbox(wintext), fill="black", tags="bg"
            )
            self.canvas.tag_raise("fg")

game = Game(canvas)
canvas.bind_all("<Button 1>", game.tower.drawWall)
game.gameLoop()
tk.mainloop()
