import pygame
import sys
from maze import Maze



def main():
    state = "WALL"
    running = True
    LEFT = 1
    RIGHT = 3
    width = 900
    height = 900
    node_size = 30


    pygame.init()
    screen = pygame.display.set_mode((width,height), 0, 32)
    screen.fill((0,0,0))

    maze= Maze(screen, node_size)
    maze.draw_boundaries(width, height)
    maze.draw_grid(width,height)

    while running:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                x, y = event.pos[0]//node_size, event.pos[1]//node_size
                maze.draw_block(state,x,y)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                x, y = event.pos[0]//node_size, event.pos[1]//node_size
                maze.delete_block(x,y)

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    state = "START"


                if event.key == pygame.K_w:
                    state = "WALL"
                
                if event.key == pygame.K_e:
                    state = "END"
                
                if event.key == pygame.K_b:
                    maze.bfs()
                    maze.draw_path()
                    #print(maze.get_path())
                    #print(maze.get_visited())
                
                if event.key == pygame.K_d:
                    maze.dfs(maze.starting_node)
                    #print(maze.get_path())
                    #print(maze.get_visited())
                    maze.draw_path()
                
                if event.key == pygame.K_r:
                    maze.restart()
                
                if event.key == pygame.K_l:
                    maze.createMaze("maze.csv")
                
                if event.key == pygame.K_s:
                    maze.save_maze()

        pygame.display.update()
    
    pygame.quit()
    sys.exit()

main()



