import arcade
# constants:
screen_width = 800
screen_height = 700
screen_title = "Alien game"
gravity = 0.2
player_jump_speed = 15
player_moving_speed = 5

# constants used to scale sprites compared to their original size
player_size = 1
tile_size = 0.5
gem_scaling = 0.7

class PlatformGame(arcade.Window):
    # main application class
    def __init__(self):

        super().__init__(screen_width, screen_height, screen_title)

        # scene object
        self.scene = 0

        # a separate variable holding the player's sprite
        self.player_sprite = 0

        # physics engine
        self.physics_engine = 0
        # camera to scroll the display
        self.camera = 0

        # sound effects
        self.gem_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jumping_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        arcade.set_background_color(arcade.csscolor.BLUE_VIOLET)
    def GameSetup(self):
        # We are setting up the game here and calling this function to restart the game

        # initialize the scene
        self.scene = arcade.Scene()

        # sprite lists
        self.scene.add_sprite_list("Player list")
        self.scene.add_sprite_list("Ground", use_spatial_hash=True)

        # we place the player at these coordinates
        picture_resource = ":resources:images/alien/alienBlue_walk1.png"
        self.player_sprite = arcade.Sprite(picture_resource, 0.6)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 130
        self.scene.add_sprite("Player list", self.player_sprite)

        # the ground
        # a loop to place sprites horizontally
        for x in range(0, 1400, 64):
            tile = arcade.Sprite(":resources:images/tiles/planetMid.png", tile_size)
            tile.center_x = x
            tile.center_y = 32
            self.scene.add_sprite("Ground", tile)

        # put some crates on the ground
        # this shows using a coordinate list to place sprites
        coordinates = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinates:
            crate = arcade.Sprite( ":resources:images/tiles/stoneCorner_right.png", tile_size)
            crate.position = coordinate
            self.scene.add_sprite("Ground", crate)

        #create the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=gravity, walls=self.scene["Ground"])

        # setup the camera
        self.camera = arcade.Camera(self.width, self.height)

        # use a loop to place some coins to pick up
        for x in range(128, 1400, 256):
            gem = arcade.Sprite(":resources:images/items/gemBlue.png", gem_scaling)
            gem.center_y = 96
            gem.center_x = x
            self.scene.add_sprite("gems", gem)

    def on_draw(self):
        # render the screen
        arcade.start_render()
        # code to draw the screen goes here
        # draw our scene
        self.scene.draw()

        # activate our camera
        self.camera.use()

    def on_key_press(self, key, modifiers):
        # called whenever a key is pressed
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
        # Don't let camera travel past 0
        if screen_center_x < 0:
           screen_center_x = 0
        if screen_center_y < 0:
           screen_center_y = 0
        player_center = screen_center_x, screen_center_y
        self.camera.move_to(player_center)

    def update(self, delta_time):
        # movement and game logic
        # move the player with the physics engine
        self.physics_engine.update()

        #position the camera
        self.set_camera_to_player()

        # see if we hit any coins
        gem_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["gems"])

        # loop through each coin we hit and remove it
        for gem in gem_collision_list:
            # remove the coin
            gem.remove_from_sprite_lists()
            # play a sound
            arcade.play_sound((self.gem_sound))


def main_function():
    window = PlatformGame()        # احنا هون خلينا ويندو عبارة عن اوبجيكت في كلاس ماي قيم
    window.GameSetup()  # هون عملنا كول لميثود سيت اب اللي جوا الكلاس ومشيت على ويندو لانها اوبجيكت ضمن الكلاس
    arcade.run()


if __name__ == "__main__":
    main_function()
    # هون عملنا كول للفانكش
