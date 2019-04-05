import display

buf = bytearray(296//8*128)
d = display.Display(buf, None, 128, 296, rotation=display.ROTATE_90, invert=True, font=display.FONT_DEJAVU_12)
d.clear(display.BACKGROUND)
#d.fill_rect(0, 0, 4, 4)

d.text(20, 20, 'Test')

print('test')

d.update()
