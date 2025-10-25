import tkinter as tk
import random
from datetime import datetime

# --- CONFIGURATION CONSTANTS ---
CANVAS_SIZE = 600
ROAD_WIDTH = 60
INTERSECTION_SIZE = 100

# Traffic Light Timing (ms)
BASE_GREEN_TIME = 10000  # 10 seconds for demo
VEHICLE_BONUS_TIME = 2000
YELLOW_TIME = 3000
ALL_RED_TIME = 1000
UPDATE_RATE_MS = 30

# Car Movement
CAR_SPEED = 3

# Road mapping
ROAD_PAIRS_MAP = {
    'NS': ['north', 'south'],
    'EW': ['east', 'west']
}

class TrafficSimApp:
    def __init__(self, master):
        self.master = master
        master.title("Smart Traffic Light Control System")

        # --- State Variables ---
        self.roads = ['north', 'east', 'south', 'west']
        self.state = {r: {'vehicles': [], 'light': 'red'} for r in self.roads}
        self.current_pair_name = 'NS'
        self.manual_override = False
        self.is_emergency_active = False
        self.emergency_target_road = None

        # --- Setup GUI ---
        self.canvas = tk.Canvas(master, width=CANVAS_SIZE, height=CANVAS_SIZE, bg='#1a202c')
        self.canvas.pack()

        # Controls
        control_frame = tk.Frame(master)
        control_frame.pack(pady=10)
        for i, road in enumerate(self.roads):
            tk.Button(control_frame, text=f"{road.capitalize()} +1",
                      command=lambda r=road: self.add_vehicle(r)).grid(row=0, column=i, padx=5)
        tk.Button(control_frame, text="🚨 Emergency", bg='red', fg='white', command=self.toggle_emergency).grid(row=1, columnspan=4, pady=5)

        # Status
        self.status_label = tk.Label(master, text="Initializing...")
        self.status_label.pack()

        # Initialize cars for demo
        for road in self.roads:
            for _ in range(random.randint(1, 3)):
                self.add_vehicle(road)

        # Start simulation
        self.draw_road()
        self.master.after(UPDATE_RATE_MS, self.update_cars)
        self.master.after(100, self.traffic_cycle)

    # --- DRAW METHODS ---
    def draw_road(self):
        self.canvas.delete("all")
        half = CANVAS_SIZE / 2
        int_top = half - INTERSECTION_SIZE / 2
        int_bottom = half + INTERSECTION_SIZE / 2
        int_left = half - INTERSECTION_SIZE / 2
        int_right = half + INTERSECTION_SIZE / 2

        # Background
        self.canvas.create_rectangle(0, 0, CANVAS_SIZE, CANVAS_SIZE, fill='#1a202c')

        # Vertical & Horizontal Roads
        self.canvas.create_rectangle(half - ROAD_WIDTH/2, 0, half + ROAD_WIDTH/2, CANVAS_SIZE, fill='#2d3748')
        self.canvas.create_rectangle(0, half - ROAD_WIDTH/2, CANVAS_SIZE, half + ROAD_WIDTH/2, fill='#2d3748')

        # Intersection
        self.canvas.create_rectangle(int_left, int_top, int_right, int_bottom, fill='#22272e')

        # Stop lines
        self.canvas.create_line(int_left, int_top, int_right, int_top, fill='white', width=3)
        self.canvas.create_line(int_left, int_bottom, int_right, int_bottom, fill='white', width=3)
        self.canvas.create_line(int_left, int_top, int_left, int_bottom, fill='white', width=3)
        self.canvas.create_line(int_right, int_top, int_right, int_bottom, fill='white', width=3)

        self.draw_lights()
        self.draw_cars()

    def draw_lights(self):
        half = CANVAS_SIZE / 2
        size = INTERSECTION_SIZE / 2 + 10
        radius = 8
        light_map = {'red':'#ef4444','yellow':'#f59e0b','green':'#10b981'}

        self.canvas.create_oval(half-15-radius, half-size-radius, half-15+radius, half-size+radius,
                                fill=light_map[self.state['north']['light']], tags='light_north')
        self.canvas.create_oval(half+15-radius, half+size-radius, half+15+radius, half+size+radius,
                                fill=light_map[self.state['south']['light']], tags='light_south')
        self.canvas.create_oval(half+size-radius, half-15-radius, half+size+radius, half-15+radius,
                                fill=light_map[self.state['east']['light']], tags='light_east')
        self.canvas.create_oval(half-size-radius, half+15-radius, half-size+radius, half+15+radius,
                                fill=light_map[self.state['west']['light']], tags='light_west')

    def draw_cars(self):
        for road in self.roads:
            for car in self.state[road]['vehicles']:
                if car['id']:
                    self.canvas.delete(car['id'])
                fill_color = car['color']
                if car.get('is_emergency', False):
                    if (datetime.now().microsecond // 200000) % 2 == 0:
                        fill_color = '#ff0000'
                    else:
                        fill_color = '#00bfff'
                car_id = self.canvas.create_rectangle(car['x'], car['y'], car['x']+car['width'], car['y']+car['height'],
                                                      fill=fill_color, tags=car['tag'])
                car['id'] = car_id

    # --- VEHICLE LOGIC ---
    def add_vehicle(self, road, is_emergency=False):
        half = CANVAS_SIZE/2
        lane_offset = ROAD_WIDTH/2 - 15
        width, height = (15, 25) if road in ['north','south'] else (25,15)
        if road == 'north':
            x = half + lane_offset - width/2
            y = -height if not self.state[road]['vehicles'] else self.state[road]['vehicles'][-1]['y'] - height -5
        elif road == 'south':
            x = half - lane_offset - width/2
            y = CANVAS_SIZE if not self.state[road]['vehicles'] else self.state[road]['vehicles'][-1]['y'] + height +5
        elif road == 'east':
            x = CANVAS_SIZE if not self.state[road]['vehicles'] else self.state[road]['vehicles'][-1]['x'] + width +5
            y = half + lane_offset - height/2
        elif road == 'west':
            x = -width if not self.state[road]['vehicles'] else self.state[road]['vehicles'][-1]['x'] - width -5
            y = half - lane_offset - height/2

        car = {'road':road, 'x':x, 'y':y, 'width':width, 'height':height,
               'color':f'#{random.randint(0,0xFFFFFF):06x}', 'tag':f"car_{road}_{len(self.state[road]['vehicles'])}",
               'id':None, 'is_emergency':is_emergency, 'stopped':False}
        self.state[road]['vehicles'].append(car)

    def update_cars(self):
        half = CANVAS_SIZE/2
        stop_line = INTERSECTION_SIZE/2
        for road in self.roads:
            for car in self.state[road]['vehicles'][:]:
                # Determine light and movement
                current_light = self.state[road]['light']
                moving = current_light=='green' or car['is_emergency']

                if moving:
                    if road=='north':
                        car['y'] += CAR_SPEED
                    elif road=='south':
                        car['y'] -= CAR_SPEED
                    elif road=='east':
                        car['x'] -= CAR_SPEED
                    elif road=='west':
                        car['x'] += CAR_SPEED

                # Remove off-screen cars
                off_screen = ((road=='north' and car['y']>CANVAS_SIZE) or
                              (road=='south' and car['y']+car['height']<0) or
                              (road=='east' and car['x']+car['width']<0) or
                              (road=='west' and car['x']>CANVAS_SIZE))
                if off_screen:
                    if car['id']:
                        self.canvas.delete(car['id'])
                    self.state[road]['vehicles'].remove(car)

        self.draw_cars()
        self.master.after(UPDATE_RATE_MS, self.update_cars)

    # --- TRAFFIC LIGHT LOGIC ---
    def set_lights(self, road1, road2, color):
        self.state[road1]['light'] = color
        self.state[road2]['light'] = color
        for road in [road1, road2]:
            self.canvas.itemconfig(f"light_{road}", fill={'red':'#ef4444','yellow':'#f59e0b','green':'#10b981'}[color])

    def traffic_cycle(self):
        if self.manual_override:
            self.status_label.config(text=f"Manual Override ({self.current_pair_name})")
            self.master.after(1000, self.traffic_cycle)
            return

        # Adaptive logic
        ns_count = len(self.state['north']['vehicles']) + len(self.state['south']['vehicles'])
        ew_count = len(self.state['east']['vehicles']) + len(self.state['west']['vehicles'])
        next_pair = 'NS' if ns_count>=ew_count else 'EW'
        road1, road2 = ROAD_PAIRS_MAP[next_pair]
        duration = BASE_GREEN_TIME + max(ns_count, ew_count)*VEHICLE_BONUS_TIME

        # Emergency override
        if self.is_emergency_active and self.emergency_target_road:
            next_pair = 'NS' if self.emergency_target_road in ['north','south'] else 'EW'
            road1, road2 = ROAD_PAIRS_MAP[next_pair]
            duration *= 1.5
            self.is_emergency_active = False

        self.current_pair_name = next_pair
        self.set_lights(road1, road2, 'green')
        self.status_label.config(text=f"{road1.upper()}/{road2.upper()} GREEN for {duration//1000}s")

        self.master.after(duration, lambda: self._end_green_phase(road1, road2))

    def _end_green_phase(self, road1, road2):
        self.set_lights(road1, road2, 'yellow')
        self.master.after(YELLOW_TIME, lambda: self.set_lights(road1, road2, 'red'))
        self.master.after(YELLOW_TIME+ALL_RED_TIME, self.traffic_cycle)

    # --- EMERGENCY OVERRIDE ---
    def toggle_emergency(self):
        self.is_emergency_active = True
        # Pick the road with most stopped cars
        counts = {r: len(self.state[r]['vehicles']) for r in self.roads}
        self.emergency_target_road = max(counts, key=counts.get)
        # Mark first car as emergency
        for car in self.state[self.emergency_target_road]['vehicles']:
            car['is_emergency'] = True
            break

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficSimApp(root)
    root.mainloop()
