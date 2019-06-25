# HypergraphAlgorithms
Contains python module to convert datasets to hypergraph matrices for complex network analysis. This work is in conjunction with [MESH](http://mesh.cs.umn.edu/) framework developed to support scalable analysis of evolving hypergraph structures.

We encourage you to cite our research paper if you have used the following datasets in your work. You can refer to:
[Hypergraph Characterization of Small Groups. Ankit Sharma, Himanshu Kharakwal, Abhishek Chandra, Jaideep Srivastava.](http://mesh.cs.umn.edu/papers/hypchar.pdf)

Datasets:

I. Collaboration datasets
1. [DBLP](https://www.aminer.cn/citation)
2. [Pubmed](https://www.ncbi.nlm.nih.gov/pubmed/)
3. [USPatent](http://www.nber.org/patents/)
4. [Arxiv](https://arxiv.org/)

II. Communication datasets
1. [EUmail](http://www.cs.cornell.edu/~arb/data/email-Eu/index.html)

III. Movie dataset
1. [IMDB](https://www.imdb.com/interfaces/)

The module is used to convert above mentioned datasets into complete hypergraphs or category based hypergraphs.

#### Collaboration datasets
### 1. DBLP:
Categories are formed on the basis of conferences where the research paper is published:
1. Biomedical Engineering and Medical Informatics
2. Computational Theory and Mathematics
3. Computer Graphics and Computer Aided Design
4. Computer Linguistics and Speech Processing
5. Computer Networks and Communications
6. Computer Security and Cryptography
7. General Computer Science
8. Hardware Robotics and Electronics
9. Human Computer Interaction
10. Image Processing and Computer Vision
11. Information Systems
12. Machine Learning, Data Mining and Artificial Intelligence
13. Signal Processing
14. Software Engineering
15. Web Mobile and Multimedia Technologies


### 2. Pubmed:
Categories are picked from the [ncbi category search link](https://www.ncbi.nlm.nih.gov/nlmcatalog/advanced). Select "Broad Subject Term" from first drop down below "Builder". Now if you click "Show index list" on the right side of the box a list of categories appear. All the journals related to that category can be searched. We have handpicked the following categories:
1. Anatomy
2. Anesthesiology
3. Audiology
4. Behavioral sciences
5. Biochemistry
6. Biomedical engineering
7. Biotechnology
8. Cardiology
9. Clinical laboratory techniques
10. Communicable diseases
11. Critical care
12. Dentistry
13. Dermatology
14. Drug therapy
15. Emergency medicine
16. Endocrinology
17. Epidemiology
18. Ethics
19. Gastroenterology
20. General surgery
21. Genetics
22. Geriatrics
23. Gynecology
24. Hematology
25. Medical informatics
26. Medicine
27. Metabolism
28. Microbiology
29. Molecular biology
30. Neoplasms
31. Neurology
32. Neurosurgery
33. Nuclear medicine
34. Nursing
35. Nutritional sciences
36. Obstetrics
37. Ophthalmology
38. Orthopedics
39. Otolaryngology
40. Pathology
41. Pediatrics
42. Pharmacology
43. Physiology
44. Psychiatry
45. Psychology
46. Public health
47. Pulmonary medicine
48. Rheumatology
49. Social sciences
50. Therapeutics
51. Toxicology
52. Traumatology
53. Tropical medicine
54. Urology
55. Vascular diseases
56. Veterinary medicine
57. Virology

### 3. USPatent:

Categories are already provided along with the patents. Patents are divided into following [categories](http://www.nber.org/patents/subcategories.txt):
1. Chemical
2. Computers & Communications
3. Drugs & Medical
4. Electrical & Electronic
5. Mechanical
6. Others(Miscellaneous)

### 4. Arxiv:

Research paper carries information about its subject(category):
1. Physics
  - astrophysics, condensed_matter, grqc, hepl, hepp, hept, hepx, mathematical_physics, nonlinear_sciences, nuclear_experiment, nuclear_theory, quantum_physics
2. Mathematics
3. Computer Science
4. Quantitative Biology
5. Quantitative Finance
6. Statistics
7. Electrical Engineering and Systems Science
8. Economics

#### Movie dataset
### 1. IMDB:
Categories are formed on the basis of movie genres:
1. Action
2. Adult
3. Adventure
4. Animation
5. Biography
6. Comedy
7. Crime
8. Documentary
9. Drama
10. Family
11. Fantasy
12. Film-Noir
13. Game-Show
14. History
15. Horror
16. Musical
17. Music
18. Mystery
19. General
20. News
21. Reality-TV
22. Romance
23. Sci-Fi
24. Short
25. Sport
26. Talk-Show
27. Thriller
28. War
29. Western
