import cv2
import numpy as np
import sys

import optparse


def compute_barcode(input_file, output_file, barcode_height, frame_skip, save_to_output_file):
    vidcap = cv2.VideoCapture(input_file)

    print "Processing video file %s. This may take a while depending on the size of the video or the system performance..." % (input_file)

    frame_count = 0
    success = True
    barcode = None

    while success:
        success, image = vidcap.read()
        if frame_count % frame_skip == 0:
            if success:
                resized_image = cv2.resize(image, (1, 600))
            if barcode is None:
                barcode = resized_image
            else:
                barcode = np.hstack((barcode, resized_image))
        frame_count += 1

    if save_to_output_file:
        cv2.imwrite(output_file, barcode)
        print "Processing complete! Barcode image saved in %s" % (output_file)
    else:
        cv2.imshow("Movie Barcode Generator", barcode)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def run():
    # "Usage: python movie_barcode.py <video_file_name>"
    parser = optparse.OptionParser()
    parser.add_option('-s', '--source', help='source video')
    parser.add_option('-o', '--output', help='output barcode image')
    parser.add_option('-h', '--height', help='output height; proportional to width if not present (default: match source height)')
    parser.add_option('-w', '--width', help='output width; proportional to height if not present (default: match source width)')
    parser.add_option('-f', '--frameskip', default=10, help='frames to skip when creating the barcode')
    parser.add_option('-v', '--verbose', default=False, action='store_true', help='be verbose')
    options, args = parser.parse_args()
    
    height, width = compute_dimensions(options.source, options.height, options.width, options.frameskip)
    compute_barcode(options.source, options.output, barcode_height, options.frame_skip, save_to_output_file)

if __name__ == '__main__':
    sys.exit(run())
