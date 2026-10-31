# Onboarding Notes for Data Processing

## to do 02/05/2026
- add mad and peak vector rmse functions to github repo, 
- create read me's and documentation for other members to read and learn about these
- integrate repos existing datacubes to make testing of functions seamless

## super resolution (SR)
means converting low res images (LR) to high res images (HR)
- multiple methods depending on characteristics of LR images

### multi frame remote sensing (MFRS)
requirements: 
- this method requires LR images to have necessary supplementary info 
  - they cannot be transformations / resamples of each other
  - deviations must not be an integral num of pixels
  - how to get LR with necessary supp info? options include hardware control or preset sub-pixel hardware displacement
  - "This was successfully implemented with the SPOT-5 satellite with line-array CCDs being offset by 0.5 pixels"

method: 
- works by essentially layering the LR images with slight deviation
- "The sensor on SPOT-5 has two panchromatic sensors with a spatial resolution of 5m, an when SR is applied, the spatial resolution on 2.5m, a 2x improvement."

multi angle imaging (MAI) is another MFRS method
requirements:
- higher temporal res since each image needs multiple passes
- some images will ahve higher spatial res than others due to spatial res being higher at nadir

method: 
- multiple passses with diff off-nadir skew angles, use to create HR
MAI can be considered if temporal shift is difficult on payload elec end

### single frame remote sensing (SFRS)
SFRS can be used if LR images do not fit MFRS requirements
- methods include:
  1. interpolation
  2. reconstruction
  3. external database
  4. compressed sensing
- 1 & 2 are not considered effective methods since there is not enough mid range frequency data in an image to remove artifacts and clarify edges. 
  - note that the same does *not* apply for image compression

neural networks (NN) and external databases:
- with internal similarities of similar images, one can train a neural network on an external database of similar LR
- test and training sets must be very similar
- training set is augmented by randomly reducing quality of some parts of image, making random crops, flipping, and artificially producing errors
- there is ethical concerns with NN hallucinating image features. dataset should be very similar to the images you want to enhance to ensure SR works properly for iamges

compressed sensing
"can be performed by solving for sparse coefficients in a transformed domain"
- does not require similar training set nor hardware accomodations for sub-pixel accuracy
- thus the preferred method

## compression
# JPEG compression
*incomplete notes*
maximum absolute distortion (MAD) / peak absolute error (PAE)
- $MAD = \max_{i,j} \{ \left| x(i,j) - \hat{x}(i,j) \right|\} $

**measures largest single difference between corresponding pixels in og and reconstructed image**
- contrast against MSE (mean squared error) and PNSR (peak noise signal ratio) which average