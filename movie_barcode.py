import cv2
import numpy as np
import sys

import optparse


def compute_barcode(input_file, vidcap, output_file, height, width, frame_skip, save_to_output_file):
    print "Processing video file %s. This may take a while depending on the size of the video or the system performance..." % (input_file)

    frame_count = 0
    success = True
    barcode = None

    while success:
        success, image = vidcap.read()
        if frame_count % frame_skip == 0:
            if success:
                resized_image = cv2.resize(image, (1, height))
            if barcode is None:
                barcode = resized_image
            else:
                barcode = np.hstack((barcode, resized_image))
        frame_count += 1
    barcode = cv2.resize(barcode, (width, height))

    if save_to_output_file:
        cv2.imwrite(output_file, barcode)
        print "Processing complete! Barcode image saved in %s" % (output_file)
    else:
        cv2.imshow("Movie Barcode Generator", barcode)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def compute_dimensions(vidcap, height, width, frameskip, frameswidth):
    if 0 == height and 0 == width:
        height = vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        width = vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        return height, width
    if 0 != height and 0 != width:
        return height, width
    if 0 != height and 0 == width and frameswidth:
        video_frame_count = vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        width = video_frame_count / frameskip
        return height, width
    video_height = vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    video_width = vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    aspect = video_width / video_height
    if 0 != height and 0 == width:
        return height, height * aspect
    if 0 == height and 0 != width:
        return width / aspect, width

def run():
    # "Usage: python movie_barcode.py <video_file_name>"
    parser = optparse.OptionParser()
    parser.add_option('-s', '--source', help='source video')
    parser.add_option('-o', '--output', help='output barcode image')
    parser.add_option('-h', '--height', default=0, help='output height; proportional to width if not present (default: match source height)')
    parser.add_option('-w', '--width', default=0, help='output width; proportional to height if not present (default: match source width)')
    parser.add_option('-f', '--frameswidth', default=False, action='store_true', help='set output width by frame count')
    parser.add_option('-f', '--frameskip', default=10, help='frames to skip when creating the barcode')
    parser.add_option('-v', '--verbose', default=False, action='store_true', help='be verbose')
    options, args = parser.parse_args()
    
    vidcap = cv2.VideoCapture(options.source)
    height, width = compute_dimensions(vidcap, options.height, options.width, options.frameskip, options.frameswidth)
    compute_barcode(options.source, vidcap, options.output, height, width, options.frame_skip, save_to_output_file)

if __name__ == '__main__':
    sys.exit(run())
