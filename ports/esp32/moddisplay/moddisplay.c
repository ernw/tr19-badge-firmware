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

#include "py/nlr.h"
#include "py/obj.h"
#include "py/runtime.h"
#include "py/binary.h"
#include <string.h>
#include <stdio.h>

// Fonts need to be loaded first
#include "fonts/fontconfig.h"


#include "moddisplay.h"
#include "moddisplay_display.c"
#include "moddisplay_frame.c"
#ifndef UNIX
    #include "moddisplay_epd2in9.c"
#endif

STATIC mp_obj_t display_font_size(mp_obj_t id_in) {
    display_font_t *font = display_frame_get_font(mp_obj_get_int(id_in));
    if (font == NULL) {
        return mp_const_none;
    }
    mp_obj_t font_size[] = {
        mp_obj_new_int(font->width),
        mp_obj_new_int(font->height)
    };
    return mp_obj_new_tuple(2, (void*) font_size);
}
MP_DEFINE_CONST_FUN_OBJ_1(display_font_size_obj,
                          display_font_size);

STATIC const mp_rom_map_elem_t display_globals_table[] = {
  { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_display) },
  { MP_ROM_QSTR(MP_QSTR_Display), MP_ROM_PTR(&display_Display_type) },
  { MP_ROM_QSTR(MP_QSTR_fontSize), MP_ROM_PTR(&display_font_size_obj) },
  { MP_ROM_QSTR(MP_QSTR_ROTATE_0), MP_ROM_INT(ROTATE_0) },
  { MP_ROM_QSTR(MP_QSTR_ROTATE_90), MP_ROM_INT(ROTATE_90) },
  { MP_ROM_QSTR(MP_QSTR_ROTATE_180), MP_ROM_INT(ROTATE_180) },
  { MP_ROM_QSTR(MP_QSTR_ROTATE_270), MP_ROM_INT(ROTATE_270) },
  FONT_ADD_CLASS_CONSTANTS
  { MP_ROM_QSTR(MP_QSTR_BLACK), MP_ROM_INT(BLACK) },
  { MP_ROM_QSTR(MP_QSTR_WHITE), MP_ROM_INT(WHITE) },
  { MP_ROM_QSTR(MP_QSTR_BACKGROUND), MP_ROM_INT(BACKGROUND) },
  { MP_ROM_QSTR(MP_QSTR_FOREGROUND), MP_ROM_INT(FOREGROUND) },
  { MP_ROM_QSTR(MP_QSTR_NO_WRAP), MP_ROM_INT(NO_WRAP) },
  { MP_ROM_QSTR(MP_QSTR_WRAP_INDENT), MP_ROM_INT(WRAP_INDENT) },
  { MP_ROM_QSTR(MP_QSTR_WRAP_LINE_START), MP_ROM_INT(WRAP_LINE_START) },
};

STATIC MP_DEFINE_CONST_DICT (
    mp_module_display_globals,
    display_globals_table
);

const mp_obj_module_t mp_module_display = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&mp_module_display_globals,
};
