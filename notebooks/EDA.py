import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Paths ────────────────────────────────────────────────────
base      = r'C:\Users\pc\Documents\decodelab_project'
graphs    = os.path.join(base, 'outputs', 'graphs')
data_file = os.path.join(base, 'outputs', 'Cleaned_Dataset.xlsx')
os.makedirs(graphs, exist_ok=True)

def save(name):
    path = os.path.join(graphs, name)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"Saved: {name}")

sns.set_theme(style="whitegrid")

# ── Load Data ─────────────────────────────────────────────────
df = pd.read_excel(data_file)
df['Date']  = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M')
df['Year']  = df['Date'].dt.year
print(f"[LOADED] {df.shape[0]} rows × {df.shape[1]} columns")


# ═══════════════════════════════════════════════════════════
# CHART 1: Revenue by Product
# ═══════════════════════════════════════════════════════════
rev    = df.groupby('Product')['TotalPrice'].sum().sort_values()
colors = sns.color_palette("Blues_d", len(rev))

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(rev.index, rev.values, color=colors)
for bar, val in zip(bars, rev.values):
    ax.text(val + 1000, bar.get_y() + bar.get_height()/2,
            f'${val:,.0f}', va='center', fontsize=10)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.set_title('Total Revenue by Product Category', fontweight='bold', fontsize=13)
ax.set_xlabel('Total Revenue ($)')
plt.tight_layout()
save('chart1_revenue_by_product.png')


# ═══════════════════════════════════════════════════════════
# CHART 2: Annual Revenue by Year
# ═══════════════════════════════════════════════════════════
annual      = df.groupby('Year')['TotalPrice'].sum()
year_colors = ['#4C72B0', '#DD8452', '#55A868']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(annual.index.astype(str), annual.values,
              color=year_colors[:len(annual)], width=0.5)
for bar, val in zip(bars, annual.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
            f'${val:,.0f}', ha='center', fontweight='bold', fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.set_title('Annual Revenue by Year', fontweight='bold', fontsize=13)
ax.set_xlabel('Year')
ax.set_ylabel('Total Revenue ($)')
plt.tight_layout()
save('chart2_annual_revenue.png')


# ═══════════════════════════════════════════════════════════
# CHART 3: Monthly Revenue Trend
# ═══════════════════════════════════════════════════════════
monthly         = df.groupby('Month')['TotalPrice'].sum().reset_index()
monthly['Month'] = monthly['Month'].astype(str)

fig, ax = plt.subplots(figsize=(14, 5))
ax.fill_between(monthly['Month'], monthly['TotalPrice'],
                alpha=0.15, color='steelblue')
ax.plot(monthly['Month'], monthly['TotalPrice'],
        marker='o', color='steelblue', linewidth=2, markersize=5)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.set_title('Monthly Revenue Trend', fontweight='bold', fontsize=13)
ax.set_xlabel('Month')
ax.set_ylabel('Total Revenue ($)')
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()
save('chart3_monthly_trend.png')


# ═══════════════════════════════════════════════════════════
# CHART 4: Price Distributions — Mean vs Median
# ═══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Price Distributions — Mean vs. Median',
             fontweight='bold', fontsize=13)

for ax, col, color in zip(axes,
                           ['TotalPrice', 'UnitPrice'],
                           ['#4C72B0', '#DD8452']):
    mean_val   = df[col].mean()
    median_val = df[col].median()
    ax.hist(df[col], bins=30, color=color, edgecolor='white', alpha=0.85)
    ax.axvline(mean_val,   color='red',   linestyle='--', linewidth=2,
               label=f'Mean: {mean_val:.0f}')
    ax.axvline(median_val, color='green', linestyle='-',  linewidth=2,
               label=f'Median: {median_val:.0f}')
    label = 'Total' if col == 'TotalPrice' else 'Unit'
    ax.set_title(f'Distribution of {label} Price')
    ax.set_xlabel(f'{label} Price ($)')
    ax.set_ylabel('Frequency')
    ax.legend()

plt.tight_layout()
save('chart4_price_distributions.png')


# ═══════════════════════════════════════════════════════════
# CHART 5: Boxplots — Outlier Detection
# ═══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 4, figsize=(16, 6))
fig.suptitle('Boxplots — Outlier Detection (Red dots = Suspects)',
             fontweight='bold', fontsize=13)

cols        = ['TotalPrice', 'UnitPrice', 'Quantity', 'ItemsInCart']
box_colors  = ['#4C72B0', '#DD8452', '#9467BD', '#3CBFBF']

for ax, col, color in zip(axes, cols, box_colors):
    bp = ax.boxplot(df[col], patch_artist=True, widths=0.5,
                    flierprops=dict(marker='o', color='red',
                                   markerfacecolor='red', markersize=5))
    bp['boxes'][0].set_facecolor(color)
    bp['boxes'][0].set_alpha(0.7)
    ax.set_title(col, fontsize=11)
    ax.set_ylabel('Value')

plt.tight_layout()
save('chart5_boxplots_outliers.png')


# ═══════════════════════════════════════════════════════════
# CHART 6: Correlation Heatmap
# ═══════════════════════════════════════════════════════════
corr = df[['Quantity', 'UnitPrice', 'ItemsInCart', 'TotalPrice']].corr().round(2)
mask = pd.DataFrame(
    [[False, True,  True,  True ],
     [False, False, True,  True ],
     [False, False, False, True ],
     [False, False, False, False]],
    columns=corr.columns, index=corr.index)

fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            vmin=-1, vmax=1, ax=ax, linewidths=0.5,
            annot_kws={'size': 13, 'weight': 'bold'})
ax.set_title('Correlation Matrix — Numeric Variables',
             fontweight='bold', fontsize=13)
plt.tight_layout()
save('chart6_correlation_heatmap.png')


# ═══════════════════════════════════════════════════════════
# CHART 7: Payment Method & Order Status
# ═══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

payment_counts = df['PaymentMethod'].value_counts()
axes[0].pie(payment_counts.values, labels=payment_counts.index,
            autopct='%1.1f%%', startangle=90,
            colors=sns.color_palette('pastel'))
axes[0].set_title('Payment Method Distribution', fontweight='bold')

status_counts = df['OrderStatus'].value_counts()
axes[1].bar(status_counts.index, status_counts.values,
            color=sns.color_palette('Set2', len(status_counts)))
axes[1].set_title('Order Status Breakdown', fontweight='bold')
axes[1].set_xlabel('Status')
axes[1].set_ylabel('Count')

plt.tight_layout()
save('chart7_payment_status.png')


# ═══════════════════════════════════════════════════════════
# CHART 8: Referral Source Analysis
# ═══════════════════════════════════════════════════════════
ref_rev   = df.groupby('ReferralSource')['TotalPrice'].sum().sort_values(ascending=False)
ref_count = df.groupby('ReferralSource')['OrderID'].count().reindex(ref_rev.index)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].bar(ref_rev.index, ref_rev.values,
            color=sns.color_palette('mako_r', len(ref_rev)))
axes[0].set_title('Total Revenue by Referral Source', fontweight='bold')
axes[0].set_xlabel('ReferralSource')
axes[0].set_ylabel('Revenue ($)')
axes[0].yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))

axes[1].bar(ref_count.index, ref_count.values,
            color=sns.color_palette('rocket_r', len(ref_count)))
axes[1].set_title('Order Count by Referral Source', fontweight='bold')
axes[1].set_xlabel('ReferralSource')
axes[1].set_ylabel('Orders')

plt.tight_layout()
save('chart8_referral_analysis.png')


# ═══════════════════════════════════════════════════════════
# CHART 9: Quantity Distributions
# ═══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

qty_counts  = df['Quantity'].value_counts().sort_index()
cart_counts = df['ItemsInCart'].value_counts().sort_index()

axes[0].bar(qty_counts.index, qty_counts.values, color='#9467BD')
axes[0].set_title('Frequency of Order Quantities', fontweight='bold')
axes[0].set_xlabel('Quantity Ordered')
axes[0].set_ylabel('Number of Orders')

axes[1].bar(cart_counts.index, cart_counts.values, color='#3CBFBF')
axes[1].set_title('Frequency of Items in Cart', fontweight='bold')
axes[1].set_xlabel('Items in Cart')
axes[1].set_ylabel('Number of Orders')

plt.tight_layout()
save('chart9_quantity_distributions.png')


# ═══════════════════════════════════════════════════════════
# CHART 10: Coupon Impact
# ═══════════════════════════════════════════════════════════
df['CouponLabel'] = df['CouponCode'].replace('None', 'No Coupon')
coupon_avg = df.groupby('CouponLabel')['TotalPrice'].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(coupon_avg.index, coupon_avg.values,
              color=sns.color_palette('coolwarm', len(coupon_avg)))
for bar, val in zip(bars, coupon_avg.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'${val:,.0f}', ha='center', fontsize=11)
ax.set_title('Average Order Value by Coupon Code', fontweight='bold', fontsize=13)
ax.set_xlabel('CouponCode')
ax.set_ylabel('Avg Order Value ($)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.tight_layout()
save('chart10_coupon_impact.png')


# ═══════════════════════════════════════════════════════════
# CHART 11: Scatter Plots
# ═══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Scatter Plots — Relationship Between Variables',
             fontweight='bold', fontsize=13)

axes[0].scatter(df['Quantity'], df['TotalPrice'],
                alpha=0.3, color='#4C72B0', s=15)
axes[0].set_title('Quantity vs. Total Price')
axes[0].set_xlabel('Quantity')
axes[0].set_ylabel('Total Price ($)')

axes[1].scatter(df['UnitPrice'], df['TotalPrice'],
                alpha=0.3, color='#DD8452', s=15)
axes[1].set_title('Unit Price vs. Total Price')
axes[1].set_xlabel('Unit Price ($)')
axes[1].set_ylabel('Total Price ($)')

plt.tight_layout()
save('chart11_scatter_plots.png')

