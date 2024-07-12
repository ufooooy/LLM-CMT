# D<sub>sub</sub> and Taxonomy Results of CryMisTa 

This repository provides D<sub>sub</sub> dataset from CryMisTa (Cryptographic Misuses Taxonomy) scheme, which established a 'ground truth' for cryptographic API misuse (CAM) through manual analysis. It also includes the taxonomy results of CryMisTa.

## D<sub>sub</sub>
This table shows the sources of code and their programming languages, with 417 examples from previous research and 299 examples from web crawling, totaling 716 examples: 231 in Java, 120 in C/C++, 245 in Python, and 120 in Go.

|            | Java | C/C++ | Python | Go | Σ  |
|------------|------|-------|--------|----|----|
| Other tools| 196  |  \    | 203    | 18 | 417|
| Craweled   | 35   |  120  | 42     | 102| 299|
| Σ          | 231  |  120  | 245    | 120| 716|

## Taxonomy Results
Under the 'taxonomy result' directory, we present the final classification results of CMT. They include 279 Misuse objects from 'misuses.json' and the taxonomy construction results of 3 CMTs successively in the dimensions of generic cause, cryptosystem component, and security property.
