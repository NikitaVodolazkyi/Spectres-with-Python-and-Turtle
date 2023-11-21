from TurtleTools import *
from math import *
screen.colormode(255)


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

    def __init__(self, vertices, quad, tile_type):
        self.vertices = vertices
        self.quad = quad
        self.tile_type = tile_type

    @property
    def colour(self):
        return palette[self.tile_type]

    def draw(self, T):
        draw_polygon(self.vertices, T, self.colour)


class Meta:
    def __init__(self):
        self.children = []
        self.quad = []

    def add_child(self, tile, T):
        self.children.append({'tile': tile, 'transf': T})

    def draw(self, M):
        for child in self.children:
            child['tile'].draw(mul(M, child['transf']))


def build_spectre_base() -> dict[str, Meta]:
    spectre_types = [
        'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi',
        'Pi', 'Sigma', 'Phi', 'Psi']

    spectre = (
        pt(0, 0),
        pt(1.0, 0.0),
        pt(1.5, -0.8660254037844386),
        pt(2.366025403784439, -0.36602540378443865),
        pt(2.366025403784439, 0.6339745962155614),
        pt(3.366025403784439, 0.6339745962155614),
        pt(3.866025403784439, 1.5),
        pt(3.0, 2.0),
        pt(2.133974596215561, 1.5),
        pt(1.6339745962155614, 2.3660254037844393),
        pt(0.6339745962155614, 2.3660254037844393),
        pt(-0.3660254037844386, 2.3660254037844393),
        pt(-0.866025403784439, 1.5),
        pt(0.0, 1.0)
    )

    spectre = enlarge(10, spectre)
    spectre_quad = (
        spectre[3], spectre[5], spectre[7], spectre[11]
    )

    base = dict((label, Tile(spectre, spectre_quad, label)) for label in spectre_types)

    mystic = Meta()
    mystic.add_child(Tile(spectre, spectre_quad, 'Gamma1'), ident)
    mystic.add_child(Tile(spectre, spectre_quad, 'Gamma2'),
                     mul(ttrans(spectre[8]["x"], spectre[8]["y"]), trot(pi / 6)))

    mystic.quad = spectre_quad
    base['Gamma'] = mystic

    return base


def build_supertiles(base_tiles: dict[str, Meta]) -> dict[str, Meta]:
    quad = base_tiles['Delta'].quad

    connection_rules = [
        [60, 3, 1], [0, 2, 0], [60, 3, 1], [60, 3, 1],
        [0, 2, 0], [60, 3, 1], [-120, 3, 3]]

    Ts = [ident]
    total_ang = 0
    rotation = ident
    new_quad = list(quad)
    for angle, from_, to in connection_rules:
        total_ang += angle
        if angle != 0:
            rotation = trot(radians(total_ang))
            for i in range(4):
                new_quad[i] = transPt(rotation, quad[i])

        translation = transTo(new_quad[to], transPt(Ts[-1], quad[from_]))
        Ts.append(mul(translation, rotation))

    # This is x-reflection I don't completely understand how superquad is formed yet
    R = [-1, 0, 0, 0, 1, 0]
    for i in range(len(Ts)):
        Ts[i] = mul(R, Ts[i])

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
        transPt(Ts[6], quad[2]),
        transPt(Ts[5], quad[1]),
        transPt(Ts[3], quad[2]),
        transPt(Ts[0], quad[1])
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
