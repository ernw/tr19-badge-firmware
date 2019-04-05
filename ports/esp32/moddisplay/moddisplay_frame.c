/*
 * This file is part of the Troopers 19 Badge project, https://troopers.de/troopers19/
 *
 * The BSD 3-Clause License
 *
 * Copyright (c) 2019 "Malte Heinzelmann" <malte@hnzlmnn.de>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 * 3. Neither the name of the copyright holder nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#include <stdlib.h>
#include <math.h>

#include "moddisplay.h"
#include "moddisplay_frame.h"

void display_frame_init(display_frame_t *frame, int width, int height, mp_obj_t buf_obj) {
    frame->width = width % 8 ? width + 8 - (width % 8) : width;
    frame->height = height;
    frame->size = (frame->width / 8) * frame->height;
    frame->buf_obj = buf_obj; // prevent GC from deleting it!
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(frame->buf_obj, &bufinfo, MP_BUFFER_WRITE);
    frame->buf = bufinfo.buf;
}

display_font_t* display_frame_get_font(int font) {
    switch (font) {
        FONT_ADD_GET_FONT
    }
    #ifdef FONT_DEJAVU_12 // Fallback font
        return &FontDejaVu12;
    #else
        return NULL;
    #endif
}

int display_frame_load_font(display_frame_t *frame, int font) {
    frame->font = display_frame_get_font(font);
    return frame->font == NULL ? FONT_NULL : frame->font->id;
}

void display_frame_clear(display_frame_t *frame, uint8_t color) {
    for (int x = 0; x < frame->width; x++) {
        for (int y = 0; y < frame->height; y++) {
            display_frame_draw_absolute_pixel(frame, x, y, color);
        }
    }
}

void display_frame_fill(display_frame_t *frame, const uint8_t* buffer, int x, int y, int width, int height) {
    int max_width = frame->rotation == ROTATE_0 || frame->rotation == ROTATE_180 ? frame->width : frame->height;
    int max_height = frame->rotation == ROTATE_0 || frame->rotation == ROTATE_180 ? frame->height : frame->width;
    int c, r;
    uint8_t color;
    const uint8_t *ptr = buffer;
    for (int i = 0; i < width * height; i++) {
        int idx = i % 8;
        uint8_t bit = 1 << (7 - idx);
        color = (*ptr & bit) == bit ? 1 : 0;
        c = x + (i % width);
        r = y + ((i - (i % width)) / width);
        if (c < max_width && r < max_height) {
            display_frame_draw_pixel(frame, c, r, color);
        }
        if (idx == 7) {
            ptr++;
        }
    }
}

void display_frame_draw_absolute_pixel(display_frame_t *frame, int x, int y, uint8_t color) {
    if (x < 0 || x >= frame->width || y < 0 || y >= frame->height) {
        return;
    }
    if (frame->inverted) {
        color = color ? 0 : 1;
    }
    size_t index = (x + y * frame->width) >> 3;
    int offset = 7 - (x & 0x07);
    ((uint8_t*)frame->buf)[index] = (((uint8_t*)frame->buf)[index] & ~(0x01 << offset)) | ((color != 0) << offset);
    // frame->buf[(x + y * frame->width) / 8] |= 0x80 >> (x % 8);
}

uint8_t display_frame_get_absolute_pixel(display_frame_t *frame, int x, int y) {
    if (x < 0 || x >= frame->width || y < 0 || y >= frame->height) {
        return -1;
    }
    size_t index = (x + y * frame->width) >> 3;
    int offset = 7 - (x & 0x07);
    // printf("%d,%d %x %d %d ", x, y, ((uint8_t*)frame->buf)[index], 1 << offset, ((uint8_t*)frame->buf)[index] & (1 << offset));
    return (((uint8_t*)frame->buf)[index] & (1 << offset)) == (1 << offset);
}

void display_frame_draw_pixel(display_frame_t *frame, int x, int y, uint8_t color) {
    int point_temp;
    if (frame->rotation == ROTATE_0) {
        if(x < 0 || x >= frame->width || y < 0 || y >= frame->height) {
            return;
        }
        display_frame_draw_absolute_pixel(frame, x, y, color);
    } else if (frame->rotation == ROTATE_90) {
        if(x < 0 || x >= frame->height || y < 0 || y >= frame->width) {
          return;
        }
        point_temp = x;
        x = frame->width - y - 1;
        y = point_temp;
        display_frame_draw_absolute_pixel(frame, x, y, color);
    } else if (frame->rotation == ROTATE_180) {
        if(x < 0 || x >= frame->width || y < 0 || y >= frame->height) {
          return;
        }
        x = frame->width - x - 1;
        y = frame->height - y - 1;
        display_frame_draw_absolute_pixel(frame, x, y, color);
    } else if (frame->rotation == ROTATE_270) {
        if(x < 0 || x >= frame->height || y < 0 || y >= frame->width) {
          return;
        }
        point_temp = x;
        x = y;
        y = frame->height - point_temp - 1;
        display_frame_draw_absolute_pixel(frame, x, y, color);
    }
}

uint8_t display_frame_get_pixel(display_frame_t *frame, int x, int y) {
    int point_temp;
    if (frame->rotation == ROTATE_0) {
        if(x < 0 || x >= frame->width || y < 0 || y >= frame->height) {
            return -1;
        }
        return display_frame_get_absolute_pixel(frame, x, y);
    } else if (frame->rotation == ROTATE_90) {
        if(x < 0 || x >= frame->height || y < 0 || y >= frame->width) {
          return -1;
        }
        point_temp = x;
        x = frame->width - y - 1;
        y = point_temp;
        return display_frame_get_absolute_pixel(frame, x, y);
    } else if (frame->rotation == ROTATE_180) {
        if(x < 0 || x >= frame->width || y < 0 || y >= frame->height) {
          return -1;
        }
        x = frame->width - x - 1;
        y = frame->height - y - 1;
        return display_frame_get_absolute_pixel(frame, x, y);
    } else if (frame->rotation == ROTATE_270) {
        if(x < 0 || x >= frame->height || y < 0 || y >= frame->width) {
          return -1;
        }
        point_temp = x;
        x = y;
        y = frame->height - point_temp - 1;
        return display_frame_get_absolute_pixel(frame, x, y);
    }
    return -1;
}

int display_frame_draw_char_at(display_frame_t *frame, int x, int y, uint8_t ascii_char, uint8_t color) {
    if (frame->font == NULL) {
        return 0;
    }
    if (ascii_char < frame->font->min || ascii_char > frame->font->max) {
        ascii_char = '?';
        // return 0;
    }
    int i, j;
    unsigned int char_offset = (ascii_char - frame->font->offset) * frame->font->height * (frame->font->width / 8 + (frame->font->width % 8 ? 1 : 0));
    const uint8_t* ptr = &frame->font->table[char_offset];

    for (j = 0; j < frame->font->height; j++) {
        for (i = 0; i < frame->font->width; i++) {
            if (*ptr & (0x80 >> (i % 8))) {
                display_frame_draw_pixel(frame, x + i, y + j, color);
            }
            if (i % 8 == 7) {
                ptr++;
            }
        }
        if (frame->font->width % 8 != 0) {
            ptr++;
        }
    }
    return frame->font->height; // how many rows were written
}

void display_frame_draw_string_at(display_frame_t *frame, int x, int y, const uint8_t* text, uint8_t color, uint8_t wrap, int max_width, int* dimensions) {
    if (frame->font == NULL) {
        printf("No font loaded!\n");
        return;
    }
    int c = x;
    int r = y;
    int max_c = 0;
    const uint8_t *p_text = text;
    int width = (frame->rotation == ROTATE_0 || frame->rotation == ROTATE_180) ? frame->width : frame->height;
    if (max_width == 0) {
        max_width = width;
    }
    while (*p_text != 0) {
        if (c + frame->font->width > width || c + frame->font->width - x > max_width || *p_text == '\n') {
            switch (wrap) {
                case NO_WRAP: // Do not wrap
                    dimensions[0] = c - x;
                    dimensions[1] = frame->font->height;
                    return;
                case WRAP_INDENT: // Wraped line starts at initial x
                    c = x;
                    r += frame->font->height;
                    while (*p_text == ' ') {
                        p_text++;
                    }
                    break;
                case WRAP_LINE_START: // Wraped line starts at x=0
                    c = 0;
                    r += frame->font->height;
                    break;
            }
            if (*p_text == 0) {
                break;
            }
            if (*p_text == '\n') {
                p_text++;
                continue;
            }
        }
        if (c > max_c) {
            max_c = c;
        }
        if (display_frame_draw_char_at(frame, c, r, *p_text, color) > 0) {
            c += frame->font->width;
        }
        p_text++;
    }
    dimensions[0] = (r == y) ? c - x : max_c - x;
    dimensions[1] = (r + frame->font->height) - y;
    return;
}

void display_frame_draw_line(display_frame_t *frame, int x0, int y0, int x1, int y1, uint8_t color) {
    /* Bresenham algorithm */
    int dx = x1 - x0 >= 0 ? x1 - x0 : x0 - x1;
    int sx = x0 < x1 ? 1 : -1;
    int dy = y1 - y0 <= 0 ? y1 - y0 : y0 - y1;
    int sy = y0 < y1 ? 1 : -1;
    int err = dx + dy;

    while((x0 != x1) && (y0 != y1)) {
        display_frame_draw_pixel(frame, x0, y0 , color);
        if (2 * err >= dy) {
            err += dy;
            x0 += sx;
        }
        if (2 * err <= dx) {
            err += dx;
            y0 += sy;
        }
    }
}

void display_frame_draw_horizontal_line(display_frame_t *frame, int x, int y, int width, uint8_t color) {
    int i;
    for (i = x; i < x + width; i++) {
        display_frame_draw_pixel(frame, i, y, color);
    }
}

void display_frame_draw_vertical_line(display_frame_t *frame, int x, int y, int height, uint8_t color) {
    int i;
    for (i = y; i < y + height; i++) {
        display_frame_draw_pixel(frame, x, i, color);
    }
}

void display_frame_draw_rectangle(display_frame_t *frame, int x0, int y0, int x1, int y1, uint8_t color) {
    int min_x, min_y, max_x, max_y;
    min_x = x1 > x0 ? x0 : x1;
    max_x = x1 > x0 ? x1 : x0;
    min_y = y1 > y0 ? y0 : y1;
    max_y = y1 > y0 ? y1 : y0;

    display_frame_draw_horizontal_line(frame, min_x, min_y, max_x - min_x + 1, color);
    display_frame_draw_horizontal_line(frame, min_x, max_y, max_x - min_x + 1, color);
    display_frame_draw_vertical_line(frame, min_x, min_y, max_y - min_y + 1, color);
    display_frame_draw_vertical_line(frame, max_x, min_y, max_y - min_y + 1, color);
}

void display_frame_draw_filled_rectangle(display_frame_t *frame, int x0, int y0, int x1, int y1, uint8_t color) {
    int min_x, min_y, max_x, max_y;
    int i;
    min_x = x1 > x0 ? x0 : x1;
    max_x = x1 > x0 ? x1 : x0;
    min_y = y1 > y0 ? y0 : y1;
    max_y = y1 > y0 ? y1 : y0;

    for (i = min_x; i < max_x; i++) {
      display_frame_draw_vertical_line(frame, i, min_y, max_y - min_y, color);
    }
}

void display_frame_draw_circle(display_frame_t *frame, int x, int y, int radius, uint8_t color) {
    /* Bresenham algorithm */
    int x_pos = -radius;
    int y_pos = 0;
    int err = 2 - 2 * radius;
    int e2;

    do {
        display_frame_draw_pixel(frame, x - x_pos, y + y_pos, color);
        display_frame_draw_pixel(frame, x + x_pos, y + y_pos, color);
        display_frame_draw_pixel(frame, x + x_pos, y - y_pos, color);
        display_frame_draw_pixel(frame, x - x_pos, y - y_pos, color);
        e2 = err;
        if (e2 <= y_pos) {
            err += ++y_pos * 2 + 1;
            if(-x_pos == y_pos && e2 <= x_pos) {
              e2 = 0;
            }
        }
        if (e2 > x_pos) {
            err += ++x_pos * 2 + 1;
        }
    } while (x_pos <= 0);
}

void display_frame_draw_filled_circle(display_frame_t *frame, int x, int y, int radius, uint8_t color) {
    /* Bresenham algorithm */
    int x_pos = -radius;
    int y_pos = 0;
    int err = 2 - 2 * radius;
    int e2;

    do {
        display_frame_draw_pixel(frame, x - x_pos, y + y_pos, color);
        display_frame_draw_pixel(frame, x + x_pos, y + y_pos, color);
        display_frame_draw_pixel(frame, x + x_pos, y - y_pos, color);
        display_frame_draw_pixel(frame, x - x_pos, y - y_pos, color);
        display_frame_draw_horizontal_line(frame, x + x_pos, y + y_pos, 2 * (-x_pos) + 1, color);
        display_frame_draw_horizontal_line(frame, x + x_pos, y - y_pos, 2 * (-x_pos) + 1, color);
        e2 = err;
        if (e2 <= y_pos) {
            err += ++y_pos * 2 + 1;
            if(-x_pos == y_pos && e2 <= x_pos) {
                e2 = 0;
            }
        }
        if(e2 > x_pos) {
            err += ++x_pos * 2 + 1;
        }
    } while(x_pos <= 0);
}

int getAngle(int centerX, int centerY, int pointX, int pointY) {
	int x = pointX - centerX;
	int y = pointY - centerY;

	if (x == 0)
		return (y > 0) ? 180 : 0;

	int a = (int)(atan2(y, x) * 180 / PI);
	a += 90;

	if ((x < 0) && (y < 0))
		a += 360;

	return a;
}

void draw_border(display_frame_t *frame, int x, int y, int centerX, int centerY, int radius, int width, uint8_t color) {
    if (width == 0) {
        width = 1;
    }
    if (width == 1 || width == -1) {
        display_frame_draw_pixel(frame, x, y, color);
        return;
    }
    // Consider using vector distance instead of radius
    double directionX = (x - centerX) / radius;
    double directionY = (y - centerY) / radius;
    // Calculate border end
    int borderX = centerX + directionX * width;
    int borderY = centerY + directionY * width;
    display_frame_draw_line(frame, x, y, borderX, borderY, color);
}

void display_frame_draw_arc(display_frame_t *frame, int x, int y, int radius, int startAngle, int sweepAngle, int borderWidth, uint8_t color) {
    while(startAngle < 0) {
        startAngle += 360;
    }
    startAngle %= 360;
    if (sweepAngle != 360) {
        while(sweepAngle < 0) {
            sweepAngle += 360;
        }
        sweepAngle %= 360;
    }

    // Define angle 0 deg to be center top
	int currX = 0;
	int currY = radius;

	int gap = 0;
	int delta = (2 - 2 * radius);
	int angle;
	while (currY >= 0) {
		if (x + currX < frame->width && y - currY < frame->height && x + currX >= 0 && y - currY >= 0) {
			angle = getAngle(x, y, x + x, y - y);
			if ((angle >= startAngle) && (angle <= startAngle + sweepAngle)) {
				if (0 <= angle && angle <= 90) {
                    draw_border(frame, x + currX, y - currY, x, y, radius, borderWidth, color);
				}
			}
		}

		if (x + currX < frame->width && y + currY < frame->height && x + currX >= 0 && y + currY >= 0) {
			angle = getAngle(x, y, x + currX, y + currY);
			if ((angle >= startAngle) && (angle <= startAngle + sweepAngle)) {
				if (90 < angle && angle <= 180) {
                    draw_border(frame, x + currX, y + currY, x, y, radius, borderWidth, color);
				}
			}
		}

		if (x - currX < frame->width && y + currY < frame->height && x - currX >= 0 && y + currY >= 0) {
			angle = getAngle(x, y, x - currX, y + currY);
			if ((angle >= startAngle) && (angle <= startAngle + sweepAngle)) {
				if (180 < angle && angle <= 270) {
                    draw_border(frame, x - currX, y + currY, x, y, radius, borderWidth, color);
				}
			}
		}

		if (x - currX < frame->width && y - y < frame->height && x - currX >= 0 && y - currY >= 0) {
			angle = getAngle(x, y, x - currX, y - currY);
			if ((angle >= startAngle) && (angle <= startAngle + sweepAngle)) {
				if (270 < angle && angle <= 360) {
                    draw_border(frame, x - currX, y - currY, x, y, radius, borderWidth, color);
				}
			}
		}

		gap = 2 * (delta + currY) - 1;
		if (delta < 0 && gap <= 0) {
			currX++;
			delta += 2 * currX + 1;
			continue;
		}
		if (delta > 0 && gap > 0) {
			currY--;
			delta -= 2 * currY + 1;
			continue;
		}
		currX++;
		delta += 2 * (currX - currY);
		currY--;
	}
}

void display_frame_draw_filled_arc(display_frame_t *frame, int x, int y, int radius, int startAngle, int sweepAngle, uint8_t color) {
    return display_frame_draw_arc(frame, x, y, radius, startAngle, sweepAngle, -radius, color);
}
