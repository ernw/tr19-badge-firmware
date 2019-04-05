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

#ifndef MICROPY_INCLUDED_EXTMOD_DISPLAY_EPD2IN9_H
#define MICROPY_INCLUDED_EXTMOD_DISPLAY_EPD2IN9_H

#include "moddisplay_display.h"

#define LOW                                         0x00
#define HIGH                                        0x01

#define DRIVER_OUTPUT_CONTROL                       0x01
#define BOOSTER_SOFT_START_CONTROL                  0x0C
#define GATE_SCAN_START_POSITION                    0x0F
#define DEEP_SLEEP_MODE                             0x10
#define DATA_ENTRY_MODE_SETTING                     0x11
#define SW_RESET                                    0x12
#define TEMPERATURE_SENSOR_CONTROL                  0x1A
#define MASTER_ACTIVATION                           0x20
#define DISPLAY_UPDATE_CONTROL_1                    0x21
#define DISPLAY_UPDATE_CONTROL_2                    0x22
#define WRITE_RAM                                   0x24
#define WRITE_VCOM_REGISTER                         0x2C
#define WRITE_LUT_REGISTER                          0x32
#define SET_DUMMY_LINE_PERIOD                       0x3A
#define SET_GATE_TIME                               0x3B
#define BORDER_WAVEFORM_CONTROL                     0x3C
#define SET_RAM_X_ADDRESS_START_END_POSITION        0x44
#define SET_RAM_Y_ADDRESS_START_END_POSITION        0x45
#define SET_RAM_X_ADDRESS_COUNTER                   0x4E
#define SET_RAM_Y_ADDRESS_COUNTER                   0x4F
#define TERMINATE_FRAME_READ_WRITE                  0xFF

void spi_write(display_display_obj_t *self, size_t len, const uint8_t* buf);

int display_epd2in9_init(display_display_obj_t *self);
void display_epd2in9_reset(display_display_obj_t *self);
void display_epd2in9_send_lut(display_display_obj_t *self, const unsigned char *lut);
void display_epd2in9_flush(display_display_obj_t *self);
void display_epd2in9_send_command(display_display_obj_t *self, const uint8_t command);
void display_epd2in9_send_data(display_display_obj_t *self, const uint8_t data);
void display_epd2in9_send_data_buffer(display_display_obj_t *self, size_t len, const uint8_t* buf);
void display_epd2in9_wait_until_idle(display_display_obj_t *self);

void display_epd2in9_set_memory_area(display_display_obj_t *self, int x_start, int y_start, int x_end, int y_end);
void display_epd2in9_set_memory_pointer(display_display_obj_t *self, int x, int y);

void display_epd2in9_set_frame_memory_partial(display_display_obj_t *self, int x, int y, int width, int height);
void display_epd2in9_set_frame_memory(display_display_obj_t *self);
void display_epd2in9_clear_frame_memory(display_display_obj_t *self, unsigned char color);

extern const unsigned char display_epd2in9_lut_full[];
extern const unsigned char display_epd2in9_lut_partial[];

#endif // MICROPY_INCLUDED_EXTMOD_DISPLAY_EPD2IN9_H
