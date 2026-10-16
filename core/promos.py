"""
PSDR promotional rules.
Edit this file to add/remove promotions — no other code changes needed.
"""

PROMOS = [
    {
        'title': 'Book 5 hours, get 30 minutes free',
        'subtitle': 'Perfect for short business trips.',
        'icon': 'bi-clock-history',
        'badge': 'Popular',
    },
    {
        'title': 'Book 10 hours or more, get 1 hour free',
        'subtitle': 'Ideal for full-day parking and events.',
        'icon': 'bi-gift-fill',
        'badge': 'Best value',
    },
    {
        'title': 'Premium for 5–10 hours → free full car wash',
        'subtitle': 'VIP treatment, sparkling car.',
        'icon': 'bi-droplet-fill',
        'badge': 'Premium only',
    },
]


def compute_promo_bonus(hours, category_name):
    """
    Return dict:
      {
        'free_minutes': int,
        'free_wash': bool,
        'label': str,
      }
    """
    free_minutes = 0
    free_wash    = False
    label        = ''

    if hours >= 10:
        free_minutes = 60
        label = '10h+ booking: 1 hour free added 🎉'
    elif hours >= 5:
        free_minutes = 30
        label = '5h+ booking: 30 minutes free added 🎉'

    if category_name.lower() == 'premium' and 5 <= hours <= 10:
        free_wash = True
        if label:
            label += ' + free car wash 🚗💦'
        else:
            label = 'Premium 5–10h: free car wash 🚗💦'

    return {
        'free_minutes': free_minutes,
        'free_wash':    free_wash,
        'label':        label,
    }