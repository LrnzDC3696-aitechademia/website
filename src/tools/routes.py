import statistics
from scipy import skew as skew_, kurtosis as kurtosis_

from flask import Blueprint, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError


tools = Blueprint("tools", __name__)


class Tool:
    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url


class DescriptiveStatistic:
    def __init__(self, dataset: list[int]):
        self.dataset = dataset

    @property
    def mean(self):
        """ Calculate mean of the dataset """
        return statistics.mean(self.dataset)

    @property
    def median(self):
        """ Calculate median of the dataset """
        return statistics.median(self.dataset)

    @property
    def mode(self):
        """ Calculate mode of the dataset """
        return statistics.mode(self.dataset)

    @property
    def range(self):
        """ Calculate range of the dataset """
        return max(self.dataset) - min(self.dataset)

    @property
    def standard_deviation(self):
        """ Calculate standard deviation of the dataset """
        return statistics.stdev(self.dataset)

    @property
    def skewness(self):
        """ Calculate skewness of the dataset """
        return skew_(self.dataset)

    @property
    def kurtosis(self):
        """ Calculate kurtosis of the dataset """
        return kurtosis_(self.dataset)


class DSForm(FlaskForm):
    """Form for Descriptive Statistics"""

    dataset = TextAreaField("Dataset", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_dataset(self, dataset):
        """ Validate dataset checks if the dataset is only numbers"""
        try:
            if not dataset.data.replace(" ", "").replace("\n", "").replace("\r", "").isdigit():
                raise ValidationError("Dataset must be only numbers")
        except ValueError:
            raise ValidationError("Please check your input for newlines")


@tools.route("/tools/")
def index():
    tool = Tool(
        name="Descriptive Statistics",
        description="A tool to calculate descriptive statistics for a dataset.",
        url=url_for("tools.descriptive_statistics"),
    )
    return render_template("tools/index.html", tools=[tool])


@tools.route("/tools/descriptive-statistics", methods=["GET", "POST"])
def descriptive_statistics():
    tool = Tool(
        name="Descriptive Statistics",
        description="A tool to calculate descriptive statistics for a dataset.",
        url=url_for("tools.descriptive_statistics"),
    )

    form = DSForm()
    if form.validate_on_submit():
        return render_template(
            "tools/dstatistics.html",
            tool=tool,
            form=form,
            dataset=form.dataset.data,
            result=DescriptiveStatistic(
                dataset=[int(i) for i in form.dataset.data.split(" ")],
            ),
        )

    return render_template("tools/dstatistics.html", form=form, tool=tool)
