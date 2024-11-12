from blueprints.app import  db,ckeditor

from  sqlalchemy import  String,Integer
from  sqlalchemy.orm import  Mapped,mapped_column

from flask_login import  LoginManager, UserMixin,login_user,login_required,logout_user
from  flask_wtf import  FlaskForm
from  flask_wtf.file import  FileField,FileRequired,FileAllowed
from flask_ckeditor import  CKEditorField
from  wtforms import  StringField, SubmitField,IntegerField,FileField,SelectField
from  wtforms.validators import  DataRequired,Optional


class UserData(UserMixin,db.Model):
    __tablename__ = "管理者名單"
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    user_name : Mapped[str] = mapped_column(String,unique=True)
    user_account : Mapped[str] = mapped_column(String,unique=True)
    user_password: Mapped[str] = mapped_column(String)

    def __init__(self,user_name=user_name,user_password=user_password,user_account=user_account):
        self.user_name = user_name
        self.user_account = user_account
        self.user_password = user_password

class UserLogin(FlaskForm):
    useraccount =StringField(label="使用者帳號",validators=[DataRequired()])
    userpassword = StringField(label="使用者密碼",validators=[DataRequired()])
    submit = SubmitField("送出")


class User(FlaskForm):
    username = StringField(label="老師名稱",validators=[DataRequired()])
    useraccount =StringField(label="使用者帳號",validators=[DataRequired()])
    userpassword = StringField(label="使用者密碼",validators=[DataRequired()])
    submit = SubmitField("送出")

class Course(db.Model):
    __tablename__ = "課程花絮"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    posttime: Mapped[str] = mapped_column(String)
    class_ : Mapped[str] = mapped_column(String,nullable=False)
    title : Mapped[str] =mapped_column(String,nullable=False)
    context : Mapped[str] = mapped_column(String,nullable=False)
    picture_path1 : Mapped[str] = mapped_column(String)
    picture_path2: Mapped[str] = mapped_column(String)
    picture_path3 : Mapped[str] = mapped_column(String)


class CourseFrom(FlaskForm):
    class_= SelectField("班級",choices=[ ],validators=[DataRequired()])
    title = StringField("標題",validators=[DataRequired()])
    context=CKEditorField("內容",validators=[DataRequired()])
    picture_path1=FileField("照片一",validators=[FileRequired()])
    picture_path2=FileField("照片二",validators=[FileRequired()])
    picture_path3=FileField("照片三",validators=[FileRequired()])
    submit =SubmitField("送出")

    def __init__(self,classname=None):
        super().__init__()
        if classname:
            self.class_.choices= [item.class_name for item in classname]
            self.class_.choices.append("全園活動")




class SchoolDisplay(db.Model):
    __tablename__ = "學校介紹內文"
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    title : Mapped[str] = mapped_column(String)
    content : Mapped[str] = mapped_column(String)


class SchoolIntroduce(FlaskForm):
    title = StringField("標題",validators=[DataRequired()])
    content =  CKEditorField("內容",validators=[DataRequired()])
    submit = SubmitField("送出")


class StructureDisplay(db.Model):
    __tablename__  = "學校行政架構"
    id : Mapped[str] = mapped_column(Integer,primary_key=True)
    team_name : Mapped[str] = mapped_column(String)
    teacher_name : Mapped[str] = mapped_column(String)



class SchoolStructure(FlaskForm):
    team_name = StringField("行政工作",validators=[DataRequired()])
    teacher_name = SelectField("行政負責教師",choices=[],validators=[DataRequired()])
    submit = SubmitField("送出")
    def __init__(self,teachername=None):
        super().__init__()
        if teachername:
            self.teacher_name.choices= [item.user_name for item in teachername]



class ClassDisplay(db.Model):
    __tablename__ = "班級介紹"
    class_name : Mapped[str] = mapped_column(String,primary_key=True)
    class_teacher1 : Mapped[str] = mapped_column(String)
    class_teacher2 : Mapped[str] = mapped_column(String)


class ClassData(FlaskForm):
    class_name = StringField("班級名稱",validators=[DataRequired()])
    teacher_name1 = SelectField("班級導師",choices=[],validators=[DataRequired()])
    teacher_name2 = SelectField("班級導師",choices=[],validators=[DataRequired()])
    submit = SubmitField("送出")

    def __init__(self, teachername=None):
        super().__init__()
        if teachername:
            self.teacher_name1.choices = [item.user_name for item in teachername]
            self.teacher_name2.choices = [item.user_name for item in teachername]


class Library(db.Model):
    __tablename__  = "學校藏書"
    id : Mapped[str] = mapped_column(Integer,primary_key=True)
    book_title : Mapped[str] = mapped_column(String)
    author : Mapped[str] = mapped_column(String)
    ISBN_number : Mapped[str] = mapped_column(String)


class AddBook(FlaskForm):
    id = StringField("書本編號",validators=[DataRequired()])
    book_title = StringField("書名",validators=[DataRequired()])
    author = StringField("作者",validators=[DataRequired()])
    ISBN_number = StringField("ISBN碼",validators=[DataRequired()])
    submit = SubmitField("送出")


class SearchBook(FlaskForm):
    ways = SelectField ("搜尋方式",choices={"書名", "作者","編號","ISBN碼"},validators=[Optional()])
    content = StringField("關鍵字",validators=[Optional()])
    submit = SubmitField("搜尋")