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

#include "moddisplay/moddisplay_font.h"

#define FONT_DEJAVU_8   3


const uint8_t Font_DejaVu8_Table[] = {
// @0 0x20 32(" ") width: 5
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */


// @32 0x21 33("!") width: 5
	0x00, /*          */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x00, /*          */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */


// @64 0x22 34(""") width: 5
	0x00, /*          */
	0x50, /*  # #     */
	0x50, /*  # #     */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */


// @96 0x23 35("#") width: 5
	0x00, /*          */
	0x50, /*  # #     */
	0xF0, /* ####     */
	0x60, /*  ##      */
	0xF0, /* ####     */
	0xA0, /* # #      */
	0x00, /*          */
	0x00, /*          */


// @128 0x24 36("$") width: 5
	0x20, /*   #      */
	0x70, /*  ###     */
	0x60, /*  ##      */
	0x70, /*  ###     */
	0x30, /*   ##     */
	0x70, /*  ###     */
	0x20, /*   #      */
	0x00, /*          */


// @160 0x25 37("%") width: 5
	0x00, /*          */
	0xC0, /* ##       */
	0xD0, /* ## #     */
	0x60, /*  ##      */
	0xB0, /* # ##     */
	0x30, /*   ##     */
	0x00, /*          */
	0x00, /*          */


// @192 0x26 38("&") width: 5
	0x00, /*          */
	0x30, /*   ##     */
	0x20, /*   #      */
	0x58, /*  # ##    */
	0x58, /*  # ##    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @224 0x27 39("'") width: 5
	0x00, /*          */
	0x20, /*   #      */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */


// @256 0x28 40("(") width: 5
	0x20, /*   #      */
	0x40, /*  #       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */


// @288 0x29 41(")") width: 5
	0x40, /*  #       */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x40, /*  #       */
	0x00, /*          */
	0x00, /*          */


// @320 0x2A 42("*") width: 5
	0x00, /*          */
	0x20, /*   #      */
	0x70, /*  ###     */
	0x70, /*  ###     */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */


// @352 0x2B 43("+") width: 5
	0x00, /*          */
	0x00, /*          */
	0x20, /*   #      */
	0x70, /*  ###     */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */


// @384 0x2C 44(",") width: 5
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x20, /*   #      */
	0x40, /*  #       */
	0x00, /*          */


// @416 0x2D 45("-") width: 5
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x60, /*  ##      */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */


// @448 0x2E 46(".") width: 5
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */


// @480 0x2F 47("/") width: 5
	0x00, /*          */
	0x10, /*    #     */
	0x20, /*   #      */
	0x20, /*   #      */
	0x40, /*  #       */
	0x40, /*  #       */
	0x80, /* #        */
	0x00, /*          */


// @512 0x30 48("0") width: 5
	0x00, /*          */
	0x30, /*   ##     */
	0x48, /*  #  #    */
	0x68, /*  ## #    */
	0x48, /*  #  #    */
	0x30, /*   ##     */
	0x00, /*          */
	0x00, /*          */


// @544 0x31 49("1") width: 5
	0x00, /*          */
	0x60, /*  ##      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x70, /*  ###     */
	0x00, /*          */
	0x00, /*          */


// @576 0x32 50("2") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x08, /*     #    */
	0x10, /*    #     */
	0x20, /*   #      */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @608 0x33 51("3") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x08, /*     #    */
	0x30, /*   ##     */
	0x08, /*     #    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @640 0x34 52("4") width: 5
	0x00, /*          */
	0x10, /*    #     */
	0x30, /*   ##     */
	0x70, /*  ###     */
	0x78, /*  ####    */
	0x10, /*    #     */
	0x00, /*          */
	0x00, /*          */


// @672 0x35 53("5") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x40, /*  #       */
	0x70, /*  ###     */
	0x08, /*     #    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @704 0x36 54("6") width: 5
	0x00, /*          */
	0x38, /*   ###    */
	0x40, /*  #       */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x38, /*   ###    */
	0x00, /*          */
	0x00, /*          */


// @736 0x37 55("7") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x10, /*    #     */
	0x10, /*    #     */
	0x20, /*   #      */
	0x60, /*  ##      */
	0x00, /*          */
	0x00, /*          */


// @768 0x38 56("8") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x30, /*   ##     */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @800 0x39 57("9") width: 5
	0x00, /*          */
	0x70, /*  ###     */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x08, /*     #    */
	0x70, /*  ###     */
	0x00, /*          */
	0x00, /*          */


// @832 0x3A 58(":") width: 5
	0x00, /*          */
	0x00, /*          */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */


// @864 0x3B 59(";") width: 5
	0x00, /*          */
	0x00, /*          */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */
	0x20, /*   #      */
	0x40, /*  #       */
	0x00, /*          */


// @896 0x3C 60("<") width: 5
	0x00, /*          */
	0x00, /*          */
	0x08, /*     #    */
	0x70, /*  ###     */
	0x60, /*  ##      */
	0x18, /*    ##    */
	0x00, /*          */
	0x00, /*          */


// @928 0x3D 61("=") width: 5
	0x00, /*          */
	0x00, /*          */
	0x78, /*  ####    */
	0x00, /*          */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */


// @960 0x3E 62(">") width: 5
	0x00, /*          */
	0x00, /*          */
	0x40, /*  #       */
	0x38, /*   ###    */
	0x18, /*    ##    */
	0x60, /*  ##      */
	0x00, /*          */
	0x00, /*          */


// @992 0x3F 63("?") width: 5
	0x00, /*          */
	0x70, /*  ###     */
	0x10, /*    #     */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */


// @1024 0x40 64("@") width: 5
	0x00, /*          */
	0x60, /*  ##      */
	0x90, /* #  #     */
	0xB0, /* # ##     */
	0xB0, /* # ##     */
	0x80, /* #        */
	0x70, /*  ###     */
	0x00, /*          */


// @1056 0x41 65("A") width: 5
	0x00, /*          */
	0x60, /*  ##      */
	0x60, /*  ##      */
	0x60, /*  ##      */
	0xF0, /* ####     */
	0x90, /* #  #     */
	0x00, /*          */
	0x00, /*          */


// @1088 0x42 66("B") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x70, /*  ###     */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @1120 0x43 67("C") width: 5
	0x00, /*          */
	0x38, /*   ###    */
	0x40, /*  #       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x38, /*   ###    */
	0x00, /*          */
	0x00, /*          */


// @1152 0x44 68("D") width: 5
	0x00, /*          */
	0x70, /*  ###     */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x70, /*  ###     */
	0x00, /*          */
	0x00, /*          */


// @1184 0x45 69("E") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x40, /*  #       */
	0x78, /*  ####    */
	0x40, /*  #       */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @1216 0x46 70("F") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x40, /*  #       */
	0x78, /*  ####    */
	0x40, /*  #       */
	0x40, /*  #       */
	0x00, /*          */
	0x00, /*          */


// @1248 0x47 71("G") width: 5
	0x00, /*          */
	0x38, /*   ###    */
	0x40, /*  #       */
	0x58, /*  # ##    */
	0x48, /*  #  #    */
	0x38, /*   ###    */
	0x00, /*          */
	0x00, /*          */


// @1280 0x48 72("H") width: 5
	0x00, /*          */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x00, /*          */
	0x00, /*          */


// @1312 0x49 73("I") width: 5
	0x00, /*          */
	0x70, /*  ###     */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x70, /*  ###     */
	0x00, /*          */
	0x00, /*          */


// @1344 0x4A 74("J") width: 5
	0x00, /*          */
	0x18, /*    ##    */
	0x08, /*     #    */
	0x08, /*     #    */
	0x08, /*     #    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @1376 0x4B 75("K") width: 5
	0x00, /*          */
	0x50, /*  # #     */
	0x70, /*  ###     */
	0x60, /*  ##      */
	0x50, /*  # #     */
	0x58, /*  # ##    */
	0x00, /*          */
	0x00, /*          */


// @1408 0x4C 76("L") width: 5
	0x00, /*          */
	0x40, /*  #       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @1440 0x4D 77("M") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x78, /*  ####    */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x00, /*          */
	0x00, /*          */


// @1472 0x4E 78("N") width: 5
	0x00, /*          */
	0x68, /*  ## #    */
	0x68, /*  ## #    */
	0x78, /*  ####    */
	0x58, /*  # ##    */
	0x48, /*  #  #    */
	0x00, /*          */
	0x00, /*          */


// @1504 0x4F 79("O") width: 5
	0x00, /*          */
	0x30, /*   ##     */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x30, /*   ##     */
	0x00, /*          */
	0x00, /*          */


// @1536 0x50 80("P") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x40, /*  #       */
	0x40, /*  #       */
	0x00, /*          */
	0x00, /*          */


// @1568 0x51 81("Q") width: 5
	0x00, /*          */
	0x30, /*   ##     */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x30, /*   ##     */
	0x08, /*     #    */
	0x00, /*          */


// @1600 0x52 82("R") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x70, /*  ###     */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x00, /*          */
	0x00, /*          */


// @1632 0x53 83("S") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x40, /*  #       */
	0x30, /*   ##     */
	0x08, /*     #    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @1664 0x54 84("T") width: 5
	0x00, /*          */
	0x70, /*  ###     */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */


// @1696 0x55 85("U") width: 5
	0x00, /*          */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @1728 0x56 86("V") width: 5
	0x00, /*          */
	0x90, /* #  #     */
	0x90, /* #  #     */
	0x60, /*  ##      */
	0x60, /*  ##      */
	0x60, /*  ##      */
	0x00, /*          */
	0x00, /*          */


// @1760 0x57 87("W") width: 5
	0x00, /*          */
	0x90, /* #  #     */
	0xF0, /* ####     */
	0xF0, /* ####     */
	0xF0, /* ####     */
	0x60, /*  ##      */
	0x00, /*          */
	0x00, /*          */


// @1792 0x58 88("X") width: 5
	0x00, /*          */
	0x90, /* #  #     */
	0x60, /*  ##      */
	0x60, /*  ##      */
	0x60, /*  ##      */
	0x90, /* #  #     */
	0x00, /*          */
	0x00, /*          */


// @1824 0x59 89("Y") width: 5
	0x00, /*          */
	0xD8, /* ## ##    */
	0x50, /*  # #     */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */


// @1856 0x5A 90("Z") width: 5
	0x00, /*          */
	0x78, /*  ####    */
	0x10, /*    #     */
	0x30, /*   ##     */
	0x20, /*   #      */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @1888 0x5B 91("[") width: 5
	0x60, /*  ##      */
	0x40, /*  #       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x60, /*  ##      */
	0x00, /*          */
	0x00, /*          */


// @1920 0x5C 92("\") width: 5
	0x00, /*          */
	0x80, /* #        */
	0x80, /* #        */
	0x40, /*  #       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x20, /*   #      */
	0x00, /*          */


// @1952 0x5D 93("]") width: 5
	0x60, /*  ##      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x60, /*  ##      */
	0x00, /*          */
	0x00, /*          */


// @1984 0x5E 94("^") width: 5
	0x00, /*          */
	0x60, /*  ##      */
	0x90, /* #  #     */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */


// @2016 0x5F 95("_") width: 5
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0xF0, /* ####     */


// @2048 0x60 96("`") width: 5
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */


// @2080 0x61 97("a") width: 5
	0x00, /*          */
	0x00, /*          */
	0x38, /*   ###    */
	0x08, /*     #    */
	0x78, /*  ####    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @2112 0x62 98("b") width: 5
	0x40, /*  #       */
	0x40, /*  #       */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @2144 0x63 99("c") width: 5
	0x00, /*          */
	0x00, /*          */
	0x38, /*   ###    */
	0x40, /*  #       */
	0x40, /*  #       */
	0x38, /*   ###    */
	0x00, /*          */
	0x00, /*          */


// @2176 0x64 100("d") width: 5
	0x08, /*     #    */
	0x08, /*     #    */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @2208 0x65 101("e") width: 5
	0x00, /*          */
	0x00, /*          */
	0x38, /*   ###    */
	0x78, /*  ####    */
	0x40, /*  #       */
	0x38, /*   ###    */
	0x00, /*          */
	0x00, /*          */


// @2240 0x66 102("f") width: 5
	0x30, /*   ##     */
	0x20, /*   #      */
	0x70, /*  ###     */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x00, /*          */
	0x00, /*          */


// @2272 0x67 103("g") width: 5
	0x00, /*          */
	0x00, /*          */
	0x38, /*   ###    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x38, /*   ###    */
	0x78, /*  ####    */
	0x00, /*          */


// @2304 0x68 104("h") width: 5
	0x40, /*  #       */
	0x40, /*  #       */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x00, /*          */
	0x00, /*          */


// @2336 0x69 105("i") width: 5
	0x20, /*   #      */
	0x00, /*          */
	0x60, /*  ##      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x70, /*  ###     */
	0x00, /*          */
	0x00, /*          */


// @2368 0x6A 106("j") width: 5
	0x20, /*   #      */
	0x00, /*          */
	0x60, /*  ##      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x60, /*  ##      */
	0x00, /*          */


// @2400 0x6B 107("k") width: 5
	0x40, /*  #       */
	0x40, /*  #       */
	0x50, /*  # #     */
	0x60, /*  ##      */
	0x50, /*  # #     */
	0x58, /*  # ##    */
	0x00, /*          */
	0x00, /*          */


// @2432 0x6C 108("l") width: 5
	0xC0, /* ##       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x60, /*  ##      */
	0x00, /*          */
	0x00, /*          */


// @2464 0x6D 109("m") width: 5
	0x00, /*          */
	0x00, /*          */
	0x70, /*  ###     */
	0x70, /*  ###     */
	0x70, /*  ###     */
	0x70, /*  ###     */
	0x00, /*          */
	0x00, /*          */


// @2496 0x6E 110("n") width: 5
	0x00, /*          */
	0x00, /*          */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x00, /*          */
	0x00, /*          */


// @2528 0x6F 111("o") width: 5
	0x00, /*          */
	0x00, /*          */
	0x30, /*   ##     */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x30, /*   ##     */
	0x00, /*          */
	0x00, /*          */


// @2560 0x70 112("p") width: 5
	0x00, /*          */
	0x00, /*          */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x40, /*  #       */
	0x00, /*          */


// @2592 0x71 113("q") width: 5
	0x00, /*          */
	0x00, /*          */
	0x78, /*  ####    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x08, /*     #    */
	0x00, /*          */


// @2624 0x72 114("r") width: 5
	0x00, /*          */
	0x00, /*          */
	0x70, /*  ###     */
	0x40, /*  #       */
	0x40, /*  #       */
	0x40, /*  #       */
	0x00, /*          */
	0x00, /*          */


// @2656 0x73 115("s") width: 5
	0x00, /*          */
	0x00, /*          */
	0x78, /*  ####    */
	0x60, /*  ##      */
	0x18, /*    ##    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @2688 0x74 116("t") width: 5
	0x00, /*          */
	0x40, /*  #       */
	0xE0, /* ###      */
	0x40, /*  #       */
	0x40, /*  #       */
	0x60, /*  ##      */
	0x00, /*          */
	0x00, /*          */


// @2720 0x75 117("u") width: 5
	0x00, /*          */
	0x00, /*          */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @2752 0x76 118("v") width: 5
	0x00, /*          */
	0x00, /*          */
	0x48, /*  #  #    */
	0x78, /*  ####    */
	0x30, /*   ##     */
	0x30, /*   ##     */
	0x00, /*          */
	0x00, /*          */


// @2784 0x77 119("w") width: 5
	0x00, /*          */
	0x00, /*          */
	0x90, /* #  #     */
	0xF0, /* ####     */
	0xF0, /* ####     */
	0x60, /*  ##      */
	0x00, /*          */
	0x00, /*          */


// @2816 0x78 120("x") width: 5
	0x00, /*          */
	0x00, /*          */
	0x78, /*  ####    */
	0x30, /*   ##     */
	0x30, /*   ##     */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @2848 0x79 121("y") width: 5
	0x00, /*          */
	0x00, /*          */
	0x48, /*  #  #    */
	0x30, /*   ##     */
	0x30, /*   ##     */
	0x20, /*   #      */
	0x60, /*  ##      */
	0x00, /*          */


// @2880 0x7A 122("z") width: 5
	0x00, /*          */
	0x00, /*          */
	0x78, /*  ####    */
	0x10, /*    #     */
	0x20, /*   #      */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */


// @2912 0x7B 123("{") width: 5
	0x30, /*   ##     */
	0x20, /*   #      */
	0x20, /*   #      */
	0x40, /*  #       */
	0x20, /*   #      */
	0x30, /*   ##     */
	0x00, /*          */
	0x00, /*          */


// @2944 0x7C 124("|") width: 5
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x00, /*          */


// @2976 0x7D 125("}") width: 5
	0x60, /*  ##      */
	0x20, /*   #      */
	0x20, /*   #      */
	0x10, /*    #     */
	0x20, /*   #      */
	0x60, /*  ##      */
	0x00, /*          */
	0x00, /*          */


// @3008 0x7E 126("~") width: 5
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x78, /*  ####    */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */
	0x00, /*          */


// @3040 0x7F 127("?") width: 5
	0x78, /*  ####    */
	0x78, /*  ####    */
	0x78, /*  ####    */
	0x78, /*  ####    */
	0x78, /*  ####    */
	0x78, /*  ####    */
	0x78, /*  ####    */
	0x78, /*  ####    */


};

display_font_t FontDejaVu8 = {
	Font_DejaVu8_Table,
	FONT_DEJAVU_8,
	5, /* Width */
	8, /* Height */
	32, /* Minimum */
	127, /* Maximum */
	32, /* Offset */
};
