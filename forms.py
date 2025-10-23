from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Optional

class InquiryForm(FlaskForm):
    name = StringField("Họ và tên", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Số điện thoại", validators=[Optional()])
    area = SelectField("Lĩnh vực cần tư vấn", choices=[
        ("doanh-nghiep", "Doanh nghiệp & Đầu tư"),
        ("dat-dai", "Đất đai & Xây dựng"),
        ("hop-dong", "Hợp đồng & Dân sự"),
        ("lao-dong", "Lao động"),
        ("hanh-chinh", "Hành chính")
    ], validators=[DataRequired()])
    message = TextAreaField("Mô tả ngắn vấn đề", validators=[Optional()])
