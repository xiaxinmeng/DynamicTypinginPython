from fisher import pvalue

# compute p value
fisher_val = pvalue(8, 2, 1, 5)
print(fisher_val)


# 疗效	有效	无效
# A	8	2
# B	7	23

import scipy.stats as stats
oddsratio, pvalue = stats.fisher_exact([[8, 2], [1, 5]])
print(oddsratio,pvalue)