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

import sys
import numpy as np
import math
import base64

def convert(image, width):
	offset = 0
	char_data = 1 - image
	char_bytes = np.packbits(char_data, axis=1)
	return char_bytes

def load_image(file, width):
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
		return data.reshape((data.shape[0] // int(width), int(width)))


def create_image(file, width):
	image = load_image(file, width)
	return convert(image, width), image.shape


def convert_image(file, width):
	image, shape = create_image(file, width)
	print(base64.b64encode(image).decode('ascii'))
	print(shape)

if len(sys.argv) > 2:
	convert_image(sys.argv[1], sys.argv[2])
else:
	print('Usage: convert.py [image].h [width]')

