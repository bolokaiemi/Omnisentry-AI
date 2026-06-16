import pandas as pd


def build_training_data():

    data = pd.DataFrame({

        "credit_card_request": [

            0, 0, 1, 1, 1

        ],

        "urgency_language": [

            0, 1, 0, 1, 1

        ],

        "phishing": [

            0, 0, 1, 1, 1

        ],

        "label": [

            0, 0, 1, 1, 1

        ]
    })

    return data