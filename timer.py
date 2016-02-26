# from makerbuttons import Manager, Button,TextBox, DraggableButton, foo, MenuButton # noqa
import pyglet # noqa
import time
from pyglet.gl import * # noqa
from pyglet.window import key # noqa
from pyglet.window import mouse # noqa
import sys


clock = 30
try:
    clock = int(sys.argv[1])
except:
    clock = 30

batches = [pyglet.graphics.Batch(), pyglet.graphics.Batch(), pyglet.graphics.Batch(), ]


def load_image(image, anchor=True):
    try:
        return image_dict(image)
    except:
        img = pyglet.image.load('images/' + image)
        if anchor:
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2
        return img

fps_display = pyglet.clock.ClockDisplay()

# button = load_image('button.png', False)
# buttonhover = load_image('buttonhover.png', False)
# buttondown = load_image('buttondown.png', False)
# sprite = pyglet.sprite.Sprite(
# 	button,
# 	100, 100, batch=batches[0]
# )


class Game(pyglet.window.Window):
    def __init__(self, height, width, batches):
        super(Game, self).__init__(width, height, caption='Buttons')
        self.dorun = True
        pyglet.gl.glClearColor(.2, .2, .2, .2)
        self.alive = True
        self.batches = batches
        self.time = None
        self.trial = 1
        self.label = pyglet.text.Label(
            "nothing",
            font_name='Times New Roman',
            font_size=128,
            x=window_width / 2,
            y=window_height / 2,
            anchor_x='center',
            anchor_y='center',
            batch=self.batches[0]
        )

        self.blocklabel = pyglet.text.Label(
            "block 1 trial 1",
            font_name='Times New Roman',
            font_size=32,
            x=window_width - 200,
            y=window_height - 50,
            anchor_x='center',
            anchor_y='center',
            batch=self.batches[0]
        )

        self.notify = None

    def render(self, *args):
        self.update()
        self.clear()
        for batch in self.batches:
            batch.draw()
        fps_display.draw()

        self.flip()

    def force_draw(self):
        self.clear()
        for batch in self.batches:
            batch.draw()
        fps_display.draw()

        self.flip()

    def make_dict(self):
        pass

    def update(self):
        if self.dorun:
            newtime = time.time()
            elapsed = int(newtime - self.time)
        # elapsed = int(elapsed)
            # print elapsed
            if clock - elapsed == 0:
                self.label.text = "X"
                if self.trial < 5:
                    self.trial += 1
                    self.force_draw()
                    time.sleep(2)
                    self.time = time.time()
                    self.blocklabel.text = "block 1 trial " + str(self.trial)
                else:
                    self.label.text = ""
                    self.dorun = False
                    self.notify = pyglet.text.Label(
                        "Please notify the experimenter",
                        font_name='Times New Roman',
                        font_size=32,
                        x=window_width / 2,
                        y=window_height / 2 + 100,
                        anchor_x='center',
                        anchor_y='center',
                        batch=self.batches[0]
                    )

            else:
                self.label.text = str(clock - elapsed)
        # if key_handler[key.D]:
        #     sprite.x += 1
        # if key_handler[key.A]:
        #     sprite.x -= 1
        # if key_handler[key.W]:
        #     sprite.y += 1
        # if key_handler[key.S]:
        #     sprite.y -= 1

    def on_draw(self):
        self.render()

    def set_time(self):
        self.time = time.time()

    def on_close(self):
        self.alive = False

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def run(self):
        while self.alive:
            event = self.dispatch_events()
            if event:
                print(event)
            self.render()

window_height = 800
window_width = 1400
window = Game(window_height, window_width, batches)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

if __name__ == '__main__':
    window.set_time()
    pyglet.clock.set_fps_limit(10)

    window.run()
