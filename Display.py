import cv2

class Display:
    """
    Display an representation of the computer vision to the user
    """
    def show_image(self, img, game, game_state):
        """
        Show an visual representation of the AI's vision
        """
        distance, height = game_state[0], game_state[1]
        cv2.putText(img, str(game.score), 
                org=(img.shape[1] // 2, 80), 
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=1, color=0, thickness=3)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.rectangle(img, (game.right, game.top), (game.right, img.shape[0]-1), (0,0,255), 1)
        if(height):
            cv2.rectangle(img, (game.right, height), (game.right + distance, height), (0, 255, 0), 3)
        cv2.imshow("Computer Vision", img)