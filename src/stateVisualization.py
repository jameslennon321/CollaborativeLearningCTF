from Tkinter import *
from copy import copy
import random
from game import GameListener
from model import Action
from qFunction import QFunction


class StateVisualization(GameListener):

    def __init__(self, game, team, num):
        self.scale = 5.0
        self.resolution = 20
        self.value_clip = 30
        self.team = team
        self.num = num

        self.master = Tk()
        self.w      = Canvas(self.master, width=game.width*self.scale, height=game.height*self.scale)
        self.w.pack()

    def handle_loop(self, game_state):

        # if random.random() > .1:
        #     return

        game = game_state.game
        state = copy(game_state.states[self.team][self.num])

        tile_width  = float(game.width) / self.resolution * self.scale
        tile_height = float(game.height) / self.resolution * self.scale

        vmin = None
        vmax = None
        values = []

        for x in xrange(self.resolution):
            for y in xrange(self.resolution):
                state.pos = (x*tile_width/self.scale, y*tile_height/self.scale)
                tmp_state = game.transition_model.apply_action(state, Action.stay, game_state)
                features  = tmp_state.q_features(Action.stay)
                value     = QFunction.evaluate(features)

                print tmp_state.pos, value, features[-3]
                values.append(value)
                if vmax is None or value > vmax:
                    vmax = value
                if vmin is None or value < vmin:
                    vmin = value

        self.w.delete(ALL)
        i = 0
        for x in xrange(self.resolution):
            for y in xrange(self.resolution):
                value = values[i]
                scaled_value = (value - vmin) / float(vmax - vmin + 1)
                color = colorString(scaled_value*255,0,0)
                self.w.create_rectangle(x*tile_width, y*tile_height, (x+1)*tile_width, (y+1)*tile_height, fill=color)

                i += 1

        self.master.update_idletasks()
        self.master.update()


def colorString(r,g,b):

    color = '#%02x%02x%02x' % (r, g, b)
    return color

# def visualize_state(game_state, state, scale = 5.0, resolution = 20, value_clip=30):
#
#
#
#     tile_width  = float(game.width) / resolution * scale
#     tile_height = float(game.height) / resolution * scale
#
#     for x in xrange(resolution):
#         for y in xrange(resolution):
#             state.pos = (x, y)
#             value     = QFunction.evaluate(state.q_features(Action.stay))
#             # print value
#             scaled_value = (value + value_clip) / float(2*value_clip)
#             scaled_value = min(1, max(scaled_value, 0))
#             color = colorString(scaled_value*255,0,0)
#             w.create_rectangle(x*tile_width, y*tile_height, (x+1)*tile_width, (y+1)*tile_height, fill=color)
#
#     master.update_idletasks()
#     master.update()