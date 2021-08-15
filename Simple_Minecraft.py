from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)

blocks = [grass_texture, stone_texture, brick_texture, dirt_texture]
block_pick = 0

"""window.fps_counter.enabled = False
window.exit_button.visible = False"""


def update():
    global block_pick

    if held_keys['left mouse']:
        hand.active()
        punch_sound.play()
    else:
        hand.passive()

    if held_keys['z']: block_pick = 0
    if held_keys['x']: block_pick = 1
    if held_keys['c']: block_pick = 2
    if held_keys['v']: block_pick = 3


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), tex=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=tex,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                voxel = Voxel(position=self.position + mouse.normal,
                              tex=blocks[block_pick])
            if key == 'left mouse down':
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True
        )


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -20, 0),
            position=Vec2(0.4, -0.6)
        )

    def active(self):
        # self.rotation = Vec3(150, -10, 0)
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        # self.rotation = Vec3(150, -10, 0)
        self.position = Vec2(0.4, -0.6)


for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()
