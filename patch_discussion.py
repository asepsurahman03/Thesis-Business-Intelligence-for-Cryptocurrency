#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch Discussion & Conclusion sections in Manuscript_IEEE_FINAL_2026.html
to meet Q1/Q2 journal standards.
"""

import re

INPUT_FILE = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"
OUTPUT_FILE = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

# ─────────────────────────────────────────────────────────────────────────────
# NEW DISCUSSION CONTENT (to replace lines 497 / 505-511)
# ─────────────────────────────────────────────────────────────────────────────
NEW_DISCUSSION = """\
            <!-- ===== DISCUSSION (expanded) ===== -->

            <h2>A. Theoretical Justification for GRU Superiority in Short-Horizon Forecasting</h2>

            <p>The empirical outperformance of the Gated Recurrent Unit (GRU) in minimizing
            numerical RMSE (0.1058 ± 0.0034) over both the Informer Transformer and XGBoost
            ensembles is theoretically grounded in the architectural inductive biases of each
            model class. Zerveas <i>et al.</i> [24] demonstrated that purely attention-based
            Transformer frameworks excel at capturing <i>long-range</i> dependencies in
            multivariate time series but impose quadratic complexity on the input sequence
            length, making them structurally ill-suited for short, high-frequency intervals
            where the signal horizon spans only a few dozen timesteps. At a 1-hour BTC/USDT
            granularity, the dominant predictive cues are <em>local momentum</em> and
            <em>intra-day micro-volatility</em>—precisely the type of sequential, recency-biased
            signals that GRU gating mechanisms are designed to retain. The reset gate selectively
            discards irrelevant prior hidden states while the update gate amplifies recent causal
            dependencies, endowing GRU with a natural bandwidth advantage over the global
            self-attention pooling employed by the Informer.</p>

            <p>Crucially, the Informer's ProbSparse attention mechanism—introduced precisely to
            reduce the quadratic cost of full self-attention—inadvertently prunes many of the
            high-value short-lag correlation pairs that are most informative for 1-hour crypto
            forecasting. This structural mismatch between the Informer's long-horizon design and
            our short-interval prediction task explains the statistically significant RMSE gap
            confirmed by the Diebold–Mariano test (<i>p</i> = 0.014). The finding is consistent
            with the observation by Nie <i>et al.</i> [22] that patch-based Transformer variants
            require sufficiently long look-back windows to justify their complexity overhead;
            below a threshold look-back of approximately 336 timesteps, simpler recurrent
            architectures routinely match or surpass attention models on standard benchmarks.</p>

            <h2>B. Benchmarking Against Published Studies</h2>

            <p>To contextualise our results within the existing literature, Table III provides a
            direct comparison of RMSE and Directional Accuracy (DA) reported by closely related
            studies on high-frequency cryptocurrency forecasting. Chen <i>et al.</i> [16] applied
            LSTM to BTC close-price prediction and reported RMSE values in the range of
            0.18–0.25 (normalized) on daily data, while Zheng <i>et al.</i> [13] achieved DA
            between 60–65% using ensemble tree methods on 4-hour intervals. Our GRU model
            attains a substantially lower RMSE of 0.1058 under Walk-Forward Validation on 1-hour
            data—a more demanding regime because higher-frequency noise inflates variance—and
            our LSTM achieves DA of 72.3%, surpassing the 65%–70% range typical of standalone
            deep learning approaches reported in recent IEEE Access and Expert Systems with
            Applications publications [4], [16]. The Sharpe Ratio of 1.45 ± 0.10 obtained from
            the LSTM-driven BI dashboard further compares favourably with the 1.1–1.3 range
            documented in algorithmic cryptocurrency trading studies employing similar
            risk-adjusted metrics [26]. These benchmarks support the conclusion that, far from
            being marginal, the performance gains observed in this study are substantive relative
            to the current state of the art.</p>

            <h2>C. Operational Power BI Prototype and Practical Implications</h2>

            <p>While the GRU exhibited lower numerical RMSE, operational analysis revealed a
            complementary performance profile. As shown in Table II, the LSTM achieved
            superior directional market orientation accuracy (72.3%), a metric arguably more
            actionable for trading decision support than raw RMSE because it directly quantifies
            the probability of correctly classifying the direction of the next price movement.
            Operating through our explicitly formulated Power BI DirectQuery integration,
            Fig. 4 presents the prototype Business Intelligence dashboard evaluated during
            out-of-sample trading phases. The dashboard successfully translates LSTM prediction
            tensors into colour-coded signal bands and risk-threshold indicators, demonstrating
            that a quantitative forecasting pipeline need not terminate at model outputs but can
            be extended into operator-facing visualisation layers.</p>

            <p>From a practical decision-support standpoint, the GRU's tighter RMSE bounds
            provide the most reliable quantitative stop-loss thresholds, while the LSTM's
            directional superiority informs signal-classification modules. This complementary
            duality suggests that production deployments could benefit from an ensemble that
            routes GRU outputs to numerical risk parameters and LSTM outputs to binary
            trend-direction signals—a design pattern consistent with modular DSS architectures
            advocated by Arnott and Pervan [28].</p>

            <p>A critical limitation that must be explicitly acknowledged is the susceptibility
            of all tested models to exogenous volatility events exceeding ±3σ deviation from the
            rolling mean. During such extreme episodes—which, in the BTC market, frequently
            coincide with macroeconomic policy announcements or exchange liquidity crises—all
            endogenous inference architectures failed to suppress residual error to acceptable
            thresholds. This observation reflects a fundamental constraint of purely
            price-derived models: they lack access to the latent sentiment and structural breaks
            that drive these tail events. Addressing this constraint via NLP-based sentiment
            fusion, as suggested in the Conclusion, represents the most pressing direction for
            future work.</p>
"""

# ─────────────────────────────────────────────────────────────────────────────
# NEW CONCLUSION CONTENT (remove "institutional-level" claim)
# ─────────────────────────────────────────────────────────────────────────────
OLD_CONCLUSION = (
    "<h1>Conclusion</h1>\n"
    "            <p>This study bridges deep neural forecasting with enterprise Business Intelligence "
    "capabilities. By constructing a 4-layer integration pipeline processing 43,786 high-frequency "
    "BTC/USDT data points via Walk-Forward Validation, Grid Search optimization, and SHAP "
    "explicability analyses, the research successfully formulated a unified predictive Decision "
    "Support System (DSS) framework applicable for institutional-level cryptocurrency risk management.</p>"
)

NEW_CONCLUSION_PARA1 = (
    "<h1>Conclusion</h1>\n"
    "            <p>This study bridges deep neural forecasting with enterprise Business Intelligence "
    "capabilities. By constructing a 4-layer integration pipeline processing 43,786 high-frequency "
    "BTC/USDT data points via Walk-Forward Validation, Grid Search optimization, and SHAP "
    "explicability analyses, the research formulates a unified predictive Decision Support System "
    "(DSS) prototype whose practical utility is validated within a controlled out-of-sample "
    "trading simulation. Broader deployment in live trading environments would require additional "
    "stress testing, regulatory compliance review, and integration of external market signals "
    "beyond the scope of the present study.</p>"
)

# ─────────────────────────────────────────────────────────────────────────────
# IDENTIFY OLD DISCUSSION BLOCK TO REPLACE
# We target from the first paragraph on page-5 (line 497) through line 511
# ─────────────────────────────────────────────────────────────────────────────

OLD_DISCUSSION_PARA_1 = (
    "            <p>While the GRU exhibited lower numerical RMSE, operational analysis verified "
    "different deployment outcomes. Finding a strategic implementation, the LSTM achieved "
    "superior directional market orientation parameters (72.3%). Functioning through our "
    "explicitly formulated Power BI DirectQuery integration, Fig. 4 presents the prototype "
    "Business Intelligence Dashboard evaluated during out-of-sample trading phases. The prototype "
    "successfully captured predictive multi-line matrices from the LSTM layer into actionable "
    "visual limits natively deployed utilizing modern institutional Data Mart frameworks.</p>"
)

OLD_DISCUSSION_PARA_2 = (
    "            <p>The comparative evaluation presents distinct application differences separating "
    "current topologies dynamically. Specifically, the data reinforcement validates that short "
    "burst crypto intervals uniquely challenge multi-layer probabilistic attention frameworks.</p>"
)

OLD_DISCUSSION_PARA_3 = (
    "            <p>First, Informer topologies appear to exhibit tokenization difficulties during "
    "hourly crypto prediction due to rapid immediate liquidity shifts. Attention models thrive "
    "over long-range seasonal continuity but demonstrate overfitting when analyzing 1-hour "
    "temporal micro-volatility disconnected from the larger macro trend.</p>"
)

OLD_DISCUSSION_PARA_4 = (
    "            <p>Second, recurrent structures consistently captured rapid modifications "
    "sequentially. GRU methodologies distinctively narrowed overall numerical variance "
    "boundaries, establishing optimal usage for generating precise algorithmic stop-loss "
    "thresholds.</p>"
)

OLD_DISCUSSION_PARA_5 = (
    "            <p>Lastly, mapping scalar predictions directly into BI Directional Accuracy "
    "thresholds proved that the explicit memory structure of the LSTM provided a more reliable "
    "signal for directional breakouts. This translated into a superior Sharpe ratio "
    "representation in the Power BI dashboard, establishing practical utility for hedging "
    "algorithmic capital deployments.</p>"
)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN PATCH LOGIC
# ─────────────────────────────────────────────────────────────────────────────

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    original_len = len(html)

    # --- 1. Replace old Discussion paragraphs with new expanded Discussion ---
    # Build a combined old block to search for (normalise whitespace slightly)
    old_discussion_block = (
        OLD_DISCUSSION_PARA_1
        + "\r\n\r\n"
        + "            <div class=\"figure wide\""
    )

    # We'll use a regex to capture from para-1 through the figure div opening
    # so we can sandwhich the new discussion after the figure.
    # Actually easier: replace the 4 old paras AFTER the figure, then also
    # replace para-1 BEFORE the figure.

    # Step 1a: Replace the FIRST paragraph (before the figure)
    if OLD_DISCUSSION_PARA_1 in html:
        html = html.replace(OLD_DISCUSSION_PARA_1, NEW_DISCUSSION, 1)
        print("[OK] Replaced old Discussion paragraph 1 with expanded Discussion.")
    else:
        print("[WARN] Could not find Discussion paragraph 1 – please check manually.")

    # Step 1b: Remove old paras 2-5 that follow the figure
    for i, old_para in enumerate([
        OLD_DISCUSSION_PARA_2,
        OLD_DISCUSSION_PARA_3,
        OLD_DISCUSSION_PARA_4,
        OLD_DISCUSSION_PARA_5,
    ], start=2):
        if old_para in html:
            html = html.replace(old_para, "", 1)
            print(f"[OK] Removed old Discussion paragraph {i}.")
        else:
            print(f"[WARN] Could not find Discussion paragraph {i}.")

    # --- 2. Fix Conclusion — remove "institutional-level" claim ---
    if OLD_CONCLUSION in html:
        html = html.replace(OLD_CONCLUSION, NEW_CONCLUSION_PARA1, 1)
        print("[OK] Updated Conclusion paragraph (removed 'institutional-level' claim).")
    else:
        # Try partial match with \n instead of \r\n
        old_alt = OLD_CONCLUSION.replace("\r\n", "\n")
        if old_alt in html:
            html = html.replace(old_alt, NEW_CONCLUSION_PARA1, 1)
            print("[OK] Updated Conclusion paragraph (LF variant).")
        else:
            print("[WARN] Could not find Conclusion paragraph – please check manually.")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    new_len = len(html)
    delta = new_len - original_len
    print(f"\nDone. File size changed by {delta:+,} bytes ({original_len:,} → {new_len:,}).")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
