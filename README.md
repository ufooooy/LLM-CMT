# Small Dataset and Taxonomy Results of CMT 

This repository provides the small dataset and taxonomy results of Cryptographic Misuse Taxonomy (CMT) scheme.

## Small Dataset 
This table shows a summary of data sources categorized by whether they contain cryptographic API misuse or not. "Other tools" show the highest count with 362 instances of misuse and no instances without misuse. The "Craweled" category has both, 217 instances with misuse and 113 without misuse. The "Handmade" category only includes instances with misuse (24) and none without misuse. In total (Σ), there are 603 instances with misuse and 113 instances without misuse in this dataset.

| Source     | w/ misuse | w/o misuse |
|------------|-----------|------------|
| Other tools|    362    |     0      |
| Craweled   |    217    |    113     |
| Handmade   |     24    |     0      |
| Σ          |    603    |    113     |

## Taxonomy Results
Under the 'taxonomy result' directory, we present the final classification results of CMT. They include 279 Misuse objects from 'misuses.json' and the taxonomy construction results of 3 CMTs successively in the dimensions of generic cause, cryptosystem component, and security property.
