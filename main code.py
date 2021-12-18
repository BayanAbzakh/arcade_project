"This code was made using the official arcade documentation website"
"The source code was borrowed from the documentation"
"https://api.arcade.academy/en/latest/examples/platform_tutorial/index.html"

import arcade
import random

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
RIGHT_FACING = 0
LEFT_FACING = 1
intro_text = "Start"


class InstructionView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(intro_text, self.window.width / 2, self.window.height / 2, arcade.color.WHITE, font_size=50,
                         anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = PlatformGame()
        game_view.setup()
        self.window.show_view(game_view)


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):

        super().__init__()
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING
        main_path = ":resources:images/alien/alienBlue"
        self.idle_texture_pair = load_texture_pair(f"{main_path}_front.png")
        self.walk_textures = []
        for i in range(1, 3, 1):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)
        self.texture = self.idle_texture_pair[0]

    def update_animation(self, delta_time: float = 1 / 600):

        if self.change_x < 0:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0:
            self.character_face_direction = RIGHT_FACING

        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        self.cur_texture += 1
        if self.cur_texture > 1:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]


class PlatformGame(arcade.View):
    def __init__(self):
        # super().__init__(screen_width, screen_height, screen_title)
        super().__init__()
        self.scene = 0
        self.player_sprite = 0
        self.physics_engine = 0
        self.camera = 0
        self.score_camera = 0
        self.gem_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jumping_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        arcade.set_background_color(arcade.csscolor.BLUE_VIOLET)

        self.score = 0

    def setup(self):
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player list")
        self.scene.add_sprite_list("Ground", use_spatial_hash=True)

        self.score = 0

        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 130
        self.scene.add_sprite("Player", self.player_sprite)

        for x in range(0, map_size, 64):
            tile = arcade.Sprite(":resources:images/tiles/planetMid.png", tile_size)
            tile.center_x = x
            tile.center_y = 32
            self.scene.add_sprite("Ground", tile)

        for x in range(250, map_size, 128):
            rand_num = random.randint(0, 2)
            if rand_num == 0:
                ground = arcade.Sprite(":resources:images/tiles/stoneCorner_right.png", ground_scaling)  # 64px
                ground.position = [x, 96]
                self.scene.add_sprite("Ground", ground)
            if rand_num == 1:
                gem = arcade.Sprite(":resources:images/items/gemBlue.png", gem_scaling)
                gem.center_y = 96
                gem.center_x = x
                self.scene.add_sprite("gems", gem)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=gravity,
                                                             walls=self.scene["Ground"])
        self.camera = arcade.Camera(screen_width, screen_height)
        self.score_camera = arcade.Camera(screen_width, screen_height)

    def on_draw(self):
        arcade.start_render()

        self.camera.use()
        self.scene.draw()

        self.score_camera.use()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = player_moving_speed
                arcade.play_sound(self.jumping_sound)
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -player_moving_speed
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = player_moving_speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def set_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_center = screen_center_x, screen_center_y
        self.camera.move_to(player_center)

    def update(self, delta_time):

        self.physics_engine.update()
        self.set_camera_to_player()
        gem_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["gems"])
        for gem in gem_collision_list:
            gem.remove_from_sprite_lists()
            arcade.play_sound((self.gem_sound))
            self.score += 1

        self.scene.update_animation(
            delta_time, ["gems", "Ground", "Player"]
        )
        global intro_text
        if len(self.scene["gems"]) == 0:
            intro_text = "You won.\nPlay again?"
            PlatformGame().setup()
            view = InstructionView()
            self.window.show_view(view)

        if self.player_sprite.center_x < 0 or self.player_sprite.center_x > map_size:
            intro_text = "Game over.\nPlay again?"
            PlatformGame().setup()
            view = InstructionView()
            self.window.show_view(view)


def main_function():
    window = arcade.Window(screen_width, screen_height, screen_title)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main_function()
    
"This code was made using the official arcade documentation website"
"The source code was borrowed from the documentation"
"https://api.arcade.academy/en/latest/examples/platform_tutorial/index.html"
