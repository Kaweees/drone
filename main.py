import time
import pygame
import ardrone


def wait_for_state(drone, key, value, timeout=10):
    """Poll navdata until state[key] == value, or timeout."""
    start = time.time()
    while time.time() - start < timeout:
        state = drone.navdata.get('state', {})
        if state.get(key) == value:
            return True
        time.sleep(0.1)
    return False


drone = ardrone.ARDrone()

# Wait for navdata stream to start
if not wait_for_state(drone, 'navdata_demo', 1):
    print("No navdata received - is the drone connected?")
    drone.halt()
    exit(1)

# Clear emergency state if set from a previous session
if drone.navdata['state']['emergency']:
    print("Clearing emergency state...")
    drone.reset()
    wait_for_state(drone, 'emergency', 0)

drone.trim()

pygame.init()
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("AR.Drone")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_t:
                drone.takeoff()
            elif event.key == pygame.K_l:
                drone.land()
            elif event.key == pygame.K_r:
                drone.reset()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        drone.move_forward()
    elif keys[pygame.K_DOWN]:
        drone.move_backward()
    elif keys[pygame.K_LEFT]:
        drone.move_left()
    elif keys[pygame.K_RIGHT]:
        drone.move_right()
    elif keys[pygame.K_w]:
        drone.move_up()
    elif keys[pygame.K_s]:
        drone.move_down()
    elif keys[pygame.K_a]:
        drone.move(0, 0, 0, -0.5)
    elif keys[pygame.K_d]:
        drone.move(0, 0, 0, 0.5)
    else:
        drone.hover()

    surface = pygame.image.frombuffer(drone.image.tobytes(), (640, 360), 'RGB')
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
drone.halt()
