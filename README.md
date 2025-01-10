# LLM-CMT
This repository provides research artifacts for the "CryMisTa" scheme.

The repository is organized as follows:

- **/Dsub**: Contains the Dsub code collection and manually labeled CAM tags stored in `label.csv`.
- **/evalution**: Includes evaluation and analysis scripts from the paper.
- **/scripts**: Stores the CryMisTa code and crawling scripts.
- **/taxonomy result**: Provides the taxonomy construction results of several LLMs on different datasets.

## D<sub>sub</sub>
This table shows the sources of code and their programming languages, with 417 examples from previous research and 299 examples from web crawling, totaling 716 examples: 231 in Java, 120 in C/C++, 245 in Python, and 120 in Go.

|            | Java | C/C++ | Python | Go | Σ  |
|------------|------|-------|--------|----|----|
| Crawled    | 35   |  120  | 42     | 102| 299|
| Other tools| 196  |  0    | 203    | 18 | 417|
| Σ          | 231  |  120  | 245    | 120| 716|

### No CAM(Cryptographic API Misuses) Codes in Crawled Data
The crawled data includes codes without CAM as follows:
- C: 73 (Correct: 63, Orthogonal: 10)
- Go: 40 (Correct: 30, Orthogonal: 10)
- Java: 30 (Correct: 13, Orthogonal: 17)
- Python: 33 (Correct: 12, Orthogonal: 21)

## Taxonomy Results
Under the 'taxonomy result' directory, we present the final classification results of CMT. They include 279 Misuse objects from `misuses.json` and the taxonomy construction results of 3 CMTs successively in the dimensions of generic cause, cryptosystem component, and security property.