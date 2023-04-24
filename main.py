from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv


class CafeForm(FlaskForm):
    cafe_name = StringField(label='Cafe Name', validators=[DataRequired()])
    location_url = URLField(label='Cafe Location on Google Maps (URL)', validators=[URL(), DataRequired()])
    open_time = StringField(label='Opening Time (e.g. 8am)', validators=[DataRequired()])
    close_time = StringField(label='Closing Time (e.g. 10pm)', validators=[DataRequired()])
    coffee_rating = SelectField(label='Coffee Rating', choices=[('1', '☕️'), ('', '☕️☕️'), ('3', '☕️☕️☕️'), ('4', '☕️☕️☕️☕️'), ('5', '☕️☕️☕️☕️☕️')], validators=[DataRequired()])
    wifi_rating = SelectField(label='Wifi Strength Rating', choices=[('1', '✘'), ('2', '💪'), ('3', '💪💪'), ('4', '💪💪💪️'), ('5', '💪💪💪💪'), ('6', '💪💪💪💪💪')], validators=[DataRequired()])
    price_rating = SelectField(label='Price', choices=[('1', '＄'), ('2', '＄＄'), ('3', '＄＄＄'), ('4', '＄＄＄＄'), ('5', '＄＄＄＄＄')], validators=[DataRequired()])
    submit = SubmitField(label="Submit")


app = Flask(__name__)
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', 'a', newline='', encoding="utf8") as csv_file:
            csv_file.write(f"\n{form.cafe_name.data},{form.location_url.data},{form.open_time.data},{form.close_time.data},{form.coffee_rating.choices[int(form.coffee_rating.data)][1]},{form.wifi_rating.choices[int(form.wifi_rating.data)][1]},{form.price_rating.choices[int(form.price_rating.data)][1]}")
        return redirect('/cafes')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
