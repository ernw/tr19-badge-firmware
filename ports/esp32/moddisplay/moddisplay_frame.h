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


#ifndef MICROPY_INCLUDED_EXTMOD_DISPLAY_FRAME_H
#define MICROPY_INCLUDED_EXTMOD_DISPLAY_FRAME_H

#define PI 3.14159265

#include "moddisplay_font.h"

// this is the actual C-structure for our new object
typedef struct _display_frame_t {
    unsigned char rotation, inverted;
    display_font_t *font;
    mp_obj_t buf_obj;
    unsigned char *buf;
    unsigned int size, width, height;
} display_frame_t;

void display_frame_init(display_frame_t *frame, int width, int height, mp_obj_t buf_obj);
display_font_t* display_frame_get_font(int font);
int display_frame_load_font(display_frame_t *frame, int font);
void display_frame_clear(display_frame_t *frame, uint8_t color);
void display_frame_fill(display_frame_t *frame, const uint8_t* buffer, int x, int y, int width, int height);
void display_frame_draw_absolute_pixel(display_frame_t *frame, int x, int y, uint8_t color);
uint8_t display_frame_get_absolute_pixel(display_frame_t *frame, int x, int y);
void display_frame_draw_pixel(display_frame_t *frame, int x, int y, uint8_t color);
uint8_t display_frame_get_pixel(display_frame_t *frame, int x, int y);
int display_frame_draw_char_at(display_frame_t *frame, int x, int y, uint8_t ascii_char, uint8_t color);
void display_frame_draw_string_at(display_frame_t *frame, int x, int y, const uint8_t* text, uint8_t color, uint8_t wrap, int max_width, int* dimensions);
void display_frame_draw_line(display_frame_t *frame, int x0, int y0, int x1, int y1, uint8_t color);
void display_frame_draw_horizontal_line(display_frame_t *frame, int x, int y, int width, uint8_t color);
void display_frame_draw_vertical_line(display_frame_t *frame, int x, int y, int height, uint8_t color);
void display_frame_draw_rectangle(display_frame_t *frame, int x0, int y0, int x1, int y1, uint8_t color);
void display_frame_draw_filled_rectangle(display_frame_t *frame, int x0, int y0, int x1, int y1, uint8_t color);
void display_frame_draw_circle(display_frame_t *frame, int x, int y, int radius, uint8_t color);
void display_frame_draw_filled_circle(display_frame_t *frame, int x, int y, int radius, uint8_t color);
void display_frame_draw_arc(display_frame_t *frame, int x, int y, int radius, int startAngle, int sweepAngle, int borderWidth, uint8_t color);
void display_frame_draw_filled_arc(display_frame_t *frame, int x, int y, int radius, int startAngle, int sweepAngle, uint8_t color);

#endif // MICROPY_INCLUDED_EXTMOD_DISPLAY_FRAME_H
