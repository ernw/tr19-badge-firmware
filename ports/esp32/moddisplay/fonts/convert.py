lic="""/*
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

"""

import numpy as np
import math

def convert(font, width, low, c):
	offset = (c - low) * width
	char_data = 1 - font[:,range(offset, offset + width)]
	char_bytes = np.packbits(char_data, axis=1)
	return char_bytes

def write_char(font, width, low, f, c):
	char_bytes = convert(font, width, low, c)
	f.write('// @{} 0x{:02X} {}(\"{}\") width: {}\n'.format((c - low) * 16 * math.ceil(11 / 8), c, c, chr(c) if c < 127 else '?', width))
	for row in char_bytes:
		for byte in row:
			f.write('\t0x{0:02X}, '.format(byte))
		f.write('/* ')
		for byte in row:
			for bit in format(byte, '#010b')[2:]:
				f.write('#' if int(bit) == 1 else ' ')
		f.write(' */\n')
	f.write('\n\n')

def write_header(font, width, height, name, id, low, high):
	name = name.replace(' ', '_')
	with open('./font_{}{}.c'.format(name.lower(), height), 'w') as f:
		f.write(lic)
		f.write('#include "moddisplay/moddisplay_font.h"\n\n')
		f.write('#define FONT_{}_{}   {}\n\n\n'.format(name.upper(), height, id))
		f.write('const uint8_t Font_{}{}_Table[] = {{\n'.format(name, height))
		for c in range(low, high + 1):
			write_char(font, width, low, f, c)
		f.write('}};\n\ndisplay_font_t Font{}{} = {{\n\tFont_{}{}_Table,\n\tFONT_{}_{},\n\t{}, /* Width */\n\t{}, /* Height */\n\t{}, /* Minimum */\n\t{}, /* Maximum */\n\t{}, /* Offset */\n}};\n\n'.format(
			name,
			height,
			name,
			height,
			name.upper(),
			height,
			width,
			height,
			low,
			high,
			low,
		))
	return (
		'Font{}{}'.format(name, height),
		'FONT_{}_{}'.format(name.upper(), height),
		'font_{}{}.c'.format(name.lower(), height),
		id,
	)

def load_font(width, height, chars, file):
	with open(file, 'r') as f:
		numbers = []
		arrayStarted = False
		while True:
			line = f.readline()
			if line == '':
				break
			if 'static char header_data[] = {' in line:
				arrayStarted = True
				continue
			if arrayStarted:
				if '};' in line:
					break
				for i in line.strip().split(','):
					if i == '':
						continue
					numbers.append(int(i))
		data = np.array(numbers)
		return data.reshape((height, data.shape[0] // height))


def create_file(width, height, chars, file, name, id, low=32, high=126):
	font = load_font(width, height, chars, file)
	return write_header(font, width, height, name, id, low, high)


def create_files(input):
	fonts = []
	for i, file in enumerate(input):
		# 'DejaVu', 1
		fonts.append(create_file(file['width'], file['height'], file['chars'], file['file'], file['name'], i + 1, file['low'], file['high']))
	with open('./fontconfig.h', 'w') as f:
		f.write(lic)
		f.write('// Defining the fonts\n')
		for obj, name, file, id in fonts:
			f.write('#define {}    {}\n'.format(name, id))
		f.write('\n\n')
		f.write('// Configures all fonts\n\n')
		f.write('#define FONT_ADD_CLASS_CONSTANTS \\\n')
		for obj, name, file, id in fonts:
			f.write('{{ MP_ROM_QSTR(MP_QSTR_{0}), MP_ROM_INT({0}) }},\\\n'.format(name))
		f.write('\n\n')
		f.write('#define FONT_ADD_GET_FONT \\\n')
		for obj, name, file, id in fonts:
			f.write('case {}: return &{};\\\n'.format(name, obj))
		f.write('\n\n')
		f.write('#define FONT_ADD_EXTERN_FONT \\\n')
		for obj, name, file, id in fonts:
			f.write('extern display_font_t {};\\\n'.format(obj))
		f.write('\n\n')
		f.write('// Including the fonts\n')
		for obj, name, file, id in fonts:
			f.write('#include "{}"\n'.format(file))
		f.write('\n\n')
	with open('./qstrdefs.h', 'w') as f:
		f.write(lic)
		f.write('// Font names\n')
		for obj, name, file, id in fonts:
			f.write('Q({})\n'.format(name))
		f.write('\n\n')


create_files([
	{
		'width': 14,
		'height': 16,
		'chars': 195,
		'file': 'dejavu14_16_emoji.h',
		'name': 'DejaVuEmoji',
		'low': 32,
		'high': 135,
	},
	{
		'width': 9,
		'height': 16,
		'chars': 96,
		'file': 'dejavu9_16_no_emoji.h',
		'name': 'DejaVu',
		'low': 32,
		'high': 127,
	},
	{
		'width': 5,
		'height': 8,
		'chars': 96,
		'file': 'dejavu5_8_no_emoji.h',
		'name': 'DejaVu',
		'low': 32,
		'high': 127,
	},
	{
		'width': 7,
		'height': 12,
		'chars': 96,
		'file': 'dejavu7_12_no_emoji.h',
		'name': 'DejaVu',
		'low': 32,
		'high': 127,
	},
	{
		'width': 13,
		'height': 24,
		'chars': 96,
		'file': 'dejavu13_24_no_emoji.h',
		'name': 'DejaVu',
		'low': 32,
		'high': 127,
	},
	{
		'width': 21,
		'height': 42,
		'chars': 96,
		'file': 'dejavu21_42_no_emoji.h',
		'name': 'DejaVu',
		'low': 32,
		'high': 127,
	},
	{
		'width': 32,
		'height': 32,
		'chars': 7,
		'file': 'logos32_32.h',
		'name': 'Logos',
		'low': 65,
		'high': 71,
	},
])
