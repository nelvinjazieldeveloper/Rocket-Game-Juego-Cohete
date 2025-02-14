import pygame
import random
import cv2
import mediapipe as mp
import numpy as np

# Initialize video capture
# Inicializar la captura de video
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Face Mesh
# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Initialize Pygame
# Inicializar Pygame
pygame.init()
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Load and scale the background image
# Cargar y escalar la imagen de fondo
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (ANCHO_PANTALLA, ALTO_PANTALLA))

# Set the window title
# Título de la ventana
pygame.display.set_caption("Juego cohete")

class Cohete():
    def __init__(self):
        # Initialize rocket properties
        # Inicializar las propiedades del cohete
        self.x = 400
        self.y = 500
        self.score = 0
        self.velocidad = 0
        self.angulo = 0
        self.detener = False
        # Load and scale the rocket image
        # Cargar y escalar la imagen del cohete
        self.image_original = pygame.image.load("rocket.png")
        self.image_original = pygame.transform.scale(self.image_original, (70, 70))
        self.image = self.image_original
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        # Draw the rocket on the screen
        # Dibujar el cohete en la pantalla
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def move(self):
        # Move the rocket according to its speed
        # Mover el cohete según su velocidad
        self.x += self.velocidad
        if self.velocidad < 0:  # If moving left
            # Rotate left
            # Rota hacia la izquierda
            self.angulo += 5  
        elif self.velocidad > 0:  # If moving right
            # Rotate right
            # Rota hacia la derecha
            self.angulo -= 5  

        # Limit the angle to not exceed 15 or -15 degrees
        # Limitar el ángulo para que no se pase de 15 o -15 grados
        self.angulo = max(-15, min(self.angulo, 15))

        # Rotate the rocket image
        # Rotar la imagen del cohete
        self.image = pygame.transform.rotate(self.image_original, self.angulo)
        self.rect = self.image.get_rect(center=self.rect.center)

class Enemigo():
    def __init__(self):
        # Initialize enemy properties
        # Inicializar las propiedades del enemigo
        self.x = random.randint(0, ANCHO_PANTALLA)
        self.y = 0
        image = pygame.image.load("misil.png")
        image = pygame.transform.scale(image, (50, 50))
        image = pygame.transform.rotate(image, 180)  # Rotate the missile image
        # Rotar la imagen del misil
        self.image = pygame.sprite.Sprite()
        self.image.image = image
        self.image.rect = self.image.image.get_rect()

    def draw(self):
        # Draw the enemy on the screen
        # Dibujar el enemigo en la pantalla
        screen.blit(self.image.image, (self.x, self.y))

    def move(self):
        # Move the enemy downwards
        # Mover el enemigo hacia abajo
        self.y += 10

    def remove(self):
        # Remove the enemy if it goes off the screen
        # Eliminar el enemigo si sale de la pantalla
        if self.y > ALTO_PANTALLA:
            enemigos.remove(self)
            return True

    def chocar(self, cohete):
        # Check if the enemy collides with the rocket
        # Comprobar si el enemigo choca con el cohete
        if self.x < cohete.x + (50 * 0.7) and self.x > cohete.x - (50 * 0.7) and self.y < cohete.y + (50 * 0.7) and self.y > cohete.y - (50 * 0.7):
            return True
        else:
            return False

# Create an instance of the rocket
# Crear una instancia del cohete
cohete = Cohete()
enemigos = []

# Waiting screen to start the game
# Pantalla de espera para iniciar el juego
esperando = True
while esperando:
    text = pygame.font.Font(None, 36)
    texto = text.render(f"Presione 'SPACE' para iniciar", True, (255, 255, 255))

    # Draw the waiting screen
    # Dibujar la pantalla de espera
    screen.blit(background_image, (0, 0))
    screen.blit(texto, (ANCHO_PANTALLA // 2 - texto.get_width() // 2, ALTO_PANTALLA // 2 - texto.get_height() // 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                esperando = False
    pygame.display.flip()

# Create a FaceMesh object
# Crear un objeto FaceMesh
with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    while True:
        screen.blit(background_image, (0, 0))
        if not cohete.detener:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Flip the frame horizontally for a selfie view
            # Voltear el marco horizontalmente para una visualización tipo selfie
            frame = cv2.flip(frame, 1)
            
            # Convert the frame from BGR to RGB
            # Convertir el marco de BGR a RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame and find face landmarks
            # Procesar el marco y encontrar los puntos de referencia de la cara
            results = face_mesh.process(frame_rgb)
            
            # Draw face landmarks on the frame
            # Dibujar los puntos de referencia de la cara en el marco
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    x_abajo = int(face_landmarks.landmark[152].x * frame.shape[1])
                    y_abajo = int(face_landmarks.landmark[152].y * frame.shape[0])
                    
                    x_arriba = int(face_landmarks.landmark[10].x * frame.shape[1])
                    y_arriba = int(face_landmarks.landmark[10].y * frame.shape[0])
                    
                    # Draw circles and line between landmarks
                    # Dibujar círculos y línea entre los puntos de referencia
                    cv2.circle(frame, (x_abajo, y_abajo), 10, (252, 254, 0), -1)
                    cv2.circle(frame, (x_arriba, y_arriba), 10, (252, 254, 0), -1)
                    cv2.line(frame, (x_abajo, y_abajo), (x_arriba, y_arriba), (0, 255, 0), 2)
                    
                    # Calculate the angle between landmarks
                    # Calcular el ángulo entre los puntos de referencia
                    angulo = np.degrees(np.arctan2(y_arriba - y_abajo, x_arriba - x_abajo))
                    cv2.putText(frame, f"Angulo: {angulo:.2f}o", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # Adjust the rocket's speed based on the angle
                    # Ajustar la velocidad del cohete según el ángulo
                    if angulo > -85:
                        cohete.velocidad = 10
                    elif angulo < -95:
                        cohete.velocidad = -10
                    else:
                        cohete.velocidad = 0
            
            # Flip the frame for Pygame
            # Voltear el marco para Pygame
            frame = cv2.flip(frame, 1)
            frame_pygame = pygame.surfarray.make_surface(frame)
            frame_pygame = pygame.transform.rotate(frame_pygame, 90)
            frame_pygame = pygame.transform.flip(frame_pygame, True, False)
            frame_pygame = pygame.transform.flip(frame_pygame, False, True)
            frame_pygame = pygame.transform.scale(frame_pygame, (ANCHO_PANTALLA // 5, ALTO_PANTALLA // 5))
            screen.blit(frame_pygame, (0, 0))

            # Randomly generate enemies
            # Generar enemigos aleatoriamente
            if random.randint(1, 10) == 1:
                enemigos.append(Enemigo())
            for enemigo in enemigos:
                enemigo.move()  # Move enemies
                # Mover enemigos
                if enemigo.remove():  # Remove enemies that went off the screen
                    # Eliminar enemigos que salieron de la pantalla
                    cohete.score += 1  # Increment score
                # Incrementar puntaje
                enemigo.draw()  # Draw enemies
                # Dibujar enemigos
                if enemigo.chocar(cohete):  # Check for collisions
                    # Comprobar colisiones
                    cohete.detener = True  # Stop the game if there is a collision
                    # Detener el juego si hay colisión

            cohete.move()  # Move the rocket
            # Mover el cohete
            cohete.draw()  # Draw the rocket
            # Dibujar el cohete
            pygame.display.flip()  # Update the screen
            # Actualizar la pantalla
        else:
            # Game Over screen
            # Pantalla de Game Over
            font = pygame.font.Font(None, 36)
            text = font.render(f"Game Over", True, (255, 255, 255))
            text1 = font.render(f"Puntaje: {cohete.score}", True, (255, 255, 255))
            text2 = font.render(f"Presione 'SPACE' para reiniciar", True, (255, 255, 255))
            screen.blit(text, (ANCHO_PANTALLA // 2 - text.get_width() // 2, ALTO_PANTALLA // 2 - text.get_height() // 2))
            screen.blit(text1, (ANCHO_PANTALLA // 2 - text1.get_width() // 2, ALTO_PANTALLA // 2 - text1.get_height() // 2 + 50))
            screen.blit(text2, (ANCHO_PANTALLA // 2 - text2.get_width() // 2, ALTO_PANTALLA // 2 - text2.get_height() // 2 + 100))
            pygame.display.flip()  # Update the screen
            # Actualizar la pantalla

            # Wait for the player to restart the game
            # Esperar a que el jugador reinicie el juego
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Restart the game
                        # Reiniciar el juego
                        enemigos = []
                        cohete.detener = False
                        cohete.score = 0
                        cohete.velocidad = 0
                        cohete.x = 400
                        cohete.angulo = 0  # Reset angle when restarting the game
                        # Reiniciar el ángulo al reiniciar el juego
                if event.type == pygame.QUIT:
                    exit()  # Exit the game
                    # Salir del juego