"""
Idea: create a roguelike game in python3 inspired by dungeon crawl,
capable of different graphic engines (at the moment: pygame)
author: Horst JENS
co-authors: Oskar Salomonowitz
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: https://github.com/horstjens/roguebasin_python3

based on: http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod,_part_4

field of view and exploration
see http://www.roguebasin.com/index.php?title=Comparative_study_of_field_of_view_algorithms_for_2D_grid_based_worlds

field of view improving, removing of artifacts:
see https://sites.google.com/site/jicenospam/visibilitydetermination

graphics mostly from Dungeon Crawl: http://crawl.develz.org/
"""

import pygame


def make_text(text="@", font_color=(255, 0, 255), font_size=48, font_name="mono", bold=True, grid_size=None):
    """returns pygame surface with text and x, y dimensions in pixel
       grid_size must be None or a tuple with positive integers.
       Use grid_size to scale the text to your desired dimension or None to just render it
       You still need to blit the surface.
       Example: text with one char for font_size 48 returns the dimensions 29,49
    """
    myfont = pygame.font.SysFont(font_name, font_size, bold)
    size_x, size_y = myfont.size(text)
    mytext = myfont.render(text, True, font_color)
    mytext = mytext.convert_alpha()  # pygame surface, use for blitting
    if grid_size is not None:
        # TODO error handler if grid_size is not a tuple of positive integers
        mytext = pygame.transform.scale(mytext, grid_size)
        mytext = mytext.convert_alpha()  # pygame surface, use for blitting
        return mytext, (grid_size[0], grid_size[1])

    return mytext, (size_x, size_y)


def write(background, text, x=50, y=150, color=(0, 0, 0),
          font_size=None, font_name="mono", bold=True, origin="topleft"):
    """blit text on a given pygame surface (given as 'background')
       the origin is the alignment of the text surface
    """
    if font_size is None:
        font_size = 24
    font = pygame.font.SysFont(font_name, font_size, bold)
    width, height = font.size(text)
    surface = font.render(text, True, color)

    if origin == "center" or origin == "centercenter":
        background.blit(surface, (x - width // 2, y - height // 2))
    elif origin == "topleft":
        background.blit(surface, (x, y))
    elif origin == "topcenter":
        background.blit(surface, (x - width // 2, y))
    elif origin == "topright":
        background.blit(surface, (x - width, y))
    elif origin == "centerleft":
        background.blit(surface, (x, y - height // 2))
    elif origin == "centerright":
        background.blit(surface, (x - width, y - height // 2))
    elif origin == "bottomleft":
        background.blit(surface, (x, y - height))
    elif origin == "bottomcenter":
        background.blit(surface, (x - width // 2, y))
    elif origin == "bottomright":
        background.blit(surface, (x - width, y - height))




# class FragmentSprite(VectorSprite):
#
#     def _overwrite_parameters(self):
#         super()._overwrite_parameters()
#         self.alpha = 255
#         self.delta_alpha = 255 / self.max_age if self.max_age > 0 else 1
#
#     def update(self, seconds):
#         super().update(seconds)
#         # 0 = full transparency, 255 = no transparency at all
#         self.alpha -= self.delta_alpha * seconds * 0.4  # slowly become more transparent
#         self.image.set_alpha(self.alpha)
#         self.image.convert_alpha()
#
#
# class Flytext(VectorSprite):
#     def __init__(self, text, fontsize=22, acceleration_factor=1.02, max_speed=300, **kwargs):
#         """a text flying upward and for a short time and disappearing"""
#
#         VectorSprite.__init__(self, **kwargs)
#         ##self._layer = 7  # order of sprite layers (before / behind other sprites)
#         ##pygame.sprite.Sprite.__init__(self, self.groups)  # THIS LINE IS IMPORTANT !!
#         self.text = text
#         self.acceleartion_factor = acceleration_factor
#         self.max_speed = max_speed
#         self.kill_on_edge = True
#         self.image = make_text(self.text, self.color, fontsize)[0]  # font 22
#         self.rect = self.image.get_rect()
#
#     def update(self, seconds):
#         self.move *= self.acceleartion_factor
#         if self.move.length() > self.max_speed:
#             self.move.normalize_ip()
#             self.move *= self.max_speed
#         VectorSprite.update(self, seconds)
