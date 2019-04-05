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

#include "extmod/machine_spi.h"
#include "modmachine.h"

#include "moddisplay_epd2in9.h"

void spi_write(display_display_obj_t *self, size_t len, const uint8_t* buf) {
    mp_machine_spi_transfer(self->spi, len, buf, NULL);
}

int display_epd2in9_init(display_display_obj_t *self) {
    display_epd2in9_reset(self);
    display_epd2in9_send_command(self, DRIVER_OUTPUT_CONTROL);
    display_epd2in9_send_data(self, (self->frame->height - 1) & 0xFF);
    display_epd2in9_send_data(self, ((self->frame->height - 1) >> 8) & 0xFF);
    display_epd2in9_send_data(self, 0x00);
    display_epd2in9_send_command(self, BOOSTER_SOFT_START_CONTROL);
    display_epd2in9_send_data(self, 0xD7);
    display_epd2in9_send_data(self, 0xD6);
    display_epd2in9_send_data(self, 0x9D);
    display_epd2in9_send_command(self, WRITE_VCOM_REGISTER);
    display_epd2in9_send_data(self, 0xA8);                     // VCOM 7C
    display_epd2in9_send_command(self, SET_DUMMY_LINE_PERIOD);
    display_epd2in9_send_data(self, 0x1A);                     // 4 dummy lines per gate
    display_epd2in9_send_command(self, SET_GATE_TIME);
    display_epd2in9_send_data(self, 0x08);                     // 2us per line
    display_epd2in9_send_command(self, DATA_ENTRY_MODE_SETTING);
    display_epd2in9_send_data(self, 0x03);
    if (self->partial) {
        display_epd2in9_send_lut(self, display_epd2in9_lut_partial);
    } else {
        display_epd2in9_send_lut(self, display_epd2in9_lut_full);
    }
    return 0;
}

void display_epd2in9_reset(display_display_obj_t *self) {
    gpio_set_level(self->rst, LOW);
    mp_hal_delay_ms(200);
    gpio_set_level(self->rst, HIGH);
    mp_hal_delay_ms(200);
}

void display_epd2in9_send_lut(display_display_obj_t *self, const unsigned char* lut) {
    display_epd2in9_send_command(self, WRITE_LUT_REGISTER);
    /* the length of look-up table is 30 bytes */
    for (int i = 0; i < 30; i++) {
        display_epd2in9_send_data(self, lut[i]);
    }
}

void display_epd2in9_flush(display_display_obj_t *self) {
    display_epd2in9_send_command(self, DISPLAY_UPDATE_CONTROL_2);
    display_epd2in9_send_data(self, 0xC4);
    display_epd2in9_send_command(self, MASTER_ACTIVATION);
    display_epd2in9_send_command(self, TERMINATE_FRAME_READ_WRITE);
    display_epd2in9_wait_until_idle(self);
}

void display_epd2in9_send_command(display_display_obj_t *self, const uint8_t command) {
    gpio_set_level(self->dc, LOW);
    gpio_set_level(self->cs, LOW);
    spi_write(self, 1, &command);
    gpio_set_level(self->cs, HIGH);
}

void display_epd2in9_send_data(display_display_obj_t *self, const uint8_t data) {
    gpio_set_level(self->dc, HIGH);
    gpio_set_level(self->cs, LOW);
    spi_write(self, 1, &data);
    gpio_set_level(self->cs, HIGH);
}

void display_epd2in9_send_data_buffer(display_display_obj_t *self, size_t len, const uint8_t* buf) {
    gpio_set_level(self->dc, HIGH);
    gpio_set_level(self->cs, LOW);
    spi_write(self, len, buf);
    gpio_set_level(self->cs, HIGH);
}

void display_epd2in9_wait_until_idle(display_display_obj_t *self) {
    // LOW: idle, HIGH: busy
    while(gpio_get_level(self->busy) == HIGH) {
        mp_hal_delay_ms(10);
    }
}

void display_epd2in9_set_memory_area(display_display_obj_t *self, int x_start, int y_start, int x_end, int y_end) {
    display_epd2in9_send_command(self, SET_RAM_X_ADDRESS_START_END_POSITION);
    /* x point must be the multiple of 8 or the last 3 bits will be ignored */
    display_epd2in9_send_data(self, (x_start >> 3) & 0xFF);
    display_epd2in9_send_data(self, (x_end >> 3) & 0xFF);
    display_epd2in9_send_command(self, SET_RAM_Y_ADDRESS_START_END_POSITION);
    display_epd2in9_send_data(self, y_start & 0xFF);
    display_epd2in9_send_data(self, (y_start >> 8) & 0xFF);
    display_epd2in9_send_data(self, y_end & 0xFF);
    display_epd2in9_send_data(self, (y_end >> 8) & 0xFF);
}

void display_epd2in9_set_memory_pointer(display_display_obj_t *self, int x, int y) {
    display_epd2in9_send_command(self, SET_RAM_X_ADDRESS_COUNTER);
    /* x point must be the multiple of 8 or the last 3 bits will be ignored */
    display_epd2in9_send_data(self, (x >> 3) & 0xFF);
    display_epd2in9_send_command(self, SET_RAM_Y_ADDRESS_COUNTER);
    display_epd2in9_send_data(self, y & 0xFF);
    display_epd2in9_send_data(self, (y >> 8) & 0xFF);
    display_epd2in9_wait_until_idle(self);
}

void display_epd2in9_set_frame_memory_partial(display_display_obj_t *self, int x, int y, int width, int height) {
    int x_end, y_end;

    if (x < 0 || width < 0 || y < 0 || height < 0) {
        return;
    }
    /* x point must be the multiple of 8 or the last 3 bits will be ignored */
    x &= 0xF8;
    width &= 0xF8;
    if (x + width >= self->frame->width) {
        x_end = self->frame->width - 1;
    } else {
        x_end = x + width - 1;
    }
    if (y + height >= self->frame->height) {
        y_end = self->frame->height - 1;
    } else {
        y_end = y + height - 1;
    }
    display_epd2in9_set_memory_area(self, x, y, x_end, y_end);
    display_epd2in9_set_memory_pointer(self, x, y);
    display_epd2in9_send_command(self, WRITE_RAM);
    /* send the image data */
    for (int j = 0; j < y_end - y + 1; j++) {
        for (int i = 0; i < (x_end - x + 1) / 8; i++) {
            display_epd2in9_send_data(self, self->frame->buf[i + j * (width / 8)]);
        }
    }
}

void display_epd2in9_set_frame_memory(display_display_obj_t *self) {
    display_epd2in9_set_memory_area(self, 0, 0, self->frame->width - 1, self->frame->height - 1);
    display_epd2in9_set_memory_pointer(self, 0, 0);
    display_epd2in9_send_command(self, WRITE_RAM);
    /* send the image data */
    display_epd2in9_send_data_buffer(self, self->frame->size, self->frame->buf);
}

void display_epd2in9_clear_frame_memory(display_display_obj_t *self, unsigned char color) {
    display_epd2in9_set_memory_area(self, 0, 0, self->frame->width - 1, self->frame->height - 1);
    display_epd2in9_set_memory_pointer(self, 0, 0);
    display_epd2in9_send_command(self, WRITE_RAM);
    /* send the image data */
    for (int i = 0; i < self->frame->size; i++) {
        display_epd2in9_send_data(self, color);
    }
}



const unsigned char display_epd2in9_lut_full[] = {
  0x02, 0x02, 0x01, 0x11, 0x12, 0x12, 0x22, 0x22, 0x66, 0x69, 0x69, 0x59, 0x58, 0x99, 0x99,
  0x88, 0x00, 0x00, 0x00, 0x00, 0xF8, 0xB4, 0x13, 0x51, 0x35, 0x51, 0x51, 0x19, 0x01, 0x00
};

const unsigned char display_epd2in9_lut_partial[] = {
  0x10, 0x18, 0x18, 0x08, 0x18, 0x18, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x13, 0x14, 0x44, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};
