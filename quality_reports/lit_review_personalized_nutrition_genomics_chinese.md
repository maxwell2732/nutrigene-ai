# Literature Review: Personalized Nutrition Genomics for Chinese Populations

**Date:** 2026-02-16
**Query:** Personalized nutrition genomics for Chinese population, integrate genetics and dietary recommendations

---

## Summary

Personalized nutrition genomics (nutrigenomics) is a rapidly maturing field that leverages individual genetic variation to tailor dietary recommendations, moving beyond one-size-fits-all guidelines. For Chinese populations, this field carries particular significance due to (1) unique allele frequency distributions in nutrition-relevant genes like MTHFR, FTO, FADS1/2, and APOE; (2) dramatic dietary transitions from traditional regional patterns toward Western-style diets; and (3) the rising burden of diet-related chronic diseases including type 2 diabetes, cardiovascular disease, and obesity across China.

Recent years (2023-2025) have seen an acceleration of research activity, highlighted by the establishment of the China Precision Nutrition Biobank (CPNB), comprehensive narrative reviews on SNP-diet interactions in Chinese adults, and the integration of AI/machine learning with multi-omics data for precision dietary recommendations. The field is transitioning from single-gene association studies toward polygenic, multi-omics frameworks that incorporate genomics, metabolomics, microbiomics, and phenotypic data. However, most large-scale intervention trials remain anchored in European-descent populations, leaving a critical evidence gap for East Asian and specifically Chinese populations.

The convergence of large Chinese biobanks (China Kadoorie Biobank with 510,000+ participants; CPNB), advancing genotyping technologies, and AI-driven analytical tools positions China to become a leader in population-specific precision nutrition, though significant challenges remain in translating genetic associations into actionable, culturally appropriate dietary guidance.

---

## Key Papers

### Yang et al. (2025) — SNP-Dietary Pattern Interactions and Obesity in Chinese Adults
- **Main contribution:** Comprehensive narrative review synthesizing evidence on interactions between SNPs, dietary patterns, and overweight/obesity specifically in Chinese adults (literature from 2018-2025).
- **Method:** Narrative review structured around dietary factors, obesity-related SNPs, sex and ethnic differences, multigene synergistic effects, and gene-diet interplay.
- **Key finding:** MC4R rs12970134 risk allele carriers showed BMI increase of 0.140 kg/m² with high-energy diets; Western diets associated with 2x obesity incidence vs. traditional Chinese patterns; southern Chinese diets demonstrate protective effects while northern diets show 2.04-fold elevated prevalence.
- **Relevance:** Directly addresses gene-diet interactions in Chinese populations and proposes a three-dimensional gene-diet-metabolic phenotype model highly relevant to NutriGene AI.
- **Source:** [Frontiers in Nutrition](https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2025.1603038/full) | [PMC12668921](https://pmc.ncbi.nlm.nih.gov/articles/PMC12668921/)

### China Precision Nutrition Biobank (CPNB) Consortium (2025) — Cohort Protocol
- **Main contribution:** Protocol for a prospective, longitudinal cohort study designed to investigate diet-phenotype/genotype interactions in Chinese adults aged 18-40.
- **Method:** Three-phase design: alpha (n=200 pilot), beta (n=1,450 transition), gamma (n=20,000 main cohort); collecting genetic, dietary, phenotypic, and metabolomic data from urban and rural areas.
- **Key finding:** Protocol paper — establishes infrastructure for precision dietary strategies targeting early-onset chronic diseases in Chinese populations.
- **Relevance:** Provides the methodological blueprint and future data resource for Chinese-population-specific nutrigenomics research.
- **Source:** [Nutrition Journal / Springer](https://link.springer.com/article/10.1186/s12937-025-01255-w)

### Singar et al. (2024) — Personalized Nutrition Through Genetic Insights
- **Main contribution:** Comprehensive review of how genetic variants (FTO, MTHFR, APOE, TCF7L2, BCMO1) modulate individual responses to nutrients and dietary interventions.
- **Method:** Systematic literature review integrating genomic, phenotypic, biochemical, and nutritional data.
- **Key finding:** Established a framework for personalized nutrition integrating genomic profiling, phenotypic data, clinical biomarkers, and lifestyle factors; emphasized the role of registered dietitians in delivering interventions.
- **Relevance:** Provides the general theoretical framework applicable to the NutriGene AI recommendation engine.
- **Source:** [Nutrients / MDPI](https://www.mdpi.com/2072-6643/16/16/2673) | [PMC11357412](https://pmc.ncbi.nlm.nih.gov/articles/PMC11357412/)

### Nature Communications Biology (2025) — Genetic Diversity of Central Plains Han Chinese
- **Main contribution:** Whole-genome sequencing of 492 Central Plains Han Chinese individuals revealing population-specific genetic architecture relevant to metabolic traits.
- **Method:** WGS with population genetics analysis, selection signal detection.
- **Key finding:** Identified 22.65 million SNPs; glycolipid metabolic genes (LONP2, FADS2, FGF21, SLC19A2) showed strong selection signals, indicating dietary adaptation.
- **Relevance:** Identifies Chinese-specific genetic variants under dietary selection pressure — directly informing which SNPs to prioritize in nutrigenomic models.
- **Source:** [Nature Communications Biology](https://www.nature.com/articles/s42003-025-07760-2)

### He et al. (2016) / Updated Meta-analyses — MTHFR Polymorphism Distribution in Chinese Populations
- **Main contribution:** Geographic and ethnic mapping of MTHFR C677T, A1298C, and MTRR A66G frequencies across Chinese sub-populations.
- **Method:** Meta-analysis of population studies; total T allele frequency of MTHFR C677T = 36.9% in Chinese populations.
- **Key finding:** Significant north-south gradient in MTHFR C677T frequency; northern Chinese populations have higher T allele frequency, correlating with higher homocysteine levels; clinical guidelines now recommend genotype-stratified folate supplementation (0.8-1 mg/day for TT/CT carriers planning pregnancy).
- **Relevance:** One of the most clinically actionable gene-nutrient interactions in Chinese populations; directly relevant to personalized supplementation recommendations.
- **Source:** [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0152414) | [PMC4835080](https://pmc.ncbi.nlm.nih.gov/articles/PMC4835080/)

### AI in Personalized Nutrition — Multiple Reviews (2024-2025)
- **Main contribution:** Systematic reviews documenting the explosion of AI/ML applications in personalized nutrition, reaching 83 publications in 2024 alone.
- **Method:** Systematic reviews covering gradient boosting, deep neural networks, CNNs for food image recognition, NLP for dietary recommendation systems.
- **Key finding:** Gradient boosting models predict caloric needs with MAE of 132 kcal; multi-omics integration with AI enables real-time, adaptive dietary recommendations; the field is recognized as a mature interdisciplinary research area.
- **Relevance:** Directly informs the AI/ML architecture choices for NutriGene AI.
- **Source:** [PMC12325300](https://pmc.ncbi.nlm.nih.gov/articles/PMC12325300/) | [PMC12193492](https://pmc.ncbi.nlm.nih.gov/articles/PMC12193492/) | [PMC11013624](https://pmc.ncbi.nlm.nih.gov/articles/PMC11013624/) | [PMC12700061](https://pmc.ncbi.nlm.nih.gov/articles/PMC12700061/)

### China Kadoorie Biobank — Diet and Chronic Disease
- **Main contribution:** Large-scale prospective evidence on diet-disease relationships in Chinese adults (510,000+ participants), with genomic data now available for 100,000+.
- **Method:** Prospective cohort with questionnaire, physical measurements, blood biobanking, and genome-wide genotyping (Axiom arrays).
- **Key finding:** Dairy consumption inversely associated with cardiovascular disease; red meat intake associated with 11% higher diabetes risk per 50 g/day; effects modified by bodily iron stores.
- **Relevance:** Largest available Chinese cohort with both dietary and genomic data — essential validation resource for nutrigenomic models.
- **Source:** [CKB Official Site](https://www.ckbiobank.org/) | [CKB Diet Achievements](https://www.ckbiobank.org/achievements/diet-1)

### Tanaka et al. (2011) / Updated Studies — FADS1/FADS2 Polymorphisms in Asians
- **Main contribution:** Demonstrated that FADS1/FADS2 SNPs significantly alter desaturase activity in Asian populations, with population-specific allele distributions.
- **Method:** Genotyping of 19 SNPs across FADS1/FADS2 locus in Caucasian and Asian young adults.
- **Key finding:** FADS1 rs174547 showed strongest association with AA:LA ratio in Asians (p=5.0 × 10⁻⁵); FADS2 rs498793 associated with EPA:ALA ratio; FADS2 shows strong selection signals in Han Chinese WGS data.
- **Relevance:** FADS variants determine individual omega-3/omega-6 metabolism efficiency — critical for personalized fatty acid intake recommendations in Chinese populations.
- **Source:** [PubMed 21414826](https://pubmed.ncbi.nlm.nih.gov/21414826/)

---

## Thematic Organization

### Theoretical Contributions

The field is converging on a **multi-layered framework** for personalized nutrition that integrates:

1. **Genomic layer** — SNPs in nutrition-relevant genes (FTO, MC4R, MTHFR, APOE, FADS1/2, TCF7L2, BCMO1, ADIPOQ) that modulate nutrient metabolism, absorption, and disease susceptibility.
2. **Metabolomic layer** — Circulating metabolites (homocysteine, LCPUFAs, short-chain fatty acids) as dynamic biomarkers of gene-diet interaction effects.
3. **Microbiome layer** — Gut microbiota composition mediating dietary responses; emerging evidence of population-specific microbiome signatures.
4. **Phenotypic layer** — BMI, blood pressure, glycemic response, lipid profiles as measurable outcomes.
5. **Cultural/environmental layer** — Regional dietary patterns, food availability, cooking methods, and lifestyle factors.

Yang et al. (2025) propose a **"three-dimensional gene-diet-metabolic phenotype model"** specifically for Chinese populations, which represents the most integrated theoretical framework to date for this population. This model acknowledges that identified SNPs explain <5% of BMI variation despite 40-70% heritability estimates, highlighting the need for multigene and gene-environment interaction models.

### Empirical Findings

**Population-specific allele frequencies matter.** Chinese populations show distinct frequency distributions for key nutrition-related variants:
- MTHFR C677T: 36.9% T allele frequency, with a north-south gradient
- FTO rs9939609: Lower minor allele frequency in East Asians (~12-20%) vs. Europeans (~42%), but still associated with obesity susceptibility
- FADS1/2 cluster: Strong selection signals in Han Chinese, indicating historical dietary adaptation
- Glycolipid metabolic genes (LONP2, FADS2, FGF21, SLC19A2) under positive selection in Central Plains Han Chinese

**Regional dietary patterns interact with genotype.** Southern Chinese traditional diets (rice-based, vegetable-rich) appear to buffer against genetic obesity risk, while northern diets (higher refined carbohydrates, sodium) show 2.04-fold elevated obesity prevalence. Urban dietary shifts toward processed foods exacerbate genetic susceptibility to conditions like gestational diabetes.

**Sex-specific effects are pronounced.** Carbohydrate intake is inversely associated with obesity in Chinese women only; MC4R and other obesity-associated SNPs show sex-modulated effects.

### Methodological Innovations

1. **Multi-omics integration** — Moving beyond GWAS to simultaneously analyze genomic, transcriptomic, proteomic, metabolomic, and microbiomic data for holistic individual profiling.
2. **AI/ML approaches** — Gradient boosting decision trees (GBDT), deep neural networks, CNNs for food recognition, and NLP for adaptive dietary recommendation systems; AutoPrognosis framework for model optimization.
3. **Large-scale Chinese biobanks** — CKB (510K+ participants, 100K+ genotyped), CPNB (planned 20K with deep phenotyping), and ChinaMAP providing population-specific reference data.
4. **Genotype-stratified clinical guidelines** — MTHFR-guided folate supplementation in Chinese pregnancy planning represents one of the first clinically implemented nutrigenomic interventions.

---

## Gaps and Opportunities

1. **Lack of Chinese-population-specific randomized controlled trials (RCTs).** Most nutrigenomic intervention trials have been conducted in European-descent populations. The few Chinese studies are observational or small-scale. The CPNB cohort, once mature, could partially address this gap, but large-scale genotype-stratified dietary RCTs in Chinese populations are urgently needed.

2. **Missing polygenic risk score (PRS) models for nutrition traits in Chinese populations.** While PRS for diseases like diabetes and cardiovascular disease are advancing, PRS for dietary response phenotypes (e.g., glycemic response to specific foods, lipid response to dietary fat composition) remain underdeveloped for East Asian populations due to limited training data.

3. **Insufficient integration of traditional Chinese dietary patterns into nutrigenomic frameworks.** Current models largely adopt Western dietary categories. A framework that captures the complexity of Chinese regional cuisines (Cantonese, Sichuan, northern wheat-based, etc.), traditional medicine dietary concepts, and their interactions with genotype is missing.

4. **Limited AI/ML models trained on Chinese dietary and genomic data.** Most AI-driven nutrition recommendation systems are trained on Western cohort data. Models specifically calibrated for Chinese food composition, eating patterns, and genetic backgrounds are needed.

5. **Gene-microbiome-diet triangle remains poorly characterized in Chinese populations.** The gut microbiome mediates many gene-diet interactions, but population-specific microbiome data integrated with genomic and dietary data for Chinese cohorts is sparse.

6. **Ethical and privacy framework gaps.** As direct-to-consumer genetic testing expands in China, regulatory frameworks for nutrigenomic data privacy, genetic discrimination prevention, and quality control of personalized nutrition services lag behind the technology.

7. **Translation gap: from association to actionable recommendation.** Identified SNPs explain <5% of trait variance. Converting statistical associations into clinically meaningful, individually actionable dietary recommendations remains the central challenge. MTHFR-folate is one success story; replicating this for other gene-nutrient pairs at scale is the frontier.

---

## Suggested Next Steps

- **Read in depth:** Yang et al. 2025 (PMC12668921) full text for the Chinese-specific gene-diet framework; CPNB protocol for study design inspiration
- **Data acquisition:** Explore access to China Kadoorie Biobank genotype + dietary data; consider CPNB collaboration
- **Model development priority:** Start with well-validated gene-nutrient pairs (MTHFR-folate, FADS-omega3, FTO-macronutrient ratio, APOE-lipid intake) before expanding to polygenic models
- **Chinese food composition database:** Obtain the China Food Composition Tables (中国食物成分表) for accurate nutrient mapping in recommendation algorithms
- **AI architecture:** Review gradient boosting and deep learning approaches from recent systematic reviews (PMC12325300, PMC12193492) for NutriGene AI model selection
- **Validation strategy:** Design with CKB or CPNB-style cohort validation in mind; ensure any model is testable against Chinese population data
- **Regional stratification:** Build models that account for north-south genetic and dietary gradients in China

---

## BibTeX Entries

**Note:** Some entries below are reconstructed from search results. Entries marked with `[VERIFY]` should be confirmed against the original publication before use in manuscripts.

```bibtex
@article{yang2025snp,
  title={Research progress on the mechanistic impact of single-nucleotide polymorphisms and dietary pattern interactions on overweight and obesity in Chinese adults: a narrative review},
  author={Yang, W and Xu, H and Xu, C and Cao, K and Pan, Y and Gu, R and Zhu, Q and Xiao, J},
  journal={Frontiers in Nutrition},
  volume={12},
  pages={1603038},
  year={2025},
  publisher={Frontiers},
  note={PMID: 41340654}
}

@article{singar2024personalized,
  title={Personalized Nutrition: Tailoring Dietary Recommendations through Genetic Insights},
  author={Singar, Saiful and Nagpal, Ravinder and Arjmandi, Bahram H and Akhavan, Neda S},
  journal={Nutrients},
  volume={16},
  number={16},
  pages={2673},
  year={2024},
  publisher={MDPI},
  note={PMID: 39203810}
}

@article{cpnb2025protocol,
  title={China precision nutrition biobank: protocol of a prospective cohort study on diet, human phenotype/genotype, and early-onset chronic diseases},
  author={{CPNB Consortium}},
  journal={Nutrition Journal},
  year={2025},
  publisher={Springer Nature},
  note={[VERIFY] exact author list and volume/page numbers}
}

@article{he2016mthfr,
  title={Geographical and Ethnic Distributions of the {MTHFR} {C677T}, {A1298C} and {MTRR} {A66G} Gene Polymorphisms in Chinese Populations: A Meta-Analysis},
  author={He, [VERIFY first name] and others},
  journal={PLOS ONE},
  year={2016},
  doi={10.1371/journal.pone.0152414}
}

@article{tanaka2011fads,
  title={Polymorphisms in {FADS1} and {FADS2} alter desaturase activity in young Caucasian and Asian adults},
  author={Tanaka, Toshiko and others},
  journal={Molecular Genetics and Metabolism},
  year={2011},
  note={PMID: 21414826, [VERIFY] exact journal and volume}
}

@article{han2025genetic,
  title={Genetic diversity and dietary adaptations of the Central Plains Han Chinese population in East Asia},
  author={[VERIFY]},
  journal={Communications Biology},
  year={2025},
  publisher={Nature Publishing Group}
}

@article{chen2004ckb,
  title={China Kadoorie Biobank of 0.5 million people: survey methods, baseline characteristics and long-term follow-up},
  author={Chen, Zhengming and others},
  journal={International Journal of Epidemiology},
  year={2011},
  note={[VERIFY] exact year and details; CKB has multiple protocol papers}
}

@article{ai_nutrition_2024_review,
  title={Applications of Artificial Intelligence, Machine Learning, and Deep Learning in Nutrition: A Systematic Review},
  author={[VERIFY]},
  journal={[VERIFY]},
  year={2024},
  note={PMC11013624}
}

@article{ai_personalized_diet_2025,
  title={Artificial Intelligence Applications to Personalized Dietary Recommendations: A Systematic Review},
  author={[VERIFY]},
  journal={[VERIFY]},
  year={2025},
  note={PMC12193492}
}

@article{ai_nutrition_comprehensive_2025,
  title={Artificial intelligence in personalized nutrition and food manufacturing: a comprehensive review},
  author={[VERIFY]},
  journal={[VERIFY]},
  year={2025},
  note={PMC12325300}
}
```

---

## Appendix: Key Genes for NutriGene AI Model

| Gene | Variant(s) | Function | Chinese-Specific Notes |
|------|-----------|----------|----------------------|
| FTO | rs9939609, rs1121980, rs8050136 | Obesity susceptibility, appetite regulation | Lower MAF in East Asians (~12-20%) but still significant |
| MC4R | rs17782313, rs12970134 | Energy homeostasis, satiety signaling | 0.140 kg/m² BMI increase per risk allele with high-energy diet |
| MTHFR | C677T (rs1801133), A1298C | Folate metabolism, homocysteine | 36.9% T allele; north-south gradient; clinical guidelines exist |
| APOE | e2/e3/e4 | Lipid metabolism, CVD risk | Modulates response to dietary fat; population-specific frequencies |
| FADS1/2 | rs174547, rs498793 | Omega-3/6 LCPUFA synthesis | Strong selection signals in Han Chinese; affects desaturase activity |
| TCF7L2 | Various | Type 2 diabetes risk | Gene-diet interactions with carbohydrate intake |
| BCMO1 | Various | Beta-carotene → Vitamin A conversion | Affects plant-based vitamin A efficiency |
| ADIPOQ | Various | Adiponectin, insulin sensitivity | Adipose metabolism regulation |
| FGF21 | Various | Metabolic regulation, sweet preference | Under selection in Central Plains Han Chinese |
| SLC19A2 | Various | Thiamine transport | Under selection in Central Plains Han Chinese |
