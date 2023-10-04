Authors present the first large-scale dataset for semantic Segmentation of Underwater IMagery (**SUIM**). It contains over 1500 images with pixel annotations for eight object categories: : *waterbody_background* (BW), *human_divers* (HD), *aquatic_plants_and sea-grass*, *wrecks_and_ruins* (WR), *robots* (RO), *reefs_and_invertebrates* (RI), *fish_and_vertebrates* (FV), *sea-floor_and_rocks* (SR). Authors use 3-bit binary RGB colors to represent these eight object categories in the image space.

The SUIM dataset has 1525 RGB images for training and validation; another 110 test images are provided for benchmark evaluation of semantic segmentation models. The images are of various spatial resolutions, e.g., 1906 × 1080, 1280 × 720, 640 × 480, and 256 × 256. These images are carefully chosen from a large pool of samples collected during oceanic explorations and human-robot cooperative experiments in several locations of various water types. We also utilize a few images from large-scale datasets named
[EUVP](https://arxiv.org/abs/1903.09766), [USR-248](https://ui.adsabs.harvard.edu/abs/2019arXiv190909437J/abstract), and [UFO-120](https://arxiv.org/abs/2002.01155), which authors previously proposed for underwater image enhancement and super-resolution problems. The images are chosen to accommodate a diverse set of natural underwater scenes and various setups for human-robot collaborative experiments.

![Fig](https://i.ibb.co/GkY2rtH/Screenshot-2023-10-04-064021.png)

This figure demonstrates the population of each object category, their pairwise correlations, and the distributions of RGB channel intensity values in the SUIM dataset.

All images of the SUIM dataset are pixel-annotated by seven human participants. Authors followed the guidelines discussed in [The Ocean Animal Encyclopedia](https://oceana.org/marine-life/) and [“Marine Species Identification Portal](http://species-identification.org/) for classifying potentially confusing objects of interest such as plants/reefs, vertebrates/invertebrates, etc.

<i>Please note, that some masks include bad data. Check full list at [GitHub page](https://github.com/dataset-ninja/suim/blob/main/src/convert.py#L83)</i>
