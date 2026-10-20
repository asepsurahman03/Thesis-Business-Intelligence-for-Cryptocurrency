# Mathematical Formulations for Scopus Manuscript
## Bitcoin Prediction via Big Data Analytics: LSTM vs GRU Comparative Study

---

## Section 2.3: Data Normalization

### Equation (1): Min-Max Scaling

**LaTeX Code for Word:**
```
X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}
```

**Description:**
where X denotes the original feature value, X_min and X_max represent the minimum and maximum values observed in the training dataset, respectively. This transformation maps all features to the interval [0, 1], ensuring uniform scale across heterogeneous technical indicators.

---

## Section 2.4: Technical Indicators

### Equation (2): Moving Average

**LaTeX Code for Word:**
```
MA_n = \frac{1}{n} \sum_{i=0}^{n-1} P_{t-i}
```

**Description:**
where P_t is the closing price at time t, and n is the window size (7 or 21 periods for short and medium-term trend analysis).

---

### Equation (3): Relative Strength Index (RSI)

**LaTeX Code for Word:**
```
RSI = 100 - \frac{100}{1 + RS}
```

**Where:**
```
RS = \frac{Average Gain_{14}}{Average Loss_{14}}
```

**Description:**
where Average Gain and Average Loss are calculated over a 14-period rolling window, providing a momentum oscillator that identifies overbought (RSI > 70) and oversold (RSI < 30) market conditions.

---

### Equation (4): Moving Average Convergence Divergence (MACD)

**LaTeX Code for Word:**
```
MACD = EMA_{12} - EMA_{26}
```

**Signal Line:**
```
Signal = EMA_9(MACD)
```

**Description:**
where EMA_n denotes the Exponential Moving Average with span n. The MACD indicator detects trend reversals and momentum shifts through the convergence and divergence of short-term and long-term exponential moving averages.

---

### Equation (5): Bollinger Bands

**LaTeX Code for Word:**
```
BB_{upper} = MA_{20} + 2\sigma_{20}
```
```
BB_{lower} = MA_{20} - 2\sigma_{20}
```

**Description:**
where σ_20 is the 20-period standard deviation of closing prices. Bollinger Bands provide dynamic support and resistance levels that adapt to market volatility, with prices typically contained within the ±2σ envelope.

---

### Equation (6): Logarithmic Returns

**LaTeX Code for Word:**
```
r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)
```

**Description:**
providing a normalized, time-additive measure of relative price movement that ensures stationarity and reduces heteroscedasticity in the time series.

---

### Equation (7): Rolling Volatility

**LaTeX Code for Word:**
```
\sigma_t = \sqrt{\frac{1}{n} \sum_{i=0}^{n-1} (P_{t-i} - \bar{P})^2}
```

**Description:**
where P̄ is the mean price over the rolling window of n=24 hours. This metric quantifies the degree of price dispersion and serves as a proxy for market risk and uncertainty.

---

## Section 2.5: Deep Learning Architectures

### Equations (8-13): LSTM Cell Operations

**Forget Gate (8):**
```
f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)
```

**Input Gate (9):**
```
i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)
```

**Candidate Cell State (10):**
```
\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)
```

**Cell State Update (11):**
```
C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t
```

**Output Gate (12):**
```
o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)
```

**Hidden State (13):**
```
h_t = o_t \odot \tanh(C_t)
```

**Description:**
where σ denotes the sigmoid activation function σ(x) = 1/(1+e^(-x)), ⊙ represents element-wise (Hadamard) multiplication, W and b are learnable weight matrices and bias vectors, respectively. The LSTM architecture employs three multiplicative gates to regulate information flow, enabling the network to capture long-term temporal dependencies while mitigating the vanishing gradient problem.

---

### Equations (14-17): GRU Cell Operations

**Update Gate (14):**
```
z_t = \sigma(W_z \cdot [h_{t-1}, x_t] + b_z)
```

**Reset Gate (15):**
```
r_t = \sigma(W_r \cdot [h_{t-1}, x_t] + b_r)
```

**Candidate Hidden State (16):**
```
\tilde{h}_t = \tanh(W_h \cdot [r_t \odot h_{t-1}, x_t] + b_h)
```

**Hidden State Update (17):**
```
h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t
```

**Description:**
The GRU architecture simplifies LSTM by merging the forget and input gates into a single update gate z_t, reducing the number of parameters while maintaining comparable representational capacity. This architectural parsimony results in faster training convergence and lower computational overhead, making GRU particularly suitable for high-velocity Big Data applications.

---

## Section 2.6: Evaluation Metrics

### Equation (18): Root Mean Square Error (RMSE)

**LaTeX Code for Word:**
```
RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}
```

**Description:**
where y_i represents the actual observed value and ŷ_i denotes the model prediction. RMSE measures the square root of the average squared prediction errors, providing a scale-dependent metric that penalizes larger deviations more heavily due to the quadratic term.

---

### Equation (19): Mean Absolute Error (MAE)

**LaTeX Code for Word:**
```
MAE = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|
```

**Description:**
MAE provides a linear, robust measure of average prediction error that treats all deviations equally regardless of magnitude. Unlike RMSE, MAE is less sensitive to outliers and offers an intuitive interpretation in the original price units.

---

### Equation (20): Mean Absolute Percentage Error (MAPE)

**LaTeX Code for Word:**
```
MAPE = \frac{100\%}{n} \sum_{i=1}^{n} \left|\frac{y_i - \hat{y}_i}{y_i}\right|
```

**Description:**
MAPE expresses prediction accuracy as a percentage of the actual values, making it scale-independent and facilitating comparison across different asset classes and price ranges. A MAPE value below 5% is generally considered indicative of high forecasting accuracy in financial time series applications.

---

## Instructions for Copying to Microsoft Word:

1. **Using Word's Equation Editor:**
   - In Word, go to: Insert → Equation
   - Select "Professional" mode
   - Copy the LaTeX code from above
   - Paste into the equation editor
   - Word will automatically convert LaTeX to formatted equations

2. **Alternative Method (MathType):**
   - If you have MathType installed
   - Copy the LaTeX code
   - In MathType: Preferences → Cut and Copy Preferences → MathML or TeX
   - Paste directly into MathType
   - Copy from MathType to Word

3. **Manual Entry:**
   - Use Word's equation editor symbols
   - Build equations using the graphical interface
   - Reference the LaTeX code for structure

---

## Citation Format (APA Style):

When referencing these equations in your manuscript:

- "As shown in Equation (1), the Min-Max normalization..."
- "The LSTM architecture (Equations 8-13) employs..."
- "Model performance was evaluated using RMSE (Equation 18)..."

---

**Note:** All equations follow Scopus formatting standards with:
- Sequential numbering in parentheses: (1), (2), (3)...
- Proper mathematical notation and symbols
- Clear variable definitions
- Academic language suitable for peer-reviewed publication
