# pylint: disable=missing-docstring

INVENTORY = """
QListWidget {
    background-color: #fff7fb;
    border-radius: 12px;
    padding: 7px;
}

QListWidget::item {
    background-color: #f5c4dc;
    border-style: outset;
    border-width: 5px;
    border-radius: 12px;
    border-color: #f59ac8;
}

QListWidget::item:selected {
    background-color: #f59ac8;
    border-style: inset;
    border-color: #ba4e85;
}
"""

HP_BAR = """
QListWidget {
    background-color: transparent;
    border-radius: 25px;
}

QListWidget::item {
    padding: 7px;
}
"""

NORMAL_BUTTON = """
QPushButton {
    background-color: #f5c4dc;
    border-style: outset;
    border-width: 3px;
    border-radius: 10px;
    border-color: #f59ac8;
    padding: 0 8px;

    color: #803b5d;
    font-size: 14px;
    font-weight: bold;
    font-family: "Courier New";
}

QPushButton:disabled {
    background-color: #fff7fb;
    border-color: #f5c4dc;

    color: #dbd7d9;
}

QPushButton:pressed {
    background-color: #f59ac8;
    border-style: inset;
    border-color: #ba4e85;
}
"""


LOGO = """
QLabel {
    background-color: transparent;
    border-style: outset;
    border-width: 3px;
    border-radius: 10px;
    border-color: #f59ac8;
}
"""

TEXT = """
QLabel {
    background-color: transparent;
    border-style: outset;
    border-width: 3px;
    border-radius: 10px;
    border-color: #f59ac8;

    color: #803b5d;
    font-size: 24px;
    font-weight: bold;
    font-family: "Courier New";
}
"""

TEXT_INPUT = """
QLineEdit {
    background-color: #fff7fb;
    border-style: inset;
    border-width: 3px;
    border-radius: 10px;
    border-color: #f59ac8;
    padding: 0 8px;

    color: #803b5d;
    font-size: 18px;
    font-weight: bold;
    font-family: "Courier New";
}
"""

RANKING_LABEL = """
QLabel {
    background-color: transparent;
    border-style: inset;
    border-width: 3px;
    border-radius: 10px;
    border-color: #f59ac8;
    padding: 0 8px;

    color: #803b5d;
    font-size: 18px;
    font-weight: bold;
    font-family: "Courier New";
}
"""

if __name__ == "__main__":
    pass
