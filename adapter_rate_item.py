from review import Review


class AdapterRateItem:
    def generateRate(self, appTitle, reviews: list) -> dict:
        content = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "type": "AdaptiveCard",
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.3",
                    },
                }
            ],
        }

        body = [
            {
                "type": "TextBlock",
                "size": "Large",
                "weight": "Bolder",
                "text": appTitle,
            }
        ]

        for review in reviews:
            body.append(review[0])
            body.append(review[1])

        content["attachments"][0]["content"]["body"] = body
        # print(content)
        return content

    def generateRateAdapter(self, review: Review) -> dict:
        dict = [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "Image",
                                "style": "Person",
                                "url": review.userImage,
                                "size": "Small",
                            }
                        ],
                        "width": "auto",
                    },
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "TextBlock",
                                "weight": "Bolder",
                                "text": review.userName,
                                "wrap": True,
                            },
                            {
                                "type": "TextBlock",
                                "spacing": "None",
                                "text": review.at,
                                "isSubtle": True,
                                "wrap": True,
                            },
                        ],
                        "width": "stretch",
                    },
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": str(review.score),
                                "size": "ExtraLarge",
                                "wrap": True,
                                "fontType": "Default",
                                "weight": "Bolder",
                                "height": "stretch",
                                "horizontalAlignment": "Center",
                            }
                        ],
                        "width": "auto",
                        "horizontalAlignment": "Center",
                        "verticalContentAlignment": "Bottom",
                    },
                ],
            },
            {"type": "TextBlock", "text": review.content, "wrap": True},
        ]
        return dict
