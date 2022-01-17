# pupil-apriltags: Python bindings for the apriltags3 library

[![Build Status](https://travis-ci.org/pupil-labs/apriltags.svg?branch=master)](https://travis-ci.org/pupil-labs/apriltags)
[![PyPI](https://img.shields.io/pypi/v/pupil-apriltags)](https://pypi.org/project/pupil-apriltags/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pupil-apriltags)](https://pypi.org/project/pupil-apriltags/)
[![PyPI - Format](https://img.shields.io/pypi/format/pupil-apriltags)](https://pypi.org/project/pupil-apriltags/)

These are Python bindings for the [Apriltags3](https://github.com/AprilRobotics/apriltags) library developed by [AprilRobotics](https://april.eecs.umich.edu/), specifically adjusted to work with the pupil-labs software. The original bindings were provided by [duckietown](https://github.com/duckietown/apriltags3-py) and were inspired by the [Apriltags2 bindings](https://github.com/swatbotics/apriltag) by [Matt Zucker](https://github.com/mzucker).

## How to get started:

### Requirements

Note that **pupil-apriltags** currently only runs on Python 3.6 or higher.

Also we are using a newer python build system, which can fail for older versions of pip with potentially misleading errors.
Please make sure you are using pip > 19 or consider upgrading pip to the latest version to be on the safe side:
```bash
python -m pip install --upgrade pip
```

### Install from PyPI

This is the recommended and easiest way to install pupil-apriltags.

```sh
pip install pupil-apriltags
```

We offer pre-built binary wheels for common operating systems.
In case your system does not match, the installation might take some time, since the native library (apriltags-source) will be compiled first.

### Manual installation from source (for development)

You can of course clone the repository and build from there. For development you should install the development requirements as well. This project uses the new python build system configuration from [PEP 517](https://www.python.org/dev/peps/pep-0517/) and [PEP 518](https://www.python.org/dev/peps/pep-0518/).

```sh
# clone the repository
git clone --recursive https://github.com/pupil-labs/apriltags.git
cd apriltags

# install apriltags in editable mode with development requirements
pip install -e .[dev]

# run tests
tox
```

## Usage
Some examples of usage can be seen in the `src/pupil_apriltags/bindings.py` file.

The `Detector` class is a wrapper around the Apriltags functionality. You can initialize it as following:

```python
from pupil_apriltags import Detector

at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
```

The options are:

| **Option**        	| **Default**   	| **Explanation**                                                                                                                                                                                                                                                                                                                  	|
|-------------------	|---------------	|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| families          	| 'tag36h11'    	| Tag families, separated with a space                                                                                                                                                                                                                                                                                             	|
| nthreads          	| 1             	| Number of threads                                                                                                                                                                                                                                                                                                                	|
| quad_decimate     	| 2.0           	| Detection of quads can be done on a lower-resolution image, improving speed at a cost of pose accuracy and a slight decrease in detection rate. Decoding the binary payload is still done at full resolution. Set this to 1.0 to use the full resolution.                                                                        	|
| quad_sigma        	| 0.0           	| What Gaussian blur should be applied to the segmented image. Parameter is the standard deviation in pixels. Very noisy images benefit from non-zero values (e.g. 0.8)                                                                                                                                                            	|
| refine_edges      	| 1             	| When non-zero, the edges of the each quad are adjusted to "snap to" strong gradients nearby. This is useful when decimation is employed, as it can increase the quality of the initial quad estimate substantially. Generally recommended to be on (1). Very computationally inexpensive. Option is ignored if quad_decimate = 1 	|
| decode_sharpening 	| 0.25          	| How much sharpening should be done to decoded images? This can help decode small tags but may or may not help in odd lighting conditions or low light conditions                                                                                                                                                                 	|
| debug             	| 0             	| If 1, will save debug images. Runs very slow  

Detection of tags in images is done by running the `detect` method of the detector:

```python
tags = at_detector.detect(img, estimate_tag_pose=False, camera_params=None, tag_size=None)
```

If you also want to extract the tag pose, `estimate_tag_pose` should be set to `True` and `camera_params` (`[fx, fy, cx, cy]`) and `tag_size` (in meters) should be supplied. The `detect` method returns a list of `Detection` objects each having the following attributes (note that the ones with an asterisks are computed only if `estimate_tag_pose=True`):

| **Attribute**   	| **Explanation**                                                                                                                                                                                                                                                                                                                                                                                            	|
|-----------------	|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| tag_family      	| The family of the tag.                                                                                                                                                                                                                                                                                                                                                                                     	|
| tag_id          	| The decoded ID of the tag.                                                                                                                                                                                                                                                                                                                                                                                 	|
| hamming         	| How many error bits were corrected? Note: accepting large numbers of corrected errors leads to greatly increased false positive rates. NOTE: As of this implementation, the detector cannot detect tags with a Hamming distance greater than 2.                                                                                                                                                            	|
| decision_margin 	| A measure of the quality of the binary decoding process: the average difference between the intensity of a data bit versus the decision threshold. Higher numbers roughly indicate better decodes. This is a reasonable measure of detection accuracy only for very small tags-- not effective for larger tags (where we could have sampled anywhere within a bit cell and still gotten a good detection.) 	|
| homography      	| The 3x3 homography matrix describing the projection from an "ideal" tag (with corners at (-1,1), (1,1), (1,-1), and (-1, -1)) to pixels in the image.                                                                                                             	|
| center          	| The center of the detection in image pixel coordinates.                                                                                                                                                                                                                                                                                                                                                    	|
| corners         	| The corners of the tag in image pixel coordinates. These always wrap counter-clock wise around the tag.                                                                                                                                                                                                                                                                                                    	|
| pose_R*         	| Rotation matrix of the pose estimate.                                                                                                                                                                                                                                                                                                                                                                      	|
| pose_t*         	| Translation of the pose estimate.                                                                                                                                                                                                                                                                                                                                                                          	|
| pose_err*       	| Object-space error of the estimation.                                                                                                                                                                                                                                                                                                                                                                      	|
