import TileObject, World, Creature, pyglet

f = None
data = None

SIZE_X = 75
SIZE_Y = 45
tileSize = 16
world = World.World(SIZE_X, SIZE_Y)

window = pyglet.window.Window(
    width  = SIZE_X * tileSize,
    height = SIZE_Y * tileSize
)


def makeTileImg(path):
    img = pyglet.resource.image(path)
    img.width = tileSize
    img.height = tileSize
    return img

batch = pyglet.graphics.Batch()
tileImages = {
    TileObject.Tree:       makeTileImg('img/tree.png'),
    TileObject.Food:       makeTileImg('img/food.png'),
    TileObject.TileObject: makeTileImg('img/tile.png'),
    Creature.Creature:     makeTileImg('img/creature.png')
}
sprites = [
    [pyglet.sprite.Sprite(tileImages[TileObject.TileObject],
                            col*tileSize, row*tileSize, batch=batch)
        for col in range(SIZE_X)]
    for row in range(SIZE_Y)
]



@window.event
def on_draw():
    setSpriteImages()
    batch.draw()
    getCurrentState().draw()

def getCurrentState():
    return pyglet.text.Label('time step: %d  born: %d  dead: %d  alive: %d' %(world.time, world.born,
                              world.dead, world.alive),
                              font_name='mono',
                              font_size= 10,
                              x=window.width / 100, y=window.height / 100,
                              anchor_x='left', anchor_y='bottom')

def setSpriteImages():
    for row in range(SIZE_Y):
        for col in range(SIZE_X):
            tileObject = world.tiles[row][col].visibleTileObject()
            img = tileImages[tileObject.__class__]
            sprites[row][col].image = img
'time step: %d  born: %d  dead: %d  alive: %d'

def step(dx):
    world.step()

    if world.saveData == True:
        data = "%d %d %d %d\n" %(world.time, world.born, world.dead, world.alive)
        f.write(data)

pyglet.clock.schedule_interval(step, 0.01)

def main():
    print "To begin simulation type 'run'."
    print "To exit simulation, exit window."
    print "To quit program type 'quit'."
    print "To save data from run, type 'create file'."

    while True:
        commandLine = raw_input(">>> ")
        if commandLine == 'run':
            pyglet.app.run()
        if commandLine == 'create file':
            filename = raw_input("enter file name: ")
            global f
            f = open(filename, 'w')
            f.write('timestep born dead alive\n')
            world.saveData = True
        if commandLine == 'quit':
            if world.saveData == True:
                genomes = [c.genome for c in world.getCreatures()]
                s = str(genomes)
                f.write(s)
                f.close()
            return False



main()
