import cv2
import numpy as np
import pygame
import random
import sys


# ==========================================
# 1. KELAS DETEKSI WEBCAM (OpenCV)
# ==========================================
class ObjectTracker:

    def __init__(self, src=0, width=640, height=480):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Ambang warna hitam (HSV)
        self.lower_black = np.array([0, 0, 0])
        self.upper_black = np.array([180, 255, 70])
        self.kernel = np.ones((5, 5), np.uint8)

    def process_frame(self, target_width, target_height):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        # Mirror kamera
        frame = cv2.flip(frame, 1)

        # Konversi untuk tampilan Pygame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (target_width, target_height))

        frame_surface = pygame.surfarray.make_surface(np.rot90(frame_resized))
        webcam_surface = pygame.transform.flip(frame_surface, True, False)

        # Deteksi Objek Hitam
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_black, self.upper_black)
        mask = cv2.erode(mask, self.kernel, iterations=1)
        mask = cv2.dilate(mask, self.kernel, iterations=2)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        detected_x_ratio = None
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 800:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    detected_x_ratio = cx / frame.shape[1]

        return webcam_surface, detected_x_ratio

    def release(self):
        self.cap.release()


# ==========================================
# 2. KELAS KERANJANG (BASKET)
# ==========================================
class Basket:

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.width = 120
        self.height = 25
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - 60
        self.color = (50, 150, 250)  # BLUE

    def update_position(self, x_ratio):
        if x_ratio is not None:
            self.x = int(x_ratio * self.screen_width) - (self.width // 2)

        # Clamp batas layar
        self.x = max(0, min(self.screen_width - self.width, self.x))

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (self.x, self.y, self.width, self.height),
            border_radius=8,
        )


# ==========================================
# 3. KELAS BOLA (BALL)
# ==========================================
class Ball:

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = 15
        self.color = (230, 50, 50)  # RED
        self.reset()

    def reset(self):
        self.x = random.randint(self.radius, self.screen_width - self.radius)
        self.y = 0
        self.speed = 6

    def update(self):
        self.y += self.speed

    def is_caught_by(self, basket):
        caught = (
            basket.y <= self.y + self.radius <= basket.y + basket.height
        ) and (basket.x <= self.x <= basket.x + basket.width)

        if caught:
            self.y = 0
            self.x = random.randint(
                self.radius, self.screen_width - self.radius
            )
            self.speed += 0.2
        return caught

    def is_out_of_bounds(self):
        if self.y > self.screen_height:
            self.y = 0
            self.x = random.randint(
                self.radius, self.screen_width - self.radius
            )
            return True
        return False

    def draw(self, surface):
        pygame.draw.circle(
            surface, self.color, (int(self.x), int(self.y)), self.radius
        )


# ==========================================
# 4. KELAS UTAMA GAME (GAME MANAGER)
# ==========================================
class CatchTheBallGame:

    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game Tangkap Bola - OOP Version")
        self.clock = pygame.time.Clock()

        # Objek Utama
        self.tracker = ObjectTracker()
        self.basket = Basket(width, height)
        self.ball = Ball(width, height)

        # Warna
        self.WHITE = (255, 255, 255)
        self.BLACK = (20, 20, 20)
        self.YELLOW = (255, 215, 0)
        self.BLUE = (50, 150, 250)
        self.GREEN = (50, 200, 80)

        # Font
        self.font_title = pygame.font.SysFont(None, 64)
        self.font_btn = pygame.font.SysFont(None, 36)
        self.font_ui = pygame.font.SysFont(None, 28)

        # State & Skor
        self.state = "MENU"
        self.score = 0
        self.running = True

        # Tombol
        self.btn_play_rect = pygame.Rect(width // 2 - 100, 250, 200, 50)
        self.btn_quit_rect = pygame.Rect(width // 2 - 100, 330, 200, 50)

    def reset_game(self):
        self.score = 0
        self.ball.reset()

    def draw_button(self, rect, text, is_hover):
        color = self.YELLOW if is_hover else self.BLUE
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, self.WHITE, rect, width=2, border_radius=10)

        btn_text = self.font_btn.render(
            text, True, self.BLACK if is_hover else self.WHITE
        )
        text_rect = btn_text.get_rect(center=rect.center)
        self.screen.blit(btn_text, text_rect)

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.state == "MENU":
                    if self.btn_play_rect.collidepoint(mouse_pos):
                        self.reset_game()
                        self.state = "PLAY"
                    elif self.btn_quit_rect.collidepoint(mouse_pos):
                        self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "PLAY":
                        self.state = "MENU"
                    elif self.state == "MENU":
                        self.running = False

    def render_menu(self, mouse_pos):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        title_surface = self.font_title.render(
            "CATCH THE BALL", True, self.GREEN
        )
        self.screen.blit(
            title_surface,
            title_surface.get_rect(center=(self.width // 2, 150)),
        )

        self.draw_button(
            self.btn_play_rect,
            "PLAY",
            self.btn_play_rect.collidepoint(mouse_pos),
        )
        self.draw_button(
            self.btn_quit_rect,
            "QUIT",
            self.btn_quit_rect.collidepoint(mouse_pos),
        )

        info_text = self.font_ui.render(
            "Gunakan Masker Hitam di Depan Kamera untuk Mengontrol Keranjang",
            True,
            self.WHITE,
        )
        self.screen.blit(
            info_text,
            info_text.get_rect(
                center=(self.width // 2, self.height - 50)
            ),
        )

    def render_play_ui(self):
        score_surface = self.font_btn.render(
            f"Skor: {self.score}", True, self.YELLOW
        )
        pygame.draw.rect(
            self.screen,
            self.BLACK,
            (15, 15, score_surface.get_width() + 10, 40),
        )
        self.screen.blit(score_surface, (20, 20))

        esc_surface = self.font_ui.render(
            "Tekan ESC untuk Kembali ke Menu", True, self.WHITE
        )
        pygame.draw.rect(
            self.screen,
            self.BLACK,
            (15, self.height - 40, esc_surface.get_width() + 10, 30),
        )
        self.screen.blit(esc_surface, (20, self.height - 35))

    def run(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()

            # 1. Webcam Frame & Object Tracking
            webcam_surface, x_ratio = self.tracker.process_frame(
                self.width, self.height
            )
            self.basket.update_position(x_ratio)

            # 2. Event Handling
            self.handle_events()

            # 3. Drawing Background
            if webcam_surface:
                self.screen.blit(webcam_surface, (0, 0))
            else:
                self.screen.fill(self.BLACK)

            # 4. State Management
            if self.state == "MENU":
                self.render_menu(mouse_pos)

            elif self.state == "PLAY":
                self.ball.update()

                if self.ball.is_caught_by(self.basket):
                    self.score += 1

                if self.ball.is_out_of_bounds():
                    self.score = max(0, self.score - 1)

                # Draw Game Objects
                self.basket.draw(self.screen)
                self.ball.draw(self.screen)
                self.render_play_ui()

            pygame.display.flip()
            self.clock.tick(60)

        # Cleanup
        self.tracker.release()
        pygame.quit()
        sys.exit()


# ==========================================
# RUN GAME
# ==========================================
if __name__ == "__main__":
    game = CatchTheBallGame()
    game.run()