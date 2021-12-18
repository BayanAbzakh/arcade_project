import arcade
import random
"""The library used to make the platform game"""
"""The library used to generate randomness"""


screen_width = 800
screen_height = 700

screen_title = "Alien game"
gravity = 0.5
player_jump_speed = 20
player_moving_speed = 10
player_size = 1
tile_size = 0.5
gem_scaling = 0.7
map_size = 5000
ground_scaling = .5
CHARACTER_SCALING = .7
# they will be 0,1 in the list index
RIGHT_FACING = 0
LEFT_FACING = 1
# for start menu
intro_text = "Start"
"""constants"""


class InstructionView(arcade.View):
    """
       A class used for the starting screen

       ...

       Attributes
       ----------
       game_view = PlatformGame()
           a variable that contains the PlatformGame class


       Methods
       -------
       def on_show(self):
           this method is called to show the view for the first time

       def on_draw(self):
           This method is called to start drawing the view and rendering the screen

       def on_mouse_press(self, _x, _y, _button, _modifiers):
           This method calls the game when the mouse is pressed

       """

def load_texture_pair(filename):
    """
    In this function we have the list of the textures of player's sprite

    Parameters
    ----------
    filename
        the name of the file leading to the picture of sprite

        [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]
        list containing the static idle, right and mirrored textures

    """

class PlayerCharacter(arcade.Sprite):
    """class That contains the player sprite object

    methods
    ----------
    def update_animation(self, delta_time: float = 1 / 600):
        this method defines which player sprite texture is shown according
        to the movement of the sprite using if statements
    """



    def __init__(self):
        """parent function to initiate


        Attributes
        ----------
        self.character_face_direction:
             variable that contains the RIGHT_FACING variable = 0
        self.cur_texture:
            set the value of texture to zero
        self.scale:
            the scaling of the player sprite
        main_path:
            the main path of the player sprite picture
        self.idle_texture_pair:
            call the function of load_texture_pair and the path to picture when sprite is static
        self.walk_textures = []
            list of textures of when the sprite is moving
        """


class PlatformGame(arcade.Window):
    """This is the main application class that all functions belong to"""

    def __init__(self):
        super().__init__(screen_width, screen_height, screen_title)
        """call the parent class and set up the window
        
        methods
        def on_draw(self):
        def on_key_press(self, key, modifiers)
        def on_key_release(self, key, modifiers):
        def set_camera_to_player(self):
        
        
         ----------
         Parameters
         ----------
        self.scene:
            scene object
        self.player_sprite:
            variable holding sprite
        self.physics_engine:
            physics engine variable
        self.camera:
            camera to track player sprite
        self.score_camera:
            camera to track score
        self.gem_sound = arcade.load_sound()
            variable containing sound resource
        self.jumping_sound = arcade.load_sound()
            variable containing sound resource
        arcade.set_background_color(arcade.csscolor.BLUE_VIOLET)
            color of background
        self.score = 0
         """


         self.scene = 0
         """Scene is used to manage a number of different SpriteLists.
         """


    def Setup(self):
        """This function is used to set up the game and restart it

        Attributes
        ----------
        self.scene:
            to initialize the scene
        self.scene.add_sprite_list() : str
            to create new lists and add them to scene object
        self.player_sprite():
            variable holding the player sprite added as a PlayerCharacter() object
        self.scene.add_sprite():
            adds a variable to a list
        tile:
            variable containing attributes for ground tiles
        rand_num = random.randint(0, 2):
            this is a random number generator using random library
        self.scene.add_sprite:
            to add something to a list
        self.physics_engine = arcade.PhysicsEnginePlatformer():
            controls the physics of the game by assigning a
            gravity constant to player sprite and not assigning
            to other non-moving sprites
        self.camera = arcade.Camera():
            camera that keeps player sprite in center
        self.score_camera = arcade.Camera:
            static camera that tracks the score
        """


        self.scene.add_sprite("Player list", self.player_sprite)
        self.scene.add_sprite("Ground", tile)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=gravity,
                                                             walls=self.scene["Ground"])


    def update(self, delta_time):
        """
        function that updates the game methods
        """


def main_function():
    """This is the method that calls the methods before
    to start the start screen
    """


window = arcade.Window(screen_width, screen_height, screen_title)
start_view = InstructionView()
window.show_view(start_view)
arcade.run()