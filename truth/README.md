# The Science Behind DNA Parentage Testing
## A Technical Overview of Canine Genetic Analysis
# DNA亲子鉴定背后的科学
## 犬类遗传分析的技术概述

*详细内容我就不给造谣方翻译了，在澳洲留学应该要看得懂英文教案，不要给澳洲留子丢脸。在网上造谣更应该懂得法律后果。* :p

---

## Introduction / 介绍

**DNA Parentage Testing** is a scientific method used to determine biological relationships between individuals using genetic markers.

**Key Applications:**
- Verify breeding records
- Confirm pedigrees
- Resolve paternity disputes
- Maintain breed integrity
- ***Support legal proceedings / 支持法律诉讼***

**Accuracy:** Modern DNA testing achieves >99.9% accuracy in parentage determination¹

**References:**
¹ Butler, J.M. (2015). Advanced Topics in Forensic DNA Typing: Interpretation. Academic Press.

---

## The Foundation - DNA Basics / DNA基础知识

**DNA Structure:**
- Every cell contains DNA with unique genetic information
- DNA is inherited: 50% from mother, 50% from father
- Specific locations on DNA = **genetic markers**

**Genetic Markers:**
- **SNPs** (Single Nucleotide Polymorphisms): Single letter changes in DNA
- **STRs** (Short Tandem Repeats): Repeated sequences of 2-7 base pairs
- Each marker has multiple possible variants (**alleles**)

**Genotype:** The combination of alleles at a specific marker (e.g., A/G, T/T)²

**References:**
² Hartl, D.L. & Clark, A.G. (2019). Principles of Population Genetics. 4th Edition. Sinauer Associates.

---

## Mendelian Inheritance / 孟德尔遗传定律

**Mendel's Laws:**
1. Each parent contributes one allele per marker
2. Offspring inherit one allele from each parent
3. Inheritance follows predictable patterns

**Example:**
- Mother: A/G (can contribute A or G)
- Father: T/T (can only contribute T)
- **Possible offspring:** A/T or G/T
- **Impossible offspring:** A/A, G/G, C/C

**Exclusion Principle:** If offspring has impossible genotype → parentage excluded³

**References:**
³ Evett, I.W. & Weir, B.S. (1998). Interpreting DNA Evidence: Statistical Genetics for Forensic Scientists. Sinauer Associates.

---

## How My Analysis Works / 分析步骤

**1. Data Loading**
- Extract genotypes from DNA profile files
- Parse allele combinations (A/G, T/T, etc.)
- Identify common markers across all individuals

**2. Mendelian Analysis**
- For each marker, generate all possible offspring genotypes
- Compare actual offspring genotype to possible combinations
- Mark as "consistent" or "exclusion"

**3. Statistical Evaluation**
- Count total consistent vs. inconsistent markers
- Calculate confidence levels based on exclusion patterns

---

## The Algorithm in Detail / 算法说明

```python
def check_mendelian_inheritance(parent1, parent2, offspring):
    # Generate all possible offspring combinations
    possible_offspring = []
    for allele1 in parent1:
        for allele2 in parent2:
            possible_offspring.append(sorted([allele1, allele2]))
    
    # Check if actual offspring matches any possibility
    return sorted(offspring) in possible_offspring
```

**Example Calculation:**
- Mother: [A, G] 
- Father: [T, T]
- Possible offspring: [[A,T], [G,T]]
- Actual offspring: [A,T] → **CONSISTENT**

---

## DNA Markers Used / 使用的DNA标记

**My analysis uses SNP markers from DNA Page 3:**
- BICF2G630255439 → A/G
- BICF2G630271966 → A/G
- BICF2P1308802 → A/C
- BICF2G630307199 → A/A

**SNP Advantages:**
- High discrimination power (220+ markers)
- Very stable (low mutation rate)⁴
- Standardized across laboratories
- Reliable for complex cases

**Data Format:**
- MarkerID | Genotype
- Clean, consistent format
- 124 markers per dog
- No missing data

**References:**
⁴ International Society for Animal Genetics. (2020). "Comparison test for parentage testing in dogs using SNP markers." Animal Genetics, 51(3), 363-369.

---

## Statistical Interpretation / 统计解释

**Confidence Categories:**
- **Very High:** 0 exclusions, ≥20 consistent markers
- **High:** ≤1 exclusion, ≥15 consistent markers  
- **Moderate:** ≤2 exclusions, ≥10 consistent markers
- **Low:** >2 exclusions or <10 consistent markers

**Exclusion Tolerance:**
- 0-1 exclusions: Likely parentage (mutations/technical errors)
- 2-3 exclusions: Questionable, investigate further
- 4+ exclusions: Parentage excluded

**Why Some Exclusions are Acceptable:**
- Spontaneous mutations (~0.1% rate)⁵
- Technical errors in testing
- Sample contamination

**References:**
⁵ Weber, J.L. & Wong, C. (1993). "Mutation of human short tandem repeats." Human Molecular Genetics, 2(8), 1123-1128.

---

## Real-World Applications / 现实应用
### 堵上造谣方的嘴

**When dog owners spread ridiculous rumors about breeders supposedly "swapping dogs" for DNA tests:**

DNA evidence doesn't lie. People do.

While some owners love to create conspiracy theories and spread gossip about their breeders allegedly switching samples, scientific DNA analysis cuts through all the nonsense with cold, hard facts.

No amount of dramatic accusations or social media rumors can change what the genetic markers reveal.

---

## Scientific Validation / 科学验证

**Legal Acceptance / 法律认可:**
- Court-admissible evidence / 法庭可采纳证据⁶

**References:**
⁶ National Research Council. (1996). The Evaluation of Forensic DNA Evidence. National Academy Press, Washington, DC.

---

## References

1. Butler, J.M. (2015). Advanced Topics in Forensic DNA Typing: Interpretation. Academic Press.

2. Hartl, D.L. & Clark, A.G. (2019). Principles of Population Genetics. 4th Edition. Sinauer Associates.

3. Evett, I.W. & Weir, B.S. (1998). Interpreting DNA Evidence: Statistical Genetics for Forensic Scientists. Sinauer Associates.

4. International Society for Animal Genetics. (2020). "Comparison test for parentage testing in dogs using SNP markers." Animal Genetics, 51(3), 363-369.

5. Weber, J.L. & Wong, C. (1993). "Mutation of human short tandem repeats." Human Molecular Genetics, 2(8), 1123-1128.

6. National Research Council. (1996). The Evaluation of Forensic DNA Evidence. National Academy Press, Washington, DC.