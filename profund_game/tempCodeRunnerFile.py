if reset_check:
            screen.fill(GREEN)
            if yes_button.draw(screen):
                level = 1
                score = 0
                player.temp_score = 0
                player_name_confirm = False
                player_name = ''
                world_data = reset_level()
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, health_bar = world.process_data(world_data)
                reset_check == False
            if no_button.draw(screen):
                reset_check == False