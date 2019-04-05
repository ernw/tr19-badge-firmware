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

#include "py/obj.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "extmod/machine_spi.h"
#include "moddisplay.h"
#include "moddisplay_display.h"
#include "moddisplay_frame.h"
#ifndef UNIX
    #include "moddisplay_epd2in9.h"
#endif

/*
Get or set the rotation of the display
*/
STATIC mp_obj_t display_display_call_rotation(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    if (n_args > 1) {
        self->frame->rotation = mp_obj_get_int(args[1]);
        return mp_const_none;
    } else {
        return mp_obj_new_int(self->frame->rotation);
    }
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_call_rotation_obj,
    1, 2,
    display_display_call_rotation
);

/*
Get or set the inversion of the display
*/
STATIC mp_obj_t display_display_call_inverted(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    if (n_args > 1) {
        self->frame->inverted = mp_obj_get_int(args[1]);
        return mp_const_none;
    } else {
        return mp_obj_new_bool(self->frame->inverted);
    }
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_call_inverted_obj,
    1, 2,
    display_display_call_inverted
);

/*
Toggle color invert
*/
STATIC mp_obj_t display_display_invert(mp_obj_t self_in) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(self_in);
    self->frame->inverted = 1 - self->frame->inverted;
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(display_display_invert_obj,
                          display_display_invert);


/*
Get or set the font of the display
*/
STATIC mp_obj_t display_display_call_font(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    if (n_args > 1) {
    	self->font = display_frame_load_font(self->frame, mp_obj_get_int(args[1]));
        return mp_obj_new_bool(self->font != FONT_NULL);
    } else {
        return mp_obj_new_int(self->font);
    }
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_call_font_obj,
    1, 2,
    display_display_call_font
);

/*
Initialize the display
*/
STATIC mp_obj_t display_display_init(mp_obj_t self_in) {
    #ifndef UNIX
        display_display_obj_t *self = MP_OBJ_TO_PTR(self_in);
        display_epd2in9_init(self);
    #endif
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(display_display_init_obj,
                          display_display_init);

/*
Clear the screen
*/
STATIC mp_obj_t display_display_clear(mp_obj_t self_in, mp_obj_t color_in) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(self_in);
    int color = mp_obj_get_int(color_in);
    #ifndef UNIX
        display_frame_clear(self->frame, color ? 0 : 1);
        display_epd2in9_set_frame_memory(self);
        display_epd2in9_flush(self);
        display_frame_clear(self->frame, color ? 1 : 0);
        display_epd2in9_set_frame_memory(self);
        display_epd2in9_flush(self);
    #else
        display_frame_clear(self->frame, color ? 1 : 0);
    #endif
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(display_display_clear_obj,
                        display_display_clear);

/*
Fill the framebuffer
*/
STATIC mp_obj_t display_display_fill(mp_obj_t self_in, mp_obj_t color_in) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(self_in);
    int color = mp_obj_get_int(color_in);
    display_frame_clear(self->frame, color);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(display_display_fill_obj,
                          display_display_fill);

/*
Update the display
*/
STATIC mp_obj_t display_display_update(mp_obj_t self_in) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(self_in);
    #ifndef UNIX
        display_epd2in9_set_frame_memory(self);
        display_epd2in9_flush(self);
    #else
        int width = (self->frame->rotation == ROTATE_0 || self->frame->rotation == ROTATE_180) ? self->frame->width : self->frame->height;
        int height = (self->frame->rotation == ROTATE_0 || self->frame->rotation == ROTATE_180) ? self->frame->height : self->frame->width;
        printf("---INIT DISPLAY UPDATE---\n");
        // printf("%d,%d\n", width, height);
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                // display_frame_get_pixel(self->frame, x, y);
                printf("%d", display_frame_get_pixel(self->frame, x, y));
            }
            printf("\n");
        }
        // for (int i = 0; i < height; i++) {
        //     for (int j = 0; j < (int) (width / 8); j++) {
        //         uint8_t b = self->frame->buf[(i * (int) (width / 8)) + j];
        //         for (int k = 7; k >= 0; k--) {
        //             printf((b & (1 << k)) == BACKGROUND ? "1" : "0");
        //         }
        //     }
        //     printf("\n");
        // }
        printf("---DONE DISPLAY UPDATE---\n");
    #endif
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(display_display_update_obj,
                          display_display_update);

/*
Set a single pixel
*/
STATIC mp_obj_t display_display_pixel(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    int x = mp_obj_get_int(args[1]);
    int y = mp_obj_get_int(args[2]);
    int color = FOREGROUND;
    if (n_args >= 4 && args[3] != mp_const_none) {
        color = mp_obj_get_int(args[3]);
    }
    display_frame_draw_pixel(self->frame, x, y, color);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
  display_display_pixel_obj,
  3, 4,
  display_display_pixel
);

/*
Draw a text at a defined position
*/
STATIC mp_obj_t display_display_text(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    int x = mp_obj_get_int(args[1]);
    int y = mp_obj_get_int(args[2]);
    const uint8_t *str = (const uint8_t*) mp_obj_str_get_str(args[3]);
    int color = FOREGROUND;
    if (n_args >= 5 && args[4] != mp_const_none) {
        color = mp_obj_get_int(args[4]);
    }
    uint8_t wrap = 0;
    if (n_args >= 6 && args[5] != mp_const_none) {
        wrap = mp_obj_get_int(args[5]);
    }
    int max_width = 0;
    if (n_args >= 7 && args[6] != mp_const_none) {
        max_width = mp_obj_get_int(args[6]);
    }
    int dim[2];
    display_frame_draw_string_at(self->frame, x, y, str, color, wrap, max_width, dim);
    mp_obj_t dimensions[] = {
        mp_obj_new_int(dim[0]),
        mp_obj_new_int(dim[1])
    };
    return mp_obj_new_tuple(2, (void*) dimensions);
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_text_obj,
    4, 7,
    display_display_text
);

/*
Draw a line
*/
STATIC mp_obj_t display_display_line(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    int x0 = mp_obj_get_int(args[1]);
    int y0 = mp_obj_get_int(args[2]);
    int x1 = mp_obj_get_int(args[3]);
    int y1 = mp_obj_get_int(args[4]);
    int color = FOREGROUND;
    if (n_args >= 6 && args[5] != mp_const_none) {
        color = mp_obj_get_int(args[5]);
    }
    display_frame_draw_line(self->frame, x0, y0, x1, y1, color);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_line_obj,
    5, 6,
    display_display_line
);

/*
Draw a horizontal line
*/
STATIC mp_obj_t display_display_hline(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    int x = mp_obj_get_int(args[1]);
    int y = mp_obj_get_int(args[2]);
    int width = mp_obj_get_int(args[3]);
    int color = FOREGROUND;
    if (n_args >= 5 && args[4] != mp_const_none) {
        color = mp_obj_get_int(args[4]);
    }
    display_frame_draw_horizontal_line(self->frame, x, y, width, color);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_hline_obj,
    4, 5,
    display_display_hline
);

/*
Draw a vertical line
*/
STATIC mp_obj_t display_display_vline(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    int x = mp_obj_get_int(args[1]);
    int y = mp_obj_get_int(args[2]);
    int height = mp_obj_get_int(args[3]);
    int color = FOREGROUND;
    if (n_args >= 5 && args[4] != mp_const_none) {
        color = mp_obj_get_int(args[4]);
    }
    display_frame_draw_vertical_line(self->frame, x, y, height, color);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_vline_obj,
    4, 5,
    display_display_vline
);

/*
Draw a rectangle
*/
STATIC mp_obj_t display_display_rectangle(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    int x0 = mp_obj_get_int(args[1]);
    int y0 = mp_obj_get_int(args[2]);
    int x1 = mp_obj_get_int(args[3]);
    int y1 = mp_obj_get_int(args[4]);
    int color = FOREGROUND;
    if (n_args >= 6 && args[5] != mp_const_none) {
        color = mp_obj_get_int(args[5]);
    }
    display_frame_draw_rectangle(self->frame, x0, y0, x1, y1, color);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_rectangle_obj,
    5, 6,
    display_display_rectangle
);

/*
Draw a filled rectangle
*/
STATIC mp_obj_t display_display_filled_rectangle(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    int x0 = mp_obj_get_int(args[1]);
    int y0 = mp_obj_get_int(args[2]);
    int x1 = mp_obj_get_int(args[3]);
    int y1 = mp_obj_get_int(args[4]);
    int color = FOREGROUND;
    if (n_args >= 6 && args[5] != mp_const_none) {
        color = mp_obj_get_int(args[5]);
    }
    display_frame_draw_filled_rectangle(self->frame, x0, y0, x1, y1, color);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_filled_rectangle_obj,
    5, 6,
    display_display_filled_rectangle
);

/*
Draw a circle
*/
STATIC mp_obj_t display_display_circle(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    int x = mp_obj_get_int(args[1]);
    int y = mp_obj_get_int(args[2]);
    int radius = mp_obj_get_int(args[3]);
    int color = FOREGROUND;
    if (n_args >= 5 && args[4] != mp_const_none) {
        color = mp_obj_get_int(args[4]);
    }
    display_frame_draw_circle(self->frame, x, y, radius, color);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_circle_obj,
    4, 5,
    display_display_circle
);

/*
Draw a filled circle
*/
STATIC mp_obj_t display_display_filled_circle(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    int x = mp_obj_get_int(args[1]);
    int y = mp_obj_get_int(args[2]);
    int radius = mp_obj_get_int(args[3]);
    int color = FOREGROUND;
    if (n_args >= 5 && args[4] != mp_const_none) {
        color = mp_obj_get_int(args[4]);
    }
    display_frame_draw_filled_circle(self->frame, x, y, radius, color);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_filled_circle_obj,
    4, 5,
    display_display_filled_circle
);

/*
Draw an filled arc
*/
STATIC mp_obj_t display_display_arc(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    int x = mp_obj_get_int(args[1]);
    int y = mp_obj_get_int(args[2]);
    int radius = mp_obj_get_int(args[3]);
    int startAngle = 0;
    if (n_args >= 5 && args[4] != mp_const_none) {
        startAngle = mp_obj_get_int(args[4]);
    }
    int sweepAngle = 360;
    if (n_args >= 6 && args[5] != mp_const_none) {
        sweepAngle = mp_obj_get_int(args[5]);
    }
    int borderWidth = 1;
    if (n_args >= 7 && args[6] != mp_const_none) {
        borderWidth = mp_obj_get_int(args[6]);
    }
    int color = FOREGROUND;
    if (n_args >= 8 && args[7] != mp_const_none) {
        color = mp_obj_get_int(args[7]);
    }
    display_frame_draw_arc(self->frame, x, y, radius, startAngle, sweepAngle, borderWidth, color);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_arc_obj,
    4, 8,
    display_display_arc
);

/*
Draw an filled
*/
STATIC mp_obj_t display_display_fill_arc(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    int x = mp_obj_get_int(args[1]);
    int y = mp_obj_get_int(args[2]);
    int radius = mp_obj_get_int(args[3]);
    int startAngle = 0;
    if (n_args >= 5 && args[4] != mp_const_none) {
        startAngle = mp_obj_get_int(args[4]);
    }
    int sweepAngle = 360;
    if (n_args >= 6 && args[5] != mp_const_none) {
        sweepAngle = mp_obj_get_int(args[5]);
    }
    int color = FOREGROUND;
    if (n_args >= 7 && args[6] != mp_const_none) {
        color = mp_obj_get_int(args[6]);
    }
    display_frame_draw_filled_arc(self->frame, x, y, radius, startAngle, sweepAngle, color);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_fill_arc_obj,
    4, 7,
    display_display_fill_arc
);

/*
Fill the frame buffer
*/
STATIC mp_obj_t display_display_fill_bytes(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[1], &bufinfo, MP_BUFFER_READ);
    int x = mp_obj_get_int(args[2]);
    int y = mp_obj_get_int(args[3]);
    int width = mp_obj_get_int(args[4]);
    int height = mp_obj_get_int(args[5]);
    display_frame_fill(self->frame, (const uint8_t *) bufinfo.buf, x, y, width, height);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_fill_bytes_obj,
    6, 6,
    display_display_fill_bytes
);

uint8_t base64_decode_lookup(uint8_t c) {
    if ('A' <= c && c <= 'Z') {
        return c - 'A';
    }
    if ('a' <= c && c <= 'z') {
        return c - 71;
    }
    if ('0' <= c && c <= '9') {
        return c + 4;
    }
    if (c == '+') {
        return 62;
    }
    if (c == '/') {
        return 63;
    }
    return -1;
}

/*
Fill the frame buffer using a base64 encoded string
*/
STATIC mp_obj_t display_display_fill_b64(size_t n_args, const mp_obj_t *args) {
    display_display_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    const uint8_t *str = (const uint8_t*) mp_obj_str_get_str(args[1]);
    int x = mp_obj_get_int(args[2]);
    int y = mp_obj_get_int(args[3]);
    int width = mp_obj_get_int(args[4]);
    int height = mp_obj_get_int(args[5]);
    // int max_width = self->frame->rotation == ROTATE_0 || self->frame->rotation == ROTATE_180 ? self->frame->width : self->frame->height;
    // int max_height = self->frame->rotation == ROTATE_0 || self->frame->rotation == ROTATE_180 ? self->frame->height : self->frame->width;
    int max_x = x + width; // Inefficient but working!
    int max_y = y + height;
    int col = x;
    int row = y;
    const uint8_t *p;
    const uint8_t *ptr = str;
    int shifts = 0;
    while(true) {
        if (*ptr == 0 || *ptr == '=') {
            break;
        }
        uint8_t sextet_a = base64_decode_lookup(*ptr);
        if (sextet_a < 0) {
            printf("Invalid base64 string!");
            break;
        }
        uint8_t sextet_b = *(ptr + 1) == 0 || *(ptr + 1) == '=' ? 0 : base64_decode_lookup(*(ptr + 1));
        if (sextet_b < 0) {
            printf("Invalid base64 string!");
            break;
        }
        uint8_t c;
        if (shifts == 0) {
            c = (sextet_a << 2) + (sextet_b >> 4);
            shifts++;
        } else if (shifts == 1) {
            c = (sextet_a << 4) + (sextet_b >> 2);
            shifts++;
        } else if (shifts == 2) {
            c = (sextet_a << 6) + sextet_b;
            shifts = 0;
            ptr++;
        }
        p = &c;
        display_frame_fill(self->frame, p, col, row, 8, 1);
        col += 8;
        if (col >= max_x) {
            col = x;
            row++;
        }
        if (row >= max_y) {
            break;
        }
        ptr++;
    }
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(
    display_display_fill_b64_obj,
    6, 6,
    display_display_fill_b64
);


// creating the table of global members
STATIC const mp_rom_map_elem_t display_display_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_rotation), MP_ROM_PTR(&display_display_call_rotation_obj) },
    { MP_ROM_QSTR(MP_QSTR_inverted), MP_ROM_PTR(&display_display_call_inverted_obj) },
    { MP_ROM_QSTR(MP_QSTR_invert), MP_ROM_PTR(&display_display_invert_obj) },
    { MP_ROM_QSTR(MP_QSTR_font), MP_ROM_PTR(&display_display_call_font_obj) },
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&display_display_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_clear), MP_ROM_PTR(&display_display_clear_obj) },
    { MP_ROM_QSTR(MP_QSTR_fill), MP_ROM_PTR(&display_display_fill_obj) },
    { MP_ROM_QSTR(MP_QSTR_update), MP_ROM_PTR(&display_display_update_obj) },
    { MP_ROM_QSTR(MP_QSTR_pixel), MP_ROM_PTR(&display_display_pixel_obj) },
    { MP_ROM_QSTR(MP_QSTR_text), MP_ROM_PTR(&display_display_text_obj) },
    { MP_ROM_QSTR(MP_QSTR_line), MP_ROM_PTR(&display_display_line_obj) },
    { MP_ROM_QSTR(MP_QSTR_hline), MP_ROM_PTR(&display_display_hline_obj) },
    { MP_ROM_QSTR(MP_QSTR_vline), MP_ROM_PTR(&display_display_vline_obj) },
    { MP_ROM_QSTR(MP_QSTR_rect), MP_ROM_PTR(&display_display_rectangle_obj) },
    { MP_ROM_QSTR(MP_QSTR_fill_rect), MP_ROM_PTR(&display_display_filled_rectangle_obj) },
    { MP_ROM_QSTR(MP_QSTR_circ), MP_ROM_PTR(&display_display_circle_obj) },
    { MP_ROM_QSTR(MP_QSTR_fill_circ), MP_ROM_PTR(&display_display_filled_circle_obj) },
    { MP_ROM_QSTR(MP_QSTR_arc), MP_ROM_PTR(&display_display_arc_obj) },
    { MP_ROM_QSTR(MP_QSTR_fill_arc), MP_ROM_PTR(&display_display_arc_obj) },
    { MP_ROM_QSTR(MP_QSTR_fill_bytes), MP_ROM_PTR(&display_display_fill_bytes_obj) },
    { MP_ROM_QSTR(MP_QSTR_fill_b64), MP_ROM_PTR(&display_display_fill_b64_obj) },
};
STATIC MP_DEFINE_CONST_DICT(display_display_locals_dict,
                            display_display_locals_dict_table);

STATIC mp_obj_t display_display_make_new( const mp_obj_type_t *type,
                                  size_t n_args,
                                  size_t n_kw,
                                  const mp_obj_t *all_args ) {
    enum { ARG_buffer, ARG_spi, ARG_width, ARG_height,
        ARG_rst, ARG_dc, ARG_cs, ARG_busy,
        ARG_rotation, ARG_invert, ARG_font, ARG_partial };
    static const mp_arg_t allowed_args[] = {
      { MP_QSTR_buffer,     MP_ARG_OBJ | MP_ARG_REQUIRED },
      { MP_QSTR_spi,        MP_ARG_OBJ | MP_ARG_REQUIRED },
      { MP_QSTR_width,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0} },
      { MP_QSTR_height,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0} },
      { MP_QSTR_rst,        MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
      { MP_QSTR_dc,         MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
      { MP_QSTR_cs,         MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
      { MP_QSTR_busy,       MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
      { MP_QSTR_rotation,   MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = ROTATE_0} },
      { MP_QSTR_invert,     MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = 0} },
      { MP_QSTR_font,       MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = FONT_NULL} },
      { MP_QSTR_partial,    MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = 1} },
    };

    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    if (args[ARG_buffer].u_obj == MP_OBJ_NULL) {
        mp_raise_ValueError("Invalid buffer instance");
    }
    if (args[ARG_spi].u_obj == MP_OBJ_NULL) {
        mp_raise_ValueError("Invalid SPI instance");
    }
    // this checks the number of arguments (min 1, max 1);
    // on error -> raise python exception
    // create a new object of our C-struct type
    display_display_obj_t *self = m_new_obj(display_display_obj_t);
    // give it a type
    self->base.type = type;
    // mp_obj_base_t *spi = (mp_obj_base_t*) args[ARG_spi].u_obj;
    // if (spi == NULL || spi->type == NULL || spi->type->protocol) {
    //   mp_raise_ValueError("Invalid SPI object");
    // }
    // self->spi = (mp_machine_spi_p_t*)spi->type->protocol;

    self->spi = (mp_obj_t*) args[ARG_spi].u_obj;
    #ifndef UNIX
        self->rst = args[ARG_rst].u_obj == MP_OBJ_NULL ? -1 : machine_pin_get_id(args[ARG_rst].u_obj);
        self->dc = args[ARG_dc].u_obj == MP_OBJ_NULL ? -1 : machine_pin_get_id(args[ARG_dc].u_obj);
        self->cs = args[ARG_cs].u_obj == MP_OBJ_NULL ? -1 : machine_pin_get_id(args[ARG_cs].u_obj);
        self->busy = args[ARG_busy].u_obj == MP_OBJ_NULL ? -1 : machine_pin_get_id(args[ARG_busy].u_obj);
    #endif

    // set the member number with the first argument of the constructor
    // self->display_number = mp_obj_get_int(args[0]);
    /* 1 byte = 8 pixels, so the width should be the multiple of 8 */
    int width = args[ARG_width].u_int;
    int height = args[ARG_height].u_int;
    // display_frame_t frame;
    // self->frame_obj = frame;
    self->frame = &self->frame_obj; // prevent GC from deleting it!
    display_frame_init(self->frame, width, height, args[ARG_buffer].u_obj);

    // kw args
    self->partial = args[ARG_partial].u_bool;
    self->frame->rotation = args[ARG_rotation].u_int;
    self->frame->inverted = args[ARG_invert].u_bool;

    self->font = args[ARG_font].u_int;
    if (display_frame_load_font(self->frame, self->font) == FONT_NULL) {
        printf("WARNING: No font loaded!");
    }

    return MP_OBJ_FROM_PTR(self);
}

// create the class-object itself
STATIC const mp_obj_type_t display_Display_type = {
    // "inherit" the type "type"
    { &mp_type_type },
     // give it a name
    .name = MP_QSTR_Display,
     // give it a constructor
    .make_new = display_display_make_new,
     // and the global members
    .locals_dict = (mp_obj_dict_t*)&display_display_locals_dict,
};
