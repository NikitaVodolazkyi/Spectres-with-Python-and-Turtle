from __future__ import annotations
from turtle_tools import *
from math import *


spectre_types = [
    'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi',
    'Pi', 'Sigma', 'Phi', 'Psi']


palette = {
    'Gamma': [203, 157, 126],
    'Gamma1': [203, 157, 126],
    'Gamma2': [203, 157, 126],
    'Delta': [163, 150, 133],
    'Theta': [208, 215, 150],
    'Lambda': [184, 205, 178],
    'Xi': [211, 177, 144],
    'Pi': [218, 197, 161],
    'Sigma': [191, 146, 126],
    'Phi': [228, 213, 167],
    'Psi': [224, 223, 156]
}


class Tile:
    global palette

    def __init__(self, vertices, quad, tile_type: str):
        self.vertices = vertices
        self.quad = quad
        self.tile_type = tile_type

    @property
    def colour(self) -> list[int]:
        return palette[self.tile_type]

    def draw(self, T: Matrix):
        draw_polygon(self.vertices, T, self.colour)


# Consider changing the drawing method and how the transformations are stored
class Meta:
    def __init__(self):
        self.children = []
        self.quad = []

    def add_child(self, tile: Meta | Tile, T: Matrix) -> None:
        self.children.append({'tile': tile, 'transf': T})

    def draw(self, M: Matrix) -> None:
        for child in self.children:
            child['tile'].draw(M * child['transf'])


def build_spectre_base() -> dict[str, Meta]:

    spectre = (
        Point(0, 0),
        Point(1.0, 0.0),
        Point(1.5, -0.8660254037844386),
        Point(2.366025403784439, -0.36602540378443865),
        Point(2.366025403784439, 0.6339745962155614),
        Point(3.366025403784439, 0.6339745962155614),
        Point(3.866025403784439, 1.5),
        Point(3.0, 2.0),
        Point(2.133974596215561, 1.5),
        Point(1.6339745962155614, 2.3660254037844393),
        Point(0.6339745962155614, 2.3660254037844393),
        Point(-0.3660254037844386, 2.3660254037844393),
        Point(-0.866025403784439, 1.5),
        Point(0.0, 1.0)
    )

    spectre_quad = (
        spectre[3], spectre[5], spectre[7], spectre[11]
    )

    base = dict((label, Tile(spectre, spectre_quad, label)) for label in spectre_types)

    mystic = Meta()
    mystic.add_child(Tile(spectre, spectre_quad, 'Gamma1'), IDENT)
    mystic.add_child(Tile(spectre, spectre_quad, 'Gamma2'),
                     Matrix.trans(spectre[8].x, spectre[8].y) * Matrix.rot(pi / 6))

    mystic.quad = spectre_quad
    base['Gamma'] = mystic

    return base


def build_supertiles(base_tiles: dict[str, Meta]) -> dict[str, Meta]:
    quad = base_tiles['Delta'].quad

    connection_rules = [
        [60, 3, 1], [0, 2, 0], [60, 3, 1], [60, 3, 1],
        [0, 2, 0], [60, 3, 1], [-120, 3, 3]]

    Ts = [IDENT]
    total_ang = 0
    rotation = IDENT
    new_quad = list(quad)
    for angle, i_from, i_to in connection_rules:
        total_ang += angle
        if angle != 0:
            rotation = Matrix.rot(radians(total_ang))
            for i in range(4):
                new_quad[i] = rotation * quad[i]

        translation = trans_to(new_quad[i_to], Ts[-1] * quad[i_from])
        Ts.append(translation * rotation)

    # This is x-reflection and IDK why is it here
    # This can also be optimized
    R = Matrix([-1, 0, 0, 0, 1, 0])
    for i in range(len(Ts)):
        Ts[i] = R * Ts[i]

    supertile_rules = {
        'Gamma': ['Pi', 'Delta', 'null', 'Theta', 'Sigma', 'Xi', 'Phi', 'Gamma'],
        'Delta': ['Xi', 'Delta', 'Xi', 'Phi', 'Sigma', 'Pi', 'Phi', 'Gamma'],
        'Theta': ['Psi', 'Delta', 'Pi', 'Phi', 'Sigma', 'Pi', 'Phi', 'Gamma'],
        'Lambda': ['Psi', 'Delta', 'Xi', 'Phi', 'Sigma', 'Pi', 'Phi', 'Gamma'],
        'Xi': ['Psi', 'Delta', 'Pi', 'Phi', 'Sigma', 'Psi', 'Phi', 'Gamma'],
        'Pi': ['Psi', 'Delta', 'Xi', 'Phi', 'Sigma', 'Psi', 'Phi', 'Gamma'],
        'Sigma': ['Xi', 'Delta', 'Xi', 'Phi', 'Sigma', 'Pi', 'Lambda', 'Gamma'],
        'Phi': ['Psi', 'Delta', 'Psi', 'Phi', 'Sigma', 'Pi', 'Phi', 'Gamma'],
        'Psi': ['Psi', 'Delta', 'Psi', 'Phi', 'Sigma', 'Psi', 'Phi', 'Gamma']
    }

    supertile_quad = [
        Ts[6] * quad[2],
        Ts[5] * quad[1],
        Ts[3] * quad[2],
        Ts[0] * quad[1]
    ]

    supertile = {}
    for main_type, sub_types in supertile_rules.items():
        sup = Meta()
        for i, sub_type in enumerate(sub_types):
            if sub_type == 'null':
                continue

            sup.add_child(base_tiles[sub_type], Ts[i])

        sup.quad = supertile_quad
        supertile[main_type] = sup
        # draw_polygon(sup.quad)
    return supertile
