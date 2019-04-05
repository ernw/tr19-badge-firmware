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

// Defining the fonts
#define FONT_DEJAVUEMOJI_16    1
#define FONT_DEJAVU_16    2
#define FONT_DEJAVU_8    3
#define FONT_DEJAVU_12    4
#define FONT_DEJAVU_24    5
#define FONT_DEJAVU_42    6
#define FONT_LOGOS_32    7


// Configures all fonts

#define FONT_ADD_CLASS_CONSTANTS \
{ MP_ROM_QSTR(MP_QSTR_FONT_DEJAVUEMOJI_16), MP_ROM_INT(FONT_DEJAVUEMOJI_16) },\
{ MP_ROM_QSTR(MP_QSTR_FONT_DEJAVU_16), MP_ROM_INT(FONT_DEJAVU_16) },\
{ MP_ROM_QSTR(MP_QSTR_FONT_DEJAVU_8), MP_ROM_INT(FONT_DEJAVU_8) },\
{ MP_ROM_QSTR(MP_QSTR_FONT_DEJAVU_12), MP_ROM_INT(FONT_DEJAVU_12) },\
{ MP_ROM_QSTR(MP_QSTR_FONT_DEJAVU_24), MP_ROM_INT(FONT_DEJAVU_24) },\
{ MP_ROM_QSTR(MP_QSTR_FONT_DEJAVU_42), MP_ROM_INT(FONT_DEJAVU_42) },\
{ MP_ROM_QSTR(MP_QSTR_FONT_LOGOS_32), MP_ROM_INT(FONT_LOGOS_32) },\


#define FONT_ADD_GET_FONT \
case FONT_DEJAVUEMOJI_16: return &FontDejaVuEmoji16;\
case FONT_DEJAVU_16: return &FontDejaVu16;\
case FONT_DEJAVU_8: return &FontDejaVu8;\
case FONT_DEJAVU_12: return &FontDejaVu12;\
case FONT_DEJAVU_24: return &FontDejaVu24;\
case FONT_DEJAVU_42: return &FontDejaVu42;\
case FONT_LOGOS_32: return &FontLogos32;\


#define FONT_ADD_EXTERN_FONT \
extern display_font_t FontDejaVuEmoji16;\
extern display_font_t FontDejaVu16;\
extern display_font_t FontDejaVu8;\
extern display_font_t FontDejaVu12;\
extern display_font_t FontDejaVu24;\
extern display_font_t FontDejaVu42;\
extern display_font_t FontLogos32;\


// Including the fonts
#include "font_dejavuemoji16.c"
#include "font_dejavu16.c"
#include "font_dejavu8.c"
#include "font_dejavu12.c"
#include "font_dejavu24.c"
#include "font_dejavu42.c"
#include "font_logos32.c"


