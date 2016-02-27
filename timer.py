# from makerbuttons import Manager, Button,TextBox, DraggableButton, foo, MenuButton # noqa
import pyglet # noqa
import time
from pyglet.gl import * # noqa
from pyglet.window import key # noqa
from pyglet.window import mouse # noqa
import sys


class Button(object):
    def __init__(self, upsprite, hoversprite, downsprite, x, y, callback=None, batch=None, label=None, args=None, labelbatch=None):
        self.func = callback
        self.upsprite = upsprite
        self.downsprite = downsprite
        self.hoversprite = hoversprite
        self.trigger = 0
        self.sprite = pyglet.sprite.Sprite(
            upsprite,
            x, y, batch=batch
        )
        if label is not None:
            self.label = pyglet.text.Label(
                label,
                font_name='Times New Roman',
                font_size=32,
                x=self.sprite.x + self.sprite.width / 2,
                y=self.sprite.y + self.sprite.height / 2,
                anchor_x='center',
                anchor_y='center',
                batch=labelbatch
            )

    def on_mouse_motion(self, x, y, dx, dy):
        if (self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and
                y < self.sprite.y + self.sprite.height):
            self.sprite.image = self.hoversprite
        else:
            self.trigger = 0
            self.sprite.image = self.upsprite

    def move(self, x, y):
        self.sprite.x, self.label.x = x, x
        self.sprite.y, self.label.y = y, y

    def on_mouse_press(self, x, y, mode):
        if (self.sprite.x < x and
                x < self.sprite.x + self.sprite.width and
                self.sprite.y < y and
                y < self.sprite.y + self.sprite.height):
            if mode == 1 and self.trigger == 1:
                self.trigger = 0
                self.sprite.image = self.hoversprite
                try:
                    self.do_action()
                except:
                    pass
            if mode == 0:
                self.sprite.image = self.downsprite
                self.trigger = 1

    def do_action(self):
        try:
            self.func()
        except:
            pass


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

button = load_image('button.png', False)
buttonhover = load_image('buttonhover.png', False)
buttondown = load_image('buttondown.png', False)
# sprite = pyglet.sprite.Sprite(
# 	button,
# 	100, 100, batch=batches[0]
# )


class Game(pyglet.window.Window):
    def __init__(self, height, width, batches):
        super(Game, self).__init__(width, height, caption='Buttons')
        self.dorun = False
        pyglet.gl.glClearColor(.5, .5, .5, 1)
        self.alive = True
        self.batches = batches
        self.time = None
        self.trial = 1
        self.button = None
        self.label = pyglet.text.Label(
            "",
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
        self.setup()

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

    def set_time(self):
        self.time = time.time()

    def start(self):
        if not self.dorun:
            self.dorun = True
            self.set_time()

    def on_draw(self):
        self.render()

    def setup(self):
        self.button = Button(
            button, buttondown, buttonhover, (window_width - button.width) / 2,
            100, self.start, self.batches[1], "Start", None, self.batches[2]
        )

    def on_close(self):
        self.alive = False

    def on_mouse_release(self, x, y, button, modifiers):
        self.button.on_mouse_press(x, y, 1)

    def on_mouse_press(self, x, y, button, modifiers):
        self.button.on_mouse_press(x, y, 0)

    def on_mouse_motion(self, x, y, dx, dy):
        self.button.on_mouse_motion(x, y, dx, dy)

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
