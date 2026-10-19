"""Stable visual meanings shared by screen, print and standalone exports."""
PILLAR_COLORS = ['#087984', '#2d5f9f', '#76508b', '#407a51']
MODEL_SERIES = [
    ('china', '中国', 'China', '#4E87C5'),
    ('unitedStates', '美国', 'United States', '#279FA9'),
    ('europe', '欧洲', 'Europe', '#9973B7'),
]
MODEL_TICKS = [(0, '2023.11'), (7, '2024.06'), (14, '2025.01'), (21, '2025.08'), (27, '2026.02')]

# Chart types and topology are stable; controls and detail panels adapt to the medium.
VISUAL_FORMS = {
    '1-0-1': 'foundation → four parallel research chapters → shared action',
    '1-1-1': 'two descending horizontal ranking panels; separate denominators',
    '1-1-2': '28 monthly stacked share columns + four directed Qwen relations',
    '1-1-3': '17-sector SDG wheel + 3×3 DPGA condition matrix',
    '1-2-1': 'four ordered pillar rows; dimensions read left to right',
    '1-3-1': '2×2 pillar overview; dimensions and indicators nested within each pillar',
    '1-3-2': 'four pillars on the left → seven themes on the right',
}
