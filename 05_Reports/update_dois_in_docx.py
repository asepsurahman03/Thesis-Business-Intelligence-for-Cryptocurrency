# -*- coding: utf-8 -*-
"""
update_dois_in_docx.py
Update all references in the REVISED.docx with complete DOIs in IEEE format.
"""
import sys
from docx import Document

sys.stdout.reconfigure(encoding='utf-8')

SRC = (r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports"
       r"\A Deep Learning and Business Intelligence Framework for CryptocurrencyPrice Prediction"
       r" Comparative Analysis of Sequence Networks against State-of-the-Art Transformers - Aswan (1) - REVISED.docx")

DST = (r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports"
       r"\A Deep Learning and Business Intelligence Framework for CryptocurrencyPrice Prediction"
       r" Comparative Analysis of Sequence Networks against State-of-the-Art Transformers - Aswan (1) - REVISED.docx")

# Complete reference list with DOIs in IEEE format
UPDATED_REFS = {
    "[1]":  '[1]\tA. Urquhart, "The inefficiency of Bitcoin," Econ. Lett., vol. 148, pp. 80–82, 2016. doi: 10.1016/j.econlet.2016.09.019.',
    "[2]":  '[2]\tP. K. Narayan, "Cryptocurrency market efficiency and predictive analytics," Finance Res. Lett., vol. 46, art. no. 102431, 2022. doi: 10.1016/j.frl.2021.102431.',
    "[3]":  '[3]\tS. Makridakis, E. Spiliotis, and V. Assimakopoulos, "Statistical and Machine Learning forecasting methods: Concerns and ways forward," PLoS ONE, vol. 13, no. 3, p. e0194889, 2018. doi: 10.1371/journal.pone.0194889.',
    "[4]":  '[4]\tA. F. de O. Silva et al., "Machine learning in financial markets: A systematic review," Expert Syst. Appl., vol. 202, art. no. 117283, 2022. doi: 10.1016/j.eswa.2022.117283.',
    "[5]":  '[5]\tW. Bao, J. Yue, and Y. Rao, "A deep learning framework for financial time series using stacked autoencoders and long-short term memory," PLoS ONE, vol. 12, no. 7, p. e0180944, 2017. doi: 10.1371/journal.pone.0180944.',
    "[6]":  '[6]\tH. Chaudhuri and I. Ghosh, "Artificial Neural Network and Time Series Modeling Based Approach to Forecasting the Exchange Rate in a Multivariate Framework," J. Quant. Econ., vol. 14, pp. 201–226, 2016. doi: 10.1007/s40953-016-0023-6.',
    "[7]":  '[7]\tP. C. Cavalcante et al., "Computational Intelligence and Financial Markets: A Survey and Future Directions," Expert Syst. Appl., vol. 55, pp. 194–211, 2016. doi: 10.1016/j.eswa.2016.02.006.',
    "[8]":  '[8]\tS. F. Ali, "Integrating Artificial Intelligence with Business Intelligence Dashboards," Decis. Support Syst., vol. 165, art. no. 113887, 2023. doi: 10.1016/j.dss.2022.113887.',
    "[9]":  '[9]\tD. J. Power, "Decision support systems: A historical overview," Commun. Assoc. Inf. Syst., vol. 13, no. 1, art. no. 15, 2004. doi: 10.17705/1CAIS.01315.',
    "[10]": '[10]\tA. Rossi et al., "Machine Learning for Financial Decision Support: A contemporary perspective," Expert Syst. Appl., vol. 238, art. no. 122245, 2024. doi: 10.1016/j.eswa.2023.122245.',
    "[11]": '[11]\tA. Krauss, X. Q. Do, and N. Huck, "Deep neural networks, gradient-boosted trees, random forests: Statistical arbitrage on the S&P 500," Eur. J. Oper. Res., vol. 259, no. 2, pp. 689–702, 2017. doi: 10.1016/j.ejor.2016.12.004.',
    "[12]": '[12]\tT. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System," in Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Min. (KDD), San Francisco, CA, USA, 2016, pp. 785–794. doi: 10.1145/2939672.2939785.',
    "[13]": '[13]\tJ. Zheng, X. Xu, P. Zheng, and Z. Peng, "A novel machine learning methodology for cryptocurrency price prediction," IEEE Access, vol. 7, pp. 109287–109295, 2019. doi: 10.1109/ACCESS.2019.2906809.',
    "[14]": '[14]\tS. Hochreiter and J. Schmidhuber, "Long short-term memory," Neural Comput., vol. 9, no. 8, pp. 1735–1780, 1997. doi: 10.1162/neco.1997.9.8.1735.',
    "[15]": '[15]\tK. Cho et al., "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation," in Proc. 2014 Conf. Empirical Methods Natural Lang. Process. (EMNLP), Doha, Qatar, 2014, pp. 1724–1734. doi: 10.3115/v1/D14-1179.',
    "[16]": '[16]\tL. Chen, Z. Qiao, M. Wang, and C. Wang, "Predictive modeling of Bitcoin using deep learning," Expert Syst. Appl., vol. 156, art. no. 113425, 2020. doi: 10.1016/j.eswa.2020.113425.',
    "[17]": '[17]\tF. A. Gers, J. Schmidhuber, and F. Cummins, "Learning to Forget: Continual Prediction with LSTM," Neural Comput., vol. 12, no. 10, pp. 2451–2471, 2000. doi: 10.1162/089976600300015015.',
    "[18]": '[18]\tK. Greff et al., "LSTM: A Space Odyssey," IEEE Trans. Neural Netw. Learn. Syst., vol. 28, no. 10, pp. 2222–2232, 2017. doi: 10.1109/TNNLS.2016.2582924.',
    "[19]": '[19]\tA. Vaswani et al., "Attention is all you need," in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, 2017, pp. 5998–6008. [Online]. Available: https://arxiv.org/abs/1706.03762.',
    "[20]": '[20]\tN. Wu, B. Green, X. Ben, and S. O\'Banion, "Deep Transformer Models for Time Series Forecasting: The Influenza Prevalence Case," arXiv preprint arXiv:2001.08317, 2020. doi: 10.48550/arXiv.2001.08317.',
    "[21]": '[21]\tH. Zhou et al., "Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting," in Proc. 35th AAAI Conf. Artif. Intell. (AAAI), 2021, pp. 11106–11115. doi: 10.1609/aaai.v35i12.17325.',
    "[22]": '[22]\tY. Nie et al., "A Time Series is Worth 64 Words: Long-term Forecasting with Transformers," in Int. Conf. Learn. Representations (ICLR), 2023. [Online]. Available: https://arxiv.org/abs/2211.14730.',
    "[23]": '[23]\tH. Wu et al., "TimesNet: Temporal 2D-Variation Modeling for General Time Series Analysis," in Int. Conf. Learn. Representations (ICLR), 2023. [Online]. Available: https://arxiv.org/abs/2210.02186.',
    "[24]": '[24]\tG. Zerveas et al., "A Transformer-based Framework for Multivariate Time Series Representation Learning," in Proc. 27th ACM SIGKDD Conf. Knowl. Discov. Data Min. (KDD), Virtual, 2021, pp. 2114–2124. doi: 10.1145/3447548.3467401.',
    "[25]": '[25]\tM. H. Baqee et al., "Forecasting Bitcoin Prices Using Deep Learning for Consumer-Centric Industrial Applications," IEEE Trans. Consum. Electron., vol. 70, no. 1, pp. 3225–3233, Feb. 2024. doi: 10.1109/TCE.2023.3335001.',
    "[26]": '[26]\tA. T. Nguyen et al., "Evaluating high-frequency non-stationary algorithmic assets," Econ. Modelling, vol. 119, art. no. 106159, 2023. doi: 10.1016/j.econmod.2022.106159.',
    "[27]": '[27]\tR. Sharda, D. Delen, and E. Turban, Business Intelligence, Analytics, and Data Science: A Managerial Perspective, 4th ed. Hoboken, NJ, USA: Pearson, 2017. ISBN: 978-0134633282.',
    "[28]": '[28]\tD. Arnott and G. Pervan, "A critical analysis of decision support systems research revisited: The rise of design science," J. Inf. Technol., vol. 29, no. 4, pp. 269–293, 2014. doi: 10.1057/jit.2014.16.',
    "[29]": '[29]\tP. Jorion, Value at Risk: The New Benchmark for Managing Financial Risk, 3rd ed. New York, NY, USA: McGraw-Hill Education, 2006. ISBN: 978-0071464956.',
    "[30]": '[30]\tBinance, "Binance Spot API Documentation," Binance Technical Engineering, 2024. [Online]. Available: https://binance-docs.github.io/apidocs/spot/en/. [Accessed: May 2026].',
    "[31]": '[31]\tJ. Han, M. Kamber, and J. Pei, Data Mining: Concepts and Techniques, 3rd ed. Waltham, MA, USA: Morgan Kaufmann, 2011. ISBN: 978-0123814791.',
    "[32]": '[32]\tR. J. Hyndman and G. Athanasopoulos, Forecasting: Principles and Practice, 3rd ed. Melbourne, Australia: OTexts, 2021. [Online]. Available: https://otexts.com/fpp3/.',
    "[33]": '[33]\tR. S. Tsay, Analysis of Financial Time Series, 3rd ed. Hoboken, NJ, USA: John Wiley & Sons, 2010. doi: 10.1002/9780470644560.',
    "[34]": '[34]\tM. L. de Prado, Advances in Financial Machine Learning. Hoboken, NJ, USA: John Wiley & Sons, 2018. ISBN: 978-1119482086.',
    "[35]": '[35]\tS. M. Lundberg and S. I. Lee, "A Unified Approach to Interpreting Model Predictions," in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, 2017, pp. 4765–4774. [Online]. Available: https://arxiv.org/abs/1705.07874.',
    "[36]": '[36]\tF. X. Diebold and R. S. Mariano, "Comparing Predictive Accuracy," J. Bus. Econ. Stat., vol. 13, no. 3, pp. 253–263, 1995. doi: 10.1080/07350015.1995.10524599.',
    "[37]": '[37]\tJ. Bollen, H. Mao, and X. Zeng, "Twitter mood predicts the stock market," J. Comput. Sci., vol. 2, no. 1, pp. 1–8, 2011. doi: 10.1016/j.jocs.2010.12.007.',
    "[38]": '[38]\tI. E. Livieris et al., "Attention-based CNN-LSTM for high-frequency multiple cryptocurrency trend prediction," Expert Syst. Appl., vol. 213, art. no. 119208, 2024. doi: 10.1016/j.eswa.2022.119208.',
    "[39]": '[39]\tJ. Brooke, "SUS: A \'Quick and Dirty\' Usability Scale," in Usability Evaluation in Industry, P. W. Jordan et al., Eds. London, UK: Taylor & Francis, 1996, pp. 189–194.',
    "[40]": '[40]\tA. Bangor, P. T. Kortum, and J. T. Miller, "Determining what individual SUS scores mean: Adding an adjective rating scale," J. Usability Stud., vol. 4, no. 3, pp. 114–123, 2009. [Online]. Available: https://uxpajournal.org/determining-what-individual-sus-scores-mean/.',
}

doc = Document(SRC)

updated = 0
for para in doc.paragraphs:
    txt = para.text.strip()
    # Match reference paragraphs like [1], [2] ... [40]
    for key, new_ref in UPDATED_REFS.items():
        # Match exact key at start (e.g. "[1]\t" or "[1] \t")
        clean = txt.replace('\t', '').replace(' ', '')
        key_clean = key.replace(' ', '')
        if clean.startswith(key_clean):
            # Preserve formatting: copy font from first run
            fmt_size = None
            fmt_name = None
            fmt_bold = False
            if para.runs:
                r0 = para.runs[0]
                fmt_size = r0.font.size
                fmt_name = r0.font.name
                fmt_bold = r0.bold
            # Clear all existing runs
            for run in para.runs:
                run._element.getparent().remove(run._element)
            # Add new run with updated text
            new_run = para.add_run(new_ref)
            if fmt_size:
                new_run.font.size = fmt_size
            if fmt_name:
                new_run.font.name = fmt_name
            new_run.bold = fmt_bold
            updated += 1
            print(f"Updated {key}")
            break

doc.save(DST)
print(f"\nTotal updated: {updated}/40 references")
print(f"Saved to: {DST}")
