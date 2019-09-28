import pyscreenshot as ImageGrab


def parse_screen():
    # grab fullscreen
    im = ImageGrab.grab()

    # save image file
    im.save('screenshot.png')

    # show image in a window
    im.show()
